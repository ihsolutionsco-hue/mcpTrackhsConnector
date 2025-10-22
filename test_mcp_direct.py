#!/usr/bin/env python3
"""
Script para probar directamente el MCP de TrackHS y entender cómo funcionan los filtros de fechas
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Importar el servidor MCP
from trackhs_mcp.server import create_mcp_server


async def test_mcp_direct():
    """Probar el MCP directamente para entender el filtrado por fechas"""

    print("🔍 Probando MCP directamente...")

    # Crear servidor MCP
    mcp_server = create_mcp_server()

    # Test 1: Búsqueda básica sin filtros
    print("\n=== TEST 1: Búsqueda básica sin filtros ===")
    try:
        # Simular llamada MCP
        result = await mcp_server.call_tool(
            "search_reservations",
            {"page": 1, "size": 3, "sort_column": "name", "sort_direction": "asc"},
        )
        print(f"✅ Búsqueda básica exitosa")
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    # Test 2: Filtro por fecha de llegada específica
    print("\n=== TEST 2: Filtro por fecha de llegada (2024-03-01) ===")
    try:
        result = await mcp_server.call_tool(
            "search_reservations",
            {
                "page": 1,
                "size": 3,
                "sort_column": "name",
                "sort_direction": "asc",
                "arrival_start": "2024-03-01",
                "arrival_end": "2024-03-01",
            },
        )
        print(f"✅ Filtro por fecha exitoso")
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"❌ Error en filtro por fecha: {e}")

    # Test 3: Filtro por rango de fechas
    print("\n=== TEST 3: Filtro por rango de fechas (marzo 2024) ===")
    try:
        result = await mcp_server.call_tool(
            "search_reservations",
            {
                "page": 1,
                "size": 3,
                "sort_column": "name",
                "sort_direction": "asc",
                "arrival_start": "2024-03-01",
                "arrival_end": "2024-03-31",
            },
        )
        print(f"✅ Filtro por rango exitoso")
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"❌ Error en filtro por rango: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_direct())
