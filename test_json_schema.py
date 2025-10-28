#!/usr/bin/env python3
"""
Test para investigar el esquema JSON generado para search_units
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.server import app


def test_json_schema():
    """Investigar el esquema JSON de search_units"""

    print("🔍 Investigando esquema JSON de search_units...")

    try:
        # Obtener la aplicación MCP
        print(f"📱 App type: {type(app)}")

        # Listar herramientas
        tools = app.list_tools()
        print(f"🔧 Total herramientas: {len(tools.tools)}")

        # Buscar search_units
        search_units_tool = None
        for tool in tools.tools:
            if tool.name == "search_units":
                search_units_tool = tool
                break

        if search_units_tool:
            print(f"✅ search_units encontrada")
            print(f"   - Nombre: {search_units_tool.name}")
            print(f"   - Descripción: {search_units_tool.description[:100]}...")

            # Verificar el esquema de entrada
            if hasattr(search_units_tool, "inputSchema"):
                schema = search_units_tool.inputSchema
                print(f"   - Schema type: {type(schema)}")

                if hasattr(schema, "properties"):
                    properties = schema.properties
                    print(f"   - Propiedades del schema:")

                    # Verificar los parámetros problemáticos
                    problem_params = ["bedrooms", "is_active", "is_bookable"]
                    for param in problem_params:
                        if param in properties:
                            prop = properties[param]
                            print(f"     - {param}: {prop}")
                        else:
                            print(f"     - {param}: NO ENCONTRADO")
                else:
                    print(f"   - No hay propiedades en el schema")
            else:
                print(f"   - No hay inputSchema")
        else:
            print("❌ search_units no encontrada")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_json_schema()
