#!/usr/bin/env python3
"""
Test para verificar el esquema JSON generado después de los cambios
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_schema_verification():
    """Verificar el esquema JSON generado"""

    print("🔍 Verificando esquema JSON después de los cambios...")

    try:
        # Importar la función directamente para verificar su signature
        import inspect

        from trackhs_mcp.server import search_units

        # Obtener la signature de la función
        sig = inspect.signature(search_units)

        print(f"📋 Parámetros de search_units después de los cambios:")
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

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_schema_verification()
