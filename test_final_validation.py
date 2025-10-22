#!/usr/bin/env python3
"""
Script de prueba final para validación completa de fechas
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


async def test_final_validation():
    """Prueba final de validación completa"""

    print("🔍 Prueba final de validación completa...")

    # Configurar cliente API
    config = TrackHSConfig.from_env()
    api_client = TrackHSApiClient(config)

    # Lista de valores inválidos a probar
    invalid_values = [
        ("null", "String 'null'"),
        ("None", "String 'None'"),
        ("", "String vacío"),
        ("   ", "String de espacios"),
        ("invalid-date", "Fecha inválida"),
        ("2024-13-01", "Fecha imposible"),
        ("2024-02-30", "Fecha imposible"),
    ]

    print("\n=== PROBANDO VALORES INVÁLIDOS ===")
    for value, description in invalid_values:
        print(f"\n--- {description}: '{value}' ---")
        try:
            result = await search_reservations_v2(
                api_client=api_client,
                page=1,
                size=3,
                arrival_start=value,
                arrival_end=value,
            )
            print(f"❌ ERROR: La validación no funcionó - debería haber fallado")
        except ValidationError as e:
            print(f"✅ Validación funcionó: {str(e)[:100]}...")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    # Lista de valores válidos a probar
    valid_values = [
        ("2024-03-01", "Fecha válida"),
        ("2024-12-31", "Fecha válida"),
        ("2024-01-15T10:00:00Z", "Fecha con tiempo"),
    ]

    print("\n=== PROBANDO VALORES VÁLIDOS ===")
    for value, description in valid_values:
        print(f"\n--- {description}: '{value}' ---")
        try:
            result = await search_reservations_v2(
                api_client=api_client,
                page=1,
                size=3,
                arrival_start=value,
                arrival_end=value,
            )
            print(
                f"✅ Funcionó correctamente: {result.get('total_items', 'N/A')} reservaciones"
            )
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    # Probar omitir parámetros
    print("\n=== PROBANDO OMITIR PARÁMETROS ===")
    try:
        result = await search_reservations_v2(
            api_client=api_client,
            page=1,
            size=3,
            # No incluir arrival_start ni arrival_end
        )
        print(
            f"✅ Omitir parámetros funcionó: {result.get('total_items', 'N/A')} reservaciones"
        )
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Cerrar cliente
    await api_client.close()

    print("\n🎉 ¡Prueba final completada!")


if __name__ == "__main__":
    asyncio.run(test_final_validation())
