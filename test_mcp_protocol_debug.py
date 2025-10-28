#!/usr/bin/env python3
"""
Test directo del protocolo MCP para debuggear el problema de validación
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict


async def test_mcp_protocol():
    """Test directo usando el protocolo MCP correcto"""

    # Iniciar el servidor MCP como subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "src.trackhs_mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Test 1: Inicializar la sesión MCP
        print("🧪 Test 1: Inicializar sesión MCP")

        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        # Enviar request
        request_line = json.dumps(init_request) + "\n"
        process.stdin.write(request_line)
        process.stdin.flush()

        # Leer respuesta
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(
                f"✅ Inicialización: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}"
            )
        else:
            print("❌ No se recibió respuesta de inicialización")
            return

        # Test 2: Listar herramientas
        print("\n🧪 Test 2: Listar herramientas")

        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        request_line = json.dumps(list_tools_request) + "\n"
        process.stdin.write(request_line)
        process.stdin.flush()

        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            tools = response.get("result", {}).get("tools", [])
            print(f"✅ Herramientas encontradas: {len(tools)}")

            # Buscar search_units
            search_units_tool = None
            for tool in tools:
                if tool.get("name") == "search_units":
                    search_units_tool = tool
                    break

            if search_units_tool:
                print("✅ search_units encontrada")
                input_schema = search_units_tool.get("inputSchema", {})
                print(f"   Input schema type: {input_schema.get('type', 'unknown')}")

                # Mostrar propiedades de bedrooms
                properties = input_schema.get("properties", {})
                if "bedrooms" in properties:
                    bedrooms_schema = properties["bedrooms"]
                    print(f"   bedrooms schema: {bedrooms_schema}")
                else:
                    print("   ❌ bedrooms no encontrado en schema")
            else:
                print("❌ search_units no encontrada")
        else:
            print("❌ No se recibió respuesta de list_tools")
            return

        # Test 3: Llamar search_units sin parámetros
        print("\n🧪 Test 3: search_units sin parámetros")

        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "search_units", "arguments": {}},
        }

        request_line = json.dumps(call_request) + "\n"
        process.stdin.write(request_line)
        process.stdin.flush()

        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                result = response["result"]
                content = result.get("content", [])
                print(f"✅ search_units sin parámetros: {len(content)} elementos")
                if content:
                    print(f"   Primer elemento: {content[0].get('text', '')[:100]}...")
            else:
                print(f"❌ Error en search_units: {response}")
        else:
            print("❌ No se recibió respuesta de search_units")

        # Test 4: Llamar search_units con parámetros como enteros
        print("\n🧪 Test 4: search_units con enteros")

        call_request = {
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
        }

        request_line = json.dumps(call_request) + "\n"
        process.stdin.write(request_line)
        process.stdin.flush()

        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                result = response["result"]
                content = result.get("content", [])
                print(f"✅ search_units con enteros: {len(content)} elementos")
            else:
                print(f"❌ Error en search_units con enteros: {response}")
        else:
            print("❌ No se recibió respuesta de search_units con enteros")

        # Test 5: Llamar search_units con parámetros como strings
        print("\n🧪 Test 5: search_units con strings")

        call_request = {
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
        }

        request_line = json.dumps(call_request) + "\n"
        process.stdin.write(request_line)
        process.stdin.flush()

        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                result = response["result"]
                content = result.get("content", [])
                print(f"✅ search_units con strings: {len(content)} elementos")
            else:
                print(f"❌ Error en search_units con strings: {response}")
        else:
            print("❌ No se recibió respuesta de search_units con strings")

    finally:
        # Terminar el proceso
        process.terminate()
        process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())
