#!/usr/bin/env python3
"""
Script simple para probar el servidor TrackHS MCP
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Configurar variables de entorno para test
os.environ["TRACKHS_USERNAME"] = "test_user"
os.environ["TRACKHS_PASSWORD"] = "test_password"
os.environ["TRACKHS_BASE_URL"] = "https://api-test.trackhs.com/api"


async def test_server():
    """Test básico del servidor"""
    try:
        from fastmcp.client import Client
        from fastmcp.client.transports import FastMCPTransport

        from trackhs_mcp.server import mcp

        print("🚀 Iniciando test del servidor TrackHS MCP...")

        # Crear cliente
        async with Client(transport=FastMCPTransport(mcp)) as client:
            print("✅ Cliente MCP creado exitosamente")

            # Listar herramientas
            tools = await client.list_tools()
            print(f"✅ Encontradas {len(tools)} herramientas:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n🎉 Test del servidor completado exitosamente!")

    except Exception as e:
        print(f"❌ Error en test del servidor: {str(e)}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)
