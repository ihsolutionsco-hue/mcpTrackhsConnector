#!/usr/bin/env python3
"""
Script para probar el filtrado por fechas usando el MCP directamente
"""

import asyncio
import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Cargar variables de entorno
from dotenv import load_dotenv

load_dotenv()

# Importar el servidor MCP
from trackhs_mcp.server import create_mcp_server


async def test_mcp_date_filtering():
    """Probar el filtrado por fechas usando el MCP"""

    print("🔍 Probando filtrado por fechas con MCP...")

    # Crear servidor MCP
    mcp_server = create_mcp_server()

    # Test 1: Búsqueda básica sin filtros
    print("\n=== TEST 1: Búsqueda básica sin filtros ===")
    try:
        result = await mcp_server.call_tool(
            "search_reservations",
            {"page": 1, "size": 3, "sort_column": "name", "sort_direction": "asc"},
        )
        print(f"✅ Búsqueda básica exitosa")
        print(f"Total items: {result.get('total_items', 'N/A')}")
        print(f"Page: {result.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(result.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de llegada de las primeras 3 reservaciones
        reservations = result.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"  Reservación {i+1}: arrivalDate = {arrival_date}")

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
        print(f"Total items: {result.get('total_items', 'N/A')}")
        print(f"Page: {result.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(result.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de llegada de las reservaciones encontradas
        reservations = result.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"  Reservación {i+1}: arrivalDate = {arrival_date}")

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
        print(f"Total items: {result.get('total_items', 'N/A')}")
        print(f"Page: {result.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(result.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de llegada de las reservaciones encontradas
        reservations = result.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"  Reservación {i+1}: arrivalDate = {arrival_date}")

    except Exception as e:
        print(f"❌ Error en filtro por rango: {e}")

    # Test 4: Filtro por fecha de salida
    print("\n=== TEST 4: Filtro por fecha de salida (2024-03-15) ===")
    try:
        result = await mcp_server.call_tool(
            "search_reservations",
            {
                "page": 1,
                "size": 3,
                "sort_column": "name",
                "sort_direction": "asc",
                "departure_start": "2024-03-15",
                "departure_end": "2024-03-15",
            },
        )
        print(f"✅ Filtro por salida exitoso")
        print(f"Total items: {result.get('total_items', 'N/A')}")
        print(f"Page: {result.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(result.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de salida de las reservaciones encontradas
        reservations = result.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            departure_date = res.get("departureDate", "N/A")
            print(f"  Reservación {i+1}: departureDate = {departure_date}")

    except Exception as e:
        print(f"❌ Error en filtro por salida: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_date_filtering())
