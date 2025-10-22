#!/usr/bin/env python3
"""
Script para probar las mejoras de validación en el MCP de TrackHS
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

from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

# Importar las funciones MCP directamente
from trackhs_mcp.infrastructure.mcp.search_reservations_v2 import search_reservations_v2


async def test_validation_improvements():
    """Probar las mejoras de validación"""

    print("🔍 Probando mejoras de validación...")

    # Configurar cliente API
    config = TrackHSConfig.from_env()
    api_client = TrackHSApiClient(config)

    # Test 1: Validación de "null" como string
    print("\n=== TEST 1: Validación de 'null' como string ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            arrival_start="null",  # ❌ Esto debería fallar
            arrival_end="null",  # ❌ Esto debería fallar
        )
        print("❌ ERROR: La validación no funcionó - debería haber fallado")
    except ValidationError as e:
        print(f"✅ Validación funcionó correctamente: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test 2: Validación de "None" como string
    print("\n=== TEST 2: Validación de 'None' como string ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            arrival_start="None",  # ❌ Esto debería fallar
            arrival_end="None",  # ❌ Esto debería fallar
        )
        print("❌ ERROR: La validación no funcionó - debería haber fallado")
    except ValidationError as e:
        print(f"✅ Validación funcionó correctamente: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test 3: Validación de string vacío
    print("\n=== TEST 3: Validación de string vacío ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            arrival_start="",  # ❌ Esto debería fallar
            arrival_end="",  # ❌ Esto debería fallar
        )
        print("❌ ERROR: La validación no funcionó - debería haber fallado")
    except ValidationError as e:
        print(f"✅ Validación funcionó correctamente: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test 4: Uso correcto de fechas
    print("\n=== TEST 4: Uso correcto de fechas ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            arrival_start="2024-03-01",  # ✅ Esto debería funcionar
            arrival_end="2024-03-01",  # ✅ Esto debería funcionar
        )
        print(
            f"✅ Uso correcto funcionó: {result.get('total_items', 'N/A')} reservaciones"
        )
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test 5: Omitir parámetros (uso correcto)
    print("\n=== TEST 5: Omitir parámetros (uso correcto) ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            # ✅ No incluir arrival_start ni arrival_end
        )
        print(
            f"✅ Omitir parámetros funcionó: {result.get('total_items', 'N/A')} reservaciones"
        )
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Cerrar cliente
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(test_validation_improvements())
