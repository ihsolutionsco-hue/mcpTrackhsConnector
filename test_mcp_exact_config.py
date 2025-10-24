#!/usr/bin/env python3
"""
Script de prueba que usa exactamente la misma configuración que el MCP
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
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def test_with_mcp_config():
    """Probar con la configuración exacta del MCP"""
    print("🔧 PROBANDO CON CONFIGURACIÓN EXACTA DEL MCP")
    print("=" * 60)

    try:
        # Usar la misma configuración que el MCP
        config = TrackHSConfig.from_env()

        print(f"🔐 Base URL: {config.base_url}")
        print(f"👤 Username: {config.username}")
        print(f"⏱️ Timeout: {config.timeout}")
        print(f"🔍 Search Timeout: {config.search_timeout}")
        print()

        # Crear cliente API
        api_client = TrackHSApiClient(config)

        # Crear parámetros mínimos
        params = CreateWorkOrderParams(
            date_received="2025-01-24",
            priority=5,
            status=WorkOrderStatus.OPEN,
            summary="Test minimal work order",
            estimated_cost=100.0,
            estimated_time=60,
        )

        print("📦 Parámetros mínimos:")
        print(f"  - date_received: {params.date_received}")
        print(f"  - priority: {params.priority}")
        print(f"  - status: {params.status}")
        print(f"  - summary: {params.summary}")
        print(f"  - estimated_cost: {params.estimated_cost}")
        print(f"  - estimated_time: {params.estimated_time}")
        print()

        # Crear caso de uso
        use_case = CreateWorkOrderUseCase(api_client)

        print("🚀 Ejecutando caso de uso...")
        response = await use_case.execute(params)

        print("✅ ÉXITO - Work Order creado")
        print(f"📄 Response: {json.dumps(response.work_order.to_dict(), indent=2)}")
        return True

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

        return False

    finally:
        # Cerrar cliente
        try:
            await api_client.close()
        except:
            pass


async def test_with_detailed_logging():
    """Probar con logging detallado para ver el payload exacto"""
    print("\n" + "=" * 60)
    print("🔍 PROBANDO CON LOGGING DETALLADO")
    print("=" * 60)

    # Activar modo debug
    os.environ["DEBUG"] = "true"

    try:
        config = TrackHSConfig.from_env()
        api_client = TrackHSApiClient(config)

        # Crear parámetros con todos los campos opcionales
        params = CreateWorkOrderParams(
            date_received="2025-01-24",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test work order with all fields",
            estimated_cost=200.0,
            estimated_time=90,
            description="Test description",
            source="Test Source",
            source_name="Test User",
            source_phone="+1234567890",
        )

        print("📦 Parámetros completos:")
        print(f"  - date_received: {params.date_received}")
        print(f"  - priority: {params.priority}")
        print(f"  - status: {params.status}")
        print(f"  - summary: {params.summary}")
        print(f"  - estimated_cost: {params.estimated_cost}")
        print(f"  - estimated_time: {params.estimated_time}")
        print(f"  - description: {params.description}")
        print(f"  - source: {params.source}")
        print(f"  - source_name: {params.source_name}")
        print(f"  - source_phone: {params.source_phone}")
        print()

        use_case = CreateWorkOrderUseCase(api_client)

        print("🚀 Ejecutando caso de uso con logging detallado...")
        response = await use_case.execute(params)

        print("✅ ÉXITO - Work Order creado")
        print(f"📄 Response: {json.dumps(response.work_order.to_dict(), indent=2)}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"🔍 Tipo de error: {type(e).__name__}")

        if hasattr(e, "status_code"):
            print(f"📊 Status Code: {e.status_code}")
        if hasattr(e, "message"):
            print(f"📄 Message: {e.message}")
        if hasattr(e, "response_body"):
            print(f"📄 Response Body: {e.response_body}")

        return False

    finally:
        try:
            await api_client.close()
        except:
            pass


if __name__ == "__main__":
    print("🧪 TRACKHS MCP - EXACT CONFIG TEST")
    print("=" * 70)

    # Ejecutar pruebas
    success1 = asyncio.run(test_with_mcp_config())

    if not success1:
        success2 = asyncio.run(test_with_detailed_logging())

        if not success2:
            print("\n❌ Ambas pruebas fallaron")
            print("🔍 El problema podría ser:")
            print("  1. Credenciales inválidas")
            print("  2. Permisos insuficientes")
            print("  3. Formato de datos incorrecto")
            print("  4. Configuración de la API")

    print("\n" + "=" * 70)
    print("🏁 PRUEBA COMPLETADA")
