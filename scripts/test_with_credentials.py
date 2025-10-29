#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento con credenciales configuradas
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_with_credentials():
    """Prueba el sistema con credenciales de ejemplo"""
    print("PRUEBA CON CREDENCIALES DE EJEMPLO")
    print("=" * 50)

    # Configurar credenciales de ejemplo
    os.environ["TRACKHS_USERNAME"] = "test_user"
    os.environ["TRACKHS_PASSWORD"] = "test_password"
    os.environ["TRACKHS_API_URL"] = "https://ihmvacations.trackhs.com"

    print("Credenciales configuradas:")
    print(f"  USERNAME: {os.getenv('TRACKHS_USERNAME')}")
    print(f"  PASSWORD: {'*' * len(os.getenv('TRACKHS_PASSWORD', ''))}")
    print(f"  API_URL: {os.getenv('TRACKHS_API_URL')}")

    try:
        from mcp_tools import register_tools_with_mcp, setup_tools
        from server_logic import create_api_client, create_mcp_server

        print("\n1. Creando cliente API...")
        api_client = create_api_client()

        if api_client:
            print("   Cliente API creado exitosamente")

            print("\n2. Creando servidor MCP...")
            mcp_server = create_mcp_server()
            print("   Servidor MCP creado exitosamente")

            print("\n3. Configurando herramientas...")
            setup_tools(api_client)
            register_tools_with_mcp(mcp_server)
            print("   Herramientas configuradas exitosamente")

            print("\n4. Verificando herramientas registradas...")
            # Obtener lista de herramientas registradas
            tools = getattr(mcp_server, "_tools", {})
            print(f"   Herramientas registradas: {len(tools)}")
            for tool_name in tools.keys():
                print(f"     - {tool_name}")

            print("\nRESULTADO: Sistema configurado correctamente")
            print("   Los endpoints deberian funcionar una vez que se configuren")
            print("   las credenciales reales de TrackHS.")

        else:
            print("   ERROR: No se pudo crear cliente API")
            return False

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")
        return False

    return True


def test_error_handling():
    """Prueba el manejo de errores sin credenciales"""
    print("\n" + "=" * 50)
    print("PRUEBA DE MANEJO DE ERRORES (SIN CREDENCIALES)")
    print("=" * 50)

    # Limpiar credenciales
    if "TRACKHS_USERNAME" in os.environ:
        del os.environ["TRACKHS_USERNAME"]
    if "TRACKHS_PASSWORD" in os.environ:
        del os.environ["TRACKHS_PASSWORD"]

    try:
        from server_logic import create_api_client

        print("Intentando crear cliente API sin credenciales...")
        api_client = create_api_client()

        if api_client is None:
            print("   CORRECTO: Cliente API es None (como se esperaba)")
        else:
            print("   ERROR: Cliente API deberia ser None")
            return False

    except Exception as e:
        print(f"   ERROR INESPERADO: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    print("INICIANDO PRUEBAS DEL SISTEMA TRACKHS MCP")
    print("=" * 60)

    # Prueba 1: Con credenciales
    success1 = test_with_credentials()

    # Prueba 2: Sin credenciales (manejo de errores)
    success2 = test_error_handling()

    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS:")
    print(f"  Con credenciales: {'PASO' if success1 else 'FALLO'}")
    print(f"  Sin credenciales: {'PASO' if success2 else 'FALLO'}")

    if success1 and success2:
        print("\nTODAS LAS PRUEBAS PASARON")
        print("El sistema esta listo para usar con credenciales reales.")
    else:
        print("\nALGUNAS PRUEBAS FALLARON")
        print("Revisar los errores anteriores.")

    sys.exit(0 if (success1 and success2) else 1)
