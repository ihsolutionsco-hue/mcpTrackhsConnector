#!/usr/bin/env python3
"""
Test para verificar el formato de autenticación y credenciales
"""

import asyncio
import base64
import os
import sys

from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.config import TrackHSConfig
from trackhs_mcp.core.api_client import TrackHSApiClient

# Cargar variables de entorno
load_dotenv()


async def test_auth_format():
    """Test del formato de autenticación"""
    print("🔐 VERIFICACIÓN: Formato de Autenticación")
    print("=" * 50)

    config = TrackHSConfig.from_env()

    # Mostrar credenciales (parcialmente)
    print(f"Username: {config.username}")
    print(f"Password: {config.password[:10]}...{config.password[-4:]}")

    # Verificar formato de autenticación
    credentials = f"{config.username}:{config.password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    print("\n🔑 Credenciales codificadas:")
    print(f"Raw: {credentials}")
    print(f"Base64: {encoded_credentials}")
    print(f"Header: Basic {encoded_credentials}")

    # Verificar si las credenciales parecen válidas
    print("\n🔍 Análisis de credenciales:")
    print(f"Username length: {len(config.username)}")
    print(f"Password length: {len(config.password)}")
    username_is_hex = all(c in "0123456789abcdef" for c in config.username.lower())
    password_is_hex = all(c in "0123456789abcdef" for c in config.password.lower())
    print(f"Username format: {'hex' if username_is_hex else 'other'}")
    print(f"Password format: {'hex' if password_is_hex else 'other'}")


async def test_direct_api_call():
    """Test de llamada directa a la API"""
    print("\n🌐 VERIFICACIÓN: Llamada Directa a la API")
    print("=" * 50)

    import httpx

    config = TrackHSConfig.from_env()

    # Crear headers manualmente
    credentials = f"{config.username}:{config.password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"Headers: {headers}")

    try:
        async with httpx.AsyncClient() as client:
            # Intentar llamada directa
            response = await client.get(
                f"{config.base_url}/v2/pms/reservations",
                headers=headers,
                params={"size": 1},
            )

            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")

            if response.status_code == 200:
                print("✅ Autenticación exitosa!")
                data = response.json()
                print(f"Data keys: {list(data.keys())}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error en llamada directa: {e}")


async def test_alternative_credentials():
    """Test con credenciales alternativas"""
    print("\n🔄 VERIFICACIÓN: Credenciales Alternativas")
    print("=" * 50)

    # Probar con credenciales de ejemplo del archivo env.example
    test_credentials = [
        ("your_username_here", "your_password_here"),
        ("test_user", "test_password"),
        ("admin", "admin"),
        ("", ""),  # Credenciales vacías
    ]

    for username, password in test_credentials:
        print(f"\nProbando: {username} / {password[:5]}...")

        try:
            # Crear configuración temporal
            temp_config = TrackHSConfig(
                base_url="https://ihmvacations.trackhs.com/api",
                username=username,
                password=password,
                timeout=30,
            )

            client = TrackHSApiClient(temp_config)
            await client.get("/v2/pms/reservations", params={"size": 1})
            print(f"✅ Éxito con {username}")
            break

        except Exception as e:
            print(f"❌ Falló con {username}: {str(e)[:100]}...")


async def main():
    """Función principal de verificación"""
    print("🚀 INICIANDO VERIFICACIÓN DE AUTENTICACIÓN")
    print("=" * 60)

    try:
        await test_auth_format()
        await test_direct_api_call()
        await test_alternative_credentials()

        print("\n✅ VERIFICACIÓN COMPLETADA")
        print("=" * 60)

        print("\n🎯 CONCLUSIONES:")
        print("- Si todas las pruebas fallan, las credenciales están expiradas")
        print("- Necesitas contactar al administrador de TrackHS")
        print("- O verificar si hay credenciales válidas en otro lugar")

    except Exception as e:
        print(f"\n❌ ERROR EN VERIFICACIÓN: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
