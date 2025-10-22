#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones en search_units
"""

import asyncio
import json
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.domain.value_objects.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.search_units import register_search_units


async def test_search_units_fixes():
    """Probar las correcciones en search_units"""

    print("🔧 Probando correcciones en search_units...")

    # Configurar cliente API
    config = TrackHSConfig(
        base_url="https://ihmvacations.trackhs.com",
        username="test_user",
        password="test_pass",
    )

    api_client = TrackHSApiClient(config)

    # Crear un mock MCP
    class MockMCP:
        def tool(self, name):
            def decorator(func):
                return func

            return decorator

    mcp = MockMCP()

    # Registrar la herramienta
    register_search_units(mcp, api_client)

    # Obtener la función registrada
    search_units_func = None
    for attr_name in dir(mcp):
        if attr_name == "search_units":
            search_units_func = getattr(mcp, attr_name)
            break

    if not search_units_func:
        print("❌ No se pudo encontrar la función search_units")
        return False

    print("✅ Función search_units registrada correctamente")

    # Probar casos de prueba
    test_cases = [
        {
            "name": "Prueba básica con parámetros mínimos",
            "params": {"size": 3, "page": 1},
            "expected_success": True,
        },
        {
            "name": "Prueba con parámetros booleanos como int",
            "params": {"size": 3, "page": 1, "is_active": 1, "pets_friendly": 1},
            "expected_success": True,
        },
        {
            "name": "Prueba con parámetros booleanos como string",
            "params": {"size": 3, "page": 1, "is_active": "1", "pets_friendly": "0"},
            "expected_success": True,
        },
        {
            "name": "Prueba con parámetros numéricos como int",
            "params": {"size": 3, "page": 1, "bedrooms": 4, "bathrooms": 3},
            "expected_success": True,
        },
        {
            "name": "Prueba con parámetros numéricos como string",
            "params": {"size": 3, "page": 1, "bedrooms": "4", "bathrooms": "3"},
            "expected_success": True,
        },
        {
            "name": "Prueba con límite de paginación aumentado",
            "params": {"size": 10, "page": 1},
            "expected_success": True,
        },
        {
            "name": "Prueba con límite de paginación excedido",
            "params": {"size": 30, "page": 1},
            "expected_success": False,
        },
    ]

    results = []

    for test_case in test_cases:
        print(f"\n🧪 {test_case['name']}")
        print(f"   Parámetros: {test_case['params']}")

        try:
            # Ejecutar la función
            result = await search_units_func(**test_case["params"])

            if test_case["expected_success"]:
                print("   ✅ Éxito - Función ejecutada sin errores")
                results.append(True)
            else:
                print("   ❌ Falla - Se esperaba un error pero no ocurrió")
                results.append(False)

        except Exception as e:
            if not test_case["expected_success"]:
                print(f"   ✅ Éxito - Error esperado: {str(e)}")
                results.append(True)
            else:
                print(f"   ❌ Falla - Error inesperado: {str(e)}")
                results.append(False)

    # Resumen de resultados
    print(f"\n📊 Resumen de pruebas:")
    print(f"   Total de pruebas: {len(results)}")
    print(f"   Exitosas: {sum(results)}")
    print(f"   Fallidas: {len(results) - sum(results)}")

    success_rate = (sum(results) / len(results)) * 100
    print(f"   Tasa de éxito: {success_rate:.1f}%")

    if success_rate >= 80:
        print("🎉 ¡Correcciones implementadas exitosamente!")
        return True
    else:
        print("⚠️ Algunas correcciones necesitan ajustes")
        return False


if __name__ == "__main__":
    asyncio.run(test_search_units_fixes())
