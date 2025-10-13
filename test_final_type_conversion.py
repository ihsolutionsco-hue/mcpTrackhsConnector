#!/usr/bin/env python3
"""
Script de prueba final para verificar conversión de tipos en search_units
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


def test_comprehensive_type_conversion():
    """Probar conversión de tipos con casos reales del MCP"""

    print("🔍 TESTING COMPREHENSIVE TYPE CONVERSION")
    print("=" * 60)

    # Casos de prueba que simulan llamadas reales del MCP
    test_cases = [
        {
            "name": "Filtros Numéricos - Strings",
            "params": {
                "bedrooms": "2",
                "bathrooms": "1",
                "min_bedrooms": "1",
                "max_bedrooms": "3",
                "page": "1",
                "size": "5",
            },
        },
        {
            "name": "Filtros Booleanos - Strings",
            "params": {
                "pets_friendly": "1",
                "is_active": "1",
                "is_bookable": "1",
                "events_allowed": "1",
                "smoking_allowed": "0",
                "children_allowed": "1",
                "is_accessible": "1",
                "page": "1",
                "size": "5",
            },
        },
        {
            "name": "Filtros Mixtos - Strings e Integers",
            "params": {
                "bedrooms": "2",  # String
                "bathrooms": 1,  # Integer
                "pets_friendly": "1",  # String
                "is_active": 1,  # Integer
                "min_bedrooms": "1",  # String
                "max_bedrooms": 3,  # Integer
                "page": 1,
                "size": 5,
            },
        },
        {
            "name": "Filtros de Rango - Strings",
            "params": {
                "min_bedrooms": "1",
                "max_bedrooms": "3",
                "min_bathrooms": "1",
                "max_bathrooms": "2",
                "page": "1",
                "size": "10",
            },
        },
        {
            "name": "Filtros Booleanos Complejos",
            "params": {
                "pets_friendly": "1",
                "allow_unit_rates": "1",
                "computed": "1",
                "inherited": "0",
                "limited": "0",
                "is_bookable": "1",
                "include_descriptions": "1",
                "is_active": "1",
                "events_allowed": "1",
                "smoking_allowed": "0",
                "children_allowed": "1",
                "is_accessible": "1",
                "page": "1",
                "size": "5",
            },
        },
        {
            "name": "Valores Límite - 0 y 1",
            "params": {
                "pets_friendly": "0",
                "is_active": "1",
                "is_bookable": "0",
                "events_allowed": "1",
                "page": "1",
                "size": "5",
            },
        },
    ]

    success_count = 0
    total_count = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        print(f"Input params: {test_case['params']}")

        try:
            # Crear SearchUnitsParams
            search_params = SearchUnitsParams(**test_case["params"])
            print("✅ SUCCESS: SearchUnitsParams created successfully")

            # Verificar tipos convertidos
            print("   Converted types:")
            for key, value in test_case["params"].items():
                if key in ["page", "size"]:
                    continue  # Skip pagination params
                param_value = getattr(search_params, key, None)
                if param_value is not None:
                    print(f"     {key}: {param_value} ({type(param_value).__name__})")

            success_count += 1

        except ValidationError as e:
            print(f"❌ VALIDATION ERROR: {e}")
            print(f"   Error details: {e.errors() if hasattr(e, 'errors') else str(e)}")
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")

    print(
        f"\n📊 RESULTS: {success_count}/{total_count} tests passed ({success_count/total_count*100:.1f}%)"
    )
    return success_count == total_count


def test_edge_cases():
    """Probar casos límite y valores inválidos"""

    print("\n\n🔍 TESTING EDGE CASES")
    print("=" * 60)

    edge_cases = [
        {
            "name": "Valores inválidos para booleanos",
            "params": {"pets_friendly": "2", "page": 1, "size": 5},
            "should_fail": True,
        },
        {
            "name": "Valores negativos para booleanos",
            "params": {"pets_friendly": "-1", "page": 1, "size": 5},
            "should_fail": True,
        },
        {
            "name": "Strings no numéricos para numéricos",
            "params": {"bedrooms": "invalid", "page": 1, "size": 5},
            "should_fail": True,
        },
        {
            "name": "Valores válidos en límite",
            "params": {"pets_friendly": "0", "is_active": "1", "page": 1, "size": 5},
            "should_fail": False,
        },
    ]

    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n--- Edge Case {i}: {test_case['name']} ---")
        print(f"Input params: {test_case['params']}")
        print(f"Expected to fail: {test_case['should_fail']}")

        try:
            search_params = SearchUnitsParams(**test_case["params"])
            if test_case["should_fail"]:
                print("❌ UNEXPECTED SUCCESS: Should have failed but didn't")
            else:
                print("✅ SUCCESS: Validated correctly")
        except ValidationError as e:
            if test_case["should_fail"]:
                print("✅ SUCCESS: Correctly rejected invalid input")
            else:
                print("❌ UNEXPECTED FAILURE: Should have succeeded")
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("🚀 FINAL TYPE CONVERSION TESTING")
    print("=" * 60)

    # Ejecutar tests principales
    main_success = test_comprehensive_type_conversion()

    # Ejecutar tests de casos límite
    test_edge_cases()

    print("\n" + "=" * 60)
    if main_success:
        print("🎉 ALL TESTS PASSED - TYPE CONVERSION IS WORKING!")
    else:
        print("❌ SOME TESTS FAILED - NEEDS FIXING")
    print("🏁 TESTING COMPLETED")
