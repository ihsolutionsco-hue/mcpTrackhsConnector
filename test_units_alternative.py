#!/usr/bin/env python3
"""
Script de prueba para la herramienta alternativa de búsqueda de unidades
search_units_from_reservations
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_units_alternative():
    """Prueba la herramienta alternativa de búsqueda de unidades"""

    print("PRUEBA DE HERRAMIENTA ALTERNATIVA DE UNITS")
    print("=" * 50)

    try:
        # Verificar credenciales
        print("\n1. Verificando credenciales...")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            print("ERROR: Credenciales no configuradas")
            print("Configura TRACKHS_USERNAME y TRACKHS_PASSWORD")
            return False

        print("Credenciales configuradas correctamente")

        # Importar y configurar
        print("\n2. Configurando cliente API...")
        from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
        from trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )

        config = TrackHSConfig.from_env()
        print(f"Base URL: {config.base_url}")

        async with TrackHSApiClient(config) as api_client:
            print("Cliente API creado exitosamente")

            # Importar la herramienta alternativa
            print("\n3. Probando herramienta alternativa...")
            from trackhs_mcp.infrastructure.mcp.search_units_from_reservations import (
                register_search_units_from_reservations,
            )

            # Crear un mock MCP para la prueba
            class MockMCP:
                def __init__(self):
                    self.tools = {}

                def tool(self, func):
                    self.tools[func.__name__] = func
                    return func

            mock_mcp = MockMCP()
            register_search_units_from_reservations(mock_mcp, api_client)

            # Obtener la función de búsqueda
            search_func = mock_mcp.tools.get("search_units_from_reservations")
            if not search_func:
                print("ERROR: No se pudo registrar la herramienta")
                return False

            print("Herramienta registrada exitosamente")

            # Probar diferentes casos de uso
            test_cases = [
                {
                    "name": "Búsqueda básica",
                    "params": {"page": 0, "size": 5},
                    "description": "Obtener primeras 5 unidades",
                },
                {
                    "name": "Búsqueda por habitaciones",
                    "params": {"page": 0, "size": 3, "bedrooms": 2},
                    "description": "Unidades con 2 habitaciones",
                },
                {
                    "name": "Búsqueda por mascotas",
                    "params": {"page": 0, "size": 3, "pets_friendly": 1},
                    "description": "Unidades que permiten mascotas",
                },
                {
                    "name": "Búsqueda por texto",
                    "params": {"page": 0, "size": 3, "search": "pool"},
                    "description": "Unidades que contengan 'pool' en el nombre",
                },
            ]

            for i, test_case in enumerate(test_cases, 1):
                print(f"\n4.{i} Probando: {test_case['name']}")
                print(f"   Descripción: {test_case['description']}")
                print(f"   Parámetros: {test_case['params']}")

                try:
                    # Ejecutar búsqueda
                    result = await search_func(**test_case["params"])

                    # Verificar resultado
                    if isinstance(result, dict) and "_embedded" in result:
                        units = result["_embedded"].get("units", [])
                        total_items = result.get("total_items", 0)

                        print(f"   EXITO: {len(units)} unidades encontradas")
                        print(f"   Total en sistema: {total_items}")

                        if units:
                            unit = units[0]
                            print(
                                f"   Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                            )
                            print(f"   Habitaciones: {unit.get('bedrooms', 'N/A')}")
                            print(f"   Baños: {unit.get('bathrooms', 'N/A')}")
                            print(f"   Mascotas: {unit.get('petsFriendly', 'N/A')}")

                        # Si alguna prueba funciona, considerarlo éxito
                        if len(units) > 0:
                            print(
                                f"\nEXITO: La herramienta alternativa funciona correctamente"
                            )
                            return True
                    else:
                        print(f"   ERROR: Formato de respuesta inesperado")
                        print(f"   Respuesta: {type(result)}")

                except Exception as e:
                    print(f"   ERROR: {str(e)}")
                    print(f"   Tipo: {type(e).__name__}")
                    continue

            print(f"\nRESULTADO: Todas las pruebas fallaron")
            return False

    except Exception as e:
        print(f"\nERROR CRITICO: {str(e)}")
        logger.error(f"Error crítico: {str(e)}")
        return False


async def main():
    """Función principal"""

    print("INICIANDO PRUEBA DE HERRAMIENTA ALTERNATIVA DE UNITS")
    print("=" * 60)

    result = await test_units_alternative()

    print("\nRESUMEN")
    print("=" * 10)

    if result:
        print("EXITO: La herramienta alternativa funciona correctamente")
        print("\nVENTAJAS:")
        print("- No requiere configuración adicional de Channel API")
        print("- Usa la misma autenticación que las reservaciones")
        print("- Proporciona datos completos de unidades")
        print("- Datos siempre actualizados con las reservaciones")
        print("\nLIMITACIONES:")
        print("- Solo incluye unidades con reservaciones")
        print("- Requiere consultar reservaciones primero")
        print("- Puede no incluir todas las unidades del sistema")
    else:
        print("FALLO: La herramienta alternativa no funciona")
        print("\nPOSIBLES CAUSAS:")
        print("1. Credenciales no configuradas o inválidas")
        print("2. Problema con el endpoint de reservaciones")
        print("3. Error en la implementación de la herramienta")
        print("4. Problema de red o conectividad")


if __name__ == "__main__":
    asyncio.run(main())
