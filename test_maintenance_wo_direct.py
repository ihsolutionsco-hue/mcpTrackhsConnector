#!/usr/bin/env python3
"""
Script de prueba directo para la API de TrackHS - Create Maintenance Work Order
Prueba la llamada directa a la API sin pasar por el MCP
"""

import asyncio
import json
from datetime import datetime

import httpx

# Configuración de la API
BASE_URL = "https://api-integration-example.tracksandbox.io"
ENDPOINT = "/api/pms/maintenance/work-orders"

# Headers básicos (sin autenticación por ahora para ver el error exacto)
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Payload de prueba basado en la especificación OpenAPI
TEST_PAYLOAD = {
    "dateReceived": "2025-01-24",
    "priority": 5,
    "status": "open",
    "summary": "Test work order - Aire acondicionado no funciona",
    "estimatedCost": 150.0,
    "estimatedTime": 120,
}


async def test_direct_api_call():
    """Probar llamada directa a la API"""
    print("🧪 INICIANDO PRUEBA DIRECTA A LA API")
    print("=" * 50)

    print(f"📡 URL: {BASE_URL}{ENDPOINT}")
    print(f"📦 Payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
    print()

    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST...")
            response = await client.post(
                f"{BASE_URL}{ENDPOINT}",
                json=TEST_PAYLOAD,
                headers=HEADERS,
                timeout=30.0,
            )

            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(response.headers)}")
            print()

            if response.is_success:
                print("✅ ÉXITO - Work Order creado")
                print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
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

        except httpx.RequestError as e:
            print(f"🌐 Error de red: {e}")
        except Exception as e:
            print(f"💥 Error inesperado: {e}")


async def test_with_different_payloads():
    """Probar con diferentes variaciones del payload"""
    print("\n" + "=" * 50)
    print("🔄 PROBANDO DIFERENTES VARIACIONES")
    print("=" * 50)

    # Variación 1: Sin campos opcionales
    payload1 = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "status": "open",
        "summary": "Test minimal payload",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
    }

    # Variación 2: Con campos opcionales
    payload2 = {
        "dateReceived": "2025-01-24",
        "priority": 3,
        "status": "not-started",
        "summary": "Test with optional fields",
        "estimatedCost": 200.0,
        "estimatedTime": 90,
        "description": "Test description",
        "source": "Test Source",
        "sourceName": "Test User",
        "sourcePhone": "+1234567890",
    }

    # Variación 3: Con fecha programada
    payload3 = {
        "dateReceived": "2025-01-24",
        "priority": 1,
        "status": "open",
        "summary": "Test with scheduled date",
        "estimatedCost": 50.0,
        "estimatedTime": 30,
        "dateScheduled": "2025-01-25",
    }

    payloads = [
        ("Minimal", payload1),
        ("With Optional Fields", payload2),
        ("With Scheduled Date", payload3),
    ]

    async with httpx.AsyncClient() as client:
        for name, payload in payloads:
            print(f"\n🧪 Probando: {name}")
            print(f"📦 Payload: {json.dumps(payload, indent=2)}")

            try:
                response = await client.post(
                    f"{BASE_URL}{ENDPOINT}", json=payload, headers=HEADERS, timeout=30.0
                )

                print(f"📊 Status: {response.status_code}")

                if response.is_success:
                    print("✅ ÉXITO")
                    result = response.json()
                    print(f"📄 Work Order ID: {result.get('id', 'N/A')}")
                else:
                    print("❌ ERROR")
                    print(f"📄 Response: {response.text}")

            except Exception as e:
                print(f"💥 Error: {e}")


if __name__ == "__main__":
    print("🔧 TRACKHS API - CREATE MAINTENANCE WORK ORDER TEST")
    print("=" * 60)

    # Ejecutar pruebas
    asyncio.run(test_direct_api_call())
    asyncio.run(test_with_different_payloads())

    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
