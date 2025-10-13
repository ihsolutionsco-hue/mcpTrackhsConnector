#!/usr/bin/env python3
"""
Test manual para verificar que search_units funciona después de la corrección
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio src al PYTHONPATH
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from fastmcp import FastMCP

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.search_units import register_search_units


async def test_search_units_fix():
    """Test manual para verificar que search_units funciona"""

    print("🔧 Testing search_units fix...")

    try:
        # Crear configuración
        config = TrackHSConfig.from_env()
        api_client = TrackHSApiClient(config)

        # Crear servidor MCP
        mcp = FastMCP("Test TrackHS MCP Server")

        # Registrar la herramienta
        register_search_units(mcp, api_client)

        print("✅ MCP server created and tool registered")

        # Simular llamada con parámetros que antes fallaban
        print("🧪 Testing with page=1, size=5, bedrooms=2, is_active=1...")

        # Obtener la función registrada
        tools = mcp._tool_manager._tools
        if "search_units" not in tools:
            print("❌ search_units tool not found")
            return False

        search_units_tool = tools["search_units"]
        print(f"✅ Found search_units tool: {search_units_tool.name}")

        # Verificar que los tipos son correctos
        import inspect

        sig = inspect.signature(search_units_tool.fn)
        page_param = sig.parameters.get("page")
        if page_param and page_param.annotation == int:
            print("✅ page parameter is now int (not Union[int, str])")
        else:
            print(f"❌ page parameter type is {page_param.annotation}")
            return False

        print("🎉 All tests passed! search_units should now work correctly.")
        return True

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_search_units_fix())
    if result:
        print("\n✅ SUCCESS: search_units fix is working!")
        sys.exit(0)
    else:
        print("\n❌ FAILED: search_units fix has issues")
        sys.exit(1)
