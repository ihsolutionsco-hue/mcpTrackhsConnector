#!/usr/bin/env python3
"""
Script de prueba para verificar la validación de parámetros en search_units
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_binary_int,
    normalize_int,
)


def test_parameter_normalization():
    """Probar la normalización de parámetros"""

    print("🔧 Probando normalización de parámetros...")

    # Casos de prueba para normalize_binary_int
    binary_test_cases = [
        {"value": 1, "expected": 1, "description": "int 1"},
        {"value": 0, "expected": 0, "description": "int 0"},
        {"value": "1", "expected": 1, "description": "string '1'"},
        {"value": "0", "expected": 0, "description": "string '0'"},
        {"value": None, "expected": None, "description": "None"},
        {"value": True, "expected": 1, "description": "bool True"},
        {"value": False, "expected": 0, "description": "bool False"},
    ]

    print("\n🧪 Probando normalize_binary_int:")
    binary_results = []

    for test_case in binary_test_cases:
        try:
            result = normalize_binary_int(test_case["value"], "test_param")
            if result == test_case["expected"]:
                print(
                    f"   ✅ {test_case['description']}: {test_case['value']} → {result}"
                )
                binary_results.append(True)
            else:
                print(
                    f"   ❌ {test_case['description']}: {test_case['value']} → {result} (esperado: {test_case['expected']})"
                )
                binary_results.append(False)
        except Exception as e:
            print(f"   ❌ {test_case['description']}: Error - {str(e)}")
            binary_results.append(False)

    # Casos de prueba para normalize_int
    int_test_cases = [
        {"value": 42, "expected": 42, "description": "int 42"},
        {"value": "42", "expected": 42, "description": "string '42'"},
        {"value": 42.0, "expected": 42, "description": "float 42.0"},
        {"value": None, "expected": None, "description": "None"},
    ]

    print("\n🧪 Probando normalize_int:")
    int_results = []

    for test_case in int_test_cases:
        try:
            result = normalize_int(test_case["value"], "test_param")
            if result == test_case["expected"]:
                print(
                    f"   ✅ {test_case['description']}: {test_case['value']} → {result}"
                )
                int_results.append(True)
            else:
                print(
                    f"   ❌ {test_case['description']}: {test_case['value']} → {result} (esperado: {test_case['expected']})"
                )
                int_results.append(False)
        except Exception as e:
            print(f"   ❌ {test_case['description']}: Error - {str(e)}")
            int_results.append(False)

    # Resumen de resultados
    print(f"\n📊 Resumen de pruebas:")
    print(
        f"   normalize_binary_int: {sum(binary_results)}/{len(binary_results)} exitosas"
    )
    print(f"   normalize_int: {sum(int_results)}/{len(int_results)} exitosas")

    total_success = sum(binary_results) + sum(int_results)
    total_tests = len(binary_results) + len(int_results)
    success_rate = (total_success / total_tests) * 100

    print(f"   Tasa de éxito general: {success_rate:.1f}%")

    if success_rate >= 90:
        print("🎉 ¡Normalización de parámetros funcionando correctamente!")
        return True
    else:
        print("⚠️ Algunos casos de normalización necesitan ajustes")
        return False


if __name__ == "__main__":
    test_parameter_normalization()
