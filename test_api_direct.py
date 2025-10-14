#!/usr/bin/env python3
"""
Script de testing directo contra API TrackHS
Usa httpx directamente para evitar problemas de parsing
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import httpx

# Agregar el directorio src al PYTHONPATH
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from dotenv import load_dotenv

from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.utils.auth import TrackHSAuth


async def test_api_direct():
    """Probar conectividad directa con httpx"""
    print("TESTING DIRECTO CONTRA API TRACKHS")
    print("=" * 50)

    try:
        # Cargar variables de entorno
        load_dotenv()
        print("OK: Variables de entorno cargadas")

        # Crear configuración
        config = TrackHSConfig.from_env()
        print(f"OK: Configuracion cargada:")
        print(f"   URL: {config.base_url}")
        print(f"   Username: {config.username[:8]}***")
        print(f"   Timeout: {config.timeout}s")

        # Crear autenticación
        auth = TrackHSAuth(config)
        headers = auth.get_headers()
        print(f"OK: Headers de autenticacion: {list(headers.keys())}")

        # Crear cliente httpx directo
        async with httpx.AsyncClient(
            base_url=config.base_url, timeout=config.timeout or 30
        ) as client:
            print("OK: Cliente HTTP creado")

            # Test 1: Búsqueda básica de reservaciones
            print("\n1. Probando search_reservations_v2...")
            try:
                response = await client.get(
                    "/v2/pms/reservations",
                    headers=headers,
                    params={"page": 1, "size": 1},
                )
                print(f"   Status Code: {response.status_code}")
                print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   OK: JSON parseado exitosamente")
                        if "data" in data:
                            print(f"   Registros encontrados: {len(data['data'])}")
                            if data["data"]:
                                print(
                                    f"   Primer ID: {data['data'][0].get('id', 'N/A')}"
                                )
                        if "pagination" in data:
                            print(f"   Total: {data['pagination'].get('total', 'N/A')}")
                    except json.JSONDecodeError as e:
                        print(f"   ERROR: No se pudo parsear JSON: {e}")
                        print(
                            f"   Respuesta (primeros 200 chars): {response.text[:200]}"
                        )
                else:
                    print(f"   ERROR: Status {response.status_code}")
                    print(f"   Respuesta: {response.text[:200]}")

            except Exception as e:
                print(f"   ERROR: {e}")

            # Test 2: Obtener reservación específica
            print("\n2. Probando get_reservation_v2...")
            try:
                response = await client.get("/v2/pms/reservations/1", headers=headers)
                print(f"   Status Code: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   OK: JSON parseado exitosamente")
                        print(f"   ID: {data.get('id', 'N/A')}")
                        print(f"   Estado: {data.get('status', 'N/A')}")
                        print(f"   Nombre: {data.get('name', 'N/A')}")
                    except json.JSONDecodeError as e:
                        print(f"   ERROR: No se pudo parsear JSON: {e}")
                        print(f"   Respuesta: {response.text[:200]}")
                else:
                    print(f"   ERROR: Status {response.status_code}")
                    print(f"   Respuesta: {response.text[:200]}")

            except Exception as e:
                print(f"   ERROR: {e}")

            # Test 3: Obtener folio
            print("\n3. Probando get_folio...")
            try:
                response = await client.get("/pms/folios/1", headers=headers)
                print(f"   Status Code: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   OK: JSON parseado exitosamente")
                        print(f"   ID: {data.get('id', 'N/A')}")
                        print(f"   Estado: {data.get('status', 'N/A')}")
                        print(f"   Tipo: {data.get('type', 'N/A')}")
                    except json.JSONDecodeError as e:
                        print(f"   ERROR: No se pudo parsear JSON: {e}")
                        print(f"   Respuesta: {response.text[:200]}")
                else:
                    print(f"   ERROR: Status {response.status_code}")
                    print(f"   Respuesta: {response.text[:200]}")

            except Exception as e:
                print(f"   ERROR: {e}")

            # Test 4: Búsqueda de unidades (issue crítico)
            print("\n4. Probando search_units (issue critico)...")
            try:
                response = await client.get(
                    "/pms/units", headers=headers, params={"page": 1, "size": 1}
                )
                print(f"   Status Code: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   OK: JSON parseado exitosamente")
                        if "data" in data:
                            print(f"   Unidades encontradas: {len(data['data'])}")
                            if data["data"]:
                                print(
                                    f"   Primera unidad ID: {data['data'][0].get('id', 'N/A')}"
                                )
                                print(
                                    f"   Nombre: {data['data'][0].get('name', 'N/A')}"
                                )
                    except json.JSONDecodeError as e:
                        print(f"   ERROR: No se pudo parsear JSON: {e}")
                        print(f"   Respuesta: {response.text[:200]}")
                else:
                    print(f"   ERROR: Status {response.status_code}")
                    print(f"   Respuesta: {response.text[:200]}")

            except Exception as e:
                print(f"   ERROR: {e}")

        print("\nTESTING COMPLETADO")
        print("=" * 50)

    except Exception as e:
        print(f"ERROR general: {e}")
        return False

    return True


if __name__ == "__main__":
    asyncio.run(test_api_direct())
