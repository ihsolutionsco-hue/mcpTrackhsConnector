#!/usr/bin/env python3
"""
Test para verificar la generación del esquema JSON después de la corrección final
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_schema_generation_final():
    """Verificar la generación del esquema JSON después de la corrección final"""

    print("🔍 Verificando esquema JSON después de la corrección final...")

    try:
        # Importar la función directamente para verificar su signature
        import inspect

        from trackhs_mcp.server import search_units

        # Obtener la signature de la función
        sig = inspect.signature(search_units)

        print(f"📋 Parámetros de search_units después de la corrección final:")
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

        # Test con Pydantic para verificar que funciona
        print(f"\n🧪 Test con Pydantic:")
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
    test_schema_generation_final()
