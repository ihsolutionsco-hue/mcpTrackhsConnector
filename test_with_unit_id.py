#!/usr/bin/env python3
"""
Script de prueba con unitId incluido
"""

import asyncio
import base64
import json
import os

import httpx


# Cargar credenciales del archivo .env
def load_env_credentials():
    """Cargar credenciales del archivo .env"""
    credentials = {}
    try:
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    credentials[key] = value
    except FileNotFoundError:
        print("⚠️ Archivo .env no encontrado")

    return credentials


# Cargar credenciales
env_vars = load_env_credentials()
username = env_vars.get("TRACKHS_USERNAME", "demo_user")
password = env_vars.get("TRACKHS_PASSWORD", "demo_password")
base_url = env_vars.get("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")

print(f"🔐 Usando credenciales: {username}")
print(f"🌐 Base URL: {base_url}")

# Crear headers con autenticación básica
auth_string = f"{username}:{password}"
auth_bytes = auth_string.encode("ascii")
auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth_b64}",
}

# Payload de prueba CON unitId
TEST_PAYLOAD = {
    "dateReceived": "2025-01-24",
    "priority": 5,
    "summary": "Test work order - Aire acondicionado no funciona",
    "estimatedCost": 150.0,
    "estimatedTime": 120,
    "unitId": 1,  # Agregar unitId
}


async def test_with_unit_id():
    """Probar con unitId incluido"""
    print("🧪 PROBANDO CON UNIT ID")
    print("=" * 50)

    endpoint = f"{base_url}/pms/maintenance/work-orders"
    print(f"📡 URL: {endpoint}")
    print(f"📦 Payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
    print()

    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST con unitId...")
            response = await client.post(
                endpoint, json=TEST_PAYLOAD, headers=HEADERS, timeout=30.0
            )

            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(response.headers)}")
            print()

            if response.is_success:
                print("✅ ÉXITO - Work Order creado con unitId")
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ ERROR - Falló la creación")
                print(f"📄 Response Body: {response.text}")

                # Intentar parsear como JSON para ver detalles
                try:
                    error_json = response.json()
                    print(f"📄 Error JSON: {json.dumps(error_json, indent=2)}")

                    # Mostrar mensajes de validación si existen
                    if "validation_messages" in error_json:
                        print(
                            f"🔍 Validation Messages: {error_json['validation_messages']}"
                        )
                    if "detail" in error_json:
                        print(f"🔍 Detail: {error_json['detail']}")

                except Exception as e:
                    print(f"⚠️ No se pudo parsear como JSON: {e}")

                return False

        except httpx.RequestError as e:
            print(f"🌐 Error de red: {e}")
            return False
        except Exception as e:
            print(f"💥 Error inesperado: {e}")
            return False


async def test_with_different_unit_ids():
    """Probar con diferentes unit IDs"""
    print("\n" + "=" * 50)
    print("🔄 PROBANDO DIFERENTES UNIT IDs")
    print("=" * 50)

    unit_ids = [1, 2, 3, 10, 100]

    async with httpx.AsyncClient() as client:
        for unit_id in unit_ids:
            print(f"\n🧪 Probando con unitId: {unit_id}")

            payload = {
                "dateReceived": "2025-01-24",
                "priority": 5,
                "summary": f"Test work order for unit {unit_id}",
                "estimatedCost": 100.0,
                "estimatedTime": 60,
                "unitId": unit_id,
            }

            try:
                response = await client.post(
                    f"{base_url}/pms/maintenance/work-orders",
                    json=payload,
                    headers=HEADERS,
                    timeout=30.0,
                )

                print(f"📊 Status: {response.status_code}")

                if response.is_success:
                    print("✅ ÉXITO - Work Order creado")
                    result = response.json()
                    print(f"📄 Work Order ID: {result.get('id', 'N/A')}")
                    return unit_id
                else:
                    print(f"❌ Error: {response.status_code}")
                    if response.status_code == 422:
                        try:
                            error_json = response.json()
                            if "validation_messages" in error_json:
                                print(
                                    f"🔍 Validation: {error_json['validation_messages']}"
                                )
                        except:
                            pass

            except Exception as e:
                print(f"💥 Error: {e}")

    return None


if __name__ == "__main__":
    print("🔧 TRACKHS API - TEST WITH UNIT ID")
    print("=" * 70)

    # Ejecutar pruebas
    success1 = asyncio.run(test_with_unit_id())

    if not success1:
        print("\n🔄 Probando diferentes unit IDs...")
        working_unit_id = asyncio.run(test_with_different_unit_ids())

        if working_unit_id:
            print(f"\n✅ Unit ID que funciona: {working_unit_id}")
        else:
            print("\n❌ Ningún unit ID funcionó")

    print("\n" + "=" * 70)
    print("🏁 PRUEBAS COMPLETADAS")
