#!/usr/bin/env python3
"""
Script completo de testing para create_maintenance_work_order
Simula llamadas de servicio al cliente y testing técnico
"""

import asyncio
import base64
import json
import os
from datetime import datetime, timedelta

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


async def test_technical_parameters():
    """Testing técnico de parámetros"""
    print("🔧 TESTING TÉCNICO - PARÁMETROS")
    print("=" * 60)

    # Test 1: Parámetros obligatorios básicos
    print("\n📋 Test 1: Parámetros obligatorios básicos")
    payload1 = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Test básico - Parámetros obligatorios",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result1 = await call_api(payload1, "Parámetros obligatorios")
    if result1["success"]:
        print(f"✅ ÉXITO - Work Order ID: {result1['work_order_id']}")
    else:
        print(f"❌ ERROR - {result1['error']}")

    # Test 2: Parámetros opcionales
    print("\n📋 Test 2: Parámetros opcionales")
    payload2 = {
        "dateReceived": "2025-01-24",
        "priority": 3,
        "summary": "Test con parámetros opcionales",
        "estimatedCost": 200.0,
        "estimatedTime": 90,
        "unitId": 1,
        "dateScheduled": "2025-01-25",
        "description": "Descripción detallada del trabajo",
        "source": "Guest Request",
        "sourceName": "María González",
        "sourcePhone": "+52-998-1234567",
    }

    result2 = await call_api(payload2, "Parámetros opcionales")
    if result2["success"]:
        print(f"✅ ÉXITO - Work Order ID: {result2['work_order_id']}")
    else:
        print(f"❌ ERROR - {result2['error']}")

    # Test 3: Validación de prioridades
    print("\n📋 Test 3: Validación de prioridades")
    priorities = [1, 3, 5]
    for priority in priorities:
        payload = {
            "dateReceived": "2025-01-24",
            "priority": priority,
            "summary": f"Test prioridad {priority}",
            "estimatedCost": 50.0,
            "estimatedTime": 30,
            "unitId": 1,
        }

        result = await call_api(payload, f"Prioridad {priority}")
        if result["success"]:
            print(f"✅ Prioridad {priority}: ÉXITO - ID: {result['work_order_id']}")
        else:
            print(f"❌ Prioridad {priority}: ERROR - {result['error']}")

    # Test 4: Fechas en formato ISO 8601
    print("\n📋 Test 4: Validación de fechas ISO 8601")
    date_formats = ["2025-01-24", "2025-01-24T10:30:00Z", "2025-01-24T15:45:00-05:00"]

    for date_format in date_formats:
        payload = {
            "dateReceived": date_format,
            "priority": 3,
            "summary": f"Test fecha {date_format}",
            "estimatedCost": 75.0,
            "estimatedTime": 45,
            "unitId": 1,
        }

        result = await call_api(payload, f"Fecha {date_format}")
        if result["success"]:
            print(f"✅ Fecha {date_format}: ÉXITO - ID: {result['work_order_id']}")
        else:
            print(f"❌ Fecha {date_format}: ERROR - {result['error']}")


