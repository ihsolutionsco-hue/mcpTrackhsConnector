#!/usr/bin/env python3
"""
Debug para investigar la estructura del MCP tool y acceder a la función subyacente
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_debug_mcp_tool():
    """Debug del MCP tool para encontrar la función subyacente"""

    print("🔍 Debugging MCP tool structure...")

    try:
        # Importar el tool
        from trackhs_mcp.server import search_units

        print(f"📋 Tipo de search_units: {type(search_units)}")
        print(f"📋 Atributos: {dir(search_units)}")

        # Intentar acceder a la función subyacente
        if hasattr(search_units, "func"):
            print(f"✅ Encontrado .func: {type(search_units.func)}")
            print(f"📋 Atributos de .func: {dir(search_units.func)}")

            # Obtener la signature de la función subyacente
            import inspect

            sig = inspect.signature(search_units.func)
            print(f"📋 Signature de la función subyacente:")
            for param_name, param in sig.parameters.items():
                print(f"   - {param_name}: {param.annotation}")

        # Intentar acceder a otros atributos posibles
        for attr in ["_func", "function", "handler", "callable"]:
            if hasattr(search_units, attr):
                print(f"✅ Encontrado .{attr}: {type(getattr(search_units, attr))}")

        # Verificar el esquema JSON
        if hasattr(search_units, "inputSchema"):
            print(f"📋 inputSchema: {search_units.inputSchema}")

            # Buscar específicamente los parámetros problemáticos
            if "properties" in search_units.inputSchema:
                problem_params = ["bedrooms", "is_active", "is_bookable"]
                for param in problem_params:
                    if param in search_units.inputSchema["properties"]:
                        prop = search_units.inputSchema["properties"][param]
                        print(f"🎯 {param}: {prop}")
                    else:
                        print(f"❌ {param}: NO ENCONTRADO")

        # Intentar acceder a la función original desde el módulo
        print(f"\n🔍 Buscando función original en el módulo...")
        import trackhs_mcp.server as server_module

        print(
            f"📋 Atributos del módulo: {[attr for attr in dir(server_module) if not attr.startswith('_')]}"
        )

        # Buscar funciones que contengan 'search_units'
        for attr in dir(server_module):
            if "search_units" in attr.lower():
                print(f"✅ Encontrado: {attr} = {type(getattr(server_module, attr))}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_debug_mcp_tool()
