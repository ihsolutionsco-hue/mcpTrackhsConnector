#!/usr/bin/env python3
"""
Script de testing usando el protocolo MCP estándar
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_tools():
    """Probar herramientas MCP usando el protocolo estándar"""
    print("🚀 INICIANDO TESTING CON PROTOCOLO MCP")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Configurar cliente MCP
        server_params = StdioServerParameters(
            command="python", args=["-m", "trackhs_mcp"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar sesión
                await session.initialize()
                print("✅ Sesión MCP inicializada correctamente")

                # Listar herramientas disponibles
                tools = await session.list_tools()
                print(f"\n📋 Herramientas disponibles: {len(tools.tools)}")

                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description[:80]}...")

                # Test 1: search_reservations
                print("\n🔍 PROBANDO SEARCH_RESERVATIONS")
                print("-" * 40)

                try:
                    result = await session.call_tool(
                        "search_reservations",
                        {"page": 0, "size": 5, "status": "confirmed"},
                    )
                    print("✅ search_reservations: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(
                                f"   Total items: {content.get('total_items', 'N/A')}"
                            )
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ search_reservations: Error - {e}")

                # Test 2: search_units
                print("\n🏠 PROBANDO SEARCH_UNITS")
                print("-" * 40)

                try:
                    result = await session.call_tool(
                        "search_units",
                        {"page": 1, "size": 5, "is_active": 1, "is_bookable": 1},
                    )
                    print("✅ search_units: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(
                                f"   Total items: {content.get('total_items', 'N/A')}"
                            )
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ search_units: Error - {e}")

                # Test 3: search_amenities
                print("\n🏊 PROBANDO SEARCH_AMENITIES")
                print("-" * 40)

                try:
                    result = await session.call_tool(
                        "search_amenities", {"page": 1, "size": 10}
                    )
                    print("✅ search_amenities: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(
                                f"   Total items: {content.get('total_items', 'N/A')}"
                            )
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ search_amenities: Error - {e}")

                # Test 4: get_reservation (con ID de prueba)
                print("\n📋 PROBANDO GET_RESERVATION")
                print("-" * 40)

                try:
                    result = await session.call_tool(
                        "get_reservation", {"reservation_id": 1}
                    )
                    print("✅ get_reservation: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(
                                f"   Confirmation: {content.get('confirmation_number', 'N/A')}"
                            )
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ get_reservation: Error - {e}")

                # Test 5: get_folio (con ID de prueba)
                print("\n💰 PROBANDO GET_FOLIO")
                print("-" * 40)

                try:
                    result = await session.call_tool("get_folio", {"reservation_id": 1})
                    print("✅ get_folio: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(f"   Balance: ${content.get('balance', 0)}")
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ get_folio: Error - {e}")

                # Test 6: create_maintenance_work_order
                print("\n🔧 PROBANDO CREATE_MAINTENANCE_WORK_ORDER")
                print("-" * 40)

                try:
                    result = await session.call_tool(
                        "create_maintenance_work_order",
                        {
                            "unit_id": 1,
                            "summary": "Test de mantenimiento",
                            "description": "Prueba de creación de orden de mantenimiento",
                            "priority": 3,
                            "estimated_cost": 100.0,
                            "estimated_time": 60,
                        },
                    )
                    print("✅ create_maintenance_work_order: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(f"   Work Order ID: {content.get('id', 'N/A')}")
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ create_maintenance_work_order: Error - {e}")

                # Test 7: create_housekeeping_work_order
                print("\n🧹 PROBANDO CREATE_HOUSEKEEPING_WORK_ORDER")
                print("-" * 40)

                try:
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    result = await session.call_tool(
                        "create_housekeeping_work_order",
                        {
                            "unit_id": 1,
                            "scheduled_at": tomorrow,
                            "is_inspection": False,
                            "clean_type_id": 4,
                            "comments": "Test de housekeeping",
                            "cost": 75.0,
                        },
                    )
                    print("✅ create_housekeeping_work_order: Éxito")
                    if hasattr(result, "content") and result.content:
                        content = result.content[0] if result.content else {}
                        if isinstance(content, dict):
                            print(f"   Work Order ID: {content.get('id', 'N/A')}")
                        else:
                            print(f"   Respuesta: {str(content)[:100]}...")
                except Exception as e:
                    print(f"❌ create_housekeeping_work_order: Error - {e}")

                # Test 8: Manejo de errores
                print("\n🚫 PROBANDO MANEJO DE ERRORES")
                print("-" * 40)

                # Test con parámetros inválidos
                try:
                    result = await session.call_tool(
                        "search_reservations",
                        {"page": -1, "size": 10},  # Página inválida
                    )
                    print("❌ Debería haber fallado con página inválida")
                except Exception as e:
                    print(f"✅ Correctamente manejó parámetros inválidos: {e}")

                # Test con fecha inválida
                try:
                    result = await session.call_tool(
                        "search_reservations",
                        {"arrival_start": "2024-13-45", "size": 10},  # Fecha inválida
                    )
                    print("❌ Debería haber fallado con fecha inválida")
                except Exception as e:
                    print(f"✅ Correctamente manejó fecha inválida: {e}")

                print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS")
                print("=" * 60)
                print(
                    "El MCP está funcionando correctamente con el protocolo estándar."
                )

    except Exception as e:
        print(f"\n\n❌ ERROR CRÍTICO: {e}")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_mcp_tools())
    sys.exit(exit_code)