async def test_customer_service_calls():
    """Simulación de llamadas de servicio al cliente"""
    print("\n" + "=" * 60)
    print("📞 SIMULACIÓN DE LLAMADAS DE SERVICIO AL CLIENTE")
    print("=" * 60)

    # CASO 1: Aire acondicionado no funciona
    print("\n🔧 CASO 1: Aire acondicionado no funciona")
    print(
        "Llamada: 'Buenos días, tengo un huésped en la Villa 5 que dice que el aire acondicionado no enciende. Hace mucho calor y están muy molestos. ¿Pueden ayudarme?'"
    )

    payload_ac = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Aire acondicionado no funciona - Villa 5",
        "estimatedCost": 150.0,
        "estimatedTime": 120,
        "unitId": 5,
        "description": "Huésped reporta que el A/C no enciende. Temperatura ambiente alta. Requiere atención inmediata para comodidad del huésped.",
        "source": "Guest Complaint",
        "sourceName": "María González",
        "sourcePhone": "+52-998-1234567",
    }

    result_ac = await call_api(payload_ac, "Aire acondicionado")
    if result_ac["success"]:
        print("✅ RESPUESTA DEL SISTEMA: Work Order creado exitosamente")
        print(f"📄 Work Order ID: {result_ac['work_order_id']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'Señora González, he creado una orden de trabajo prioritaria (Prioridad 5/5). El técnico debería revisar el aire acondicionado en aproximadamente 2 horas. El costo estimado es de $150. Le mantendremos informada del progreso.'"
        )
        print(
            "📋 SEGUIMIENTO: Notificar al equipo técnico inmediatamente, contactar al huésped cada 30 minutos con actualizaciones, considerar cambio de habitación si la reparación toma más de 3 horas"
        )
    else:
        print(f"❌ RESPUESTA DEL SISTEMA: Error - {result_ac['error']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'Señora González, hay un problema técnico con el sistema de órdenes de trabajo. Voy a contactar directamente al plomero de emergencia mientras resuelvo el problema del sistema.'"
        )

    # CASO 2: Fuga de agua en villa 10
    print("\n💧 CASO 2: Fuga de agua en villa 10")
    print(
        "Llamada: '¡Emergencia! La Villa 10 tiene una fuga de agua en el baño. El agua está saliendo por debajo de la puerta. Hay huéspedes dentro y están alarmados.'"
    )

    payload_water = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "EMERGENCIA - Fuga de agua severa Villa 10",
        "estimatedCost": 500.0,
        "estimatedTime": 240,
        "unitId": 10,
        "description": "Fuga importante en baño principal. Agua saliendo por debajo de puerta. Huéspedes presentes. Riesgo de daño estructural. ATENCIÓN INMEDIATA REQUERIDA.",
        "source": "Staff Emergency",
        "sourceName": "Pedro Sánchez - Supervisor",
        "sourcePhone": "+52-998-5555555",
        "blockCheckin": True,
    }

    result_water = await call_api(payload_water, "Fuga de agua")
    if result_water["success"]:
        print("✅ RESPUESTA DEL SISTEMA: Orden de emergencia creada exitosamente")
        print(f"📄 Work Order ID: {result_water['work_order_id']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He activado el protocolo de emergencia. El técnico está en camino (tiempo estimado: 15 minutos). Por favor, cierre la llave de paso del agua en el baño si es posible. Voy a coordinar con los huéspedes para reubicarlos temporalmente si es necesario.'"
        )
        print(
            "📋 SEGUIMIENTO: Llamar al plomero de emergencia, cerrar llave de paso principal, ofrecer cambio de villa a los huéspedes, documentar daños con fotos"
        )
    else:
        print(f"❌ RESPUESTA DEL SISTEMA: Error - {result_water['error']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He intentado crear la orden de emergencia pero hay un problema técnico con el sistema. Voy a contactar directamente al plomero de emergencia mientras resuelvo el problema del sistema.'"
        )

    # CASO 3: Problemas de WiFi
    print("\n📡 CASO 3: Problemas de WiFi")
    print(
        "Llamada: 'Tengo varios huéspedes quejándose del WiFi. Algunos dicen que no conecta y otros que es muy lento. ¿Es problema del router o del proveedor?'"
    )

    payload_wifi = {
        "dateReceived": "2025-01-24",
        "priority": 3,
        "summary": "Problemas de conectividad WiFi - Múltiples unidades",
        "estimatedCost": 75.0,
        "estimatedTime": 90,
        "unitId": 1,
        "description": "Múltiples huéspedes reportan WiFi lento o sin conexión. Verificar: 1) Estado del router principal, 2) Repetidores, 3) Conexión con ISP. Posible sobrecarga de red.",
        "source": "Guest Complaint",
        "referenceNumber": "ISP-2025-0124",
    }

    result_wifi = await call_api(payload_wifi, "Problemas WiFi")
    if result_wifi["success"]:
        print("✅ RESPUESTA DEL SISTEMA: Orden de trabajo creada exitosamente")
        print(f"📄 Work Order ID: {result_wifi['work_order_id']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He creado una orden de trabajo para el equipo técnico. Van a revisar el router y la conexión con el proveedor. Tiempo estimado de resolución: 1.5 horas. Si es problema del proveedor de internet, puede tomar más tiempo. Mantendré informados a los huéspedes.'"
        )
        print(
            "📋 SEGUIMIENTO: Reiniciar router principal como solución temporal, verificar número de dispositivos conectados, contactar al ISP si problema persiste"
        )
    else:
        print(f"❌ RESPUESTA DEL SISTEMA: Error - {result_wifi['error']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He intentado crear la orden para el problema de WiFi pero el sistema tiene problemas técnicos. Voy a reiniciar el router como solución temporal y contactar al proveedor de internet directamente.'"
        )

    # CASO 4: Limpieza profunda post-fiesta
    print("\n🧹 CASO 4: Limpieza profunda post-fiesta")
    print(
        "Llamada: 'La Villa Paraíso necesita limpieza profunda urgente. Los huéspedes tuvieron una fiesta y dejaron todo muy sucio. El próximo check-in es mañana a las 3 PM.'"
    )

    payload_cleaning = {
        "dateReceived": "2025-01-24",
        "dateScheduled": "2025-01-24T14:00:00Z",
        "priority": 4,
        "summary": "Limpieza profunda post-evento - Villa Paraíso",
        "estimatedCost": 350.0,
        "estimatedTime": 360,
        "unitId": 15,
        "description": "Limpieza profunda requerida después de fiesta. Incluye: limpieza de manchas, organización completa, lavado de cortinas, limpieza profunda de cocina y baños. Check-in programado para mañana 3 PM.",
        "source": "Property Inspection",
    }

    result_cleaning = await call_api(payload_cleaning, "Limpieza profunda")
    if result_cleaning["success"]:
        print("✅ RESPUESTA DEL SISTEMA: Orden de limpieza programada exitosamente")
        print(f"📄 Work Order ID: {result_cleaning['work_order_id']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He programado el equipo de limpieza profunda para hoy a las 2 PM. Van a trabajar 6 horas aproximadamente. El costo es de $350. La villa estará lista para el check-in de mañana. Voy a hacer una inspección final mañana a las 11 AM para confirmar que todo esté perfecto.'"
        )
        print(
            "📋 SEGUIMIENTO: Confirmar disponibilidad del equipo de limpieza, tomar fotos del estado actual, coordinar con housekeeping para suministros extra, inspección de calidad antes del check-in"
        )
    else:
        print(f"❌ RESPUESTA DEL SISTEMA: Error - {result_cleaning['error']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He intentado programar la limpieza profunda pero hay un problema técnico con el sistema. Voy a contactar directamente al equipo de limpieza mientras resuelvo el problema del sistema.'"
        )

    # CASO 5: Mejoras en la villa
    print("\n🔨 CASO 5: Mejoras en la villa")
    print(
        "Llamada: 'Soy propietario de la Villa Sunset. Quiero instalar un jacuzzi nuevo y mejorar la terraza. No tengo reservas en febrero. ¿Pueden coordinar las mejoras?'"
    )

    payload_improvements = {
        "dateReceived": "2025-01-24",
        "dateScheduled": "2025-02-01T08:00:00Z",
        "priority": 2,
        "summary": "Mejoras mayores - Instalación jacuzzi y renovación terraza",
        "estimatedCost": 8500.0,
        "estimatedTime": 10080,
        "unitId": 20,
        "description": "Proyecto de mejoras propietario-aprobado: 1) Instalación de jacuzzi 6 personas, 2) Renovación de deck de terraza, 3) Mejora de iluminación exterior. Estimado: 2 semanas. Presupuesto: $8,500 aprobado por propietario.",
        "source": "Owner Request",
        "sourceName": "Ana Rodríguez",
        "sourcePhone": "+52-998-7777777",
        "referenceNumber": "UPGRADE-SUNSET-2025",
        "blockCheckin": True,
    }

    result_improvements = await call_api(payload_improvements, "Mejoras villa")
    if result_improvements["success"]:
        print("✅ RESPUESTA DEL SISTEMA: Proyecto de mejoras creado exitosamente")
        print(f"📄 Work Order ID: {result_improvements['work_order_id']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'Excelente, Doña Ana. He creado el proyecto de mejoras para iniciar el 1 de febrero. Duración estimada: 2 semanas. Costo total: $8,500. He bloqueado la villa durante febrero completo para asegurar tiempo suficiente. Le enviaré actualizaciones semanales con fotos del progreso.'"
        )
        print(
            "📋 SEGUIMIENTO: Confirmar disponibilidad del contratista, enviar recordatorio al propietario 24 horas antes, bloquear villa en el calendario hasta completar trabajo, inspeccionar trabajo antes de desbloquear"
        )
    else:
        print(f"❌ RESPUESTA DEL SISTEMA: Error - {result_improvements['error']}")
        print(
            "💬 INFORMACIÓN PARA EL CLIENTE: 'He intentado crear el proyecto de mejoras pero hay un problema técnico con el sistema. Voy a contactar directamente al contratista mientras resuelvo el problema del sistema.'"
        )


