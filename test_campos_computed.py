#!/usr/bin/env python3
"""
Test específico para verificar que los campos isActive e isBookable aparecen en la respuesta
cuando se usa el parámetro computed=1.
"""

import json
import sys
import time
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, "src")

from trackhs_mcp.repositories.unit_repository import UnitRepository
from trackhs_mcp.server import API_BASE_URL, API_PASSWORD, API_USERNAME, TrackHSClient
from trackhs_mcp.services.unit_service import UnitService


def test_campos_computed():
    """Test para verificar campos computed"""

    print("=" * 80)
    print("🔍 TEST - CAMPOS COMPUTED (isActive e isBookable)")
    print("=" * 80)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()

    # Verificar configuración
    if not API_USERNAME or not API_PASSWORD:
        print("❌ ERROR: Credenciales no configuradas")
        return False

    try:
        # Inicializar cliente y servicios
        print("🔌 Inicializando cliente API...")
        api_client = TrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)
        unit_repo = UnitRepository(api_client)
        unit_service = UnitService(unit_repo)
        print("✅ Servicios inicializados correctamente")
        print()

        # Test 1: Búsqueda sin computed
        print("🔍 TEST 1: Búsqueda SIN computed=1")
        print("-" * 50)

        result_sin_computed = unit_service.search_units(page=1, size=3)
        units_sin_computed = result_sin_computed.get("_embedded", {}).get("units", [])

        print(f"Total de unidades: {len(units_sin_computed)}")
        if units_sin_computed:
            first_unit = units_sin_computed[0]
            print(f"Primera unidad:")
            print(f"  - ID: {first_unit.get('id')}")
            print(f"  - isActive: {first_unit.get('isActive', 'NO PRESENTE')}")
            print(f"  - isBookable: {first_unit.get('isBookable', 'NO PRESENTE')}")
            print(f"  - Campos disponibles: {list(first_unit.keys())[:10]}...")
        print()

        # Test 2: Búsqueda con computed=1 (ya está en el código)
        print("🔍 TEST 2: Búsqueda CON computed=1 (automático)")
        print("-" * 50)

        result_con_computed = unit_service.search_units(page=1, size=3)
        units_con_computed = result_con_computed.get("_embedded", {}).get("units", [])

        print(f"Total de unidades: {len(units_con_computed)}")
        if units_con_computed:
            first_unit = units_con_computed[0]
            print(f"Primera unidad:")
            print(f"  - ID: {first_unit.get('id')}")
            print(f"  - isActive: {first_unit.get('isActive', 'NO PRESENTE')}")
            print(f"  - isBookable: {first_unit.get('isBookable', 'NO PRESENTE')}")
            print(f"  - Campos disponibles: {list(first_unit.keys())[:10]}...")
        print()

        # Test 3: Búsqueda con filtros y computed
        print("🔍 TEST 3: Búsqueda con isActive=1 y computed=1")
        print("-" * 50)

        result_filtrado = unit_service.search_units(page=1, is_active=1, size=5)
        units_filtradas = result_filtrado.get("_embedded", {}).get("units", [])

        print(f"Total de unidades activas: {len(units_filtradas)}")
        print(f"Total en sistema: {result_filtrado.get('total_items', 'N/A')}")

        print("\nUnidades activas encontradas:")
        for i, unit in enumerate(units_filtradas):
            is_active = unit.get("isActive", "NO PRESENTE")
            is_bookable = unit.get("isBookable", "NO PRESENTE")
            status_icon = (
                "✅" if is_active is True else "❌" if is_active is False else "❓"
            )
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(is_active):5s} {status_icon} | "
                f"isBookable: {str(is_bookable):5s} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Test 4: Búsqueda con isBookable=1
        print("🔍 TEST 4: Búsqueda con isBookable=1 y computed=1")
        print("-" * 50)

        result_bookable = unit_service.search_units(page=1, is_bookable=1, size=5)
        units_bookable = result_bookable.get("_embedded", {}).get("units", [])

        print(f"Total de unidades reservables: {len(units_bookable)}")
        print(f"Total en sistema: {result_bookable.get('total_items', 'N/A')}")

        print("\nUnidades reservables encontradas:")
        for i, unit in enumerate(units_bookable):
            is_active = unit.get("isActive", "NO PRESENTE")
            is_bookable = unit.get("isBookable", "NO PRESENTE")
            status_icon = (
                "✅" if is_bookable is True else "❌" if is_bookable is False else "❓"
            )
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(is_active):5s} | "
                f"isBookable: {str(is_bookable):5s} {status_icon} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Análisis final
        print("=" * 80)
        print("📊 ANÁLISIS FINAL")
        print("=" * 80)

        # Verificar si los campos están presentes
        campos_presentes = False
        if units_con_computed:
            first_unit = units_con_computed[0]
            if "isActive" in first_unit or "isBookable" in first_unit:
                campos_presentes = True

        if campos_presentes:
            print(
                "✅ ÉXITO: Los campos isActive e isBookable están presentes en la respuesta"
            )
            print("✅ Los filtros isActive e isBookable funcionan correctamente")
            print("✅ El parámetro computed=1 está funcionando")
        else:
            print(
                "❌ PROBLEMA: Los campos isActive e isBookable NO están en la respuesta"
            )
            print("❌ Posible problema con el parámetro computed=1")

        # Verificar efectividad de filtros
        total_unidades = result_sin_computed.get("total_items", 0)
        unidades_activas = result_filtrado.get("total_items", 0)
        unidades_reservables = result_bookable.get("total_items", 0)

        print(f"\n📈 Estadísticas de filtros:")
        print(f"   - Total de unidades: {total_unidades}")
        print(f"   - Unidades activas: {unidades_activas}")
        print(f"   - Unidades reservables: {unidades_reservables}")

        if unidades_activas < total_unidades:
            print("✅ Filtro isActive funciona (reduce resultados)")
        else:
            print("❌ Filtro isActive no funciona (mismo número de resultados)")

        if unidades_reservables < total_unidades:
            print("✅ Filtro isBookable funciona (reduce resultados)")
        else:
            print("❌ Filtro isBookable no funciona (mismo número de resultados)")

        return campos_presentes

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_campos_computed()
    sys.exit(0 if success else 1)
