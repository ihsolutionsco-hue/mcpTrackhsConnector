#!/usr/bin/env python3
"""
Test de debug para el endpoint de Units Collection
Captura logs detallados para identificar el problema del 400 Bad Request
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("units_debug.log")],
)

# Configurar variables de entorno para debug
os.environ["DEBUG"] = "true"


async def test_units_endpoint():
    """Test del endpoint de units con logging detallado"""

    try:
        # Importar después de configurar logging
        from trackhs_mcp.domain.value_objects.config import TrackHSConfig
        from trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )
        from trackhs_mcp.infrastructure.mcp.search_units import register_search_units

        print("Configurando cliente API...")

        # Crear configuración
        config = TrackHSConfig(
            base_url=os.getenv(
                "TRACKHS_BASE_URL", "https://api-integration-example.tracksandbox.io"
            ),
            username=os.getenv("TRACKHS_USERNAME"),
            password=os.getenv("TRACKHS_PASSWORD"),
            timeout=30,
        )

        print(f"Base URL: {config.base_url}")
        print(f"Username: {config.username}")
        print(f"Password: {'*' * len(config.password) if config.password else 'None'}")

        # Crear cliente API
        api_client = TrackHSApiClient(config)

        print("Iniciando pruebas del endpoint de Units...")

        # Test 1: Búsqueda sin parámetros
        print("\nTest 1: Busqueda sin parametros")
        try:
            # Simular la llamada directa al caso de uso
            from trackhs_mcp.application.use_cases.search_units import (
                SearchUnitsUseCase,
            )
            from trackhs_mcp.domain.entities.units import SearchUnitsParams

            use_case = SearchUnitsUseCase(api_client)
            params = SearchUnitsParams()

            print(f"Parametros enviados: {params.model_dump()}")
            result = await use_case.execute(params)
            print(f"Test 1 exitoso: {len(result.get('data', []))} unidades encontradas")

        except Exception as e:
            print(f"Test 1 fallo: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            if hasattr(e, "status_code"):
                print(f"Status code: {e.status_code}")

        # Test 2: Búsqueda con parámetros mínimos
        print("\nTest 2: Busqueda con parametros minimos (page=0, size=10)")
        try:
            params = SearchUnitsParams(page=0, size=10)
            print(f"Parametros enviados: {params.model_dump()}")
            result = await use_case.execute(params)
            print(f"Test 2 exitoso: {len(result.get('data', []))} unidades encontradas")

        except Exception as e:
            print(f"Test 2 fallo: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            if hasattr(e, "status_code"):
                print(f"Status code: {e.status_code}")

        # Test 3: Búsqueda con filtro is_active
        print("\nTest 3: Busqueda con filtro is_active=1")
        try:
            params = SearchUnitsParams(page=0, size=10, is_active=1)
            print(f"Parametros enviados: {params.model_dump()}")
            result = await use_case.execute(params)
            print(f"Test 3 exitoso: {len(result.get('data', []))} unidades encontradas")

        except Exception as e:
            print(f"Test 3 fallo: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            if hasattr(e, "status_code"):
                print(f"Status code: {e.status_code}")

        # Test 4: Verificar endpoint directamente
        print("\nTest 4: Verificar endpoint directamente")
        try:
            # Hacer petición directa al endpoint
            response = await api_client.get("/pms/units")
            print(f"Test 4 exitoso: Respuesta directa obtenida")
            print(f"Tipo de respuesta: {type(response)}")
            if isinstance(response, dict):
                print(f"Claves en respuesta: {list(response.keys())}")

        except Exception as e:
            print(f"Test 4 fallo: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            if hasattr(e, "status_code"):
                print(f"Status code: {e.status_code}")

        # Cerrar cliente
        await api_client.close()

    except Exception as e:
        print(f"Error general: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("Iniciando test de debug para Units Collection")
    print("Los logs detallados se guardaran en 'units_debug.log'")

    asyncio.run(test_units_endpoint())

    print("\nTest completado. Revisa 'units_debug.log' para mas detalles.")
