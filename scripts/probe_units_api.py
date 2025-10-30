"""
Probe inteligente del endpoint /api/pms/units con múltiples combinaciones de filtros.
Usa credenciales del .env. Genera un resumen en consola y un JSON de resultados.
"""

import json
import os
from datetime import datetime
from itertools import product
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv


def load_env() -> Tuple[str, str, str]:
    load_dotenv()
    # Asegurar URL base correcta: ihmvacations.trackhs.com (sin trailing slash)
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com").rstrip(
        "/"
    )
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    if not username or not password:
        raise RuntimeError("TRACKHS_USERNAME/PASSWORD no configurados en .env")
    return base_url, username, password


def call_units(
    base_url: str, auth: Tuple[str, str], params: Dict[str, Any]
) -> Dict[str, Any]:
    url = f"{base_url}/api/pms/units"
    r = requests.get(url, params=params, auth=auth, timeout=30)

    # Parsear JSON una sola vez
    try:
        data = r.json()
    except Exception as e:
        print(f"Error parseando JSON para params={params}: {e}")
        print(f"Raw response (primeros 500 chars): {r.text[:500]}")
        data = {}

    return {"status": r.status_code, "data": data}


def summarize(data: Dict[str, Any]) -> Tuple[int, int]:
    """Extrae total_items y page_len de la respuesta HAL+JSON de la API"""
    # La API devuelve HAL+JSON con _embedded.units y total_items en la raíz
    emb = data.get("_embedded", {})
    units = emb.get("units", [])
    total_items = data.get("total_items", 0)
    page_len = len(units) if isinstance(units, list) else 0

    return total_items, page_len


def probe_endpoint(
    base_url: str, auth: Tuple[str, str], endpoint: str, params: Dict[str, Any]
) -> Dict[str, Any]:
    """Probe un endpoint específico"""
    url = f"{base_url}/{endpoint.lstrip('/')}"
    try:
        r = requests.get(url, params=params, auth=auth, timeout=30)
        # Aceptar application/json y application/hal+json
        content_type = r.headers.get("content-type", "").lower()
        if "json" in content_type or "hal" in content_type:
            data = r.json()
        else:
            data = {}
        return {"status": r.status_code, "data": data, "url": url, "params": params}
    except Exception as e:
        return {"status": 0, "error": str(e), "url": url, "params": params}


def main() -> None:
    base_url, username, password = load_env()
    auth = (username, password)

    print(f"\nPROBE INTELLIGENTE - URL Base: {base_url}")
    print(f"Username: {username}")
    print("=" * 80)

    # 1. PROBE DE ENDPOINTS RELACIONADOS (para validar alcance del problema)
    print("\n[1] PROBANDO ENDPOINTS RELACIONADOS...")
    related_results = {}

    # Reservations
    r_res = probe_endpoint(
        base_url, auth, "api/pms/reservations", {"page": 1, "size": 5}
    )
    reservations_data = r_res.get("data", {})
    reservations = reservations_data.get("_embedded", {}).get("reservations", [])
    related_results["reservations"] = {
        "status": r_res.get("status"),
        "total_items": reservations_data.get("total_items", 0),
        "page_len": len(reservations) if isinstance(reservations, list) else 0,
    }
    print(f"  Reservations: {related_results['reservations']}")

    # Amenities
    r_amen = probe_endpoint(
        base_url, auth, "api/pms/units/amenities", {"page": 1, "size": 5}
    )
    amenities_data = r_amen.get("data", {})
    amenities = amenities_data.get("_embedded", {}).get(
        "amenities", amenities_data.get("amenities", [])
    )
    related_results["amenities"] = {
        "status": r_amen.get("status"),
        "total_items": amenities_data.get("total_items", 0),
        "page_len": len(amenities) if isinstance(amenities, list) else 0,
    }
    print(f"  Amenities: {related_results['amenities']}")

    # 2. PROBE DE UNITS CON CASOS MÍNIMOS PRIMERO
    print("\n[2] PROBANDO CASOS BASE DE UNITS...")

    searches = [None, "pool", "luxury", "villa"]
    sizes = [5, 20, 50]
    bools = [None, 1]  # 1 == true
    include_flags = [0, 1]

    matrix: List[Dict[str, Any]] = []

    # Casos base (sin filtros)
    matrix.append({"page": 1, "size": 5})
    matrix.append({"page": 1, "size": 20})
    matrix.append({"page": 1, "size": 50})

    # Variantes con search y flags de contenido
    for s, inc, inh, comp, sz in product(
        searches, include_flags, include_flags, include_flags, sizes
    ):
        if s is None:
            continue
        matrix.append(
            {
                "page": 1,
                "size": sz,
                "search": s,
                "includeDescriptions": inc,
                "inherited": inh,
                "computed": comp,
            }
        )

    # Variantes booleanas combinadas
    for is_bookable, pets_friendly, is_active, sz in product(
        bools, bools, bools, sizes
    ):
        p: Dict[str, Any] = {"page": 1, "size": sz}
        if is_bookable is not None:
            p["isBookable"] = is_bookable
        if pets_friendly is not None:
            p["petsFriendly"] = pets_friendly
        if is_active is not None:
            p["isActive"] = is_active
        matrix.append(p)

    # Combos con search + booleanos + flags
    for term in ["pool", "luxury"]:
        for inc, inh, comp in product(include_flags, include_flags, include_flags):
            matrix.append(
                {
                    "page": 1,
                    "size": 50,
                    "search": term,
                    "includeDescriptions": inc,
                    "inherited": inh,
                    "computed": comp,
                    "isBookable": 1,
                    "petsFriendly": 1,
                }
            )

    results: List[Dict[str, Any]] = []
    for idx, params in enumerate(matrix, 1):
        resp = call_units(base_url, auth, params)
        total_items, page_len = summarize(resp.get("data", {}))
        results.append(
            {
                "idx": idx,
                "params": params,
                "status": resp.get("status"),
                "total_items": total_items,
                "page_len": page_len,
            }
        )

    # Reporte en consola: top casos con page_len > 0 y los que dan 0
    positives = [r for r in results if r["page_len"] > 0]
    zeros = [r for r in results if r["page_len"] == 0]

    print("\n=== RESUMEN PROBE UNITS ===")
    print(f"Casos totales: {len(results)}")
    print(f"Con resultados: {len(positives)} | Sin resultados: {len(zeros)}")
    print("Ejemplos con resultados:")
    for r in positives[:5]:
        print(" -", r)
    print("Ejemplos sin resultados:")
    for r in zeros[:5]:
        print(" -", r)

    # Guardar JSON
    out = {
        "generated_at": datetime.utcnow().isoformat(),
        "base_url": base_url,
        "summary": {
            "total_cases": len(results),
            "positives": len(positives),
            "zeros": len(zeros),
        },
        "results": results,
    }
    os.makedirs("reports", exist_ok=True)
    path = os.path.join(
        "reports", f"units_probe_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Reporte guardado en: {path}")


if __name__ == "__main__":
    main()
