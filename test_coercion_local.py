#!/usr/bin/env python3
"""
Script de prueba local para verificar la coerción de tipos en las herramientas MCP
"""

import os
import sys

sys.path.append("src")

from mcp_tools import register_tools_with_mcp
from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger

# Configurar logger
logger = get_logger(__name__)


def test_coercion_functions():
    """Probar las funciones de coerción directamente"""
    print("PROBANDO FUNCIONES DE COERCION")
    print("=" * 50)

    # Definir las funciones de coerción localmente para probar
    def _coerce_bool(value):
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(int(value))
        if isinstance(value, str):
            v = value.strip().lower()
            if v in {"true", "1", "yes", "y", "si", "sí"}:
                return True
            if v in {"false", "0", "no", "n"}:
                return False
        return None

    def _coerce_int(value):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str) and value.strip() != "":
            try:
                return int(value.strip())
            except ValueError:
                return None
        return None

    def _coerce_float(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and value.strip() != "":
            try:
                return float(value.strip())
            except ValueError:
                return None
        return None

    def _coerce_date_str(value):
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            import re

            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                return v
        return None

    def _coerce_list_int(value):
        if value is None:
            return None
        if isinstance(value, list):
            result = []
            for x in value:
                i = _coerce_int(x)
                if i is not None:
                    result.append(i)
            return result if result else None
        if isinstance(value, str):
            s = value.strip()
            try:
                import json

                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return _coerce_list_int(parsed)
            except Exception:
                import re

                parts = [p for p in re.split(r"[\s,]+", s.strip("[]")) if p]
                result = []
                for p in parts:
                    i = _coerce_int(p)
                    if i is not None:
                        result.append(i)
                return result if result else None
        return None

    # Probar coerción de enteros
    print("Probando coerción de enteros:")
    test_int_values = ["2", "3.5", "0", "invalid", None, 5]
    for val in test_int_values:
        result = _coerce_int(val)
        print(f"  {val!r} -> {result}")

    # Probar coerción de booleanos
    print("\nProbando coerción de booleanos:")
    test_bool_values = [
        "true",
        "false",
        "1",
        "0",
        "yes",
        "no",
        "si",
        "sí",
        "n",
        True,
        False,
        None,
    ]
    for val in test_bool_values:
        result = _coerce_bool(val)
        print(f"  {val!r} -> {result}")

    # Probar coerción de listas de enteros
    print("\nProbando coerción de listas de enteros:")
    test_list_values = [
        "[2,3,4]",
        "[1,2,3,4,5]",
        "2,3,4",
        "1 2 3",
        [1, 2, 3],
        None,
        "invalid",
    ]
    for val in test_list_values:
        result = _coerce_list_int(val)
        print(f"  {val!r} -> {result}")

    # Probar coerción de fechas
    print("\nProbando coerción de fechas:")
    test_date_values = ["2024-01-15", "2024-12-31", "invalid", "2024/01/15", None]
    for val in test_date_values:
        result = _coerce_date_str(val)
        print(f"  {val!r} -> {result}")


def test_api_client_with_coercion():
    """Probar el cliente API con coerción de tipos"""
    print("\nPROBANDO CLIENTE API CON COERCION")
    print("=" * 50)

    try:
        # Inicializar cliente API con credenciales del .env
        from dotenv import load_dotenv

        load_dotenv()

        base_url = os.getenv("TRACKHS_BASE_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            print("  Error: Credenciales de TrackHS no configuradas en .env")
            return

        client = TrackHSAPIClient(base_url, username, password)

        # Probar búsqueda básica de unidades
        print("Probando busqueda basica de unidades...")
        response = client.search_units({"page": 1, "size": 5})
        print(f"  Respuesta exitosa: {response.get('total_items', 0)} unidades")

        # Probar búsqueda con filtros que requieren coerción
        print("\nProbando busqueda con filtros...")

        # Simular parámetros que vienen como strings del MCP
        test_params = {
            "page": "1",
            "size": "5",
            "bedrooms": "2",
            "is_active": "true",
            "pets_friendly": "true",
            "unit_ids": "[2,3,4]",
        }

        print(f"  Parametros de entrada: {test_params}")

        # Aplicar coerción manualmente usando las funciones locales
        def _coerce_int(value):
            if value is None:
                return None
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                return int(value)
            if isinstance(value, str) and value.strip() != "":
                try:
                    return int(value.strip())
                except ValueError:
                    return None
            return None

        def _coerce_bool(value):
            if value is None:
                return None
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return bool(int(value))
            if isinstance(value, str):
                v = value.strip().lower()
                if v in {"true", "1", "yes", "y", "si", "sí"}:
                    return True
                if v in {"false", "0", "no", "n"}:
                    return False
            return None

        def _coerce_list_int(value):
            if value is None:
                return None
            if isinstance(value, list):
                result = []
                for x in value:
                    i = _coerce_int(x)
                    if i is not None:
                        result.append(i)
                return result if result else None
            if isinstance(value, str):
                s = value.strip()
                try:
                    import json

                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return _coerce_list_int(parsed)
                except Exception:
                    import re

                    parts = [p for p in re.split(r"[\s,]+", s.strip("[]")) if p]
                    result = []
                    for p in parts:
                        i = _coerce_int(p)
                        if i is not None:
                            result.append(i)
                    return result if result else None
            return None

        coerced_params = {
            "page": _coerce_int(test_params["page"]) or 1,
            "size": _coerce_int(test_params["size"]) or 5,
            "bedrooms": _coerce_int(test_params["bedrooms"]),
            "is_active": _coerce_bool(test_params["is_active"]),
            "pets_friendly": _coerce_bool(test_params["pets_friendly"]),
            "unit_ids": _coerce_list_int(test_params["unit_ids"]),
        }

        print(f"  Parametros despues de coercion: {coerced_params}")

        # Probar búsqueda con parámetros coerción
        response = client.search_units(coerced_params)
        print(
            f"  Busqueda con coercion exitosa: {response.get('total_items', 0)} unidades"
        )

        # Verificar si se aplicó filtrado del lado cliente
        if response.get("filtersAppliedClientSide"):
            print("  Filtrado del lado cliente aplicado correctamente")

    except Exception as e:
        print(f"  Error en prueba de API: {e}")


def test_search_scenarios():
    """Probar escenarios de búsqueda reales"""
    print("\nPROBANDO ESCENARIOS DE BUSQUEDA")
    print("=" * 50)

    try:
        # Inicializar cliente API con credenciales del .env
        from dotenv import load_dotenv

        load_dotenv()

        base_url = os.getenv("TRACKHS_BASE_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            print("  Error: Credenciales de TrackHS no configuradas en .env")
            return

        client = TrackHSAPIClient(base_url, username, password)

        # Escenario 1: Búsqueda básica
        print("Escenario 1: Busqueda basica")
        response = client.search_units({"page": 1, "size": 3})
        print(f"  Total unidades: {response.get('total_items', 0)}")
        print(f"  Unidades en pagina: {len(response.get('units', []))}")

        # Escenario 2: Búsqueda por texto
        print("\nEscenario 2: Busqueda por texto 'luxury'")
        response = client.search_units({"search": "luxury", "page": 1, "size": 3})
        print(f"  Unidades luxury encontradas: {len(response.get('units', []))}")

        # Escenario 3: Búsqueda con filtros booleanos (simulando coerción)
        print("\nEscenario 3: Busqueda con filtros booleanos")
        response = client.search_units(
            {"is_active": True, "is_bookable": True, "page": 1, "size": 3}
        )
        print(f"  Unidades activas y reservables: {len(response.get('units', []))}")

        # Verificar si las unidades realmente cumplen los filtros
        units = response.get("units", [])
        if units:
            print("  Verificando filtros aplicados:")
            for unit in units[:2]:  # Solo mostrar las primeras 2
                print(
                    f"    ID: {unit.get('id')}, Activa: {unit.get('is_active')}, Reservable: {unit.get('is_bookable')}"
                )

    except Exception as e:
        print(f"  Error en escenarios de busqueda: {e}")


if __name__ == "__main__":
    print("INICIANDO PRUEBAS LOCALES DE COERCION DE TIPOS")
    print("=" * 60)

    # Probar funciones de coerción
    test_coercion_functions()

    # Probar cliente API con coerción
    test_api_client_with_coercion()

    # Probar escenarios de búsqueda
    test_search_scenarios()

    print("\nPRUEBAS COMPLETADAS")
    print("=" * 60)
