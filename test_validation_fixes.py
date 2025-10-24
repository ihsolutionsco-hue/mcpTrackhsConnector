#!/usr/bin/env python3
"""
Script para probar las correcciones de validación
Prueba los casos que fallaron anteriormente para verificar que ahora funcionan correctamente
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


# Configuración
env_vars = load_env_credentials()
username = env_vars.get("TRACKHS_USERNAME", "demo_user")
password = env_vars.get("TRACKHS_PASSWORD", "demo_password")
base_url = env_vars.get("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")

# Headers de autenticación
auth_string = f"{username}:{password}"
auth_bytes = auth_string.encode("ascii")
auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth_b64}",
}


async def call_api(payload, test_name):
    """Llamar a la API y retornar resultado"""
    endpoint = f"{base_url}/pms/maintenance/work-orders"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                endpoint, json=payload, headers=HEADERS, timeout=30.0
            )

            if response.is_success:
                result = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "work_order_id": result.get("id"),
                    "response": result,
                }
            else:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("detail", error_detail)
                    if "validation_messages" in error_json:
                        error_detail += (
                            f" | Validation: {error_json['validation_messages']}"
                        )
                except:
                    pass

                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": error_detail,
                }

        except Exception as e:
            return {"success": False, "error": f"Exception: {str(e)}"}


async def test_priority_validation():
    """Probar validación de prioridades inválidas"""
    print("🔧 TESTING VALIDACIÓN DE PRIORIDADES")
    print("=" * 50)

    # Test 1: Prioridad inválida (2) - Debería fallar
    print("\n📋 Test 1: Prioridad inválida (2)")
    payload_invalid_priority = {
        "dateReceived": "2025-01-24",
        "priority": 2,  # Prioridad inválida
        "summary": "Test prioridad inválida 2",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_invalid_priority, "Prioridad inválida 2")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False

    # Test 2: Prioridad inválida (4) - Debería fallar
    print("\n📋 Test 2: Prioridad inválida (4)")
    payload_invalid_priority_4 = {
        "dateReceived": "2025-01-24",
        "priority": 4,  # Prioridad inválida
        "summary": "Test prioridad inválida 4",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_invalid_priority_4, "Prioridad inválida 4")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False


async def test_date_validation():
    """Probar validación de fechas inválidas"""
    print("\n" + "=" * 50)
    print("🔧 TESTING VALIDACIÓN DE FECHAS")
    print("=" * 50)

    # Test 1: Fecha inválida (formato DD-MM-YYYY)
    print("\n📋 Test 1: Fecha formato inválido (DD-MM-YYYY)")
    payload_invalid_date = {
        "dateReceived": "24-01-2025",  # Formato inválido
        "priority": 5,
        "summary": "Test fecha inválida DD-MM-YYYY",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_invalid_date, "Fecha DD-MM-YYYY")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False

    # Test 2: Fecha inválida (formato MM/DD/YYYY)
    print("\n📋 Test 2: Fecha formato inválido (MM/DD/YYYY)")
    payload_invalid_date_2 = {
        "dateReceived": "01/24/2025",  # Formato inválido
        "priority": 5,
        "summary": "Test fecha inválida MM/DD/YYYY",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_invalid_date_2, "Fecha MM/DD/YYYY")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False


async def test_unitid_validation():
    """Probar validación de unitId obligatorio"""
    print("\n" + "=" * 50)
    print("🔧 TESTING VALIDACIÓN DE UNIT ID")
    print("=" * 50)

    # Test 1: Sin unitId - Debería fallar
    print("\n📋 Test 1: Sin unitId")
    payload_no_unit = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Test sin unitId",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        # Sin unitId
    }

    result = await call_api(payload_no_unit, "Sin unitId")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False

    # Test 2: unitId inválido (0) - Debería fallar
    print("\n📋 Test 2: unitId inválido (0)")
    payload_invalid_unit = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Test unitId inválido",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 0,  # unitId inválido
    }

    result = await call_api(payload_invalid_unit, "unitId 0")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
        return True
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )
        return False


async def test_valid_cases():
    """Probar casos válidos para asegurar que siguen funcionando"""
    print("\n" + "=" * 50)
    print("🔧 TESTING CASOS VÁLIDOS")
    print("=" * 50)

    # Test 1: Caso válido básico
    print("\n📋 Test 1: Caso válido básico")
    payload_valid = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Test caso válido",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_valid, "Caso válido")
    if result["success"]:
        print(f"✅ ÉXITO - Work Order ID: {result['work_order_id']}")
        return True
    else:
        print(f"❌ ERROR INESPERADO - {result['error']}")
        return False


async def test_edge_cases():
    """Probar casos límite"""
    print("\n" + "=" * 50)
    print("🔧 TESTING CASOS LÍMITE")
    print("=" * 50)

    # Test 1: Prioridad límite (0) - Debería fallar
    print("\n📋 Test 1: Prioridad límite (0)")
    payload_priority_0 = {
        "dateReceived": "2025-01-24",
        "priority": 0,  # Prioridad inválida
        "summary": "Test prioridad 0",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_priority_0, "Prioridad 0")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )

    # Test 2: Prioridad límite (6) - Debería fallar
    print("\n📋 Test 2: Prioridad límite (6)")
    payload_priority_6 = {
        "dateReceived": "2025-01-24",
        "priority": 6,  # Prioridad inválida
        "summary": "Test prioridad 6",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result = await call_api(payload_priority_6, "Prioridad 6")
    if not result["success"]:
        print(f"✅ ERROR ESPERADO - {result['error']}")
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
        )


if __name__ == "__main__":
    print("🧪 TRACKHS API - VALIDATION FIXES TESTING")
    print("=" * 70)
    print(f"🔐 Usando credenciales: {username}")
    print(f"🌐 Base URL: {base_url}")
    print("=" * 70)

    # Ejecutar todas las pruebas
    asyncio.run(test_priority_validation())
    asyncio.run(test_date_validation())
    asyncio.run(test_unitid_validation())
    asyncio.run(test_valid_cases())
    asyncio.run(test_edge_cases())

    print("\n" + "=" * 70)
    print("🏁 TESTING DE VALIDACIONES COMPLETADO")
    print("=" * 70)
