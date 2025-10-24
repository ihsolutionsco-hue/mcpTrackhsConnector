#!/usr/bin/env python3
"""
Script de prueba que simula exactamente el flujo del MCP
"""

import asyncio
import json
import os
import sys

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.application.use_cases.create_work_order import CreateWorkOrderUseCase
from trackhs_mcp.domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrderStatus,
)
from trackhs_mcp.domain.value_objects.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def test_mcp_workflow():
    """Probar el flujo completo del MCP"""
    print("🔧 PROBANDO FLUJO COMPLETO DEL MCP")
    print("=" * 50)

    # Cargar configuración desde .env
    config = TrackHSConfig(
        base_url="https://api-integration-example.tracksandbox.io",
        username=os.getenv("TRACKHS_USERNAME", "demo_user"),
        password=os.getenv("TRACKHS_PASSWORD", "demo_password"),
        timeout=30,
    )

    print(f"🔐 Config: {config.base_url}")
    print(f"👤 Username: {config.username}")
    print()

    # Crear cliente API
    api_client = TrackHSApiClient(config)

    # Crear parámetros de prueba
    params = CreateWorkOrderParams(
        date_received="2025-01-24",
        priority=5,
        status=WorkOrderStatus.OPEN,
        summary="Test work order - Aire acondicionado no funciona",
        estimated_cost=150.0,
        estimated_time=120,
        description="Huésped reporta que el A/C no enciende. Temperatura ambiente alta.",
        source="Guest Complaint",
        source_name="María González",
        source_phone="+52-998-1234567",
    )

    print("📦 Parámetros creados:")
    print(f"  - date_received: {params.date_received}")
    print(f"  - priority: {params.priority}")
    print(f"  - status: {params.status}")
    print(f"  - summary: {params.summary}")
    print(f"  - estimated_cost: {params.estimated_cost}")
    print(f"  - estimated_time: {params.estimated_time}")
    print()

    # Crear caso de uso
    use_case = CreateWorkOrderUseCase(api_client)

    try:
        print("🚀 Ejecutando caso de uso...")
        response = await use_case.execute(params)

        print("✅ ÉXITO - Work Order creado")
        print(f"📄 Response: {json.dumps(response.work_order.to_dict(), indent=2)}")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"🔍 Tipo de error: {type(e).__name__}")

        # Si es un error de API, mostrar más detalles
        if hasattr(e, "status_code"):
            print(f"📊 Status Code: {e.status_code}")
        if hasattr(e, "message"):
            print(f"📄 Message: {e.message}")
        if hasattr(e, "response_body"):
            print(f"📄 Response Body: {e.response_body}")

    finally:
        # Cerrar cliente
        await api_client.close()


if __name__ == "__main__":
    print("🧪 TRACKHS MCP - WORKFLOW TEST")
    print("=" * 60)

    # Ejecutar prueba
    asyncio.run(test_mcp_workflow())

    print("\n" + "=" * 60)
    print("🏁 PRUEBA COMPLETADA")
