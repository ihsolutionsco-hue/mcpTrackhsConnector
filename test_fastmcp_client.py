#!/usr/bin/env python3
"""
Test FastMCP Client - TrackHS MCP Server
Verifica que las herramientas MCP funcionen correctamente con las correcciones usando FastMCP Client
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")


async def test_with_fastmcp_client():
    """Test usando FastMCP Client correctamente"""
    print("🚀 INICIANDO TEST CON FASTMCP CLIENT")
    print("=" * 60)

    try:
        # Importar el servidor MCP y el cliente
        from fastmcp import Client

        from trackhs_mcp.server import mcp

        print("✅ Servidor MCP y cliente importados correctamente")

        # Crear cliente con el servidor
        client = Client(mcp)

        async with client:
            print("✅ Cliente conectado al servidor")

            # Test 1: Ping al servidor
            print("\n1. Testing ping...")
            try:
                await client.ping()
                print("✅ Ping: FUNCIONA")
            except Exception as e:
                print(f"❌ Ping: ERROR - {e}")

            # Test 2: Listar herramientas
            print("\n2. Listando herramientas disponibles...")
            try:
                tools = await client.list_tools()
                print(f"✅ Herramientas disponibles: {len(tools)}")
                for tool in tools:
                    print(f"  - {tool.name}: {tool.description[:50]}...")
            except Exception as e:
                print(f"❌ Error listando herramientas: {e}")

            # Test 3: Test de search_reservations
            print("\n3. Testing search_reservations...")
            try:
                result = await client.call_tool("search_reservations", {"size": 3})
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print("✅ search_reservations: FUNCIONA")
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print("❌ search_reservations: Sin contenido válido")
                else:
                    print("❌ search_reservations: Sin resultado")
            except Exception as e:
                print(f"❌ search_reservations: ERROR - {e}")

            # Test 4: Test de search_units con parámetros string (CORRECCIÓN)
            print("\n4. Testing search_units con parámetros string (CORRECCIÓN)...")
            try:
                result = await client.call_tool(
                    "search_units",
                    {
                        "bedrooms": "2",  # String - debería funcionar ahora
                        "bathrooms": "1",  # String - debería funcionar ahora
                        "is_active": "1",  # String - debería funcionar ahora
                        "is_bookable": "true",  # String - debería funcionar ahora
                        "size": 3,
                    },
                )
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print(
                            "✅ search_units con strings: FUNCIONA - CORRECCIÓN EXITOSA"
                        )
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print("❌ search_units con strings: Sin contenido válido")
                else:
                    print("❌ search_units con strings: Sin resultado")
            except Exception as e:
                print(f"❌ search_units con strings: ERROR - {e}")

            # Test 5: Test de search_amenities (CORRECCIÓN)
            print("\n5. Testing search_amenities (CORRECCIÓN)...")
            try:
                result = await client.call_tool("search_amenities", {"size": 3})
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print("✅ search_amenities: FUNCIONA - CORRECCIÓN EXITOSA")
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print("❌ search_amenities: Sin contenido válido")
                else:
                    print("❌ search_amenities: Sin resultado")
            except Exception as e:
                print(f"❌ search_amenities: ERROR - {e}")

            # Test 6: Test de get_reservation
            print("\n6. Testing get_reservation...")
            try:
                result = await client.call_tool(
                    "get_reservation", {"reservation_id": 1}
                )
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print("✅ get_reservation: FUNCIONA")
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print("❌ get_reservation: Sin contenido válido")
                else:
                    print("❌ get_reservation: Sin resultado")
            except Exception as e:
                print(f"❌ get_reservation: ERROR - {e}")

            # Test 7: Test de get_folio (CORRECCIÓN)
            print("\n7. Testing get_folio (CORRECCIÓN)...")
            try:
                result = await client.call_tool("get_folio", {"reservation_id": 1})
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print("✅ get_folio: FUNCIONA - CORRECCIÓN EXITOSA")
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print("❌ get_folio: Sin contenido válido")
                else:
                    print("❌ get_folio: Sin resultado")
            except Exception as e:
                print(f"❌ get_folio: ERROR - {e}")

            # Test 8: Test de create_maintenance_work_order con strings (CORRECCIÓN)
            print(
                "\n8. Testing create_maintenance_work_order con strings (CORRECCIÓN)..."
            )
            try:
                result = await client.call_tool(
                    "create_maintenance_work_order",
                    {
                        "unit_id": 75,
                        "summary": "Test de conversión de tipos",
                        "description": "Verificar que la conversión de strings a números funcione correctamente",
                        "priority": 3,
                        "estimated_cost": "150.50",  # String - debería funcionar ahora
                        "estimated_time": "120",  # String - debería funcionar ahora
                    },
                )
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print(
                            "✅ create_maintenance_work_order con strings: FUNCIONA - CORRECCIÓN EXITOSA"
                        )
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print(
                            "❌ create_maintenance_work_order con strings: Sin contenido válido"
                        )
                else:
                    print("❌ create_maintenance_work_order con strings: Sin resultado")
            except Exception as e:
                print(f"❌ create_maintenance_work_order con strings: ERROR - {e}")

            # Test 9: Test de create_housekeeping_work_order con strings (CORRECCIÓN)
            print(
                "\n9. Testing create_housekeeping_work_order con strings (CORRECCIÓN)..."
            )
            try:
                result = await client.call_tool(
                    "create_housekeeping_work_order",
                    {
                        "unit_id": 75,
                        "scheduled_at": "2024-01-15",
                        "is_inspection": False,
                        "clean_type_id": "1",  # String - debería funcionar ahora
                        "comments": "Test de conversión de tipos de datos",
                        "cost": "80.00",  # String - debería funcionar ahora
                    },
                )
                if result and "content" in result:
                    content = result["content"]
                    if isinstance(content, list) and len(content) > 0:
                        print(
                            "✅ create_housekeeping_work_order con strings: FUNCIONA - CORRECCIÓN EXITOSA"
                        )
                        print(f"  - Tipo de contenido: {type(content[0])}")
                        print(
                            f"  - Primer elemento: {content[0] if content else 'N/A'}"
                        )
                    else:
                        print(
                            "❌ create_housekeeping_work_order con strings: Sin contenido válido"
                        )
                else:
                    print(
                        "❌ create_housekeeping_work_order con strings: Sin resultado"
                    )
            except Exception as e:
                print(f"❌ create_housekeeping_work_order con strings: ERROR - {e}")

    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("✅ TEST FASTMCP CLIENT COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_with_fastmcp_client())
