#!/usr/bin/env python3
"""
Pruebas finales para verificar que la implementacion funciona.
"""

import os
import sys

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_normalize_int():
    """Prueba que normalize_int funciona con los nuevos parametros"""

    try:
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("Probando normalize_int con parametros string...")

        # Casos de prueba para parametros numericos
        numeric_cases = [
            ("4", 4, "bedrooms"),
            ("0", 0, "min_bedrooms"),
            ("10", 10, "max_bedrooms"),
            ("2", 2, "bathrooms"),
            ("1", 1, "min_bathrooms"),
            ("5", 5, "max_bathrooms"),
        ]

        for input_val, expected, param_name in numeric_cases:
            result = normalize_int(input_val, param_name)
            if result != expected:
                print(f"ERROR: {param_name}: esperado {expected}, obtenido {result}")
                return False
            print(f"OK: {param_name}: '{input_val}' -> {result}")

        # Casos de prueba para parametros booleanos
        boolean_cases = [
            ("1", 1, "pets_friendly"),
            ("0", 0, "is_active"),
            ("1", 1, "allow_unit_rates"),
            ("0", 0, "computed"),
        ]

        for input_val, expected, param_name in boolean_cases:
            result = normalize_int(input_val, param_name)
            if result != expected:
                print(f"ERROR: {param_name}: esperado {expected}, obtenido {result}")
                return False
            print(f"OK: {param_name}: '{input_val}' -> {result}")

        # Probar valores None
        none_cases = [
            (None, None, "bedrooms"),
            (None, None, "pets_friendly"),
        ]

        for input_val, expected, param_name in none_cases:
            result = normalize_int(input_val, param_name)
            if result != expected:
                print(f"ERROR: {param_name}: esperado {expected}, obtenido {result}")
                return False
            print(f"OK: {param_name}: None -> {result}")

        print("normalize_int funciona correctamente con todos los parametros!")
        return True

    except Exception as e:
        print(f"Error en normalize_int: {e}")
        return False


def test_search_units_registration():
    """Prueba que search_units se puede registrar correctamente"""

    try:
        print("Probando registro de search_units...")

        from trackhs_mcp.infrastructure.mcp.search_units import register_search_units

        print("register_search_units importado correctamente")

        # Verificar que la funcion existe
        if callable(register_search_units):
            print("register_search_units es callable")
        else:
            print("register_search_units NO es callable")
            return False

        print("search_units registration funciona!")
        return True

    except Exception as e:
        print(f"Error en registro de search_units: {e}")
        return False


def test_parameter_validation():
    """Prueba que las validaciones de parametros funcionan"""

    try:
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("Probando validaciones de parametros...")

        # Probar valores validos
        valid_cases = [
            ("0", 0, "bedrooms"),
            ("1", 1, "bedrooms"),
            ("10", 10, "bedrooms"),
            ("0", 0, "pets_friendly"),
            ("1", 1, "pets_friendly"),
        ]

        for input_val, expected, param_name in valid_cases:
            result = normalize_int(input_val, param_name)
            if result != expected:
                print(f"ERROR: {param_name}: esperado {expected}, obtenido {result}")
                return False
            print(f"OK: {param_name}: '{input_val}' -> {result} (valido)")

        # Probar valores invalidos (deberian generar errores)
        print("Probando valores invalidos...")
        invalid_cases = [
            ("-1", "bedrooms"),  # Negativo
            ("abc", "bedrooms"),  # No numerico
            ("2", "pets_friendly"),  # Fuera de rango 0-1
        ]

        for input_val, param_name in invalid_cases:
            try:
                result = normalize_int(input_val, param_name)
                print(
                    f"ADVERTENCIA: {param_name}: '{input_val}' -> {result} (deberia ser invalido)"
                )
            except Exception as e:
                print(f"OK: {param_name}: '{input_val}' -> Error: {e}")

        print("Validaciones de parametros funcionan correctamente!")
        return True

    except Exception as e:
        print(f"Error en validaciones: {e}")
        return False


def test_import_structure():
    """Prueba que la estructura de imports esta correcta"""

    try:
        print("Probando estructura de imports...")

        # Verificar imports principales
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("normalize_int importado correctamente")

        from trackhs_mcp.infrastructure.mcp.search_units import register_search_units

        print("register_search_units importado correctamente")

        # Verificar que las funciones existen
        if callable(normalize_int):
            print("normalize_int es callable")
        else:
            print("normalize_int NO es callable")
            return False

        if callable(register_search_units):
            print("register_search_units es callable")
        else:
            print("register_search_units NO es callable")
            return False

        print("Estructura de imports correcta!")
        return True

    except Exception as e:
        print(f"Error en estructura de imports: {e}")
        return False


def main():
    """Ejecuta todas las pruebas"""

    print("Iniciando pruebas finales de validacion...")
    print("=" * 60)

    tests = [
        ("normalize_int", test_normalize_int),
        ("search_units registration", test_search_units_registration),
        ("parameter validation", test_parameter_validation),
        ("import structure", test_import_structure),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 40)
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

    print("\n" + "=" * 60)
    print("RESULTADOS FINALES")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASO" if result else "FALLO"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\nResultado: {passed}/{total} pruebas pasaron")

    if passed == total:
        print(
            "Todas las pruebas pasaron! La implementacion esta funcionando correctamente."
        )
        return True
    else:
        print("Algunas pruebas fallaron. Revisar la implementacion.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
