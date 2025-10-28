#!/usr/bin/env python3
"""
Test para debuggear el esquema de la herramienta search_units
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from mcp.types import Tool

from trackhs_mcp.server import search_units


def test_schema_debug():
    """Debuggear el esquema de search_units"""

    print("🔍 Debuggeando esquema de search_units...")

    # Obtener la función search_units
    import inspect

    sig = inspect.signature(search_units)

    print(f"\n📋 Parámetros de la función search_units:")
    for param_name, param in sig.parameters.items():
        print(f"   - {param_name}: {param.annotation} = {param.default}")

    # Verificar si hay algún decorador que esté afectando el esquema
    print(f"\n🏷️ Anotaciones de la función:")
    print(f"   - __annotations__: {search_units.__annotations__}")

    # Verificar si hay algún middleware de validación
    print(f"\n🔧 Atributos de la función:")
    for attr in dir(search_units):
        if not attr.startswith("_"):
            print(f"   - {attr}: {getattr(search_units, attr)}")


if __name__ == "__main__":
    test_schema_debug()
