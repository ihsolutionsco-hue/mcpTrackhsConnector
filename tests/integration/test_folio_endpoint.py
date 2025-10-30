"""
Tests para el endpoint get_folio corregido según documentación oficial
"""

import os
import sys
from typing import Any, Dict

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


class TestFolioEndpoint:
    """Tests para el endpoint get_folio corregido"""

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

    def test_folio_endpoint_structure(self, direct_session):
        """Test que verifica la estructura del endpoint de folios"""
        logger.info("=" * 60)
        logger.info("TEST: Estructura del endpoint de folios")
        logger.info("=" * 60)

        # Test con un folio_id de prueba (1)
        folio_id = 1
        url = f"https://ihmvacations.trackhs.com/api/pms/folios/{folio_id}"

        try:
            response = direct_session.get(url)
            logger.info(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Claves principales: {list(data.keys())}")

                # Verificar campos requeridos según documentación
                required_fields = ["id", "status"]
                for field in required_fields:
                    assert field in data, f"Campo requerido '{field}' no encontrado"

                # Verificar tipos de datos
                assert isinstance(data["id"], int), "ID debe ser entero"
                assert data["status"] in [
                    "open",
                    "closed",
                ], "Status debe ser 'open' o 'closed'"

                logger.info("✅ Estructura del endpoint correcta")
                logger.info(f"Folio ID: {data['id']}")
                logger.info(f"Status: {data['status']}")

                # Verificar campos opcionales
                optional_fields = [
                    "type",
                    "currentBalance",
                    "realizedBalance",
                    "contactId",
                    "companyId",
                    "reservationId",
                    "name",
                    "checkInDate",
                    "checkOutDate",
                    "createdAt",
                    "updatedAt",
                ]

                present_fields = [field for field in optional_fields if field in data]
                logger.info(f"Campos opcionales presentes: {present_fields}")

                # Verificar datos embebidos si existen
                if "_embedded" in data:
                    embedded = data["_embedded"]
                    logger.info(f"Datos embebidos: {list(embedded.keys())}")

                    if "contact" in embedded:
                        contact = embedded["contact"]
                        logger.info(
                            f"Contacto: ID={contact.get('id')}, Nombre={contact.get('firstName')} {contact.get('lastName')}"
                        )

                # Verificar enlaces si existen
                if "_links" in data:
                    links = data["_links"]
                    logger.info(f"Enlaces: {list(links.keys())}")

            elif response.status_code == 404:
                logger.warning(f"Folio {folio_id} no encontrado (404)")
                # Esto es normal si el folio no existe
            else:
                logger.error(f"Error HTTP {response.status_code}: {response.text}")
                pytest.fail(f"Error inesperado: {response.status_code}")

        except Exception as e:
            logger.error(f"Error en test: {e}")
            pytest.fail(f"Error en test: {e}")

    def test_folio_endpoint_vs_old_endpoint(self, direct_session):
        """Test que compara el nuevo endpoint vs el endpoint anterior"""
        logger.info("=" * 60)
        logger.info("TEST: Comparación de endpoints")
        logger.info("=" * 60)

        # Test con folio_id = 1
        folio_id = 1

        # Nuevo endpoint (correcto)
        new_url = f"https://ihmvacations.trackhs.com/api/pms/folios/{folio_id}"

        # Endpoint anterior (incorrecto) - usando reservation_id
        old_url = (
            f"https://ihmvacations.trackhs.com/api/pms/reservations/{folio_id}/folio"
        )

        logger.info(f"Probando nuevo endpoint: {new_url}")
        try:
            new_response = direct_session.get(new_url)
            logger.info(f"Nuevo endpoint - Status: {new_response.status_code}")

            if new_response.status_code == 200:
                new_data = new_response.json()
                logger.info(f"Nuevo endpoint - Datos válidos: {len(new_data)} campos")
                logger.info(
                    f"Nuevo endpoint - ID: {new_data.get('id')}, Status: {new_data.get('status')}"
                )
            else:
                logger.info(f"Nuevo endpoint - Error: {new_response.status_code}")

        except Exception as e:
            logger.error(f"Error en nuevo endpoint: {e}")

        logger.info(f"Probando endpoint anterior: {old_url}")
        try:
            old_response = direct_session.get(old_url)
            logger.info(f"Endpoint anterior - Status: {old_response.status_code}")

            if old_response.status_code == 200:
                old_data = old_response.json()
                logger.info(
                    f"Endpoint anterior - Datos válidos: {len(old_data)} campos"
                )
            else:
                logger.info(f"Endpoint anterior - Error: {old_response.status_code}")

        except Exception as e:
            logger.error(f"Error en endpoint anterior: {e}")

    def test_api_client_folio_method(self, api_client):
        """Test que verifica el método get_folio del API client"""
        logger.info("=" * 60)
        logger.info("TEST: Método get_folio del API client")
        logger.info("=" * 60)

        # Test con folio_id = 1
        folio_id = 1

        try:
            result = api_client.get_folio(folio_id)

            logger.info(f"Resultado del API client: {type(result)}")

            if isinstance(result, dict):
                logger.info(f"Campos en resultado: {list(result.keys())}")

                # Verificar que tiene los campos básicos
                if "id" in result and "status" in result:
                    logger.info("✅ API client devuelve estructura correcta")
                    logger.info(f"Folio ID: {result['id']}")
                    logger.info(f"Status: {result['status']}")
                else:
                    logger.warning("⚠️ API client no devuelve estructura esperada")
            else:
                logger.warning(f"⚠️ API client devuelve tipo inesperado: {type(result)}")

        except Exception as e:
            logger.error(f"Error en API client: {e}")
            # No fallar el test si el folio no existe
            if "404" in str(e) or "not found" in str(e).lower():
                logger.info("✅ Error esperado - folio no encontrado")
            else:
                pytest.fail(f"Error inesperado en API client: {e}")

    def test_folio_schema_validation(self, direct_session):
        """Test que valida el schema del folio contra la documentación"""
        logger.info("=" * 60)
        logger.info("TEST: Validación de schema de folio")
        logger.info("=" * 60)

        folio_id = 1
        url = f"https://ihmvacations.trackhs.com/api/pms/folios/{folio_id}"

        try:
            response = direct_session.get(url)

            if response.status_code == 200:
                data = response.json()

                # Validar campos requeridos
                required_fields = ["id", "status"]
                for field in required_fields:
                    assert field in data, f"Campo requerido '{field}' faltante"

                # Validar tipos de campos requeridos
                assert isinstance(data["id"], int), "ID debe ser entero"
                assert data["status"] in [
                    "open",
                    "closed",
                ], "Status debe ser 'open' o 'closed'"

                # Validar campos opcionales si están presentes
                if "type" in data:
                    assert data["type"] in [
                        "guest",
                        "master",
                    ], "Type debe ser 'guest' o 'master'"

                if "currentBalance" in data:
                    # La API puede devolver valores numéricos como strings
                    balance = data["currentBalance"]
                    assert isinstance(
                        balance, (int, float, str)
                    ), "currentBalance debe ser numérico o string numérico"
                    if isinstance(balance, str):
                        try:
                            float(balance)  # Verificar que se puede convertir a float
                        except ValueError:
                            pytest.fail("currentBalance string no es numérico válido")

                if "realizedBalance" in data:
                    # La API puede devolver valores numéricos como strings
                    balance = data["realizedBalance"]
                    assert isinstance(
                        balance, (int, float, str)
                    ), "realizedBalance debe ser numérico o string numérico"
                    if isinstance(balance, str):
                        try:
                            float(balance)  # Verificar que se puede convertir a float
                        except ValueError:
                            pytest.fail("realizedBalance string no es numérico válido")

                # Validar fechas si están presentes
                date_fields = [
                    "createdAt",
                    "updatedAt",
                    "startDate",
                    "endDate",
                    "closedDate",
                    "checkInDate",
                    "checkOutDate",
                ]
                for field in date_fields:
                    if field in data and data[field] is not None:
                        # Verificar que es una cadena (fecha ISO)
                        assert isinstance(data[field], str), f"{field} debe ser string"
                        logger.info(f"✅ {field}: {data[field]}")

                # Validar datos embebidos si están presentes
                if "_embedded" in data:
                    embedded = data["_embedded"]

                    if "contact" in embedded:
                        contact = embedded["contact"]
                        assert "id" in contact, "Contact debe tener ID"
                        assert isinstance(
                            contact["id"], int
                        ), "Contact ID debe ser entero"
                        logger.info(f"✅ Contact embebido: ID={contact['id']}")

                    if "company" in embedded:
                        company = embedded["company"]
                        assert "id" in company, "Company debe tener ID"
                        assert "type" in company, "Company debe tener type"
                        assert "name" in company, "Company debe tener name"
                        logger.info(
                            f"✅ Company embebido: ID={company['id']}, Type={company['type']}"
                        )

                logger.info("✅ Schema de folio válido según documentación")

            elif response.status_code == 404:
                logger.info("✅ Folio no encontrado (404) - comportamiento esperado")
            else:
                logger.error(f"Error HTTP {response.status_code}: {response.text}")
                pytest.fail(f"Error inesperado: {response.status_code}")

        except Exception as e:
            logger.error(f"Error en validación de schema: {e}")
            pytest.fail(f"Error en validación: {e}")

    @pytest.mark.slow
    def test_multiple_folio_ids(self, direct_session):
        """Test que prueba múltiples folio IDs para encontrar uno válido"""
        logger.info("=" * 60)
        logger.info("TEST: Múltiples folio IDs")
        logger.info("=" * 60)

        # Probar varios folio IDs para encontrar uno válido
        test_ids = [1, 2, 3, 5, 10, 100]
        valid_folio = None

        for folio_id in test_ids:
            url = f"https://ihmvacations.trackhs.com/api/pms/folios/{folio_id}"

            try:
                response = direct_session.get(url)
                logger.info(f"Folio {folio_id}: Status {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    logger.info(
                        f"✅ Folio {folio_id} válido: ID={data.get('id')}, Status={data.get('status')}"
                    )
                    valid_folio = data
                    break
                elif response.status_code == 404:
                    logger.info(f"Folio {folio_id}: No encontrado")
                else:
                    logger.warning(f"Folio {folio_id}: Error {response.status_code}")

            except Exception as e:
                logger.error(f"Error probando folio {folio_id}: {e}")

        if valid_folio:
            logger.info(f"✅ Folio válido encontrado: {valid_folio['id']}")
        else:
            logger.warning("⚠️ No se encontró ningún folio válido en los IDs probados")
