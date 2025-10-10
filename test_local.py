#!/usr/bin/env python3
"""
Script de testing local para TrackHS MCP Connector
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trackhs_mcp.core.api_client import TrackHSApiClient
from trackhs_mcp.core.types import TrackHSConfig

async def test_connection():
    """Probar conexión con Track HS API"""
    print(" Probando conexión con Track HS API...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar cliente
    config = TrackHSConfig(
        base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
        username=os.getenv("TRACKHS_USERNAME", ""),
        password=os.getenv("TRACKHS_PASSWORD", ""),
        timeout=30
    )
    
    if not config.username or not config.password:
        print(" Error: TRACKHS_USERNAME y TRACKHS_PASSWORD deben estar configurados")
        return False
    
    try:
        # Crear cliente
        client = TrackHSApiClient(config)
        
        # Probar conexión básica
        print(" Probando endpoint de salud...")
        result = await client.get("/health")
        print(f" Conexión exitosa: {result}")
        
        # Probar endpoint de reservas
        print(" Probando endpoint de reservas...")
        result = await client.get("/reservations?page=1&size=1")
        print(f" Reservas accesibles: {len(result.get('_embedded', {}).get('reservations', []))} encontradas")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f" Error de conexión: {str(e)}")
        return False

async def test_tools():
    """Probar herramientas MCP"""
    print("\n Probando herramientas MCP...")
    
    try:
        from trackhs_mcp.tools.all_tools import register_all_tools
        from fastmcp import FastMCP
        
        # Crear servidor MCP
        mcp = FastMCP("Test Server")
        
        # Configurar cliente API
        load_dotenv()
        config = TrackHSConfig(
            base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
            username=os.getenv("TRACKHS_USERNAME", ""),
            password=os.getenv("TRACKHS_PASSWORD", ""),
            timeout=30
        )
        api_client = TrackHSApiClient(config)
        
        # Registrar herramientas
        register_all_tools(mcp, api_client)
        
        print(" Herramientas registradas exitosamente")
        
        await api_client.close()
        return True
        
    except Exception as e:
        print(f" Error en herramientas: {str(e)}")
        return False

async def test_resources():
    """Probar resources MCP"""
    print("\n Probando resources MCP...")
    
    try:
        from trackhs_mcp.resources import register_all_resources
        from fastmcp import FastMCP
        
        # Crear servidor MCP
        mcp = FastMCP("Test Server")
        
        # Configurar cliente API
        load_dotenv()
        config = TrackHSConfig(
            base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
            username=os.getenv("TRACKHS_USERNAME", ""),
            password=os.getenv("TRACKHS_PASSWORD", ""),
            timeout=30
        )
        api_client = TrackHSApiClient(config)
        
        # Registrar resources
        register_all_resources(mcp, api_client)
        
        print(" Resources registrados exitosamente")
        
        await api_client.close()
        return True
        
    except Exception as e:
        print(f" Error en resources: {str(e)}")
        return False

async def test_prompts():
    """Probar prompts MCP"""
    print("\n Probando prompts MCP...")
    
    try:
        from trackhs_mcp.prompts import register_all_prompts
        from fastmcp import FastMCP
        
        # Crear servidor MCP
        mcp = FastMCP("Test Server")
        
        # Configurar cliente API
        load_dotenv()
        config = TrackHSConfig(
            base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
            username=os.getenv("TRACKHS_USERNAME", ""),
            password=os.getenv("TRACKHS_PASSWORD", ""),
            timeout=30
        )
        api_client = TrackHSApiClient(config)
        
        # Registrar prompts
        register_all_prompts(mcp, api_client)
        
        print(" Prompts registrados exitosamente")
        
        await api_client.close()
        return True
        
    except Exception as e:
        print(f" Error en prompts: {str(e)}")
        return False

async def main():
    """Función principal de testing"""
    print(" TrackHS MCP Connector - Testing Local")
    print("=" * 50)
    
    # Verificar variables de entorno
    load_dotenv()
    if not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"):
        print(" Error: Configura las variables de entorno en .env")
        print("   TRACKHS_USERNAME=tu_usuario")
        print("   TRACKHS_PASSWORD=tu_contraseña")
        return
    
    # Ejecutar tests
    tests = [
        ("Conexión API", test_connection),
        ("Herramientas MCP", test_tools),
        ("Resources MCP", test_resources),
        ("Prompts MCP", test_prompts)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f" Error en {name}: {str(e)}")
            results.append((name, False))
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print(" RESUMEN DE TESTS")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = " PASS" if result else " FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\n Resultado: {passed}/{len(results)} tests pasaron")
    
    if passed == len(results):
        print(" ¡Todos los tests pasaron! El servidor está listo.")
        print("\n Para ejecutar el servidor:")
        print("   fastmcp dev")
        print("\n Para probar con MCP Inspector:")
        print("   npx @modelcontextprotocol/inspector")
    else:
        print("  Algunos tests fallaron. Revisa la configuración.")

if __name__ == "__main__":
    asyncio.run(main())
