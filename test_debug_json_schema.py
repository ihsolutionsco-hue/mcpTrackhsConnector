#!/usr/bin/env python3
"""
Debug para investigar el esquema JSON que se genera para el protocolo MCP
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_debug_json_schema():
    """Debug del esquema JSON del MCP tool"""

    print("🔍 Debugging esquema JSON del MCP tool...")

    try:
        # Importar el tool
        from trackhs_mcp.server import search_units

        print(f"📋 Tipo de search_units: {type(search_units)}")

        # Obtener el esquema JSON
        if hasattr(search_units, "schema"):
            schema = search_units.schema
            print(f"📋 Tipo de schema: {type(schema)}")

            # Convertir a dict si es necesario
            if hasattr(schema, "model_dump"):
                schema_dict = schema.model_dump()
            elif hasattr(schema, "dict"):
                schema_dict = schema.dict()
            else:
                schema_dict = schema

            print(
                f"📋 Schema keys: {list(schema_dict.keys()) if isinstance(schema_dict, dict) else 'No es dict'}"
            )

            # Buscar específicamente los parámetros problemáticos
            if isinstance(schema_dict, dict) and "properties" in schema_dict:
                problem_params = ["bedrooms", "is_active", "is_bookable"]
                print(f"\n🎯 Verificando parámetros problemáticos en el esquema JSON:")
                for param in problem_params:
                    if param in schema_dict["properties"]:
                        prop = schema_dict["properties"][param]
                        print(f"   - {param}: {prop}")

                        # Verificar el tipo específico
                        if "type" in prop:
                            print(f"     - type: {prop['type']}")
                        if "anyOf" in prop:
                            print(f"     - anyOf: {prop['anyOf']}")
                    else:
                        print(f"   - {param}: NO ENCONTRADO")

            # Mostrar el esquema completo para bedrooms
            if (
                isinstance(schema_dict, dict)
                and "properties" in schema_dict
                and "bedrooms" in schema_dict["properties"]
            ):
                print(f"\n📋 Esquema completo para bedrooms:")
                print(json.dumps(schema_dict["properties"]["bedrooms"], indent=2))

        # Intentar acceder al esquema de otra manera
        print(f"\n🔍 Intentando otras formas de acceder al esquema...")

        # Verificar si hay un método to_mcp_tool
        if hasattr(search_units, "to_mcp_tool"):
            print(f"✅ Encontrado to_mcp_tool")
            mcp_tool = search_units.to_mcp_tool()
            print(f"📋 Tipo de mcp_tool: {type(mcp_tool)}")
            print(f"📋 Atributos: {dir(mcp_tool)}")

            # Buscar inputSchema
            if hasattr(mcp_tool, "inputSchema"):
                input_schema = mcp_tool.inputSchema
                print(f"📋 inputSchema: {input_schema}")

                # Buscar los parámetros problemáticos
                if isinstance(input_schema, dict) and "properties" in input_schema:
                    problem_params = ["bedrooms", "is_active", "is_bookable"]
                    print(f"\n🎯 Parámetros problemáticos en inputSchema:")
                    for param in problem_params:
                        if param in input_schema["properties"]:
                            prop = input_schema["properties"][param]
                            print(f"   - {param}: {prop}")
                        else:
                            print(f"   - {param}: NO ENCONTRADO")

        # Verificar si hay un método schema_json
        if hasattr(search_units, "schema_json"):
            print(f"✅ Encontrado schema_json")
            schema_json = search_units.schema_json()
            print(f"📋 Tipo de schema_json: {type(schema_json)}")
            print(f"📋 Contenido: {schema_json[:500]}...")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_debug_json_schema()
