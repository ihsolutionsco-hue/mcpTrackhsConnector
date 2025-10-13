#!/usr/bin/env python3
"""
Script de diagnóstico detallado para el endpoint de Units Collection
Analiza el problema del 400 Bad Request en search_units
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.application.use_cases.search_units import SearchUnitsUseCase
from trackhs_mcp.domain.entities.units import SearchUnitsParams
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("units_debug_detailed.log")],
)

logger = logging.getLogger(__name__)


async def test_units_endpoint_detailed():
    """Prueba detallada del endpoint de units con diferentes configuraciones"""

    print("🔍 DIAGNÓSTICO DETALLADO DEL ENDPOINT DE UNITS")
    print("=" * 60)

    try:
        # 1. Verificar configuración
        print("\n1️⃣ VERIFICANDO CONFIGURACIÓN...")
        config = TrackHSConfig.from_env()
        print(f"✅ Base URL: {config.base_url}")
        print(f"✅ Username: {config.username[:10]}...")
        print(f"✅ Timeout: {config.timeout}")

        # 2. Crear cliente API
        print("\n2️⃣ CREANDO CLIENTE API...")
        async with TrackHSApiClient(config) as api_client:
            print("✅ Cliente API creado exitosamente")

            # 3. Probar diferentes configuraciones del endpoint
            test_cases = [
                {
                    "name": "Búsqueda básica sin parámetros",
                    "params": {},
                    "description": "Prueba mínima sin parámetros",
                },
                {
                    "name": "Solo paginación básica",
                    "params": {"page": 0, "size": 1},
                    "description": "Paginación mínima",
                },
                {
                    "name": "Con parámetros de ordenamiento",
                    "params": {
                        "page": 0,
                        "size": 1,
                        "sortColumn": "name",
                        "sortDirection": "asc",
                    },
                    "description": "Incluyendo ordenamiento",
                },
                {
                    "name": "Con filtro de estado activo",
                    "params": {"page": 0, "size": 1, "isActive": 1},
                    "description": "Filtro de estado activo",
                },
                {
                    "name": "Con parámetros de habitaciones",
                    "params": {"page": 0, "size": 1, "bedrooms": 2},
                    "description": "Filtro por habitaciones",
                },
            ]

            for i, test_case in enumerate(test_cases, 1):
                print(f"\n3️⃣.{i} PROBANDO: {test_case['name']}")
                print(f"   Descripción: {test_case['description']}")
                print(f"   Parámetros: {test_case['params']}")

                try:
                    # Crear caso de uso
                    use_case = SearchUnitsUseCase(api_client)

                    # Crear parámetros de búsqueda
                    search_params = SearchUnitsParams(**test_case["params"])

                    # Ejecutar búsqueda
                    result = await use_case.execute(search_params)

                    print(
                        f"   ✅ ÉXITO: {len(result.get('_embedded', {}).get('units', []))} unidades encontradas"
                    )
                    print(f"   📊 Total items: {result.get('total_items', 'N/A')}")

                    # Si funciona, mostrar algunos datos
                    if result.get("_embedded", {}).get("units"):
                        unit = result["_embedded"]["units"][0]
                        print(
                            f"   🏠 Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                        )

                    # Si alguna prueba funciona, salir del bucle
                    if result.get("_embedded", {}).get("units"):
                        print(
                            f"\n🎉 ¡ÉXITO! El endpoint funciona con la configuración: {test_case['name']}"
                        )
                        return True

                except Exception as e:
                    print(f"   ❌ ERROR: {str(e)}")
                    print(f"   🔍 Tipo de error: {type(e).__name__}")

                    # Logging detallado del error
                    logger.error(f"Error en test case {test_case['name']}: {str(e)}")
                    logger.error(f"Error type: {type(e).__name__}")
                    logger.error(f"Error args: {getattr(e, 'args', 'N/A')}")

                    # Si es un error de API, mostrar detalles
                    if hasattr(e, "status_code"):
                        print(f"   📡 Status Code: {e.status_code}")
                        print(f"   🔗 Endpoint: /pms/units")
                        print(f"   📋 Parámetros enviados: {test_case['params']}")

                    continue

            print(f"\n❌ TODAS LAS PRUEBAS FALLARON")
            print("🔍 Posibles causas:")
            print("   1. El endpoint /pms/units no existe en esta API")
            print("   2. Requiere autenticación diferente (HMAC vs Basic)")
            print("   3. La URL base no es correcta para Channel API")
            print("   4. Las credenciales no tienen permisos para Channel API")
            print("   5. El endpoint está en una API diferente")

            return False

    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {str(e)}")
        logger.error(f"Error crítico: {str(e)}")
        return False


async def test_direct_api_call():
    """Prueba directa de la API sin usar el caso de uso"""

    print("\n🔧 PRUEBA DIRECTA DE LA API")
    print("=" * 40)

    try:
        config = TrackHSConfig.from_env()

        async with TrackHSApiClient(config) as api_client:
            # Probar diferentes endpoints
            endpoints_to_test = [
                "/pms/units",
                "/api/pms/units",
                "/v1/pms/units",
                "/v2/pms/units",
                "/units",
                "/api/units",
            ]

            for endpoint in endpoints_to_test:
                print(f"\n🔗 Probando endpoint: {endpoint}")
                try:
                    # Prueba básica sin parámetros
                    response = await api_client.get(endpoint)
                    print(f"   ✅ ÉXITO: {endpoint} responde correctamente")
                    print(f"   📊 Tipo de respuesta: {type(response)}")
                    if isinstance(response, dict):
                        print(f"   📋 Claves principales: {list(response.keys())}")
                    return True
                except Exception as e:
                    print(f"   ❌ ERROR: {str(e)}")
                    if hasattr(e, "status_code"):
                        print(f"   📡 Status: {e.status_code}")
                    continue

            print("\n❌ Ningún endpoint de units funciona")
            return False

    except Exception as e:
        print(f"💥 Error en prueba directa: {str(e)}")
        return False


async def test_authentication_methods():
    """Prueba diferentes métodos de autenticación"""

    print("\n🔐 PRUEBA DE MÉTODOS DE AUTENTICACIÓN")
    print("=" * 50)

    try:
        config = TrackHSConfig.from_env()

        # Verificar headers de autenticación
        from trackhs_mcp.infrastructure.utils.auth import TrackHSAuth

        auth = TrackHSAuth(config)
        headers = auth.get_headers()

        print(f"🔑 Headers de autenticación:")
        for key, value in headers.items():
            if key == "Authorization":
                print(f"   {key}: {value[:20]}...")
            else:
                print(f"   {key}: {value}")

        # Verificar si es Basic Auth
        auth_header = headers.get("Authorization", "")
        if auth_header.startswith("Basic "):
            print("✅ Usando Basic Authentication")
        else:
            print("❓ Método de autenticación no reconocido")

        return True

    except Exception as e:
        print(f"💥 Error verificando autenticación: {str(e)}")
        return False


async def main():
    """Función principal de diagnóstico"""

    print("🚀 INICIANDO DIAGNÓSTICO COMPLETO DEL ENDPOINT DE UNITS")
    print("=" * 70)

    # Verificar variables de entorno
    print("\n0️⃣ VERIFICANDO VARIABLES DE ENTORNO...")
    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Variables faltantes: {missing_vars}")
        return False

    print("✅ Variables de entorno configuradas")

    # Ejecutar pruebas
    results = []

    # 1. Verificar autenticación
    auth_result = await test_authentication_methods()
    results.append(("Autenticación", auth_result))

    # 2. Prueba directa de API
    direct_result = await test_direct_api_call()
    results.append(("Prueba directa API", direct_result))

    # 3. Prueba con casos de uso
    usecase_result = await test_units_endpoint_detailed()
    results.append(("Caso de uso", usecase_result))

    # Resumen de resultados
    print("\n📊 RESUMEN DE RESULTADOS")
    print("=" * 30)

    for test_name, result in results:
        status = "✅ ÉXITO" if result else "❌ FALLO"
        print(f"{test_name}: {status}")

    # Recomendaciones
    print("\n💡 RECOMENDACIONES")
    print("=" * 20)

    if not any(result for _, result in results):
        print("🔧 El endpoint de units no está funcionando. Posibles soluciones:")
        print("   1. Verificar que la URL base incluya el dominio correcto")
        print("   2. Confirmar que las credenciales tienen acceso a Channel API")
        print("   3. Revisar si se requiere autenticación HMAC en lugar de Basic")
        print("   4. Verificar que el endpoint existe en la versión de API actual")
        print(
            "   5. Usar datos de unidades embebidos en reservaciones como alternativa"
        )
    else:
        print("🎉 Al menos una prueba funcionó. Revisar logs para detalles.")


if __name__ == "__main__":
    asyncio.run(main())
