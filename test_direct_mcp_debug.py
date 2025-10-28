#!/usr/bin/env python3
"""
Test directo para debuggear el problema de validación de parámetros en MCP
"""

import asyncio
import json
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_direct():
    """Test directo de la función search_units"""

    # Configuración del servidor MCP
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.trackhs_mcp"],
        env={
            "TRACKHS_USERNAME": "aba99777416466b6bdc1a25223192ccb",
            "TRACKHS_PASSWORD": "your_password_here",
        },
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la sesión
            await session.initialize()

            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("🔧 Herramientas disponibles:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Test 1: Llamada básica sin parámetros
            print("\n🧪 Test 1: Llamada básica sin parámetros")
            try:
                result = await session.call_tool("search_units", arguments={})
                print(f"✅ Éxito: {len(result.content)} resultados")
                if result.content:
                    print(f"   Primer resultado: {result.content[0].text[:200]}...")
            except Exception as e:
                print(f"❌ Error: {e}")

            # Test 2: Con parámetros como enteros
            print("\n🧪 Test 2: Con parámetros como enteros")
            try:
                result = await session.call_tool(
                    "search_units",
                    arguments={
                        "page": 0,
                        "size": 3,
                        "bedrooms": 2,
                        "bathrooms": 1,
                        "is_active": 1,
                        "is_bookable": 1,
                    },
                )
                print(f"✅ Éxito: {len(result.content)} resultados")
            except Exception as e:
                print(f"❌ Error: {e}")

            # Test 3: Con parámetros como strings
            print("\n🧪 Test 3: Con parámetros como strings")
            try:
                result = await session.call_tool(
                    "search_units",
                    arguments={
                        "page": "0",
                        "size": "3",
                        "bedrooms": "2",
                        "bathrooms": "1",
                        "is_active": "1",
                        "is_bookable": "1",
                    },
                )
                print(f"✅ Éxito: {len(result.content)} resultados")
            except Exception as e:
                print(f"❌ Error: {e}")

            # Test 4: Con búsqueda de texto
            print("\n🧪 Test 4: Con búsqueda de texto")
            try:
                result = await session.call_tool(
                    "search_units", arguments={"search": "pool", "size": 2}
                )
                print(f"✅ Éxito: {len(result.content)} resultados")
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_direct())
