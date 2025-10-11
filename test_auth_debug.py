#!/usr/bin/env python3
"""
Test de diagnóstico para verificar la autenticación con TrackHS API
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.config import TrackHSConfig
from trackhs_mcp.core.api_client import TrackHSApiClient

# Cargar variables de entorno
load_dotenv()


async def test_auth_debug():
    """Test de diagnóstico de autenticación"""
    print("🔐 DIAGNÓSTICO: Autenticación TrackHS")
    print("=" * 50)

    # Mostrar configuración actual
    print("\n📋 Configuración actual:")
    print("-" * 30)

    config = TrackHSConfig.from_env()
    print(f"Base URL: {config.base_url}")
    print(f"Username: {config.username}")
    print(f"Password: {config.password[:10]}...")  # Solo mostrar primeros 10 caracteres
    print(f"Timeout: {config.timeout}")

    # Verificar variables de entorno
    print("\n🌍 Variables de entorno:")
    print("-" * 30)
    print(f"TRACKHS_API_URL: {os.getenv('TRACKHS_API_URL', 'NO SET')}")
    print(f"TRACKHS_USERNAME: {os.getenv('TRACKHS_USERNAME', 'NO SET')}")
    print(f"TRACKHS_PASSWORD: {os.getenv('TRACKHS_PASSWORD', 'NO SET')}")

    # Test de autenticación
    print("\n🔐 Test de autenticación:")
    print("-" * 30)

    try:
        client = TrackHSApiClient(config)
        print("✅ Cliente API creado exitosamente")

        # Intentar una petición simple
        print("\n📡 Probando petición simple...")
        response = await client.get("/v2/pms/reservations", params={"size": 1})
        print(f"✅ Respuesta exitosa: {len(response.get('data', []))} reservaciones")

    except Exception as e:
        print(f"❌ Error de autenticación: {e}")

        # Analizar el tipo de error
        if "Invalid credentials" in str(e):
            print("\n🔍 Análisis del error:")
            print("- Las credenciales hardcodeadas pueden estar expiradas")
            print("- Las credenciales pueden ser incorrectas")
            print("- La API puede haber cambiado el formato de autenticación")
        elif "Connection" in str(e):
            print("\n🔍 Análisis del error:")
            print("- Problema de conectividad con la API")
            print("- La URL puede ser incorrecta")
        else:
            print(f"\n🔍 Error inesperado: {type(e).__name__}")


async def test_auth_with_env():
    """Test con variables de entorno personalizadas"""
    print("\n🔐 DIAGNÓSTICO: Con variables de entorno personalizadas")
    print("=" * 60)

    # Crear un archivo .env temporal para testing
    env_content = """# TrackHS API Configuration
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=aba99777416466b6bdc1a25223192ccb
TRACKHS_PASSWORD=18c87461011f355cc11000a24215cbda
TRACKHS_TIMEOUT=30
"""

    # Escribir archivo .env temporal
    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ Archivo .env creado con credenciales hardcodeadas")

    # Recargar variables de entorno
    load_dotenv(override=True)

    # Mostrar configuración
    config = TrackHSConfig.from_env()
    print(f"Base URL: {config.base_url}")
    print(f"Username: {config.username}")
    print(f"Password: {config.password[:10]}...")

    # Test de autenticación
    try:
        client = TrackHSApiClient(config)
        print("✅ Cliente API creado exitosamente")

        # Intentar una petición simple
        response = await client.get("/v2/pms/reservations", params={"size": 1})
        print(f"✅ Respuesta exitosa: {len(response.get('data', []))} reservaciones")

    except Exception as e:
        print(f"❌ Error de autenticación: {e}")

        # Verificar si es un problema de credenciales
        if "401" in str(e) or "Unauthorized" in str(e):
            print("\n🚨 PROBLEMA IDENTIFICADO:")
            print("- Las credenciales hardcodeadas están EXPIRADAS o son INCORRECTAS")
            print("- Necesitas obtener credenciales válidas de TrackHS")
            print("- Contacta al administrador de la cuenta TrackHS")


async def main():
    """Función principal de diagnóstico"""
    print("🚀 INICIANDO DIAGNÓSTICO DE AUTENTICACIÓN")
    print("=" * 60)

    try:
        await test_auth_debug()
        await test_auth_with_env()

        print("\n✅ DIAGNÓSTICO DE AUTENTICACIÓN COMPLETADO")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR EN DIAGNÓSTICO: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
