#!/usr/bin/env python3
"""
Test para verificar que la herramienta MCP search_units funciona después de la corrección
usando el protocolo MCP
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from trackhs_mcp.server import app


async def test_mcp_search_units_fixed():
    """Test para verificar que search_units funciona con parámetros int usando MCP"""

    print("🧪 Probando search_units MCP después de la corrección...")

    try:
        # Crear cliente MCP
        server_params = StdioServerParameters(
            command="python", args=["-m", "trackhs_mcp.server"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar
                await session.initialize()

                # Listar herramientas
                tools = await session.list_tools()
                search_units_tool = next(
                    (tool for tool in tools.tools if tool.name == "search_units"), None
                )

                if not search_units_tool:
                    print("❌ search_units no encontrada en las herramientas")
                    return

                print(
                    f"✅ search_units encontrada: {search_units_tool.description[:100]}..."
                )

                # Test 1: Con parámetros int
                print("\n1. Test con parámetros int (como viene del cliente MCP):")
                try:
                    result = await session.call_tool(
                        "search_units",
                        {"bedrooms": 4, "is_active": 1, "is_bookable": 1, "size": 5},
                    )
                    print(f"✅ search_units funcionó con parámetros int")
                    print(f"   - Content: {len(result.content)} elementos")
                    if result.content:
                        print(
                            f"   - Primer elemento: {result.content[0].text[:100]}..."
                        )
                except Exception as e:
                    print(f"❌ Error con parámetros int: {e}")

                # Test 2: Con parámetros str
                print("\n2. Test con parámetros str:")
                try:
                    result = await session.call_tool(
                        "search_units",
                        {
                            "bedrooms": "4",
                            "is_active": "1",
                            "is_bookable": "1",
                            "size": 5,
                        },
                    )
                    print(f"✅ search_units funcionó con parámetros str")
                    print(f"   - Content: {len(result.content)} elementos")
                    if result.content:
                        print(
                            f"   - Primer elemento: {result.content[0].text[:100]}..."
                        )
                except Exception as e:
                    print(f"❌ Error con parámetros str: {e}")

                # Test 3: Con parámetros mixtos
                print("\n3. Test con parámetros mixtos:")
                try:
                    result = await session.call_tool(
                        "search_units",
                        {"bedrooms": 4, "is_active": "1", "is_bookable": 0, "size": 5},
                    )
                    print(f"✅ search_units funcionó con parámetros mixtos")
                    print(f"   - Content: {len(result.content)} elementos")
                    if result.content:
                        print(
                            f"   - Primer elemento: {result.content[0].text[:100]}..."
                        )
                except Exception as e:
                    print(f"❌ Error con parámetros mixtos: {e}")

    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_mcp_search_units_fixed())
