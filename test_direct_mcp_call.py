#!/usr/bin/env python3
"""
Test directo del servidor MCP para verificar que funciona correctamente
"""

import asyncio
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


async def test_direct_mcp_call():
    """Test directo del servidor MCP"""

    print("🔍 Test directo del servidor MCP...")

    try:
        # Importar el servidor MCP
        from trackhs_mcp.server import mcp

        # Obtener la lista de herramientas
        tools = await mcp.get_tools()
        print(f"📋 Tipo de tools: {type(tools)}")
        print(f"📋 Contenido de tools: {tools}")

        # Buscar search_units
        search_units_tool = None
        if isinstance(tools, dict) and "search_units" in tools:
            search_units_tool = tools["search_units"]
            print(f"✅ Encontrado search_units: {search_units_tool.name}")
        else:
            print(f"❌ No se encontró search_units en tools")
            print(f"📋 Herramientas disponibles: {list(tools.keys())}")
            return

        if not search_units_tool:
            print("❌ No se encontró search_units")
            return

        print(f"✅ Encontrado search_units: {search_units_tool.name}")
        print(f"📋 Descripción: {search_units_tool.description[:100]}...")

        # Verificar el esquema de entrada
        if hasattr(search_units_tool, "inputSchema"):
            input_schema = search_units_tool.inputSchema
            print(
                f"📋 inputSchema keys: {list(input_schema.keys()) if isinstance(input_schema, dict) else 'No es dict'}"
            )

            # Verificar los parámetros problemáticos
            if isinstance(input_schema, dict) and "properties" in input_schema:
                problem_params = ["bedrooms", "is_active", "is_bookable"]
                print(f"\n🎯 Parámetros problemáticos en inputSchema:")
                for param in problem_params:
                    if param in input_schema["properties"]:
                        prop = input_schema["properties"][param]
                        print(f"   - {param}: {prop}")
                    else:
                        print(f"   - {param}: NO ENCONTRADO")

        # Investigar métodos disponibles en mcp
        print(f"\n🔍 Métodos disponibles en mcp:")
        methods = [attr for attr in dir(mcp) if not attr.startswith("_")]
        print(f"📋 Métodos: {methods}")

        # Intentar usar get_tool para obtener la herramienta y llamarla directamente
        print(f"\n🧪 Test con get_tool y parámetros int...")
        try:
            tool = await mcp.get_tool("search_units")
            print(f"📋 Tool obtenido: {type(tool)}")
            print(
                f"📋 Atributos del tool: {[attr for attr in dir(tool) if not attr.startswith('_')]}"
            )

            # Llamar la herramienta directamente con argumentos como diccionario
            result = await tool.run(
                {"bedrooms": 4, "is_active": 1, "is_bookable": 1, "size": 5, "page": 1}
            )
            print(f"✅ Éxito con parámetros int: {type(result)}")
            if hasattr(result, "content"):
                print(f"📋 Contenido: {result.content[:200]}...")
            else:
                print(f"📋 Resultado: {result}")
        except Exception as e:
            print(f"❌ Error con parámetros int: {e}")

        # Intentar con parámetros str
        print(f"\n🧪 Test con get_tool y parámetros str...")
        try:
            tool = await mcp.get_tool("search_units")
            print(f"📋 Tool obtenido: {type(tool)}")

            # Llamar la herramienta directamente con argumentos como diccionario
            result = await tool.run(
                {
                    "bedrooms": "4",
                    "is_active": "1",
                    "is_bookable": "1",
                    "size": 5,
                    "page": 1,
                }
            )
            print(f"✅ Éxito con parámetros str: {type(result)}")
            if hasattr(result, "content"):
                print(f"📋 Contenido: {result.content[:200]}...")
            else:
                print(f"📋 Resultado: {result}")
        except Exception as e:
            print(f"❌ Error con parámetros str: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_direct_mcp_call())
