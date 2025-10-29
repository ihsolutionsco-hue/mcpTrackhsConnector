#!/usr/bin/env python3
"""
Script de prueba con llamadas reales a la API de TrackHS
"""

import os
import sys
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv

load_dotenv()

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_tools import register_tools_with_mcp, setup_tools
from server_logic import create_api_client, create_mcp_server


def test_search_units():
    """Prueba el endpoint search_units con diferentes parámetros"""
    print("=" * 60)
    print("PRUEBA: search_units")
    print("=" * 60)

    api_client = create_api_client()
    if not api_client:
        print("ERROR: No se pudo crear cliente API")
        return False

    # Prueba 1: Búsqueda básica
    print("\n1. Búsqueda básica (page=1, size=5):")
    try:
        result = api_client.search_units({"page": 1, "size": 5})
        print(f"   Total items: {result.get('total_items', 0)}")
        print(f"   Units encontradas: {len(result.get('units', []))}")
        print(f"   Páginas totales: {result.get('total_pages', 0)}")

        if result.get("units"):
            print("   Primera unidad:")
            unit = result["units"][0]
            for key, value in unit.items():
                print(f"     {key}: {value}")
        else:
            print("   No se encontraron unidades")

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False

    # Prueba 2: Con filtros
    print("\n2. Búsqueda con filtros (is_active=True):")
    try:
        result = api_client.search_units({"page": 1, "size": 10, "is_active": True})
        print(f"   Total items: {result.get('total_items', 0)}")
        print(f"   Units encontradas: {len(result.get('units', []))}")
    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False

    return True


def test_search_amenities():
    """Prueba el endpoint search_amenities"""
    print("\n" + "=" * 60)
    print("PRUEBA: search_amenities")
    print("=" * 60)

    api_client = create_api_client()
    if not api_client:
        print("ERROR: No se pudo crear cliente API")
        return False

    print("\n1. Búsqueda básica de amenidades:")
    try:
        result = api_client.search_amenities({"page": 1, "size": 10})
        print(f"   Total items: {result.get('total_items', 0)}")
        print(f"   Amenidades encontradas: {len(result.get('amenities', []))}")

        if result.get("amenities"):
            print("   Primera amenidad:")
            amenity = result["amenities"][0]
            for key, value in amenity.items():
                print(f"     {key}: {value}")
        else:
            print("   No se encontraron amenidades")

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False

    return True


def test_search_reservations():
    """Prueba el endpoint search_reservations"""
    print("\n" + "=" * 60)
    print("PRUEBA: search_reservations")
    print("=" * 60)

    api_client = create_api_client()
    if not api_client:
        print("ERROR: No se pudo crear cliente API")
        return False

    print("\n1. Búsqueda básica de reservas:")
    try:
        result = api_client.search_reservations({"page": 1, "size": 10})
        print(f"   Total items: {result.get('total_items', 0)}")
        print(f"   Reservas encontradas: {len(result.get('reservations', []))}")

        if result.get("reservations"):
            print("   Primera reserva:")
            reservation = result["reservations"][0]
            for key, value in reservation.items():
                print(f"     {key}: {value}")
        else:
            print("   No se encontraron reservas")

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False

    return True


def test_mcp_tools():
    """Prueba las herramientas MCP registradas"""
    print("\n" + "=" * 60)
    print("PRUEBA: Herramientas MCP")
    print("=" * 60)

    try:
        # Crear servidor MCP
        mcp_server = create_mcp_server()
        api_client = create_api_client()

        if not api_client:
            print("ERROR: No se pudo crear cliente API")
            return False

        # Configurar herramientas
        setup_tools(api_client)
        register_tools_with_mcp(mcp_server)

        # Obtener herramientas registradas
        tools = getattr(mcp_server, "_tools", {})
        print(f"\nHerramientas registradas: {len(tools)}")
        for tool_name in tools.keys():
            print(f"  - {tool_name}")

        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def main():
    """Función principal de pruebas"""
    print("PRUEBAS REALES DE API TRACKHS")
    print("=" * 60)

    # Verificar credenciales
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        print("ERROR: Credenciales no configuradas")
        return False

    print(f"Usuario: {username}")
    print(f"Password: {'*' * len(password)}")

    # Ejecutar pruebas
    tests = [
        ("Search Units", test_search_units),
        ("Search Amenities", test_search_amenities),
        ("Search Reservations", test_search_reservations),
        ("MCP Tools", test_mcp_tools),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"RESULTADO: {'PASO' if success else 'FALLO'}")
        except Exception as e:
            print(f"ERROR INESPERADO: {str(e)}")
            results.append((test_name, False))

    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    passed = 0
    for test_name, success in results:
        status = "PASO" if success else "FALLO"
        print(f"{test_name:20} : {status}")
        if success:
            passed += 1

    print(f"\nPruebas pasadas: {passed}/{len(results)}")

    if passed == len(results):
        print("\nTODAS LAS PRUEBAS PASARON - Sistema funcionando correctamente")
    else:
        print(f"\n{len(results) - passed} PRUEBAS FALLARON - Revisar errores")

    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
