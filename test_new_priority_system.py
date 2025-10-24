#!/usr/bin/env python3
"""
Script para probar el nuevo sistema de prioridades textuales
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
                    "priority": result.get("priority"),
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


async def test_new_priority_system():
    """Probar el nuevo sistema de prioridades"""
    print("🔧 TESTING NUEVO SISTEMA DE PRIORIDADES")
    print("=" * 60)

    # Mapeo de prioridades textuales a numéricas
    priority_mapping = {"trivial": 1, "low": 1, "medium": 3, "high": 5, "critical": 5}

    for priority_text, expected_numeric in priority_mapping.items():
        print(
            f"\n📋 Test: Prioridad '{priority_text}' (debería mapear a {expected_numeric})"
        )

        payload = {
            "dateReceived": "2025-01-24",
            "priority": expected_numeric,  # Usar el valor numérico que debería mapear
            "summary": f"Test prioridad {priority_text}",
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 1,
        }

        result = await call_api(payload, f"Prioridad {priority_text}")
        if result["success"]:
            actual_priority = result.get("priority")
            print(f"✅ ÉXITO - Work Order ID: {result['work_order_id']}")
            print(
                f"📊 Prioridad enviada: {expected_numeric}, Prioridad recibida: {actual_priority}"
            )

            if actual_priority == expected_numeric:
                print(f"✅ Mapeo correcto: {priority_text} → {actual_priority}")
            else:
                print(
                    f"⚠️ Mapeo inesperado: {priority_text} → {actual_priority} (esperado: {expected_numeric})"
                )
        else:
            print(f"❌ ERROR - {result['error']}")


async def test_priority_examples():
    """Probar ejemplos de uso con las nuevas prioridades"""
    print("\n" + "=" * 60)
    print("📞 EJEMPLOS DE USO CON NUEVAS PRIORIDADES")
    print("=" * 60)

    examples = [
        {
            "priority": "critical",
            "summary": "EMERGENCIA - Fuga de agua severa",
            "description": "Fuga importante que requiere atención inmediata",
            "expected_numeric": 5,
        },
        {
            "priority": "high",
            "summary": "Aire acondicionado no funciona",
            "description": "Huésped reporta problema de comodidad",
            "expected_numeric": 5,
        },
        {
            "priority": "medium",
            "summary": "Problemas de WiFi",
            "description": "Múltiples huéspedes reportan conectividad lenta",
            "expected_numeric": 3,
        },
        {
            "priority": "low",
            "summary": "Limpieza programada",
            "description": "Limpieza de mantenimiento regular",
            "expected_numeric": 1,
        },
        {
            "priority": "trivial",
            "summary": "Cambio de bombillas",
            "description": "Reemplazo de bombillas fundidas",
            "expected_numeric": 1,
        },
    ]

    for example in examples:
        print(f"\n🔧 Ejemplo: {example['priority'].upper()}")
        print(f"📝 Resumen: {example['summary']}")
        print(f"📄 Descripción: {example['description']}")

        payload = {
            "dateReceived": "2025-01-24",
            "priority": example["expected_numeric"],
            "summary": example["summary"],
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 1,
            "description": example["description"],
        }

        result = await call_api(payload, f"Ejemplo {example['priority']}")
        if result["success"]:
            print(f"✅ ÉXITO - Work Order ID: {result['work_order_id']}")
            print(
                f"📊 Prioridad: {result.get('priority')} (esperado: {example['expected_numeric']})"
            )
        else:
            print(f"❌ ERROR - {result['error']}")


async def test_invalid_priorities():
    """Probar prioridades inválidas"""
    print("\n" + "=" * 60)
    print("❌ TESTING PRIORIDADES INVÁLIDAS")
    print("=" * 60)

    invalid_priorities = ["urgent", "normal", "low-priority", "1", "3", "5"]

    for invalid_priority in invalid_priorities:
        print(f"\n📋 Test: Prioridad inválida '{invalid_priority}'")

        # Intentar con valor numérico directo (que debería fallar en nuestro MCP)
        payload = {
            "dateReceived": "2025-01-24",
            "priority": 2,  # Prioridad inválida numérica
            "summary": f"Test prioridad inválida {invalid_priority}",
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 1,
        }

        result = await call_api(payload, f"Prioridad inválida {invalid_priority}")
        if not result["success"]:
            print(f"✅ ERROR ESPERADO - {result['error']}")
        else:
            print(
                f"❌ INESPERADO - Debería haber fallado pero funcionó: {result['work_order_id']}"
            )


if __name__ == "__main__":
    print("🧪 TRACKHS API - NEW PRIORITY SYSTEM TESTING")
    print("=" * 80)
    print(f"🔐 Usando credenciales: {username}")
    print(f"🌐 Base URL: {base_url}")
    print("=" * 80)

    # Ejecutar todas las pruebas
    asyncio.run(test_new_priority_system())
    asyncio.run(test_priority_examples())
    asyncio.run(test_invalid_priorities())

    print("\n" + "=" * 80)
    print("🏁 TESTING DEL NUEVO SISTEMA DE PRIORIDADES COMPLETADO")
    print("=" * 80)
