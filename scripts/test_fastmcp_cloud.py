#!/usr/bin/env python3
"""
Script de prueba específico para FastMCP Cloud
Simula el comportamiento del servidor en la nube
"""

import os
import sys
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv

load_dotenv()

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_fastmcp_cloud_compatibility():
    """Prueba la compatibilidad con FastMCP Cloud"""
    print("PRUEBA DE COMPATIBILIDAD CON FASTMCP CLOUD")
    print("=" * 60)

    # Simular el comportamiento de FastMCP Cloud
    print("\n1. Verificando configuración fastmcp.json...")

    # Verificar que el archivo fastmcp.json existe y es válido
    fastmcp_config_path = Path(__file__).parent.parent / "fastmcp.json"
    if not fastmcp_config_path.exists():
        print("   ERROR: fastmcp.json no encontrado")
        return False

    print("   OK: fastmcp.json encontrado")

    # Verificar dependencias
    print("\n2. Verificando dependencias...")
    required_deps = [
        "fastmcp>=2.13.0",
        "httpx>=0.27.0",
        "pydantic>=2.12.3",
        "python-dotenv>=1.0.1",
    ]

    for dep in required_deps:
        try:
            if "fastmcp" in dep:
                import fastmcp

                print(f"   OK: {dep} - version {fastmcp.__version__}")
            elif "httpx" in dep:
                import httpx

                print(f"   OK: {dep} - version {httpx.__version__}")
            elif "pydantic" in dep:
                import pydantic

                print(f"   OK: {dep} - version {pydantic.__version__}")
            elif "python-dotenv" in dep:
                import dotenv

                # python-dotenv no tiene __version__ en versiones antiguas
                try:
                    version = dotenv.__version__
                except AttributeError:
                    version = "installed"
                print(f"   OK: {dep} - version {version}")
        except ImportError as e:
            print(f"   ERROR: {dep} - NO INSTALADO: {e}")
            return False

    # Verificar variables de entorno requeridas
    print("\n3. Verificando variables de entorno requeridas...")
    required_env_vars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"]

    for var in required_env_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var:
                print(f"   OK: {var} - configurado (***)")
            else:
                print(f"   OK: {var} - {value}")
        else:
            print(f"   ERROR: {var} - NO CONFIGURADO")
            return False

    # Probar el entry point
    print("\n4. Probando entry point (src/__main__.py)...")
    try:
        # Simular la importación como lo haría FastMCP Cloud
        from mcp_tools import register_tools_with_mcp, setup_tools
        from server_logic import create_api_client, create_mcp_server

        print("   OK: Importaciones exitosas")

        # Crear cliente API
        api_client = create_api_client()
        if not api_client:
            print("   ERROR: No se pudo crear cliente API")
            return False
        print("   OK: Cliente API creado")

        # Crear servidor MCP
        mcp_server = create_mcp_server()
        if not mcp_server:
            print("   ERROR: No se pudo crear servidor MCP")
            return False
        print("   OK: Servidor MCP creado")

        # Configurar herramientas
        setup_tools(api_client)
        register_tools_with_mcp(mcp_server)
        print("   OK: Herramientas configuradas")

        # Verificar que el objeto server está disponible
        if hasattr(mcp_server, "run"):
            print("   OK: Metodo run() disponible")
        else:
            print("   ERROR: Metodo run() no disponible")
            return False

    except Exception as e:
        print(f"   ERROR: Error en entry point: {str(e)}")
        return False

    # Probar una llamada real a la API
    print("\n5. Probando llamada real a la API...")
    try:
        result = api_client.search_units({"page": 1, "size": 1})
        if result and "total_items" in result:
            print(
                f"   OK: API respondiendo - {result.get('total_items', 0)} unidades totales"
            )
        else:
            print("   ERROR: API no responde correctamente")
            return False
    except Exception as e:
        print(f"   ERROR: Error en llamada API: {str(e)}")
        return False

    print("\n" + "=" * 60)
    print("RESULTADO: COMPATIBLE CON FASTMCP CLOUD")
    print("=" * 60)
    print("El sistema está listo para desplegar en FastMCP Cloud")
    print("\nPara desplegar:")
    print("1. Sube el código a tu repositorio")
    print("2. Conecta el repositorio a FastMCP Cloud")
    print("3. Configura las variables de entorno en FastMCP Cloud:")
    print("   - TRACKHS_API_URL")
    print("   - TRACKHS_USERNAME")
    print("   - TRACKHS_PASSWORD")
    print("4. Despliega el servidor")

    return True


def test_cloud_environment_simulation():
    """Simula el entorno de FastMCP Cloud"""
    print("\n" + "=" * 60)
    print("SIMULACIÓN DE ENTORNO FASTMCP CLOUD")
    print("=" * 60)

    # Simular variables de entorno de la nube
    print("\nSimulando variables de entorno de FastMCP Cloud...")

    # Verificar que las credenciales están disponibles
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    api_url = os.getenv("TRACKHS_API_URL")

    if not all([username, password, api_url]):
        print("ERROR: Variables de entorno no configuradas")
        return False

    print(f"OK: Usuario: {username}")
    print(f"OK: API URL: {api_url}")
    print(f"OK: Password: {'*' * len(password)}")

    # Simular el comportamiento del servidor en la nube
    print("\nSimulando inicializacion del servidor...")
    try:
        from mcp_tools import register_tools_with_mcp, setup_tools
        from server_logic import create_api_client, create_mcp_server

        # Crear servidor como lo haria FastMCP Cloud
        api_client = create_api_client()
        mcp_server = create_mcp_server()

        if api_client:
            setup_tools(api_client)
            register_tools_with_mcp(mcp_server)
            print("OK: Servidor inicializado correctamente")

            # Verificar herramientas registradas
            tools = getattr(mcp_server, "_tools", {})
            print(f"OK: {len(tools)} herramientas registradas")

            return True
        else:
            print("ERROR: No se pudo crear cliente API")
            return False

    except Exception as e:
        print(f"ERROR: Error en simulacion: {str(e)}")
        return False


if __name__ == "__main__":
    print("INICIANDO PRUEBAS DE COMPATIBILIDAD FASTMCP CLOUD")
    print("=" * 60)

    # Prueba 1: Compatibilidad general
    success1 = test_fastmcp_cloud_compatibility()

    # Prueba 2: Simulación de entorno cloud
    success2 = test_cloud_environment_simulation()

    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)

    if success1 and success2:
        print("TODAS LAS PRUEBAS PASARON")
        print("OK: El sistema es COMPATIBLE con FastMCP Cloud")
        print("OK: Listo para desplegar en produccion")
    else:
        print("ALGUNAS PRUEBAS FALLARON")
        print("Revisar errores antes de desplegar")

    sys.exit(0 if (success1 and success2) else 1)
