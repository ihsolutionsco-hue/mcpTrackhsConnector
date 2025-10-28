#!/usr/bin/env python3
"""
Test final para search_units - Usando la función subyacente
"""

import json
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_search_units_underlying_function():
    """Test de la función subyacente de search_units"""
    print("🧪 Test Final: Probando función subyacente de search_units...")

    try:
        # Importar la función subyacente directamente
        from trackhs_mcp.server import search_units

        # Acceder a la función subyacente
        if hasattr(search_units, "func"):
            func = search_units.func
        else:
            print("❌ No se pudo acceder a la función subyacente")
            return False

        print("✅ Función subyacente encontrada")

        # Probar diferentes escenarios
        test_cases = [
            {"name": "Búsqueda básica", "params": {"size": 3}},
            {"name": "Búsqueda con dormitorios", "params": {"bedrooms": 2, "size": 2}},
            {"name": "Búsqueda activas", "params": {"is_active": 1, "size": 2}},
            {
                "name": "Búsqueda con texto",
                "params": {"search": "apartment", "size": 2},
            },
        ]

        success_count = 0

        for test_case in test_cases:
            print(f"\n🔍 Probando: {test_case['name']}")
            print(f"   Parámetros: {test_case['params']}")

            try:
                result = func(**test_case["params"])

                if "error" in result:
                    print(f"   ❌ Error: {result['error']}")
                else:
                    total_items = result.get("total_items", 0)
                    units_count = len(result.get("_embedded", {}).get("units", []))
                    print(
                        f"   ✅ Éxito: {total_items} total, {units_count} en esta página"
                    )

                    # Verificar estructura de respuesta
                    required_keys = [
                        "page",
                        "page_count",
                        "page_size",
                        "total_items",
                        "_embedded",
                        "_links",
                    ]
                    missing_keys = [key for key in required_keys if key not in result]
                    if missing_keys:
                        print(f"   ⚠️ Faltan claves: {missing_keys}")
                    else:
                        print(f"   ✅ Estructura de respuesta correcta")
                        success_count += 1

            except Exception as e:
                print(f"   ❌ Excepción: {e}")
                import traceback

                traceback.print_exc()

        print(f"\n📊 Resultado: {success_count}/{len(test_cases)} casos exitosos")

        if success_count == len(test_cases):
            print("✅ Test Final PASÓ: Todas las pruebas funcionaron")
            return True
        else:
            print("⚠️ Test Final PARCIAL: Algunas pruebas fallaron")
            return False

    except Exception as e:
        print(f"❌ Test Final FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_parameter_validation_final():
    """Test final de validación de parámetros"""
    print("\n🧪 Test Validación Final...")

    try:
        from trackhs_mcp.server import search_units

        # Acceder a la función subyacente
        if hasattr(search_units, "func"):
            func = search_units.func
        else:
            print("❌ No se pudo acceder a la función subyacente")
            return False

        # Test con parámetros correctos (int)
        print("🔍 Probando parámetros int...")
        try:
            result = func(bedrooms=2, bathrooms=1, is_active=1, size=1)
            if "error" not in result:
                print("✅ Parámetros int funcionan correctamente")
                return True
            else:
                print(f"❌ Error con parámetros int: {result['error']}")
                return False
        except Exception as e:
            print(f"❌ Excepción con parámetros int: {e}")
            import traceback

            traceback.print_exc()
            return False

    except Exception as e:
        print(f"❌ Test Validación Final FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_area_field_final():
    """Test final del manejo del campo area"""
    print("\n🧪 Test Area Final...")

    try:
        from trackhs_mcp.server import search_units

        # Acceder a la función subyacente
        if hasattr(search_units, "func"):
            func = search_units.func
        else:
            print("❌ No se pudo acceder a la función subyacente")
            return False

        # Hacer una búsqueda que devuelva unidades
        result = func(size=5)

        if "error" in result:
            print(f"❌ Error en búsqueda: {result['error']}")
            return False

        units = result.get("_embedded", {}).get("units", [])
        if not units:
            print("⚠️ No se encontraron unidades para probar el campo area")
            return True

        print(f"🔍 Analizando {len(units)} unidades...")

        area_issues = 0
        for i, unit in enumerate(units):
            area = unit.get("area")
            if area is not None:
                print(f"   Unidad {i+1}: area = {area} (tipo: {type(area)})")
                if isinstance(area, str):
                    print(f"   ⚠️ Unidad {i+1}: area es string, debería ser number")
                    area_issues += 1
                else:
                    print(f"   ✅ Unidad {i+1}: area es {type(area).__name__}")

        if area_issues == 0:
            print("✅ Test Area Final PASÓ: Todos los campos area están correctos")
            return True
        else:
            print(
                f"⚠️ Test Area Final PARCIAL: {area_issues} unidades con area problemático"
            )
            return False

    except Exception as e:
        print(f"❌ Test Area Final FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los tests finales"""
    print("🚀 Iniciando Tests Finales para search_units")
    print("=" * 60)

    tests = [
        test_search_units_underlying_function,
        test_parameter_validation_final,
        test_area_field_final,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test falló con excepción: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"📊 Resultados Finales: {passed}/{total} tests pasaron")

    if passed == total:
        print(
            "🎉 ¡Todos los tests finales pasaron! El código está listo para el servidor."
        )
        return True
    else:
        print("⚠️ Algunos tests finales fallaron. Revisar antes de subir al servidor.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
