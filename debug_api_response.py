#!/usr/bin/env python3
"""
Script para debuggear la respuesta de la API de Units
"""

import asyncio
import json
import os
import sys

# Cargar variables de entorno
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv no instalado")

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def debug_api_response():
    """Debuggear la respuesta de la API"""

    print("DEBUGGING API RESPONSE")
    print("=" * 30)

    try:
        # Configurar cliente
        config = TrackHSConfig.from_env()

        async with TrackHSApiClient(config) as api_client:
            print("1. Cliente API creado exitosamente")

            # Hacer petición simple
            print("2. Haciendo petición a /pms/units...")
            response = await api_client.get("/pms/units", params={"page": 1, "size": 1})

            print(f"3. Tipo de respuesta: {type(response)}")
            print(f"4. Contenido de respuesta: {response}")

            # Si es string, intentar parsear JSON
            if isinstance(response, str):
                print("5. Respuesta es string, intentando parsear JSON...")
                try:
                    json_data = json.loads(response)
                    print(f"6. JSON parseado exitosamente: {type(json_data)}")
                    print(
                        f"7. Claves principales: {list(json_data.keys()) if isinstance(json_data, dict) else 'No es dict'}"
                    )

                    if isinstance(json_data, dict) and "_embedded" in json_data:
                        units = json_data["_embedded"].get("units", [])
                        print(f"8. Unidades encontradas: {len(units)}")
                        if units:
                            unit = units[0]
                            print(
                                f"9. Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                            )

                            # Verificar filtros booleanos
                            print("10. Verificando filtros booleanos:")
                            print(f"    - isBookable: {unit.get('isBookable', 'N/A')}")
                            print(
                                f"    - eventsAllowed: {unit.get('eventsAllowed', 'N/A')}"
                            )
                            print(
                                f"    - petsFriendly: {unit.get('petsFriendly', 'N/A')}"
                            )
                            print(
                                f"    - isAccessible: {unit.get('isAccessible', 'N/A')}"
                            )
                            print(f"    - isActive: {unit.get('isActive', 'N/A')}")

                except json.JSONDecodeError as e:
                    print(f"6. ERROR: No se pudo parsear JSON: {e}")
                    print(f"7. Primeros 500 caracteres: {response[:500]}")
            else:
                print("5. Respuesta no es string, es dict")
                print(
                    f"6. Claves principales: {list(response.keys()) if isinstance(response, dict) else 'No es dict'}"
                )

    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Tipo de error: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(debug_api_response())
