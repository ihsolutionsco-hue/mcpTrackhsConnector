"""Analizar resultados del probe de units API"""

import json
import sys
from pathlib import Path


def main():
    reports_dir = Path("reports")
    probe_files = sorted(reports_dir.glob("units_probe_*.json"), reverse=True)

    if not probe_files:
        print("No se encontraron reportes de probe")
        return

    latest_file = probe_files[0]
    print(f"\nAnalizando: {latest_file.name}")

    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data["results"]

    # Estadísticas generales
    print("\n=== ESTADISTICAS GENERALES ===")
    print(f"Total casos: {len(results)}")
    print(f"Todos funcionan (status 200): {all(r['status'] == 200 for r in results)}")
    print(
        f"Promedio total_items: {sum(r['total_items'] for r in results) / len(results):.1f}"
    )
    print(f"Max total_items: {max(r['total_items'] for r in results)}")
    print(f"Min total_items: {min(r['total_items'] for r in results)}")

    # Casos combinados (search + isBookable + petsFriendly)
    combos = [
        r
        for r in results
        if r["params"].get("search")
        and r["params"].get("isBookable") == 1
        and r["params"].get("petsFriendly") == 1
    ]

    print("\n=== CASOS COMBINADOS (search + isBookable + petsFriendly) ===")
    print(f"Total casos combinados: {len(combos)}")
    if combos:
        print("\nEjemplos (primeros 5):")
        for c in combos[:5]:
            search = c["params"].get("search")
            total = c["total_items"]
            print(f"  '{search}': {total} unidades")

    # Casos sin filtros
    no_filters = [r for r in results if len(r["params"]) == 2]  # Solo page y size
    print("\n=== CASOS SIN FILTROS ===")
    print(f"Total casos sin filtros: {len(no_filters)}")
    if no_filters:
        for nf in no_filters:
            print(
                f"  page={nf['params']['page']}, size={nf['params']['size']}: {nf['total_items']} unidades"
            )

    # Casos con search
    with_search = [r for r in results if r["params"].get("search")]
    print("\n=== CASOS CON SEARCH ===")
    print(f"Total casos con search: {len(with_search)}")
    search_terms = {}
    for r in with_search:
        term = r["params"].get("search")
        if term not in search_terms:
            search_terms[term] = []
        search_terms[term].append(r["total_items"])

    print("\nEstadísticas por término de búsqueda:")
    for term, totals in search_terms.items():
        print(
            f"  '{term}': {len(totals)} variantes, {min(totals)}-{max(totals)} unidades (promedio: {sum(totals)/len(totals):.1f})"
        )

    print("\n=== CONCLUSIONES ===")
    all_working = all(r["status"] == 200 for r in results)
    all_have_data = all(r["total_items"] > 0 for r in results)

    if all_working and all_have_data:
        print("[OK] TODOS los casos funcionan correctamente")
        print("[OK] La API esta respondiendo correctamente")
        print("[OK] No se detectaron problemas con los filtros")
    else:
        print("[WARNING] Algunos casos pueden tener problemas")
        if not all_working:
            failed = [r for r in results if r["status"] != 200]
            print(f"  - {len(failed)} casos con status != 200")
        if not all_have_data:
            no_data = [r for r in results if r["total_items"] == 0]
            print(f"  - {len(no_data)} casos sin datos (total_items=0)")


if __name__ == "__main__":
    main()
