#!/usr/bin/env python3
"""
Script para debuggear la validación de fechas
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


async def debug_validation():
    """Debuggear la validación de fechas"""

    print("🔍 Debuggeando validación de fechas...")

    # Configurar cliente API
    config = TrackHSConfig.from_env()
    api_client = TrackHSApiClient(config)

    # Test con diferentes valores
    test_values = ["null", "None", "", "2024-03-01"]

    for test_value in test_values:
        print(f"\n=== Probando con valor: '{test_value}' ===")
        print(f"Tipo: {type(test_value)}")
        print(f"Lower: '{test_value.lower()}'")
        print(f"Es 'null': {test_value == 'null'}")
        print(f"Es 'none': {test_value.lower() == 'none'}")
        print(f"Es vacío: {test_value == ''}")
        print(
            f"Condición: {test_value.lower() in ['null', 'none', ''] or test_value == 'null'}"
        )

        try:
            result = await search_reservations_v2(
                api_client=api_client,
                page=1,
                size=3,
                arrival_start=test_value,
                arrival_end=test_value,
            )
            print(
                f"✅ No se detectó error - resultado: {result.get('total_items', 'N/A')} reservaciones"
            )
        except ValidationError as e:
            print(f"✅ Validación detectó error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    # Cerrar cliente
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(debug_validation())
