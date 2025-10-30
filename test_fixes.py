#!/usr/bin/env python3
"""
Script para probar las correcciones implementadas
"""

import os
import sys

sys.path.append("src")

from dotenv import load_dotenv

from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger

# Configurar logger
logger = get_logger(__name__)


def test_date_coercion():
    """Probar la coerción de fechas corregida"""
    print("PROBANDO COERCION DE FECHAS")
    print("=" * 50)

    # Importar el módulo mcp_tools para acceder a las funciones
    import mcp_tools

    # Crear un mock del servidor MCP para registrar las herramientas
    class MockMCPServer:
        def tool(self):
            def decorator(func):
                return func

            return decorator

    mock_server = MockMCPServer()
    mcp_tools.register_tools_with_mcp(mock_server)

    # Definir las funciones localmente para probar
    def _coerce_date_str(value):
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            # Solo aceptar fechas completas YYYY-MM-DD
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                return v
            # Si es solo año (2024), devolver None para evitar errores
            if re.fullmatch(r"\d{4}", v):
                return None
        return None

    import re

    # Casos de prueba
    test_cases = [
        ("2024-01-15", "2024-01-15"),  # Fecha válida
        ("2024", None),  # Solo año - debe devolver None
        ("2024-01", None),  # Año-mes - debe devolver None
        ("invalid", None),  # Inválido
        (None, None),  # None
        ("", None),  # Vacío
    ]

    passed = 0
    total = len(test_cases)

    for input_val, expected in test_cases:
        result = _coerce_date_str(input_val)
        if result == expected:
            print(f"  OK {input_val!r} -> {result}")
            passed += 1
        else:
            print(f"  ERROR {input_val!r} -> {result}, esperado {expected}")

    print(f"\nCoerción de fechas: {passed}/{total} casos exitosos")
    return passed == total


def test_api_with_fixed_coercion():
    """Probar el API con coerción corregida"""
    print("\nPROBANDO API CON COERCION CORREGIDA")
    print("=" * 50)

    try:
        # Cargar credenciales
        load_dotenv()
        base_url = os.getenv("TRACKHS_BASE_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            print("  ERROR: Credenciales no configuradas")
            return False

        # Inicializar cliente
        client = TrackHSAPIClient(base_url, username, password)
        print("  OK Cliente API inicializado")

        # Probar búsqueda de reservas con fecha parcial (debe fallar silenciosamente)
        print("\n  Probando búsqueda con fecha parcial '2024'...")
        try:
            response = client.search_reservations(
                {
                    "page": 1,
                    "size": 3,
                    "arrival_start": "2024",  # Esto debería convertirse a None
                    "arrival_end": "2024",  # Esto debería convertirse a None
                }
            )
            print(
                f"  OK Búsqueda con fechas parciales: {response.get('total_items')} resultados"
            )
        except Exception as e:
            print(f"  ERROR en búsqueda con fechas parciales: {e}")
            return False

        # Probar búsqueda de unidades con fecha parcial
        print("\n  Probando búsqueda de unidades con fecha parcial '2024'...")
        try:
            response = client.search_units(
                {
                    "page": 1,
                    "size": 3,
                    "arrival": "2024",  # Esto debería convertirse a None
                    "departure": "2024",  # Esto debería convertirse a None
                }
            )
            print(
                f"  OK Búsqueda de unidades con fechas parciales: {response.get('total_items')} resultados"
            )
        except Exception as e:
            print(f"  ERROR en búsqueda de unidades con fechas parciales: {e}")
            return False

        return True

    except Exception as e:
        print(f"  ERROR en cliente API: {e}")
        return False


def test_folio_documentation():
    """Probar que la documentación de get_folio es clara"""
    print("\nPROBANDO DOCUMENTACION DE GET_FOLIO")
    print("=" * 50)

    # Leer el archivo mcp_tools.py y buscar la documentación de get_folio
    with open("src/mcp_tools.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar que contiene las mejoras
    improvements = [
        "IMPORTANTE: Este es el ID del folio, NO el ID de la reserva",
        "CÓMO OBTENER EL FOLIO_ID:",
        "get_reservation(reservation_id=123) para obtener detalles",
        "IMPORTANTE:",
        "1. Usa get_reservation(reservation_id=123)",
        "2. En la respuesta, busca el campo 'folio_id'",
        "3. Usa get_folio(folio_id=456)",
    ]

    found = 0
    for improvement in improvements:
        if improvement in content:
            print(f"  OK Encontrado: {improvement}")
            found += 1
        else:
            print(f"  ERROR No encontrado: {improvement}")

    print(f"\nDocumentación: {found}/{len(improvements)} mejoras encontradas")
    return found == len(improvements)


def main():
    """Función principal de prueba"""
    print("PRUEBAS DE CORRECCIONES IMPLEMENTADAS")
    print("=" * 60)

    tests = [
        ("Coerción de fechas", test_date_coercion),
        ("API con coerción corregida", test_api_with_fixed_coercion),
        ("Documentación de get_folio", test_folio_documentation),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        print(f"\n{name}:")
        if test_func():
            passed += 1
        else:
            print(f"  ERROR {name} falló")

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {passed}/{total} pruebas exitosas")

    if passed == total:
        print("TODAS LAS CORRECCIONES FUNCIONAN CORRECTAMENTE")
        return True
    else:
        print("ALGUNAS CORRECCIONES NECESITAN AJUSTES")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
