"""
Ejemplos de Conexión de Cliente al Servidor TrackHS MCP

Demuestra cómo conectarse al servidor usando diferentes transportes
compatibles con FastMCP Cloud y ElevenLabs.

Este archivo contiene ejemplos prácticos para:
- Conexión HTTP desde clientes Python
- Configuración para Claude Desktop
- Configuración para ElevenLabs
- Manejo de autenticación y errores
"""

import asyncio
import json
import os
from typing import Any, Dict, Optional


# Ejemplo 1: Conexión HTTP básica con FastMCP Client
async def example_http_connection():
    """
    Ejemplo básico de conexión HTTP al servidor TrackHS MCP
    usando StreamableHttpTransport.
    """
    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport

        # URL del servidor (proporcionada por FastMCP Cloud)
        server_url = "https://tu-servidor.fastmcp.cloud/mcp"

        # Crear transporte HTTP
        transport = StreamableHttpTransport(url=server_url)

        # Crear cliente
        client = Client(transport)

        # Conectar y usar herramientas
        async with client:
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"Herramientas disponibles: {len(tools.tools)}")

            # Ejemplo: Buscar reservaciones
            result = await client.call_tool(
                "search_reservations_v2",
                {
                    "arrival_start": "2024-01-01",
                    "arrival_end": "2024-01-31",
                    "status": "Confirmed",
                    "size": 10,
                },
            )

            print(f"Resultado: {result.content}")

    except Exception as e:
        print(f"Error en conexión HTTP: {e}")


# Ejemplo 2: Conexión con autenticación
async def example_authenticated_connection():
    """
    Ejemplo de conexión HTTP con headers de autenticación.
    """
    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport

        server_url = "https://tu-servidor.fastmcp.cloud/mcp"

        # Headers de autenticación (opcional)
        headers = {
            "Authorization": "Bearer tu-token-aqui",
            "X-API-Key": "tu-api-key-aqui",
        }

        transport = StreamableHttpTransport(url=server_url, headers=headers)

        client = Client(transport)

        async with client:
            # Probar conexión
            await client.ping()
            print("Conexión autenticada exitosa")

    except Exception as e:
        print(f"Error en conexión autenticada: {e}")


# Ejemplo 3: Configuración para Claude Desktop
def claude_desktop_config():
    """
    Configuración JSON para Claude Desktop usando HTTP transport.
    """
    config = {
        "mcpServers": {
            "trackhs": {
                "command": "python",
                "args": ["-m", "src.trackhs_mcp"],
                "cwd": "/path/to/MCPtrackhsConnector",
                "env": {
                    "TRACKHS_API_URL": "https://ihmvacations.trackhs.com",
                    "TRACKHS_USERNAME": "tu_usuario",
                    "TRACKHS_PASSWORD": "tu_contraseña",
                },
            }
        }
    }

    # Para usar con HTTP transport (recomendado para ElevenLabs):
    http_config = {
        "mcpServers": {
            "trackhs": {
                "url": "https://tu-servidor.fastmcp.cloud/mcp",
                "transport": "http",
                "headers": {"Authorization": "Bearer tu-token-opcional"},
            }
        }
    }

    return config, http_config


# Ejemplo 4: Configuración para ElevenLabs
def elevenlabs_config():
    """
    Configuración para conectar el servidor TrackHS MCP a ElevenLabs.
    """
    config = {
        "name": "TrackHS MCP Server",
        "description": "Conector MCP para TrackHS API - Gestión de reservas y unidades",
        "server_url": "https://tu-servidor.fastmcp.cloud/mcp",
        "transport": "http",  # ElevenLabs soporta HTTP streamable transport
        "secret_token": None,  # Opcional: token de autenticación
        "http_headers": {
            # Headers adicionales opcionales
            "X-Custom-Header": "valor"
        },
        "approval_mode": "Always Ask",  # Recomendado para seguridad
        "tools_available": [
            "search_reservations_v2",
            "get_reservation_v2",
            "get_folio",
            "search_units",
            "search_amenities",
            "create_maintenance_work_order",
            "create_housekeeping_work_order",
        ],
    }

    return config


