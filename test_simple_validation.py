#!/usr/bin/env python3
"""
Pruebas simples para verificar que los cambios funcionan correctamente.
"""

import os
import sys

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_normalize_int_function():
    """Prueba que normalize_int funciona correctamente"""

    try:
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("Probando funcion normalize_int...")

        # Casos de prueba
        test_cases = [
            ("4", 4, "bedrooms"),
            ("0", 0, "min_bedrooms"),
            ("1", 1, "pets_friendly"),
            ("0", 0, "is_active"),
            (None, None, "bedrooms"),
        ]

        for input_val, expected, param_name in test_cases:
            result = normalize_int(input_val, param_name)
            if result != expected:
                print(f"ERROR: {param_name}: esperado {expected}, obtenido {result}")
                return False
            print(f"OK: {param_name}: '{input_val}' -> {result}")

        print("normalize_int funciona correctamente!")
        return True

    except Exception as e:
        print(f"Error en normalize_int: {e}")
        return False


def test_search_units_import():
    """Prueba que search_units se puede importar"""

    try:
        print("Probando import de search_units...")

        # Intentar importar el modulo
        from trackhs_mcp.infrastructure.mcp import search_units

        print("Modulo search_units importado correctamente")

        # Verificar que tiene la funcion
        if hasattr(search_units, "search_units"):
            print("Funcion search_units encontrada")
        else:
            print("Funcion search_units NO encontrada")
            return False

        print("search_units import funciona!")
        return True

    except Exception as e:
        print(f"Error en import de search_units: {e}")
        return False


def test_parameter_types():
    """Prueba que los parametros tienen los tipos correctos"""

    try:
        print("Probando tipos de parametros...")

        import inspect

        from trackhs_mcp.infrastructure.mcp.search_units import search_units

        sig = inspect.signature(search_units)

        # Verificar parametros clave
        key_params = ["bedrooms", "pets_friendly", "is_active"]

        for param_name in key_params:
            if param_name in sig.parameters:
                param = sig.parameters[param_name]
                print(f"Parametro {param_name}: {param.annotation}")
            else:
                print(f"Parametro {param_name} NO encontrado")
                return False

        print("Tipos de parametros correctos!")
        return True

    except Exception as e:
        print(f"Error en tipos de parametros: {e}")
        return False


def main():
    """Ejecuta las pruebas"""

    print("Iniciando pruebas simples...")
    print("=" * 50)

    tests = [
        ("normalize_int", test_normalize_int_function),
        ("search_units import", test_search_units_import),
        ("parameter types", test_parameter_types),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"{test_name}: PASO")
            else:
                print(f"{test_name}: FALLO")
        except Exception as e:
            print(f"{test_name}: ERROR - {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("RESULTADOS")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASO" if result else "FALLO"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\nResultado: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("Todas las pruebas pasaron!")
        return True
    else:
        print("Algunas pruebas fallaron.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
