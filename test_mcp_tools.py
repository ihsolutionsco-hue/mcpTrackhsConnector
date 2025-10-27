#!/usr/bin/env python3
"""
Test MCP Tools - TrackHS MCP Server
Verifica que las herramientas MCP funcionen correctamente con las correcciones
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


async def test_mcp_tools():
    """Test de herramientas MCP usando el servidor correctamente"""
    print("🚀 INICIANDO TEST MCP TOOLS")
    print("=" * 60)

    try:
        # Importar el servidor MCP
        from trackhs_mcp.server import mcp

        print("✅ Servidor MCP importado correctamente")

        # Test 1: Listar herramientas disponibles
        print("\n1. Listando herramientas disponibles...")
        try:
            tools = mcp.list_tools()
            print(f"✅ Herramientas disponibles: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description[:50]}...")
        except Exception as e:
            print(f"❌ Error listando herramientas: {e}")

        # Test 2: Test de search_reservations
        print("\n2. Testing search_reservations...")
        try:
            result = await mcp.call_tool("search_reservations", {"size": 3})
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ search_reservations: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print("❌ search_reservations: Sin contenido válido")
            else:
                print("❌ search_reservations: Sin resultado")
        except Exception as e:
            print(f"❌ search_reservations: ERROR - {e}")

        # Test 3: Test de search_units con parámetros string
        print("\n3. Testing search_units con parámetros string...")
        try:
            result = await mcp.call_tool(
                "search_units",
                {
                    "bedrooms": "2",  # String
                    "bathrooms": "1",  # String
                    "is_active": "1",  # String
                    "is_bookable": "true",  # String
                    "size": 3,
                },
            )
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ search_units con strings: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print("❌ search_units con strings: Sin contenido válido")
            else:
                print("❌ search_units con strings: Sin resultado")
        except Exception as e:
            print(f"❌ search_units con strings: ERROR - {e}")

        # Test 4: Test de search_amenities
        print("\n4. Testing search_amenities...")
        try:
            result = await mcp.call_tool("search_amenities", {"size": 3})
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ search_amenities: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print("❌ search_amenities: Sin contenido válido")
            else:
                print("❌ search_amenities: Sin resultado")
        except Exception as e:
            print(f"❌ search_amenities: ERROR - {e}")

        # Test 5: Test de get_reservation
        print("\n5. Testing get_reservation...")
        try:
            result = await mcp.call_tool("get_reservation", {"reservation_id": 1})
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ get_reservation: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print("❌ get_reservation: Sin contenido válido")
            else:
                print("❌ get_reservation: Sin resultado")
        except Exception as e:
            print(f"❌ get_reservation: ERROR - {e}")

        # Test 6: Test de get_folio
        print("\n6. Testing get_folio...")
        try:
            result = await mcp.call_tool("get_folio", {"reservation_id": 1})
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ get_folio: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print("❌ get_folio: Sin contenido válido")
            else:
                print("❌ get_folio: Sin resultado")
        except Exception as e:
            print(f"❌ get_folio: ERROR - {e}")

        # Test 7: Test de create_maintenance_work_order con strings
        print("\n7. Testing create_maintenance_work_order con strings...")
        try:
            result = await mcp.call_tool(
                "create_maintenance_work_order",
                {
                    "unit_id": 75,
                    "summary": "Test de conversión",
                    "description": "Verificar conversión de tipos de datos",
                    "priority": 3,
                    "estimated_cost": "150.50",  # String
                    "estimated_time": "120",  # String
                },
            )
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ create_maintenance_work_order con strings: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print(
                        "❌ create_maintenance_work_order con strings: Sin contenido válido"
                    )
            else:
                print("❌ create_maintenance_work_order con strings: Sin resultado")
        except Exception as e:
            print(f"❌ create_maintenance_work_order con strings: ERROR - {e}")

        # Test 8: Test de create_housekeeping_work_order con strings
        print("\n8. Testing create_housekeeping_work_order con strings...")
        try:
            result = await mcp.call_tool(
                "create_housekeeping_work_order",
                {
                    "unit_id": 75,
                    "scheduled_at": "2024-01-15",
                    "is_inspection": False,
                    "clean_type_id": "1",  # String
                    "comments": "Test de conversión",
                    "cost": "80.00",  # String
                },
            )
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    print("✅ create_housekeeping_work_order con strings: FUNCIONA")
                    print(f"  - Tipo de contenido: {type(content[0])}")
                else:
                    print(
                        "❌ create_housekeeping_work_order con strings: Sin contenido válido"
                    )
            else:
                print("❌ create_housekeeping_work_order con strings: Sin resultado")
        except Exception as e:
            print(f"❌ create_housekeeping_work_order con strings: ERROR - {e}")

    except Exception as e:
        print(f"❌ Error general: {e}")

    print("\n" + "=" * 60)
    print("✅ TEST MCP TOOLS COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