# Ejemplo 5: Testing de conectividad
async def test_server_connectivity(server_url: str):
    """
    Función para probar la conectividad del servidor MCP.
    """
    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport

        transport = StreamableHttpTransport(url=server_url)
        client = Client(transport)

        async with client:
            # Test básico de conectividad
            await client.ping()
            print("✅ Servidor responde correctamente")

            # Listar herramientas
            tools = await client.list_tools()
            print(f"✅ {len(tools.tools)} herramientas disponibles")

            # Listar recursos
            resources = await client.list_resources()
            print(f"✅ {len(resources.resources)} recursos disponibles")

            # Listar prompts
            prompts = await client.list_prompts()
            print(f"✅ {len(prompts.prompts)} prompts disponibles")

            return True

    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False


# Ejemplo 6: Uso completo con manejo de errores
async def complete_usage_example():
    """
    Ejemplo completo de uso del cliente con manejo de errores.
    """
    server_url = "https://tu-servidor.fastmcp.cloud/mcp"

    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport

        # Configurar transporte
        transport = StreamableHttpTransport(url=server_url)
        client = Client(transport)

        async with client:
            print("🔗 Conectando al servidor TrackHS MCP...")

            # 1. Verificar conectividad
            await client.ping()
            print("✅ Conexión establecida")

            # 2. Buscar reservaciones
            print("🔍 Buscando reservaciones...")
            reservations = await client.call_tool(
                "search_reservations_v2",
                {
                    "arrival_start": "2024-01-01",
                    "arrival_end": "2024-01-31",
                    "status": "Confirmed",
                    "size": 5,
                },
            )
            print(f"✅ Encontradas reservaciones: {reservations.content}")

            # 3. Buscar unidades
            print("🏠 Buscando unidades...")
            units = await client.call_tool(
                "search_units",
                {"bedrooms": 2, "bathrooms": 1, "is_active": 1, "size": 5},
            )
            print(f"✅ Encontradas unidades: {units.content}")

            # 4. Buscar amenidades
            print("🏊 Buscando amenidades...")
            amenities = await client.call_tool("search_amenities", {"size": 10})
            print(f"✅ Encontradas amenidades: {amenities.content}")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        print("💡 Verifica que:")
        print("   - El servidor esté desplegado en FastMCP Cloud")
        print("   - La URL sea correcta")
        print("   - Las credenciales de TrackHS estén configuradas")


# Ejemplo 7: Configuración de variables de entorno
def setup_environment():
    """
    Configuración de variables de entorno para desarrollo local.
    """
    env_vars = {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario_trackhs",
        "TRACKHS_PASSWORD": "tu_contraseña_trackhs",
        "TRACKHS_TIMEOUT": "30",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO",
    }

    print("Variables de entorno requeridas:")
    for key, value in env_vars.items():
        print(f"  {key}={value}")

    print("\nPara FastMCP Cloud, configura estas variables en el dashboard.")


# Función principal para ejecutar ejemplos
async def main():
    """
    Función principal que ejecuta todos los ejemplos.
    """
    print("🚀 Ejemplos de Conexión TrackHS MCP")
    print("=" * 50)

    # Configurar entorno
    setup_environment()

    # URL del servidor (reemplaza con tu URL real)
    server_url = "https://tu-servidor.fastmcp.cloud/mcp"

    # Test de conectividad
    print(f"\n🔍 Probando conectividad a: {server_url}")
    if await test_server_connectivity(server_url):
        print("✅ Servidor accesible")

        # Ejecutar ejemplo completo
        print("\n📋 Ejecutando ejemplo completo...")
        await complete_usage_example()
    else:
        print("❌ Servidor no accesible")
        print("💡 Asegúrate de que el servidor esté desplegado en FastMCP Cloud")


if __name__ == "__main__":
    # Ejecutar ejemplos
    asyncio.run(main())
