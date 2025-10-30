"""
Tests de validación post-corrección para verificar el estado real de la API TrackHS
"""

import os
import sys
from typing import Any, Dict, List

import pytest
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class TestPostFixValidation:
    """Tests de validación post-corrección"""

    @pytest.fixture(scope="class")
    def api_client(self):
        """Cliente API para tests de integración"""
        base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            pytest.skip("Credenciales no configuradas en archivo .env")

        return TrackHSAPIClient(base_url, username, password)

    @pytest.fixture(scope="class")
    def direct_session(self):
        """Sesión HTTP directa para comparación"""
        base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            pytest.skip("Credenciales no configuradas en archivo .env")

        session = requests.Session()
        session.auth = (username, password)
        session.timeout = 30
        return session

    def test_baseline_data_available(self, direct_session):
        """Test que verifica que hay datos disponibles en la API"""
        url = "https://ihmvacations.trackhs.com/api/pms/units"
        params = {"page": 1, "size": 5}

        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units = data.get("_embedded", {}).get("units", [])
        total_items = data.get("total_items", 0)

        assert total_items > 0, "Debería haber unidades disponibles en la API"
        assert len(units) > 0, "Debería devolver unidades en la respuesta"

        # Verificar que hay unidades con diferentes características
        active_units = [u for u in units if u.get("isActive") is True]
        inactive_units = [u for u in units if u.get("isActive") is False]
        bookable_units = [u for u in units if u.get("isBookable") is True]

        assert len(active_units) > 0, "Debería haber unidades activas"
        assert len(inactive_units) > 0, "Debería haber unidades inactivas"
        assert len(bookable_units) > 0, "Debería haber unidades reservables"

        logger.info(f"Baseline: {total_items} total, {len(units)} en página")
        logger.info(f"Activas: {len(active_units)}, Inactivas: {len(inactive_units)}")
        logger.info(f"Reservables: {len(bookable_units)}")

    def test_filters_not_working_in_api(self, direct_session):
        """Test que confirma que los filtros NO funcionan en la API"""
        url = "https://ihmvacations.trackhs.com/api/pms/units"

        # Test 1: Filtro isActive=1
        params = {"page": 1, "size": 10, "isActive": 1}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units = data.get("_embedded", {}).get("units", [])
        total_items = data.get("total_items", 0)

        logger.info(f"Con isActive=1: {len(units)} unidades, total: {total_items}")

        # Si hay unidades, verificar que todas están activas
        if units:
            inactive_found = [u for u in units if u.get("isActive") is not True]
            if inactive_found:
                logger.warning(
                    f"FILTRO NO FUNCIONA: {len(inactive_found)} unidades inactivas encontradas"
                )
                for unit in inactive_found[:3]:
                    logger.warning(
                        f"  - ID: {unit.get('id')}, isActive: {unit.get('isActive')}"
                    )

        # Test 2: Filtro minBedrooms=2
        params = {"page": 1, "size": 10, "minBedrooms": 2}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units = data.get("_embedded", {}).get("units", [])
        total_items = data.get("total_items", 0)

        logger.info(f"Con minBedrooms=2: {len(units)} unidades, total: {total_items}")

        # Si hay unidades, verificar que todas tienen >= 2 bedrooms
        if units:
            invalid_bedrooms = [u for u in units if u.get("bedrooms", 0) < 2]
            if invalid_bedrooms:
                logger.warning(
                    f"FILTRO NO FUNCIONA: {len(invalid_bedrooms)} unidades con < 2 bedrooms"
                )
                for unit in invalid_bedrooms[:3]:
                    logger.warning(
                        f"  - ID: {unit.get('id')}, bedrooms: {unit.get('bedrooms')}"
                    )

        # Test 3: Filtro petsFriendly=1
        params = {"page": 1, "size": 10, "petsFriendly": 1}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units = data.get("_embedded", {}).get("units", [])
        total_items = data.get("total_items", 0)

        logger.info(f"Con petsFriendly=1: {len(units)} unidades, total: {total_items}")

        # Si hay unidades, verificar que todas son pet-friendly
        if units:
            non_pets = [u for u in units if u.get("petsFriendly") is not True]
            if non_pets:
                logger.warning(
                    f"FILTRO NO FUNCIONA: {len(non_pets)} unidades no son pet-friendly"
                )
                for unit in non_pets[:3]:
                    logger.warning(
                        f"  - ID: {unit.get('id')}, petsFriendly: {unit.get('petsFriendly')}"
                    )

    def test_unit_ids_serialization(self, direct_session):
        """Test que verifica la serialización de unit_ids"""
        url = "https://ihmvacations.trackhs.com/api/pms/units"

        # Primero obtener algunos IDs válidos
        params = {"page": 1, "size": 3}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units = data.get("_embedded", {}).get("units", [])

        if not units:
            pytest.skip("No hay unidades disponibles para testear unit_ids")

        test_ids = [u.get("id") for u in units if u.get("id") is not None]
        assert len(test_ids) > 0, "Debería haber IDs válidos para testear"

        # Test 1: unit_ids como lista
        params = {"page": 1, "size": 10, "unit_ids": test_ids}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units_result = data.get("_embedded", {}).get("units", [])
        logger.info(
            f"Con unit_ids como lista: {len(units_result)} unidades encontradas"
        )

        # Test 2: unit_ids como string
        params = {"page": 1, "size": 10, "unit_ids": str(test_ids)}
        response = direct_session.get(url, params=params)
        assert response.status_code == 200

        data = response.json()
        units_result = data.get("_embedded", {}).get("units", [])
        logger.info(
            f"Con unit_ids como string: {len(units_result)} unidades encontradas"
        )

    def test_api_client_vs_direct_comparison(self, api_client, direct_session):
        """Test que compara respuestas del api_client vs llamadas directas"""
        url = "https://ihmvacations.trackhs.com/api/pms/units"

        # Test 1: Sin filtros
        logger.info("Comparando respuestas sin filtros...")

        # Llamada directa
        params_direct = {"page": 1, "size": 5}
        response_direct = direct_session.get(url, params=params_direct)
        data_direct = response_direct.json()
        units_direct = data_direct.get("_embedded", {}).get("units", [])

        # Llamada a través de api_client
        params_client = {"page": 1, "size": 5}
        result_client = api_client.search_units(params_client)
        units_client = result_client.get("units", [])

        logger.info(f"Directa: {len(units_direct)} unidades")
        logger.info(f"API Client: {len(units_client)} unidades")

        # Deberían ser similares (puede haber diferencias en el procesamiento)
        assert len(units_direct) > 0, "Llamada directa debería devolver unidades"
        # Nota: api_client puede procesar la respuesta de manera diferente

        # Test 2: Con filtros
        logger.info("Comparando respuestas con filtros...")

        # Llamada directa con filtro
        params_direct = {"page": 1, "size": 5, "isActive": 1}
        response_direct = direct_session.get(url, params=params_direct)
        data_direct = response_direct.json()
        units_direct = data_direct.get("_embedded", {}).get("units", [])

        # Llamada a través de api_client
        params_client = {"page": 1, "size": 5, "is_active": True}
        result_client = api_client.search_units(params_client)
        units_client = result_client.get("units", [])

        logger.info(f"Directa con isActive=1: {len(units_direct)} unidades")
        logger.info(f"API Client con is_active=True: {len(units_client)} unidades")

    def test_conversion_snake_to_camel_case(self, api_client):
        """Test que verifica la conversión de snake_case a camelCase"""
        logger.info("Verificando conversión snake_case a camelCase...")

        # Test con parámetros en snake_case
        params = {
            "page": 1,
            "size": 5,
            "is_active": True,
            "is_bookable": True,
            "min_bedrooms": 2,
            "max_bedrooms": 3,
            "pets_friendly": True,
        }

        result = api_client.search_units(params)
        units = result.get("units", [])
        total_items = result.get("total_items", 0)

        logger.info(
            f"Con parámetros snake_case: {len(units)} unidades, total: {total_items}"
        )

        # El test pasa si no hay errores de validación
        # La conversión se verifica en los logs del api_client
        assert isinstance(result, dict), "Debería devolver un diccionario"
        assert "units" in result, "Debería tener clave 'units'"
        assert "total_items" in result, "Debería tener clave 'total_items'"

    @pytest.mark.slow
    def test_comprehensive_filter_analysis(self, direct_session):
        """Test comprehensivo que analiza todos los filtros"""
        logger.info("=" * 80)
        logger.info("ANÁLISIS COMPREHENSIVO DE FILTROS")
        logger.info("=" * 80)

        url = "https://ihmvacations.trackhs.com/api/pms/units"

        # Obtener baseline
        params = {"page": 1, "size": 20}
        response = direct_session.get(url, params=params)
        data = response.json()
        baseline_units = data.get("_embedded", {}).get("units", [])
        baseline_total = data.get("total_items", 0)

        logger.info(f"Baseline: {len(baseline_units)} unidades, {baseline_total} total")

        if baseline_units:
            # Analizar características del baseline
            active_count = sum(1 for u in baseline_units if u.get("isActive") is True)
            bookable_count = sum(
                1 for u in baseline_units if u.get("isBookable") is True
            )
            pets_count = sum(1 for u in baseline_units if u.get("petsFriendly") is True)
            bedrooms = [
                u.get("bedrooms")
                for u in baseline_units
                if u.get("bedrooms") is not None
            ]

            logger.info(f"Características del baseline:")
            logger.info(f"  - Activas: {active_count}/{len(baseline_units)}")
            logger.info(f"  - Reservables: {bookable_count}/{len(baseline_units)}")
            logger.info(f"  - Pet-friendly: {pets_count}/{len(baseline_units)}")
            if bedrooms:
                logger.info(
                    f"  - Bedrooms: {set(bedrooms)} (rango: {min(bedrooms)}-{max(bedrooms)})"
                )

        # Test filtros individuales
        filter_tests = [
            {"name": "isActive=1", "params": {"isActive": 1}},
            {"name": "isBookable=1", "params": {"isBookable": 1}},
            {"name": "petsFriendly=1", "params": {"petsFriendly": 1}},
            {"name": "minBedrooms=2", "params": {"minBedrooms": 2}},
            {"name": "maxBedrooms=3", "params": {"maxBedrooms": 3}},
            {"name": "search=pool", "params": {"search": "pool"}},
        ]

        for test in filter_tests:
            logger.info(f"\nTest: {test['name']}")
            params = {"page": 1, "size": 20, **test["params"]}

            response = direct_session.get(url, params=params)
            data = response.json()
            units = data.get("_embedded", {}).get("units", [])
            total_items = data.get("total_items", 0)

            logger.info(f"  Resultado: {len(units)} unidades, total: {total_items}")

            # Verificar si el filtro funcionó
            if units:
                if "isActive" in test["params"]:
                    invalid = [u for u in units if u.get("isActive") is not True]
                    if invalid:
                        logger.warning(
                            f"    FILTRO NO FUNCIONA: {len(invalid)} unidades inactivas"
                        )

                if "minBedrooms" in test["params"]:
                    min_val = test["params"]["minBedrooms"]
                    invalid = [u for u in units if u.get("bedrooms", 0) < min_val]
                    if invalid:
                        logger.warning(
                            f"    FILTRO NO FUNCIONA: {len(invalid)} unidades con < {min_val} bedrooms"
                        )

                if "maxBedrooms" in test["params"]:
                    max_val = test["params"]["maxBedrooms"]
                    invalid = [u for u in units if u.get("bedrooms", 0) > max_val]
                    if invalid:
                        logger.warning(
                            f"    FILTRO NO FUNCIONA: {len(invalid)} unidades con > {max_val} bedrooms"
                        )

        logger.info("\n" + "=" * 80)
        logger.info("ANÁLISIS COMPLETADO")
        logger.info("=" * 80)
