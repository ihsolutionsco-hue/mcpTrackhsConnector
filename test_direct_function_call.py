#!/usr/bin/env python3
"""
Test para llamar directamente a la función search_units sin pasar por MCP
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_direct_function_call():
    """Llamar directamente a la función search_units"""

    print("🔍 Probando llamada directa a search_units...")

    try:
        # Importar la función directamente
        from trackhs_mcp.server import search_units

        print("✅ Función search_units importada correctamente")

        # Probar con parámetros int
        print("\n1. Test con parámetros int:")
        try:
            result = search_units(bedrooms=4, is_active=1, is_bookable=1, size=5)
            print(f"✅ Llamada directa exitosa con parámetros int")
            print(f"   - Resultado: {type(result)}")
            if isinstance(result, dict):
                print(f"   - Keys: {list(result.keys())}")
        except Exception as e:
            print(f"❌ Error con parámetros int: {e}")

        # Probar con parámetros str
        print("\n2. Test con parámetros str:")
        try:
            result = search_units(bedrooms="4", is_active="1", is_bookable="1", size=5)
            print(f"✅ Llamada directa exitosa con parámetros str")
            print(f"   - Resultado: {type(result)}")
            if isinstance(result, dict):
                print(f"   - Keys: {list(result.keys())}")
        except Exception as e:
            print(f"❌ Error con parámetros str: {e}")

    except Exception as e:
        print(f"❌ Error importando función: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_direct_function_call()
