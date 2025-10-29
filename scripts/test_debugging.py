#!/usr/bin/env python3
"""
Script de testing para validar las mejoras de debugging
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools.diagnose_api import DiagnoseAPITool
from tools.search_units import SearchUnitsTool
from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger


def test_debugging_features():
    """Test de las nuevas características de debugging"""
    logger = get_logger(__name__)

    # Configurar variables de entorno si no están configuradas
    if not os.getenv("TRACKHS_API_URL"):
        os.environ["TRACKHS_API_URL"] = "https://ihmvacations.trackhs.com"

    if not os.getenv("TRACKHS_USERNAME"):
        os.environ["TRACKHS_USERNAME"] = "test_user"

    if not os.getenv("TRACKHS_PASSWORD"):
        os.environ["TRACKHS_PASSWORD"] = "test_password"

    try:
        # Crear cliente API
        api_client = TrackHSAPIClient(
            base_url=os.getenv("TRACKHS_API_URL"),
            username=os.getenv("TRACKHS_USERNAME"),
            password=os.getenv("TRACKHS_PASSWORD"),
        )

        print("Testing Herramienta de Diagnostico...")

        # Test de herramienta de diagnóstico
        diagnose_tool = DiagnoseAPITool(api_client)

        # Test de conectividad
        print("\n1. Testing conectividad...")
        connectivity_result = diagnose_tool._test_connectivity()
        print(f"   Status: {connectivity_result['status']}")
        print(f"   Message: {connectivity_result['message']}")

        # Test de autenticación
        print("\n2. Testing autenticacion...")
        auth_result = diagnose_tool._test_authentication()
        print(f"   Status: {auth_result['status']}")
        print(f"   Message: {auth_result['message']}")

        # Test de endpoints
        print("\n3. Testing endpoints...")
        endpoints_result = diagnose_tool._test_endpoints()
        print(f"   Endpoints probados: {endpoints_result['endpoints_tested']}")
        print(f"   Exitosos: {endpoints_result['successful']}")
        print(f"   Fallidos: {endpoints_result['failed']}")

        # Test de estructura de datos
        print("\n4. Testing estructura de datos...")
        data_structure_result = diagnose_tool._test_data_structure()
        print(f"   Test cases: {data_structure_result['test_cases']}")
        print(f"   Exitosos: {data_structure_result['successful_tests']}")
        print(f"   Fallidos: {data_structure_result['failed_tests']}")

        print("\nTesting Busqueda de Unidades con Logging Mejorado...")

        # Test de búsqueda de unidades
        search_tool = SearchUnitsTool(api_client)

        # Test 1: Búsqueda básica
        print("\n5. Busqueda basica...")
        try:
            from schemas.unit import UnitSearchParams

            params1 = UnitSearchParams(page=1, size=5)
            result1 = search_tool._execute_logic(params1)
            print(f"   Unidades encontradas: {len(result1.get('units', []))}")
            print(f"   Total items: {result1.get('total_items', 0)}")
        except Exception as e:
            print(f"   Error: {str(e)}")

        # Test 2: Búsqueda con filtros
        print("\n6. Busqueda con filtros...")
        try:
            from schemas.unit import UnitSearchParams

            params2 = UnitSearchParams(page=1, size=5, is_active=True, bedrooms=2)
            result2 = search_tool._execute_logic(params2)
            print(f"   Unidades encontradas: {len(result2.get('units', []))}")
            print(f"   Total items: {result2.get('total_items', 0)}")
        except Exception as e:
            print(f"   Error: {str(e)}")

        print("\n[SUCCESS] Testing completado!")

        # Cerrar cliente
        api_client.close()

    except Exception as e:
        logger.error(f"Error en testing: {str(e)}")
        print(f"[ERROR] Error: {str(e)}")


def test_logging_structure():
    """Test de la estructura de logging"""
    print("\nTesting Estructura de Logging...")

    logger = get_logger(__name__)

    # Test de diferentes tipos de logs
    logger.info("Test de log INFO", extra={"test_type": "info", "value": 123})
    logger.warning("Test de log WARNING", extra={"test_type": "warning", "value": 456})
    logger.error("Test de log ERROR", extra={"test_type": "error", "value": 789})

    print("   Logs de prueba enviados al sistema de logging")


if __name__ == "__main__":
    print("Iniciando Testing de Caracteristicas de Debugging")
    print("=" * 60)

    test_logging_structure()
    test_debugging_features()

    print("\n" + "=" * 60)
    print("[SUCCESS] Testing completado!")
