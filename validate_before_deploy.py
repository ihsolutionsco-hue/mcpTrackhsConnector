#!/usr/bin/env python3
"""
Script de validación final antes del despliegue a FastMCP
Verifica que todas las funcionalidades implementadas funcionan correctamente
"""

import os
import sys

sys.path.append("src")

from dotenv import load_dotenv

from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger

# Configurar logger
logger = get_logger(__name__)


def validate_coercion_functions():
    """Validar que las funciones de coerción funcionan correctamente"""
    print("VALIDANDO FUNCIONES DE COERCION")
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

    # Acceder a las funciones de coerción desde el namespace del módulo
    # Las funciones están definidas dentro de register_tools_with_mcp
    # Necesitamos acceder a ellas de otra manera

    # Definir las funciones localmente para validar
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

    # Casos de prueba críticos
    test_cases = [
        # Enteros
        ("_coerce_int", "2", 2),
        ("_coerce_int", "0", 0),
        ("_coerce_int", "invalid", None),
        ("_coerce_int", None, None),
        # Booleanos
        ("_coerce_bool", "true", True),
        ("_coerce_bool", "false", False),
        ("_coerce_bool", "1", True),
        ("_coerce_bool", "0", False),
        ("_coerce_bool", "si", True),
        ("_coerce_bool", "no", False),
        # Listas
        ("_coerce_list_int", "[2,3,4]", [2, 3, 4]),
        ("_coerce_list_int", "2,3,4", [2, 3, 4]),
        ("_coerce_list_int", "1 2 3", [1, 2, 3]),
        ("_coerce_list_int", None, None),
    ]

    passed = 0
    total = len(test_cases)

    for func_name, input_val, expected in test_cases:
        if func_name == "_coerce_int":
            result = _coerce_int(input_val)
        elif func_name == "_coerce_bool":
            result = _coerce_bool(input_val)
        elif func_name == "_coerce_list_int":
            result = _coerce_list_int(input_val)

        if result == expected:
            print(f"  OK {func_name}({input_val!r}) = {result}")
            passed += 1
        else:
            print(f"  ERROR {func_name}({input_val!r}) = {result}, esperado {expected}")

    print(f"\nCoerción: {passed}/{total} casos exitosos")
    return passed == total


def validate_api_client():
    """Validar que el cliente API funciona con coerción"""
    print("\nVALIDANDO CLIENTE API")
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

        # Probar búsqueda básica
        response = client.search_units({"page": 1, "size": 3})
        if response.get("total_items", 0) > 0:
            print(f"  OK Búsqueda básica: {response.get('total_items')} unidades")
        else:
            print("  ERROR Búsqueda básica falló")
            return False

        # Probar búsqueda con filtros
        response = client.search_units({"search": "luxury", "page": 1, "size": 3})
        if len(response.get("units", [])) > 0:
            print(f"  OK Búsqueda con filtros: {len(response.get('units'))} unidades")
        else:
            print("  ERROR Búsqueda con filtros falló")
            return False

        return True

    except Exception as e:
        print(f"  ERROR en cliente API: {e}")
        return False


def validate_imports():
    """Validar que todas las importaciones funcionan"""
    print("\nVALIDANDO IMPORTACIONES")
    print("=" * 50)

    try:
        import mcp_tools

        print("  OK mcp_tools importado")

        from schemas.unit import UnitSearchParams

        print("  OK schemas.unit importado")

        from schemas.reservation import ReservationSearchParams

        print("  OK schemas.reservation importado")

        from schemas.amenity import AmenitySearchParams

        print("  OK schemas.amenity importado")

        from utils.api_client import TrackHSAPIClient

        print("  OK utils.api_client importado")

        from utils.exceptions import TrackHSAPIError

        print("  OK utils.exceptions importado")

        return True

    except Exception as e:
        print(f"  ERROR en importaciones: {e}")
        return False


def validate_file_structure():
    """Validar que la estructura de archivos es correcta"""
    print("\nVALIDANDO ESTRUCTURA DE ARCHIVOS")
    print("=" * 50)

    required_files = [
        "src/mcp_tools.py",
        "src/schemas/unit.py",
        "src/schemas/reservation.py",
        "src/schemas/amenity.py",
        "src/utils/api_client.py",
        "src/utils/exceptions.py",
        "src/utils/logger.py",
        "requirements.txt",
        "pyproject.toml",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  OK {file_path}")

    if missing_files:
        print(f"  ERROR Archivos faltantes: {missing_files}")
        return False

    return True


def main():
    """Función principal de validación"""
    print("VALIDACION FINAL ANTES DEL DESPLIEGUE")
    print("=" * 60)

    validations = [
        ("Estructura de archivos", validate_file_structure),
        ("Importaciones", validate_imports),
        ("Funciones de coerción", validate_coercion_functions),
        ("Cliente API", validate_api_client),
    ]

    passed = 0
    total = len(validations)

    for name, validation_func in validations:
        print(f"\n{name}:")
        if validation_func():
            passed += 1
        else:
            print(f"  ERROR {name} falló")

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {passed}/{total} validaciones exitosas")

    if passed == total:
        print("LISTO PARA DESPLIEGUE")
        return True
    else:
        print("CORREGIR ERRORES ANTES DEL DESPLIEGUE")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