async def test_error_cases():
    """Testing de casos de error"""
    print("\n" + "=" * 60)
    print("❌ TESTING DE CASOS DE ERROR")
    print("=" * 60)

    # Test 1: Sin unitId (debería fallar)
    print("\n📋 Test Error 1: Sin unitId")
    payload_no_unit = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Test sin unitId",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
    }

    result_no_unit = await call_api(payload_no_unit, "Sin unitId")
    if not result_no_unit["success"]:
        print(f"✅ ERROR ESPERADO - {result_no_unit['error']}")
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result_no_unit['work_order_id']}"
        )

    # Test 2: Prioridad inválida
    print("\n📋 Test Error 2: Prioridad inválida")
    payload_invalid_priority = {
        "dateReceived": "2025-01-24",
        "priority": 2,  # Prioridad inválida (debería ser 1, 3, o 5)
        "summary": "Test prioridad inválida",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result_invalid_priority = await call_api(
        payload_invalid_priority, "Prioridad inválida"
    )
    if not result_invalid_priority["success"]:
        print(f"✅ ERROR ESPERADO - {result_invalid_priority['error']}")
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result_invalid_priority['work_order_id']}"
        )

    # Test 3: Fecha inválida
    print("\n📋 Test Error 3: Fecha inválida")
    payload_invalid_date = {
        "dateReceived": "24-01-2025",  # Formato inválido
        "priority": 5,
        "summary": "Test fecha inválida",
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
    }

    result_invalid_date = await call_api(payload_invalid_date, "Fecha inválida")
    if not result_invalid_date["success"]:
        print(f"✅ ERROR ESPERADO - {result_invalid_date['error']}")
    else:
        print(
            f"❌ INESPERADO - Debería haber fallado pero funcionó: {result_invalid_date['work_order_id']}"
        )


if __name__ == "__main__":
    print("🧪 TRACKHS API - COMPLETE MAINTENANCE WORK ORDER TESTING")
    print("=" * 80)
    print(f"🔐 Usando credenciales: {username}")
    print(f"🌐 Base URL: {base_url}")
    print("=" * 80)

    # Ejecutar todas las pruebas
    asyncio.run(test_technical_parameters())
    asyncio.run(test_customer_service_calls())
    asyncio.run(test_error_cases())

    print("\n" + "=" * 80)
    print("🏁 TESTING COMPLETADO")
    print("=" * 80)
