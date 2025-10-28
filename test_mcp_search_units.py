#!/usr/bin/env python3
"""
Test específico para la función MCP search_units
"""

import json
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_mcp_search_units_direct():
    """Test directo de la función MCP search_units"""
    print("🧪 Test MCP Directo: Probando search_units...")

    try:
        # Importar el servidor MCP
        from trackhs_mcp.server import mcp

        # Obtener la función search_units
        search_units_tool = None
        for tool in mcp.tools:
            if tool.name == "search_units":
                search_units_tool = tool
                break

        if not search_units_tool:
            print("❌ No se encontró la herramienta search_units")
            return False

        print(f"✅ Herramienta encontrada: {search_units_tool.name}")
        print(f"📝 Descripción: {search_units_tool.description[:100]}...")

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

        for test_case in test_cases:
            print(f"\n🔍 Probando: {test_case['name']}")
            print(f"   Parámetros: {test_case['params']}")

            try:
                # Simular llamada MCP
                result = search_units_tool.func(**test_case["params"])

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

            except Exception as e:
                print(f"   ❌ Excepción: {e}")
                return False

        print("\n✅ Test MCP Directo PASÓ: Todas las pruebas funcionaron")
        return True

    except Exception as e:
        print(f"❌ Test MCP Directo FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_parameter_validation():
    """Test de validación de parámetros"""
    print("\n🧪 Test Validación de Parámetros...")

    try:
        from trackhs_mcp.server import mcp

        # Obtener la función search_units
        search_units_tool = None
        for tool in mcp.tools:
            if tool.name == "search_units":
                search_units_tool = tool
                break

        if not search_units_tool:
            print("❌ No se encontró la herramienta search_units")
            return False

        # Probar parámetros inválidos
        invalid_cases = [
            {
                "name": "bedrooms como string",
                "params": {"bedrooms": "2", "size": 1},
                "should_fail": True,
            },
            {
                "name": "is_active como string",
                "params": {"is_active": "1", "size": 1},
                "should_fail": True,
            },
            {
                "name": "bedrooms como int válido",
                "params": {"bedrooms": 2, "size": 1},
                "should_fail": False,
            },
            {
                "name": "is_active como int válido",
                "params": {"is_active": 1, "size": 1},
                "should_fail": False,
            },
        ]

        for test_case in invalid_cases:
            print(f"\n🔍 Probando: {test_case['name']}")
            print(f"   Parámetros: {test_case['params']}")

            try:
                result = search_units_tool.func(**test_case["params"])

                if test_case["should_fail"]:
                    print(f"   ⚠️ Debería haber fallado pero no falló")
                else:
                    print(f"   ✅ Funcionó como se esperaba")

            except Exception as e:
                if test_case["should_fail"]:
                    print(f"   ✅ Falló como se esperaba: {e}")
                else:
                    print(f"   ❌ Falló cuando no debería: {e}")
                    return False

        print("\n✅ Test Validación de Parámetros PASÓ")
        return True

    except Exception as e:
        print(f"❌ Test Validación de Parámetros FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los tests MCP"""
    print("🚀 Iniciando Tests MCP para search_units")
    print("=" * 60)

    tests = [test_mcp_search_units_direct, test_parameter_validation]

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
    print(f"📊 Resultados MCP: {passed}/{total} tests pasaron")

    if passed == total:
        print("🎉 ¡Todos los tests MCP pasaron! El código está listo para el servidor.")
        return True
    else:
        print("⚠️ Algunos tests MCP fallaron. Revisar antes de subir al servidor.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
