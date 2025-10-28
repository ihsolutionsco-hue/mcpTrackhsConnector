#!/usr/bin/env python3
"""
Debug para acceder a la función subyacente del MCP tool
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_debug_function_subyacente():
    """Debug de la función subyacente del MCP tool"""

    print("🔍 Debugging función subyacente del MCP tool...")

    try:
        # Importar el tool
        from trackhs_mcp.server import search_units

        print(f"📋 Tipo de search_units: {type(search_units)}")

        # Acceder a la función subyacente
        if hasattr(search_units, "fn"):
            print(f"✅ Encontrado .fn: {type(search_units.fn)}")
            print(f"📋 Atributos de .fn: {dir(search_units.fn)}")

            # Obtener la signature de la función subyacente
            import inspect

            sig = inspect.signature(search_units.fn)
            print(f"\n📋 Signature de la función subyacente:")
            for param_name, param in sig.parameters.items():
                print(f"   - {param_name}: {param.annotation}")

            # Verificar los parámetros problemáticos específicamente
            problem_params = ["bedrooms", "is_active", "is_bookable"]
            print(f"\n🎯 Verificando parámetros problemáticos:")
            for param in problem_params:
                if param in sig.parameters:
                    param_obj = sig.parameters[param]
                    print(f"   - {param}: {param_obj.annotation}")

                    # Verificar si tiene Annotated
                    if hasattr(param_obj.annotation, "__origin__"):
                        print(f"     - Origin: {param_obj.annotation.__origin__}")
                        print(f"     - Args: {param_obj.annotation.__args__}")
                    else:
                        print(f"     - Type: {type(param_obj.annotation)}")
                else:
                    print(f"   - {param}: NO ENCONTRADO")

        # Verificar el esquema JSON del tool
        print(f"\n📋 Esquema JSON del tool:")
        if hasattr(search_units, "schema"):
            schema = search_units.schema
            print(f"   - Tipo: {type(schema)}")
            if hasattr(schema, "properties"):
                problem_params = ["bedrooms", "is_active", "is_bookable"]
                for param in problem_params:
                    if param in schema.properties:
                        prop = schema.properties[param]
                        print(f"   - {param}: {prop}")
                    else:
                        print(f"   - {param}: NO ENCONTRADO")

        # Test con Pydantic para verificar que funciona
        print(f"\n🧪 Test con Pydantic usando la función subyacente:")
        from typing import Optional, Union

        from pydantic import BaseModel

        class TestModel(BaseModel):
            bedrooms: Optional[Union[int, str]] = None
            is_active: Optional[Union[int, str]] = None
            is_bookable: Optional[Union[int, str]] = None

        # Test con parámetros int
        try:
            model = TestModel(bedrooms=4, is_active=1, is_bookable=1)
            print(f"✅ Pydantic funciona con parámetros int: {model}")
        except Exception as e:
            print(f"❌ Pydantic falla con parámetros int: {e}")

        # Test con parámetros str
        try:
            model = TestModel(bedrooms="4", is_active="1", is_bookable="1")
            print(f"✅ Pydantic funciona con parámetros str: {model}")
        except Exception as e:
            print(f"❌ Pydantic falla con parámetros str: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_debug_function_subyacente()
