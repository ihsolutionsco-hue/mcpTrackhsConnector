#!/usr/bin/env python3
"""
Test HTTP directo para debuggear el problema de validación de parámetros en MCP
"""

import asyncio
import json
from typing import Any, Dict

import httpx


async def test_http_mcp():
    """Test directo usando HTTP al servidor MCP"""

    base_url = "http://localhost:8080/mcp"

    async with httpx.AsyncClient() as client:
        # Test 1: Ping al servidor
        print("🧪 Test 1: Ping al servidor")
        try:
            response = await client.post(
                base_url,
                json={"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}},
            )
            print(f"✅ Ping exitoso: {response.status_code}")
            print(f"   Respuesta: {response.json()}")
        except Exception as e:
            print(f"❌ Error en ping: {e}")
            return

        # Test 2: Listar herramientas
        print("\n🧪 Test 2: Listar herramientas")
        try:
            response = await client.post(
                base_url,
                json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            )
            print(f"✅ Lista de herramientas: {response.status_code}")
            tools_data = response.json()
            if "result" in tools_data and "tools" in tools_data["result"]:
                print(
                    f"   Herramientas encontradas: {len(tools_data['result']['tools'])}"
                )
                for tool in tools_data["result"]["tools"]:
                    if tool["name"] == "search_units":
                        print(f"   ✅ search_units encontrada")
                        print(
                            f"      Input schema: {json.dumps(tool.get('inputSchema', {}), indent=2)}"
                        )
            else:
                print(f"   Respuesta: {tools_data}")
        except Exception as e:
            print(f"❌ Error listando herramientas: {e}")

        # Test 3: Llamar search_units sin parámetros
        print("\n🧪 Test 3: search_units sin parámetros")
        try:
            response = await client.post(
                base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "search_units", "arguments": {}},
                },
            )
            print(f"✅ search_units sin parámetros: {response.status_code}")
            result = response.json()
            if "result" in result:
                print(
                    f"   Resultado: {len(result['result'].get('content', []))} elementos"
                )
            else:
                print(f"   Error: {result}")
        except Exception as e:
            print(f"❌ Error en search_units sin parámetros: {e}")

        # Test 4: Llamar search_units con parámetros como enteros
        print("\n🧪 Test 4: search_units con parámetros como enteros")
        try:
            response = await client.post(
                base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "search_units",
                        "arguments": {
                            "page": 0,
                            "size": 3,
                            "bedrooms": 2,
                            "bathrooms": 1,
                            "is_active": 1,
                            "is_bookable": 1,
                        },
                    },
                },
            )
            print(f"✅ search_units con enteros: {response.status_code}")
            result = response.json()
            if "result" in result:
                print(
                    f"   Resultado: {len(result['result'].get('content', []))} elementos"
                )
            else:
                print(f"   Error: {result}")
        except Exception as e:
            print(f"❌ Error en search_units con enteros: {e}")

        # Test 5: Llamar search_units con parámetros como strings
        print("\n🧪 Test 5: search_units con parámetros como strings")
        try:
            response = await client.post(
                base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "search_units",
                        "arguments": {
                            "page": "0",
                            "size": "3",
                            "bedrooms": "2",
                            "bathrooms": "1",
                            "is_active": "1",
                            "is_bookable": "1",
                        },
                    },
                },
            )
            print(f"✅ search_units con strings: {response.status_code}")
            result = response.json()
            if "result" in result:
                print(
                    f"   Resultado: {len(result['result'].get('content', []))} elementos"
                )
            else:
                print(f"   Error: {result}")
        except Exception as e:
            print(f"❌ Error en search_units con strings: {e}")


if __name__ == "__main__":
    asyncio.run(test_http_mcp())
