#!/usr/bin/env python3
"""
Script para probar el filtrado por fechas en el MCP de TrackHS
"""

import asyncio
import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.domain.value_objects.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

# Importar las funciones MCP directamente
from trackhs_mcp.infrastructure.mcp.search_reservations_v2 import search_reservations_v2


async def test_date_filtering():
    """Probar el filtrado por fechas directamente"""

    print("🔍 Probando filtrado por fechas directamente...")

    # Configurar cliente API
    config = TrackHSConfig()
    api_client = TrackHSApiClient(config)

    # Test 1: Búsqueda básica sin filtros
    print("\n=== TEST 1: Búsqueda básica sin filtros ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            sort_column="name",
            sort_direction="asc",
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
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            sort_column="name",
            sort_direction="asc",
            arrival_start="2024-03-01",
            arrival_end="2024-03-01",
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
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            sort_column="name",
            sort_direction="asc",
            arrival_start="2024-03-01",
            arrival_end="2024-03-31",
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
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            sort_column="name",
            sort_direction="asc",
            departure_start="2024-03-15",
            departure_end="2024-03-15",
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

    # Cerrar cliente
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(test_date_filtering())
