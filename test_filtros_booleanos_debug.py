#!/usr/bin/env python3
"""
Script de debug específico para verificar el comportamiento de los filtros is_active e is_bookable.
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


def test_filtros_booleanos_debug():
    """Debug específico de filtros booleanos"""

    print("=" * 80)
    print("🔍 DEBUG ESPECÍFICO - FILTROS BOOLEANOS is_active e is_bookable")
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

        # Test 1: Búsqueda sin filtros para ver el estado real de las unidades
        print("🔍 TEST 1: Búsqueda sin filtros (para ver estado real)")
        print("-" * 50)

        result_sin_filtros = unit_service.search_units(page=1, size=10)
        units_sin_filtros = result_sin_filtros.get("_embedded", {}).get("units", [])

        print(f"Total de unidades encontradas: {len(units_sin_filtros)}")
        print("\nEstado real de las primeras 10 unidades:")
        for i, unit in enumerate(units_sin_filtros[:10]):
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(unit.get('is_active', 'N/A')):5s} | "
                f"isBookable: {str(unit.get('is_bookable', 'N/A')):5s} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Test 2: Búsqueda con is_active=1
        print("🔍 TEST 2: Búsqueda con is_active=1")
        print("-" * 50)

        result_activas = unit_service.search_units(page=1, is_active=1, size=10)
        units_activas = result_activas.get("_embedded", {}).get("units", [])

        print(f"Parámetros enviados: is_active=1")
        print(f"Total de unidades encontradas: {len(units_activas)}")
        print(f"Total en sistema: {result_activas.get('total_items', 'N/A')}")

        print("\nUnidades retornadas con is_active=1:")
        for i, unit in enumerate(units_activas):
            is_active_real = unit.get("is_active", "N/A")
            is_bookable_real = unit.get("is_bookable", "N/A")
            status_icon = "✅" if is_active_real is True else "❌"
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(is_active_real):5s} {status_icon} | "
                f"isBookable: {str(is_bookable_real):5s} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Test 3: Búsqueda con is_bookable=1
        print("🔍 TEST 3: Búsqueda con is_bookable=1")
        print("-" * 50)

        result_reservables = unit_service.search_units(page=1, is_bookable=1, size=10)
        units_reservables = result_reservables.get("_embedded", {}).get("units", [])

        print(f"Parámetros enviados: is_bookable=1")
        print(f"Total de unidades encontradas: {len(units_reservables)}")
        print(f"Total en sistema: {result_reservables.get('total_items', 'N/A')}")

        print("\nUnidades retornadas con is_bookable=1:")
        for i, unit in enumerate(units_reservables):
            is_active_real = unit.get("is_active", "N/A")
            is_bookable_real = unit.get("is_bookable", "N/A")
            status_icon = "✅" if is_bookable_real is True else "❌"
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(is_active_real):5s} | "
                f"isBookable: {str(is_bookable_real):5s} {status_icon} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Test 4: Búsqueda con ambos filtros
        print("🔍 TEST 4: Búsqueda con is_active=1 E is_bookable=1")
        print("-" * 50)

        result_ambos = unit_service.search_units(
            page=1, is_active=1, is_bookable=1, size=10
        )
        units_ambos = result_ambos.get("_embedded", {}).get("units", [])

        print(f"Parámetros enviados: is_active=1, is_bookable=1")
        print(f"Total de unidades encontradas: {len(units_ambos)}")
        print(f"Total en sistema: {result_ambos.get('total_items', 'N/A')}")

        print("\nUnidades retornadas con ambos filtros:")
        for i, unit in enumerate(units_ambos):
            is_active_real = unit.get("is_active", "N/A")
            is_bookable_real = unit.get("is_bookable", "N/A")
            status_icon_active = "✅" if is_active_real is True else "❌"
            status_icon_bookable = "✅" if is_bookable_real is True else "❌"
            print(
                f"  {i+1:2d}. ID {str(unit.get('id', 'N/A')):3s} | "
                f"isActive: {str(is_active_real):5s} {status_icon_active} | "
                f"isBookable: {str(is_bookable_real):5s} {status_icon_bookable} | "
                f"Nombre: {unit.get('name', 'N/A')[:30]}"
            )
        print()

        # Test 5: Verificar qué parámetros se están enviando realmente a la API
        print("🔍 TEST 5: Debug de parámetros enviados a la API")
        print("-" * 50)

        # Habilitar debug logging temporalmente
        import logging

        logging.getLogger().setLevel(logging.DEBUG)

        print("Enviando request con is_active=1...")
        result_debug = unit_service.search_units(page=1, is_active=1, size=3)

        print("Request completado. Revisar logs arriba para ver parámetros enviados.")
        print()

        # Análisis de resultados
        print("=" * 80)
        print("📊 ANÁLISIS DE RESULTADOS")
        print("=" * 80)

        # Contar unidades realmente activas vs retornadas
        unidades_realmente_activas = sum(
            1 for unit in units_sin_filtros if unit.get("is_active") is True
        )
        unidades_realmente_reservables = sum(
            1 for unit in units_sin_filtros if unit.get("is_bookable") is True
        )

        print(f"📈 Estadísticas del sistema (primeras 10 unidades):")
        print(f"   - Unidades realmente activas: {unidades_realmente_activas}/10")
        print(
            f"   - Unidades realmente reservables: {unidades_realmente_reservables}/10"
        )
        print()

        print(f"🔍 Efectividad de filtros:")
        print(f"   - is_active=1 retorna: {len(units_activas)} unidades")
        print(f"   - is_bookable=1 retorna: {len(units_reservables)} unidades")
        print(f"   - Ambos filtros retorna: {len(units_ambos)} unidades")
        print()

        # Verificar si los filtros están funcionando
        filtros_funcionan = True
        if len(units_activas) > 0:
            unidades_incorrectas_activas = sum(
                1 for unit in units_activas if unit.get("is_active") is not True
            )
            if unidades_incorrectas_activas > 0:
                print(
                    f"❌ PROBLEMA: is_active=1 retorna {unidades_incorrectas_activas} unidades que NO están activas"
                )
                filtros_funcionan = False

        if len(units_reservables) > 0:
            unidades_incorrectas_reservables = sum(
                1 for unit in units_reservables if unit.get("is_bookable") is not True
            )
            if unidades_incorrectas_reservables > 0:
                print(
                    f"❌ PROBLEMA: is_bookable=1 retorna {unidades_incorrectas_reservables} unidades que NO son reservables"
                )
                filtros_funcionan = False

        if filtros_funcionan:
            print("✅ Los filtros booleanos funcionan correctamente")
        else:
            print("❌ Los filtros booleanos NO funcionan correctamente")
            print("   Posibles causas:")
            print("   1. La API de TrackHS no soporta estos parámetros")
            print("   2. Los parámetros tienen nombres diferentes")
            print("   3. Los valores esperados son diferentes (true/false vs 1/0)")
            print("   4. Los filtros están siendo ignorados por la API")

        return filtros_funcionan

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_filtros_booleanos_debug()
    sys.exit(0 if success else 1)
