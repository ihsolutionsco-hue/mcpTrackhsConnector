#!/usr/bin/env python3
"""
Simulación local de pruebas para search_units
Prueba los mismos casos que hemos estado probando con MCP
"""

import asyncio
import os
import sys
from pathlib import Path

import httpx

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.config import get_settings
from trackhs_mcp.repositories.unit_repository import UnitRepository
from trackhs_mcp.services.unit_service import UnitService


# Definir TrackHSClient localmente (copiado de server.py)
class TrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = httpx.BasicAuth(username, password)
        self.client = httpx.Client(auth=self.auth, timeout=30)

    def get(self, endpoint: str, params: dict = None):
        """Hacer petición GET a la API"""
        url = f"{self.base_url}/{endpoint}"
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Cerrar el cliente HTTP"""
        self.client.close()


def test_search_units_local():
    """Probar search_units localmente con los mismos casos que fallaron en MCP"""

    print("🧪 SIMULACIÓN LOCAL DE PRUEBAS SEARCH_UNITS")
    print("=" * 50)

    # Configurar servicios
    settings = get_settings()
    api_client = TrackHSClient(
        settings.trackhs_api_url, settings.trackhs_username, settings.trackhs_password
    )
    unit_repo = UnitRepository(api_client)
    unit_service = UnitService(unit_repo)

    # Casos de prueba que han fallado en MCP
    test_cases = [
        {
            "name": "Búsqueda básica (sin filtros)",
            "params": {"page": 1, "size": 5},
            "description": "¿Qué unidades hay disponibles?",
        },
        {
            "name": "Búsqueda por dormitorios",
            "params": {"page": 1, "size": 5, "bedrooms": "2"},
            "description": "¿Qué unidades hay con 2 dormitorios?",
        },
        {
            "name": "Búsqueda por baños",
            "params": {"page": 1, "size": 5, "bathrooms": "1"},
            "description": "¿Qué unidades hay con 1 baño?",
        },
        {
            "name": "Búsqueda por texto",
            "params": {"page": 1, "size": 5, "search": "penthouse"},
            "description": "¿Hay alguna unidad que contenga 'penthouse'?",
        },
        {
            "name": "Búsqueda por estado activo",
            "params": {"page": 1, "size": 5, "is_active": "1", "is_bookable": "1"},
            "description": "¿Qué unidades están activas y disponibles?",
        },
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Prueba {i}: {test_case['name']}")
        print(f"Pregunta: {test_case['description']}")
        print(f"Parámetros: {test_case['params']}")

        try:
            # Simular la llamada a search_units
            result = unit_service.search_units(**test_case["params"])

            print(
                f"✅ ÉXITO: {len(result.get('_embedded', {}).get('units', []))} unidades encontradas"
            )
            print(f"Total items: {result.get('total_items', 0)}")

            # Mostrar algunas unidades si hay
            units = result.get("_embedded", {}).get("units", [])
            if units:
                print("Primeras unidades:")
                for j, unit in enumerate(units[:2], 1):
                    print(
                        f"  {j}. {unit.get('name', 'Sin nombre')} - {unit.get('bedrooms', 'N/A')} dorm, {unit.get('bathrooms', 'N/A')} baños"
                    )

            results.append(
                {
                    "test": test_case["name"],
                    "status": "SUCCESS",
                    "units_found": len(units),
                    "total_items": result.get("total_items", 0),
                }
            )

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results.append(
                {"test": test_case["name"], "status": "ERROR", "error": str(e)}
            )

    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 50)

    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    error_count = sum(1 for r in results if r["status"] == "ERROR")

    print(f"✅ Pruebas exitosas: {success_count}/{len(results)}")
    print(f"❌ Pruebas fallidas: {error_count}/{len(results)}")

    for result in results:
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        if result["status"] == "SUCCESS":
            print(f"{status_icon} {result['test']}: {result['units_found']} unidades")
        else:
            print(f"{status_icon} {result['test']}: {result['error']}")

    return results


if __name__ == "__main__":
    test_search_units_local()
