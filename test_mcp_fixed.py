#!/usr/bin/env python3
"""
Test para verificar que la herramienta MCP search_units funciona después de la corrección
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.server import search_units


def test_mcp_search_units_fixed():
    """Test para verificar que search_units funciona con parámetros int"""

    print("🧪 Probando search_units MCP después de la corrección...")

    print("\n1. Test con parámetros int (como viene del cliente MCP):")
    try:
        result = search_units(bedrooms=4, is_active=1, is_bookable=1, size=5)
        print(f"✅ search_units funcionó con parámetros int")
        print(f"   - Total items: {result.get('total_items', 'N/A')}")
        print(f"   - Page count: {result.get('page_count', 'N/A')}")
        print(f"   - Units found: {len(result.get('_embedded', {}).get('units', []))}")
    except Exception as e:
        print(f"❌ Error con parámetros int: {e}")

    print("\n2. Test con parámetros str:")
    try:
        result = search_units(bedrooms="4", is_active="1", is_bookable="1", size=5)
        print(f"✅ search_units funcionó con parámetros str")
        print(f"   - Total items: {result.get('total_items', 'N/A')}")
        print(f"   - Page count: {result.get('page_count', 'N/A')}")
        print(f"   - Units found: {len(result.get('_embedded', {}).get('units', []))}")
    except Exception as e:
        print(f"❌ Error con parámetros str: {e}")

    print("\n3. Test con parámetros mixtos:")
    try:
        result = search_units(bedrooms=4, is_active="1", is_bookable=0, size=5)
        print(f"✅ search_units funcionó con parámetros mixtos")
        print(f"   - Total items: {result.get('total_items', 'N/A')}")
        print(f"   - Page count: {result.get('page_count', 'N/A')}")
        print(f"   - Units found: {len(result.get('_embedded', {}).get('units', []))}")
    except Exception as e:
        print(f"❌ Error con parámetros mixtos: {e}")


if __name__ == "__main__":
    test_mcp_search_units_fixed()
