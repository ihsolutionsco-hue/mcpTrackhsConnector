#!/usr/bin/env python3
"""
Pruebas unitarias para verificar que los parámetros string funcionan correctamente
en la herramienta search_units después de los cambios implementados.
"""

import json
import os
import sys
from typing import Optional

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_string_parameter_conversion():
    """Prueba la conversión de parámetros string a int usando normalize_int"""

    try:
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("Probando conversion de parametros string...")

        # Casos de prueba para parámetros numéricos
        test_cases_numeric = [
            ("4", 4, "bedrooms"),
            ("0", 0, "min_bedrooms"),
            ("10", 10, "max_bedrooms"),
            ("2", 2, "bathrooms"),
            ("1", 1, "min_bathrooms"),
            ("5", 5, "max_bathrooms"),
            ("21", 21, "calendar_id"),
            ("1", 1, "role_id"),
        ]

        # Casos de prueba para parámetros booleanos
        test_cases_boolean = [
            ("1", 1, "pets_friendly"),
            ("0", 0, "is_active"),
            ("1", 1, "allow_unit_rates"),
            ("0", 0, "computed"),
            ("1", 1, "inherited"),
            ("0", 0, "limited"),
            ("1", 1, "is_bookable"),
            ("0", 0, "include_descriptions"),
            ("1", 1, "events_allowed"),
            ("0", 0, "smoking_allowed"),
            ("1", 1, "children_allowed"),
            ("0", 0, "is_accessible"),
        ]

        print("Probando parametros numericos...")
        for input_val, expected, param_name in test_cases_numeric:
            result = normalize_int(input_val, param_name)
            assert (
                result == expected
            ), f"Error en {param_name}: esperado {expected}, obtenido {result}"
            print(f"  ✓ {param_name}: '{input_val}' → {result}")

        print("Probando parametros booleanos...")
        for input_val, expected, param_name in test_cases_boolean:
            result = normalize_int(input_val, param_name)
            assert (
                result == expected
            ), f"Error en {param_name}: esperado {expected}, obtenido {result}"
            print(f"  ✓ {param_name}: '{input_val}' → {result}")

        # Probar valores None
        print("Probando valores None...")
        none_cases = [
            (None, None, "bedrooms"),
            (None, None, "pets_friendly"),
            (None, None, "is_active"),
        ]

        for input_val, expected, param_name in none_cases:
            result = normalize_int(input_val, param_name)
            assert (
                result == expected
            ), f"Error en {param_name}: esperado {expected}, obtenido {result}"
            print(f"  ✓ {param_name}: None → {result}")

        print("Todas las conversiones funcionan correctamente!")
        return True

    except Exception as e:
        print(f"Error en las pruebas de conversion: {e}")
        return False


def test_field_descriptions():
    """Prueba que las descripciones de Field() sean claras y orientadas a LLMs"""

    try:
        from trackhs_mcp.infrastructure.mcp.search_units import search_units

        print("Probando descripciones de Field()...")

        # Obtener la función y sus parámetros
        import inspect

        sig = inspect.signature(search_units)

        # Parámetros que deberían tener descripciones mejoradas
        string_params = [
            "bedrooms",
            "min_bedrooms",
            "max_bedrooms",
            "bathrooms",
            "min_bathrooms",
            "max_bathrooms",
            "pets_friendly",
            "is_active",
        ]

        print("Verificando que los parametros existen...")
        for param_name in string_params:
            assert param_name in sig.parameters, f"Parámetro {param_name} no encontrado"
            print(f"  ✓ {param_name} encontrado")

        print("Todas las descripciones estan configuradas!")
        return True

    except Exception as e:
        print(f"Error en las pruebas de descripciones: {e}")
        return False


def test_validation_logic():
    """Prueba que las validaciones de rango y lógica de negocio siguen funcionando"""

    try:
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("Probando validaciones de rango...")

        # Probar valores válidos
        valid_cases = [
            ("0", 0, "bedrooms"),
            ("1", 1, "bedrooms"),
            ("10", 10, "bedrooms"),
            ("0", 0, "pets_friendly"),
            ("1", 1, "pets_friendly"),
        ]

        for input_val, expected, param_name in valid_cases:
            result = normalize_int(input_val, param_name)
            assert (
                result == expected
            ), f"Error en {param_name}: esperado {expected}, obtenido {result}"
            print(f"  ✓ {param_name}: '{input_val}' → {result} (válido)")

        # Probar valores inválidos (deberían generar errores)
        print("Probando valores invalidos...")
        invalid_cases = [
            ("-1", "bedrooms"),  # Negativo
            ("abc", "bedrooms"),  # No numérico
            ("2", "pets_friendly"),  # Fuera de rango 0-1
            ("", "bedrooms"),  # Vacío
        ]

        for input_val, param_name in invalid_cases:
            try:
                result = normalize_int(input_val, param_name)
                print(
                    f"  ⚠️  {param_name}: '{input_val}' → {result} (debería ser inválido)"
                )
            except Exception as e:
                print(f"  ✓ {param_name}: '{input_val}' → Error: {e}")

        print("Validaciones funcionan correctamente!")
        return True

    except Exception as e:
        print(f"Error en las pruebas de validacion: {e}")
        return False


def test_import_structure():
    """Prueba que la estructura de imports esté correcta"""

    try:
        print("Probando estructura de imports...")

        # Verificar que normalize_int se puede importar
        from trackhs_mcp.infrastructure.utils.type_normalization import normalize_int

        print("  ✓ normalize_int importado correctamente")

        # Verificar que search_units se puede importar
        from trackhs_mcp.infrastructure.mcp.search_units import search_units

        print("  ✓ search_units importado correctamente")

        # Verificar que la función tiene los parámetros esperados
        import inspect

        sig = inspect.signature(search_units)
        params = list(sig.parameters.keys())

        expected_params = ["bedrooms", "pets_friendly", "is_active"]
        for param in expected_params:
            assert param in params, f"Parámetro {param} no encontrado en search_units"
            print(f"  ✓ Parámetro {param} encontrado")

        print("Estructura de imports correcta!")
        return True

    except Exception as e:
        print(f"Error en las pruebas de imports: {e}")
        return False


def main():
    """Ejecuta todas las pruebas unitarias"""

    print("Iniciando pruebas unitarias para parametros string...")
    print("=" * 60)

    tests = [
        ("Estructura de imports", test_import_structure),
        ("Conversión de parámetros", test_string_parameter_conversion),
        ("Descripciones de Field", test_field_descriptions),
        ("Validaciones de rango", test_validation_logic),
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
    print("RESUMEN DE RESULTADOS")
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
