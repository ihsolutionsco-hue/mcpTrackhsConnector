#!/usr/bin/env python3
"""
Script de testing mejorado para el endpoint de Units Collection
Solo usa parámetros válidos según la documentación oficial
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print(
        "WARNING: python-dotenv no instalado, usando variables de entorno del sistema"
    )

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.application.use_cases.search_units import SearchUnitsUseCase
from trackhs_mcp.domain.entities.units import SearchUnitsParams
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("test_units_improved.log")],
)

logger = logging.getLogger(__name__)


async def test_valid_parameters():
    """Prueba solo con parámetros válidos según la documentación"""

    print("TESTING MEJORADO - SOLO PARAMETROS VALIDOS")
    print("=" * 60)

    try:
        # 1. Verificar configuración
        print("\n1. VERIFICANDO CONFIGURACION...")
        config = TrackHSConfig.from_env()
        print(f"OK Base URL: {config.base_url}")
        print(f"OK Username: {config.username[:10]}...")
        print(f"OK Timeout: {config.timeout}")

        # 2. Crear cliente API
        print("\n2. CREANDO CLIENTE API...")
        async with TrackHSApiClient(config) as api_client:
            print("OK Cliente API creado exitosamente")

            # 3. Casos de prueba con parámetros válidos
            test_cases = [
                {
                    "name": "Búsqueda básica sin parámetros",
                    "params": {},
                    "description": "Prueba mínima sin parámetros",
                },
                {
                    "name": "Paginación básica",
                    "params": {"page": 1, "size": 5},
                    "description": "Paginación con valores por defecto",
                },
                {
                    "name": "Ordenamiento por nombre",
                    "params": {
                        "page": 1,
                        "size": 5,
                        "sort_column": "name",
                        "sort_direction": "asc",
                    },
                    "description": "Ordenamiento ascendente por nombre",
                },
                {
                    "name": "Filtro por estado activo",
                    "params": {"page": 1, "size": 5, "is_active": 1},
                    "description": "Solo unidades activas",
                },
                {
                    "name": "Filtro por habitaciones",
                    "params": {"page": 1, "size": 5, "bedrooms": 2},
                    "description": "Unidades con 2 habitaciones",
                },
                {
                    "name": "Filtro por baños",
                    "params": {"page": 1, "size": 5, "bathrooms": 2},
                    "description": "Unidades con 2 baños",
                },
                {
                    "name": "Filtro por mascotas",
                    "params": {"page": 1, "size": 5, "pets_friendly": 1},
                    "description": "Unidades amigables con mascotas",
                },
                {
                    "name": "Filtro por reservabilidad",
                    "params": {"page": 1, "size": 5, "is_bookable": 1},
                    "description": "Unidades reservables",
                },
                {
                    "name": "Filtro por eventos",
                    "params": {"page": 1, "size": 5, "events_allowed": 1},
                    "description": "Unidades que permiten eventos",
                },
                {
                    "name": "Filtro por accesibilidad",
                    "params": {"page": 1, "size": 5, "is_accessible": 1},
                    "description": "Unidades accesibles",
                },
                {
                    "name": "Filtro por estado de unidad",
                    "params": {"page": 1, "size": 5, "unit_status": "clean"},
                    "description": "Unidades en estado limpio",
                },
                {
                    "name": "Filtro por fechas",
                    "params": {
                        "page": 1,
                        "size": 5,
                        "arrival": "2024-01-01",
                        "departure": "2024-01-07",
                    },
                    "description": "Disponibilidad en rango de fechas",
                },
                {
                    "name": "Filtro por nodo",
                    "params": {"page": 1, "size": 5, "node_id": "1"},
                    "description": "Unidades de nodo específico",
                },
                {
                    "name": "Filtro por amenidad",
                    "params": {"page": 1, "size": 5, "amenity_id": "1"},
                    "description": "Unidades con amenidad específica",
                },
                {
                    "name": "Filtro por tipo de unidad",
                    "params": {"page": 1, "size": 5, "unit_type_id": "1"},
                    "description": "Unidades de tipo específico",
                },
                {
                    "name": "Filtro por búsqueda de texto",
                    "params": {"page": 1, "size": 5, "search": "villa"},
                    "description": "Búsqueda de texto en nombres",
                },
                {
                    "name": "Filtro por código de unidad",
                    "params": {"page": 1, "size": 5, "unit_code": "V001"},
                    "description": "Búsqueda por código de unidad",
                },
                {
                    "name": "Filtro por nombre corto",
                    "params": {"page": 1, "size": 5, "short_name": "Villa"},
                    "description": "Búsqueda por nombre corto",
                },
                {
                    "name": "Filtro por rango de habitaciones",
                    "params": {
                        "page": 1,
                        "size": 5,
                        "min_bedrooms": 2,
                        "max_bedrooms": 4,
                    },
                    "description": "Rango de habitaciones",
                },
                {
                    "name": "Filtro por rango de baños",
                    "params": {
                        "page": 1,
                        "size": 5,
                        "min_bathrooms": 1,
                        "max_bathrooms": 3,
                    },
                    "description": "Rango de baños",
                },
                {
                    "name": "Filtro combinado",
                    "params": {
                        "page": 1,
                        "size": 5,
                        "is_active": 1,
                        "is_bookable": 1,
                        "pets_friendly": 1,
                        "bedrooms": 2,
                        "bathrooms": 2,
                    },
                    "description": "Múltiples filtros combinados",
                },
            ]

            results = []
            successful_tests = 0

            for i, test_case in enumerate(test_cases, 1):
                print(f"\n3.{i} PROBANDO: {test_case['name']}")
                print(f"   Descripcion: {test_case['description']}")
                print(f"   Parametros: {test_case['params']}")

                try:
                    # Crear caso de uso
                    use_case = SearchUnitsUseCase(api_client)

                    # Crear parámetros de búsqueda
                    search_params = SearchUnitsParams(**test_case["params"])

                    # Ejecutar búsqueda
                    result = await use_case.execute(search_params)

                    # Verificar resultado
                    units = result.get("_embedded", {}).get("units", [])
                    total_items = result.get("total_items", 0)

                    print(f"   OK EXITO: {len(units)} unidades encontradas")
                    print(f"   INFO Total items: {total_items}")

                    # Si funciona, mostrar algunos datos
                    if units:
                        unit = units[0]
                        print(
                            f"   INFO Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                        )

                        # Verificar filtros booleanos
                        if "is_bookable" in test_case["params"]:
                            is_bookable = unit.get("isBookable", None)
                            print(f"   DEBUG isBookable en resultado: {is_bookable}")

                        if "events_allowed" in test_case["params"]:
                            events_allowed = unit.get("eventsAllowed", None)
                            print(
                                f"   DEBUG eventsAllowed en resultado: {events_allowed}"
                            )

                        if "pets_friendly" in test_case["params"]:
                            pets_friendly = unit.get("petsFriendly", None)
                            print(
                                f"   DEBUG petsFriendly en resultado: {pets_friendly}"
                            )

                    results.append(
                        {
                            "test": test_case["name"],
                            "status": "PASS",
                            "units_found": len(units),
                            "total_items": total_items,
                            "params": test_case["params"],
                        }
                    )
                    successful_tests += 1

                except Exception as e:
                    print(f"   ERROR: {str(e)}")
                    print(f"   DEBUG Tipo de error: {type(e).__name__}")

                    # Logging detallado del error
                    logger.error(f"Error en test case {test_case['name']}: {str(e)}")
                    logger.error(f"Error type: {type(e).__name__}")
                    logger.error(f"Error args: {getattr(e, 'args', 'N/A')}")

                    # Si es un error de API, mostrar detalles
                    if hasattr(e, "status_code"):
                        print(f"   INFO Status Code: {e.status_code}")
                        print(f"   INFO Endpoint: /pms/units")
                        print(f"   INFO Parametros enviados: {test_case['params']}")

                    results.append(
                        {
                            "test": test_case["name"],
                            "status": "FAIL",
                            "error": str(e),
                            "error_type": type(e).__name__,
                            "params": test_case["params"],
                        }
                    )

            # Resumen de resultados
            print(f"\nRESUMEN DE RESULTADOS")
            print("=" * 40)
            print(f"Total tests: {len(test_cases)}")
            print(f"Exitosos: {successful_tests}")
            print(f"Fallidos: {len(test_cases) - successful_tests}")
            print(f"Tasa de exito: {(successful_tests / len(test_cases)) * 100:.1f}%")

            # Análisis de problemas
            print(f"\nANALISIS DE PROBLEMAS")
            print("=" * 30)

            failed_tests = [r for r in results if r["status"] == "FAIL"]
            if failed_tests:
                print("Tests fallidos:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['error']}")
            else:
                print("OK Todos los tests pasaron exitosamente")

            # Verificar filtros booleanos
            print(f"\nVERIFICACION DE FILTROS BOOLEANOS")
            print("=" * 40)

            boolean_tests = [
                r
                for r in results
                if any(
                    param in r["params"]
                    for param in [
                        "is_bookable",
                        "events_allowed",
                        "pets_friendly",
                        "is_accessible",
                    ]
                )
            ]
            if boolean_tests:
                print("Tests con filtros booleanos:")
                for test in boolean_tests:
                    print(f"  - {test['test']}: {test['status']}")
            else:
                print("No se ejecutaron tests con filtros booleanos")

            return successful_tests > 0

    except Exception as e:
        print(f"\nERROR CRITICO: {str(e)}")
        logger.error(f"Error critico: {str(e)}")
        return False


async def main():
    """Función principal de testing mejorado"""

    print("INICIANDO TESTING MEJORADO DEL ENDPOINT DE UNITS")
    print("=" * 70)

    # Verificar variables de entorno
    print("\n0. VERIFICANDO VARIABLES DE ENTORNO...")
    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"ERROR Variables faltantes: {missing_vars}")
        return False

    print("OK Variables de entorno configuradas")

    # Ejecutar testing
    result = await test_valid_parameters()

    # Resumen final
    print("\nCONCLUSION")
    print("=" * 20)

    if result:
        print("OK El endpoint de units funciona con parametros validos")
        print("INFO Recomendaciones:")
        print("  1. Usar solo parametros documentados en la API")
        print("  2. Verificar filtros booleanos para logica invertida")
        print("  3. Implementar validacion de tipos de datos")
        print("  4. Usar filtros exactos en lugar de rangos cuando sea posible")
    else:
        print("ERROR El endpoint de units no funciona correctamente")
        print("INFO Posibles soluciones:")
        print("  1. Verificar configuracion de autenticacion")
        print("  2. Confirmar que el endpoint existe en la API")
        print("  3. Revisar permisos de acceso a Channel API")
        print("  4. Usar datos embebidos de reservaciones como alternativa")


if __name__ == "__main__":
    asyncio.run(main())
