#!/usr/bin/env python3
"""
Script de debug para probar conversión de tipos en search_units
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.domain.entities.units import SearchUnitsParams
from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


def test_type_conversion():
    """Probar conversión de tipos con diferentes valores"""

    print("=== TESTING TYPE CONVERSION ===")

    # Casos de prueba problemáticos
    test_cases = [
        {
            "name": "String to Integer - bedrooms",
            "params": {"bedrooms": "2", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - bathrooms",
            "params": {"bathrooms": "1", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - min_bedrooms",
            "params": {"min_bedrooms": "1", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - max_bedrooms",
            "params": {"max_bedrooms": "3", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - pets_friendly",
            "params": {"pets_friendly": "1", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - is_active",
            "params": {"is_active": "1", "page": 1, "size": 5},
        },
        {
            "name": "String to Integer - is_bookable",
            "params": {"is_bookable": "1", "page": 1, "size": 5},
        },
        {
            "name": "Mixed types",
            "params": {
                "bedrooms": "2",  # String
                "bathrooms": 1,  # Integer
                "pets_friendly": "1",  # String
                "is_active": 1,  # Integer
                "page": 1,
                "size": 5,
            },
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        print(f"Input params: {test_case['params']}")

        try:
            # Intentar crear SearchUnitsParams directamente
            search_params = SearchUnitsParams(**test_case["params"])
            print("✅ SUCCESS: SearchUnitsParams created successfully")
            print(
                f"   bedrooms: {search_params.bedrooms} (type: {type(search_params.bedrooms)})"
            )
            print(
                f"   bathrooms: {search_params.bathrooms} (type: {type(search_params.bathrooms)})"
            )
            print(
                f"   pets_friendly: {search_params.pets_friendly} (type: {type(search_params.pets_friendly)})"
            )
            print(
                f"   is_active: {search_params.is_active} (type: {type(search_params.is_active)})"
            )

        except ValidationError as e:
            print(f"❌ VALIDATION ERROR: {e}")
            print(f"   Error details: {e.errors() if hasattr(e, 'errors') else str(e)}")
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")


def test_conversion_function():
    """Probar función de conversión manual"""

    print("\n\n=== TESTING MANUAL CONVERSION ===")

    def _convert_param(param, target_type):
        """Convierte parámetro a tipo correcto"""
        if param is None:
            return None
        if isinstance(param, target_type):
            return param
        try:
            if target_type == int:
                return int(param)
            elif target_type == str:
                return str(param)
            else:
                return param
        except (ValueError, TypeError):
            return param

    # Casos de prueba
    test_values = [
        ("2", int),
        ("1", int),
        (2, int),
        (1, int),
        ("1", int),
        (1, int),
        (None, int),
        ("invalid", int),
    ]

    for value, target_type in test_values:
        print(f"\nConverting {value} ({type(value)}) to {target_type.__name__}")
        try:
            result = _convert_param(value, target_type)
            print(f"✅ Result: {result} ({type(result)})")
        except Exception as e:
            print(f"❌ Error: {e}")


def test_pydantic_validation():
    """Probar validación de Pydantic con diferentes tipos"""

    print("\n\n=== TESTING PYDANTIC VALIDATION ===")

    # Probar con diferentes tipos de entrada
    test_cases = [
        {
            "name": "All integers",
            "data": {
                "bedrooms": 2,
                "bathrooms": 1,
                "pets_friendly": 1,
                "page": 1,
                "size": 5,
            },
        },
        {
            "name": "All strings",
            "data": {
                "bedrooms": "2",
                "bathrooms": "1",
                "pets_friendly": "1",
                "page": "1",
                "size": "5",
            },
        },
        {
            "name": "Mixed types",
            "data": {
                "bedrooms": 2,
                "bathrooms": "1",
                "pets_friendly": "1",
                "page": 1,
                "size": "5",
            },
        },
    ]

    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Input: {test_case['data']}")

        try:
            # Crear instancia de SearchUnitsParams
            params = SearchUnitsParams(**test_case["data"])
            print("✅ SUCCESS: Pydantic validation passed")
            print(
                f"   Result: bedrooms={params.bedrooms}, bathrooms={params.bathrooms}, pets_friendly={params.pets_friendly}"
            )

        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("🔍 DEBUGGING TYPE CONVERSION ISSUES")
    print("=" * 50)

    test_type_conversion()
    test_conversion_function()
    test_pydantic_validation()

    print("\n" + "=" * 50)
    print("🏁 DEBUG COMPLETED")
