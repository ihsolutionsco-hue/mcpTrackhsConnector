#!/usr/bin/env python3
"""
Script para probar directamente la API de TrackHS y entender cómo funcionan los filtros de fechas
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.domain.value_objects.config import TrackHSConfig
from trackhs_mcp.domain.value_objects.request import RequestOptions
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def test_api_direct():
    """Probar la API directamente para entender el filtrado por fechas"""

    # Configurar cliente API
    config = TrackHSConfig()
    api_client = TrackHSApiClient(config)

    print("🔍 Probando API directamente...")

    # Test 1: Búsqueda básica sin filtros
    print("\n=== TEST 1: Búsqueda básica sin filtros ===")
    try:
        response = await api_client.search_request(
            "/v2/pms/reservations",
            options=RequestOptions(method="GET"),
            params={"page": 1, "size": 3},
        )
        print(f"✅ Búsqueda básica exitosa")
        print(f"Total items: {response.get('total_items', 'N/A')}")
        print(f"Page: {response.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(response.get('_embedded', {}).get('reservations', []))}"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    # Test 2: Filtro por fecha de llegada específica
    print("\n=== TEST 2: Filtro por fecha de llegada (2024-03-01) ===")
    try:
        response = await api_client.search_request(
            "/v2/pms/reservations",
            options=RequestOptions(method="GET"),
            params={
                "page": 1,
                "size": 3,
                "arrivalStart": "2024-03-01",
                "arrivalEnd": "2024-03-01",
            },
        )
        print(f"✅ Filtro por fecha exitoso")
        print(f"Total items: {response.get('total_items', 'N/A')}")
        print(f"Page: {response.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(response.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de llegada de las reservaciones encontradas
        reservations = response.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"  Reservación {i+1}: arrivalDate = {arrival_date}")

    except Exception as e:
        print(f"❌ Error en filtro por fecha: {e}")

    # Test 3: Filtro por rango de fechas
    print("\n=== TEST 3: Filtro por rango de fechas (marzo 2024) ===")
    try:
        response = await api_client.search_request(
            "/v2/pms/reservations",
            options=RequestOptions(method="GET"),
            params={
                "page": 1,
                "size": 3,
                "arrivalStart": "2024-03-01",
                "arrivalEnd": "2024-03-31",
            },
        )
        print(f"✅ Filtro por rango exitoso")
        print(f"Total items: {response.get('total_items', 'N/A')}")
        print(f"Page: {response.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(response.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de llegada de las reservaciones encontradas
        reservations = response.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"  Reservación {i+1}: arrivalDate = {arrival_date}")

    except Exception as e:
        print(f"❌ Error en filtro por rango: {e}")

    # Test 4: Filtro por fecha de salida
    print("\n=== TEST 4: Filtro por fecha de salida (2024-03-15) ===")
    try:
        response = await api_client.search_request(
            "/v2/pms/reservations",
            options=RequestOptions(method="GET"),
            params={
                "page": 1,
                "size": 3,
                "departureStart": "2024-03-15",
                "departureEnd": "2024-03-15",
            },
        )
        print(f"✅ Filtro por salida exitoso")
        print(f"Total items: {response.get('total_items', 'N/A')}")
        print(f"Page: {response.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(response.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar fechas de salida de las reservaciones encontradas
        reservations = response.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            departure_date = res.get("departureDate", "N/A")
            print(f"  Reservación {i+1}: departureDate = {departure_date}")

    except Exception as e:
        print(f"❌ Error en filtro por salida: {e}")

    # Test 5: Combinación de filtros
    print("\n=== TEST 5: Combinación de filtros (fecha + estado) ===")
    try:
        response = await api_client.search_request(
            "/v2/pms/reservations",
            options=RequestOptions(method="GET"),
            params={
                "page": 1,
                "size": 3,
                "arrivalStart": "2024-03-01",
                "arrivalEnd": "2024-03-31",
                "status": "Confirmed",
            },
        )
        print(f"✅ Combinación de filtros exitosa")
        print(f"Total items: {response.get('total_items', 'N/A')}")
        print(f"Page: {response.get('page', 'N/A')}")
        print(
            f"Reservations count: {len(response.get('_embedded', {}).get('reservations', []))}"
        )

        # Mostrar detalles de las reservaciones encontradas
        reservations = response.get("_embedded", {}).get("reservations", [])
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            status = res.get("status", "N/A")
            print(
                f"  Reservación {i+1}: arrivalDate = {arrival_date}, status = {status}"
            )

    except Exception as e:
        print(f"❌ Error en combinación de filtros: {e}")


if __name__ == "__main__":
    asyncio.run(test_api_direct())
