#!/usr/bin/env python3
"""
Script para probar búsqueda de unidades con credenciales reales
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def load_credentials():
    """Carga credenciales desde el archivo .env"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    return (
        os.getenv("TRACKHS_API_URL"),
        os.getenv("TRACKHS_USERNAME"),
        os.getenv("TRACKHS_PASSWORD"),
    )


def test_units_search():
    """Prueba la búsqueda de unidades con credenciales reales"""
    print("Test de Busqueda de Unidades con Credenciales Reales")
    print("=" * 70)

    # Cargar credenciales
    api_url, username, password = load_credentials()

    if not all([api_url, username, password]):
        print("[ERROR] No se pudieron cargar las credenciales")
        return

    try:
        from schemas.unit import UnitSearchParams
        from tools.search_units import SearchUnitsTool
        from utils.api_client import TrackHSAPIClient

        # Crear cliente API
        print("1. Creando cliente API...")
        api_client = TrackHSAPIClient(
            base_url=api_url, username=username, password=password
        )
        print("   [OK] Cliente API creado")

        # Crear herramienta de búsqueda
        search_tool = SearchUnitsTool(api_client)

        # Test 1: Búsqueda básica
        print("\n2. Test 1: Busqueda basica (sin filtros)")
        print("-" * 50)
        try:
            params1 = UnitSearchParams(page=1, size=5)
            result1 = search_tool._execute_logic(params1)

            print(f"   Unidades encontradas: {len(result1.get('units', []))}")
            print(f"   Total items: {result1.get('total_items', 0)}")
            print(f"   Total pages: {result1.get('total_pages', 0)}")
            print(f"   Current page: {result1.get('current_page', 0)}")
            print(f"   Has next: {result1.get('has_next', False)}")
            print(f"   Has prev: {result1.get('has_prev', False)}")

            # Mostrar primera unidad si existe
            units = result1.get("units", [])
            if units:
                print(f"\n   Primera unidad encontrada:")
                first_unit = units[0]
                for key, value in first_unit.items():
                    print(f"     {key}: {value}")
            else:
                print(f"\n   [INFO] No se encontraron unidades")

        except Exception as e:
            print(f"   [ERROR] Error en búsqueda básica: {str(e)}")

        # Test 2: Búsqueda con filtros
        print(f"\n3. Test 2: Busqueda con filtros (is_active=True)")
        print("-" * 50)
        try:
            params2 = UnitSearchParams(page=1, size=5, is_active=True)
            result2 = search_tool._execute_logic(params2)

            print(f"   Unidades encontradas: {len(result2.get('units', []))}")
            print(f"   Total items: {result2.get('total_items', 0)}")
            print(f"   Total pages: {result2.get('total_pages', 0)}")

        except Exception as e:
            print(f"   [ERROR] Error en búsqueda con filtros: {str(e)}")

        # Test 3: Búsqueda con filtros de dormitorios
        print(f"\n4. Test 3: Busqueda con filtros de dormitorios (bedrooms=2)")
        print("-" * 50)
        try:
            params3 = UnitSearchParams(page=1, size=5, bedrooms=2)
            result3 = search_tool._execute_logic(params3)

            print(f"   Unidades encontradas: {len(result3.get('units', []))}")
            print(f"   Total items: {result3.get('total_items', 0)}")
            print(f"   Total pages: {result3.get('total_pages', 0)}")

        except Exception as e:
            print(f"   [ERROR] Error en búsqueda con dormitorios: {str(e)}")

        # Test 4: Búsqueda con texto
        print(f"\n5. Test 4: Busqueda con texto (search='apartment')")
        print("-" * 50)
        try:
            params4 = UnitSearchParams(page=1, size=5, search="apartment")
            result4 = search_tool._execute_logic(params4)

            print(f"   Unidades encontradas: {len(result4.get('units', []))}")
            print(f"   Total items: {result4.get('total_items', 0)}")
            print(f"   Total pages: {result4.get('total_pages', 0)}")

        except Exception as e:
            print(f"   [ERROR] Error en búsqueda con texto: {str(e)}")

        # Test 5: Búsqueda con múltiples filtros
        print(f"\n6. Test 5: Busqueda con multiples filtros")
        print("-" * 50)
        try:
            params5 = UnitSearchParams(
                page=1, size=5, is_active=True, is_bookable=True, bedrooms=2
            )
            result5 = search_tool._execute_logic(params5)

            print(f"   Unidades encontradas: {len(result5.get('units', []))}")
            print(f"   Total items: {result5.get('total_items', 0)}")
            print(f"   Total pages: {result5.get('total_pages', 0)}")

        except Exception as e:
            print(f"   [ERROR] Error en búsqueda con múltiples filtros: {str(e)}")

        api_client.close()

        print(f"\n" + "=" * 70)
        print("[SUCCESS] Testing de búsqueda de unidades completado!")
        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] Error general: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_units_search()
