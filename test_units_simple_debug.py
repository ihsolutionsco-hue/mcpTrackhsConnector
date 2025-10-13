#!/usr/bin/env python3
"""
Script de diagnóstico simple para el endpoint de Units Collection
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_units_endpoint():
    """Prueba simple del endpoint de units"""

    print("DIAGNOSTICO DEL ENDPOINT DE UNITS")
    print("=" * 40)

    try:
        # 1. Verificar configuración
        print("\n1. Verificando configuracion...")
        config = TrackHSConfig.from_env()
        print(f"Base URL: {config.base_url}")
        print(f"Username: {config.username[:10]}...")

        # 2. Crear cliente API
        print("\n2. Creando cliente API...")
        async with TrackHSApiClient(config) as api_client:
            print("Cliente API creado exitosamente")

            # 3. Probar endpoint básico
            print("\n3. Probando endpoint /pms/units...")
            try:
                # Prueba sin parámetros
                response = await api_client.get("/pms/units")
                print("EXITO: Endpoint responde correctamente")
                print(f"Tipo de respuesta: {type(response)}")
                if isinstance(response, dict):
                    print(f"Claves principales: {list(response.keys())}")
                    if "_embedded" in response:
                        units = response["_embedded"].get("units", [])
                        print(f"Unidades encontradas: {len(units)}")
                        if units:
                            unit = units[0]
                            print(
                                f"Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                            )
                return True

            except Exception as e:
                print(f"ERROR: {str(e)}")
                print(f"Tipo de error: {type(e).__name__}")

                if hasattr(e, "status_code"):
                    print(f"Status Code: {e.status_code}")
                    print(f"Endpoint: /pms/units")

                # Probar otros endpoints posibles
                print("\n4. Probando otros endpoints...")
                other_endpoints = [
                    "/api/pms/units",
                    "/v1/pms/units",
                    "/v2/pms/units",
                    "/units",
                    "/api/units",
                ]

                for endpoint in other_endpoints:
                    try:
                        print(f"Probando: {endpoint}")
                        response = await api_client.get(endpoint)
                        print(f"EXITO: {endpoint} responde correctamente")
                        return True
                    except Exception as e2:
                        print(f"ERROR en {endpoint}: {str(e2)}")
                        continue

                return False

    except Exception as e:
        print(f"ERROR CRITICO: {str(e)}")
        return False


async def main():
    """Función principal"""

    print("INICIANDO DIAGNOSTICO DEL ENDPOINT DE UNITS")
    print("=" * 50)

    # Verificar variables de entorno
    print("\nVerificando variables de entorno...")
    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"ERROR: Variables faltantes: {missing_vars}")
        return False

    print("Variables de entorno configuradas correctamente")

    # Ejecutar prueba
    result = await test_units_endpoint()

    # Resumen
    print("\nRESUMEN")
    print("=" * 10)

    if result:
        print("EXITO: El endpoint de units funciona correctamente")
    else:
        print("FALLO: El endpoint de units no funciona")
        print("\nPosibles causas:")
        print("1. El endpoint /pms/units no existe en esta API")
        print("2. Requiere autenticacion diferente (HMAC vs Basic)")
        print("3. La URL base no es correcta para Channel API")
        print("4. Las credenciales no tienen permisos para Channel API")
        print("5. El endpoint esta en una API diferente")
        print("\nAlternativa: Usar datos de unidades embebidos en reservaciones")


if __name__ == "__main__":
    asyncio.run(main())
