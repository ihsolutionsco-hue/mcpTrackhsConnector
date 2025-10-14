#!/usr/bin/env python3
"""
Script de testing real contra API TrackHS
Ejecuta pruebas de conectividad y funcionalidad
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio src al PYTHONPATH
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from dotenv import load_dotenv

from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def test_api_connectivity():
    """Probar conectividad básica con la API"""
    print("🔍 TESTING REAL CONTRA API TRACKHS")
    print("=" * 50)

    try:
        # Cargar variables de entorno
        load_dotenv()
        print("✅ Variables de entorno cargadas")

        # Crear configuración
        config = TrackHSConfig.from_env()
        print(f"✅ Configuración cargada:")
        print(f"   URL: {config.base_url}")
        print(f"   Username: {config.username[:8]}***")
        print(f"   Timeout: {config.timeout}s")

        # Crear cliente API
        api_client = TrackHSApiClient(config)
        print("✅ Cliente API creado")

        # Probar conectividad básica
        print("\n🧪 PROBANDO CONECTIVIDAD...")

        # Test 1: Búsqueda básica de reservaciones
        print("\n1️⃣ Probando search_reservations_v2...")
        try:
            response = await api_client.get(
                "/v2/pms/reservations", params={"page": 1, "size": 1}
            )
            print(f"✅ Respuesta exitosa: {response.get('status_code', 'N/A')}")
            if "data" in response:
                print(f"   Datos recibidos: {len(response['data'])} registros")
                if response["data"]:
                    print(
                        f"   Primer registro ID: {response['data'][0].get('id', 'N/A')}"
                    )
        except Exception as e:
            print(f"❌ Error en search_reservations_v2: {e}")

        # Test 2: Obtener reservación específica
        print("\n2️⃣ Probando get_reservation_v2...")
        try:
            # Usar ID 1 como prueba
            response = await api_client.get("/v2/pms/reservations/1")
            print(f"✅ Respuesta exitosa: {response.get('status_code', 'N/A')}")
            if "id" in response:
                print(f"   Reservación ID: {response.get('id')}")
                print(f"   Estado: {response.get('status', 'N/A')}")
        except Exception as e:
            print(f"❌ Error en get_reservation_v2: {e}")

        # Test 3: Obtener folio
        print("\n3️⃣ Probando get_folio...")
        try:
            response = await api_client.get("/pms/folios/1")
            print(f"✅ Respuesta exitosa: {response.get('status_code', 'N/A')}")
            if "id" in response:
                print(f"   Folio ID: {response.get('id')}")
                print(f"   Estado: {response.get('status', 'N/A')}")
        except Exception as e:
            print(f"❌ Error en get_folio: {e}")

        # Test 4: Búsqueda de unidades (issue crítico)
        print("\n4️⃣ Probando search_units (issue crítico)...")
        try:
            response = await api_client.get("/pms/units", params={"page": 1, "size": 1})
            print(f"✅ Respuesta exitosa: {response.get('status_code', 'N/A')}")
            if "data" in response:
                print(f"   Unidades encontradas: {len(response['data'])}")
                if response["data"]:
                    print(
                        f"   Primera unidad ID: {response['data'][0].get('id', 'N/A')}"
                    )
        except Exception as e:
            print(f"❌ Error en search_units: {e}")

        print("\n🎉 TESTING COMPLETADO")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

    return True


if __name__ == "__main__":
    asyncio.run(test_api_connectivity())
