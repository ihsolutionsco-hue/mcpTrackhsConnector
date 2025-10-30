#!/usr/bin/env python3
"""
Script de testing comprehensivo para la tool get_folio
"""

import json
import os
import sys
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class FolioToolTester:
    """Tester comprehensivo para la tool get_folio"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_client = TrackHSAPIClient(base_url, username, password)
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.timeout = 30

        logger.info(f"Tester inicializado para {base_url}")

    def test_folio_tool_directly(self, folio_id: int) -> Dict[str, Any]:
        """Test directo de la tool get_folio usando el API client"""
        logger.info(f"Testing tool get_folio directamente con folio_id={folio_id}")

        try:
            # Simular llamada directa a la tool
            response = self.api_client.get_folio(folio_id)

            # Validar estructura básica
            if not isinstance(response, dict):
                raise ValueError("Respuesta no es un diccionario")

            # Validar campos requeridos
            required_fields = ["id", "status"]
            missing_fields = [
                field for field in required_fields if field not in response
            ]

            if missing_fields:
                raise ValueError(f"Campos requeridos faltantes: {missing_fields}")

            # Validar tipos
            if not isinstance(response["id"], int):
                raise ValueError("ID no es entero")

            if response["status"] not in ["open", "closed"]:
                raise ValueError(f"Status inválido: {response['status']}")

            logger.info(f"✅ Tool get_folio funciona correctamente")
            logger.info(f"  Folio ID: {response['id']}")
            logger.info(f"  Status: {response['status']}")
            logger.info(f"  Tipo: {response.get('type', 'N/A')}")
            logger.info(f"  Balance Actual: {response.get('currentBalance', 'N/A')}")
            logger.info(
                f"  Balance Realizado: {response.get('realizedBalance', 'N/A')}"
            )

            return {
                "success": True,
                "folio_id": folio_id,
                "response": response,
                "message": "Tool funciona correctamente",
            }

        except Exception as e:
            logger.error(f"❌ Error en tool get_folio: {e}")
            return {
                "success": False,
                "folio_id": folio_id,
                "error": str(e),
                "message": "Tool falló",
            }

    def test_folio_api_directly(self, folio_id: int) -> Dict[str, Any]:
        """Test directo del endpoint de la API"""
        logger.info(f"Testing API endpoint directamente con folio_id={folio_id}")

        url = f"{self.base_url}/api/pms/folios/{folio_id}"

        try:
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ API endpoint funciona correctamente")
                logger.info(f"  Status HTTP: {response.status_code}")
                logger.info(f"  Content-Type: {response.headers.get('content-type')}")
                logger.info(f"  Campos en respuesta: {len(data)}")

                return {
                    "success": True,
                    "folio_id": folio_id,
                    "status_code": response.status_code,
                    "data": data,
                    "message": "API endpoint funciona correctamente",
                }
            elif response.status_code == 404:
                logger.warning(f"⚠️ Folio no encontrado (404)")
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "status_code": 404,
                    "message": "Folio no encontrado",
                }
            else:
                logger.error(f"❌ Error HTTP {response.status_code}")
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "status_code": response.status_code,
                    "message": f"Error HTTP {response.status_code}",
                }

        except Exception as e:
            logger.error(f"❌ Error en API endpoint: {e}")
            return {
                "success": False,
                "folio_id": folio_id,
                "error": str(e),
                "message": "Error en API endpoint",
            }

    def find_valid_folio_ids(self, max_attempts: int = 10) -> List[int]:
        """Buscar folio IDs válidos para testing"""
        logger.info(f"Buscando folio IDs válidos (máximo {max_attempts} intentos)")

        valid_ids = []

        for folio_id in range(1, max_attempts + 1):
            url = f"{self.base_url}/api/pms/folios/{folio_id}"

            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if "id" in data and "status" in data:
                        valid_ids.append(folio_id)
                        logger.info(
                            f"  ✅ Folio {folio_id} válido: Status={data['status']}"
                        )
                    else:
                        logger.warning(f"  ⚠️ Folio {folio_id} sin estructura válida")
                elif response.status_code == 404:
                    logger.info(f"  - Folio {folio_id} no encontrado")
                else:
                    logger.warning(f"  ⚠️ Folio {folio_id} error {response.status_code}")

            except Exception as e:
                logger.warning(f"  ⚠️ Error probando folio {folio_id}: {e}")

        logger.info(f"Encontrados {len(valid_ids)} folio IDs válidos: {valid_ids}")
        return valid_ids

    def test_folio_schema_validation(self, folio_id: int) -> Dict[str, Any]:
        """Test de validación de schema según documentación oficial"""
        logger.info(f"Validando schema de folio {folio_id}")

        url = f"{self.base_url}/api/pms/folios/{folio_id}"

        try:
            response = self.session.get(url)

            if response.status_code != 200:
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "message": f"Error HTTP {response.status_code}",
                }

            data = response.json()

            # Validar campos requeridos
            required_fields = ["id", "status"]
            missing_required = [field for field in required_fields if field not in data]

            if missing_required:
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "message": f"Campos requeridos faltantes: {missing_required}",
                }

            # Validar tipos de campos requeridos
            if not isinstance(data["id"], int):
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "message": "ID no es entero",
                }

            if data["status"] not in ["open", "closed"]:
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "message": f"Status inválido: {data['status']}",
                }

            # Validar campos opcionales si están presentes
            optional_validations = []

            if "type" in data and data["type"] not in ["guest", "master"]:
                optional_validations.append(f"Type inválido: {data['type']}")

            if "currentBalance" in data:
                balance = data["currentBalance"]
                if not isinstance(balance, (int, float, str)):
                    optional_validations.append("currentBalance tipo inválido")
                elif isinstance(balance, str):
                    try:
                        float(balance)
                    except ValueError:
                        optional_validations.append("currentBalance string no numérico")

            if "realizedBalance" in data:
                balance = data["realizedBalance"]
                if not isinstance(balance, (int, float, str)):
                    optional_validations.append("realizedBalance tipo inválido")
                elif isinstance(balance, str):
                    try:
                        float(balance)
                    except ValueError:
                        optional_validations.append(
                            "realizedBalance string no numérico"
                        )

            # Validar datos embebidos
            embedded_validations = []
            if "_embedded" in data:
                embedded = data["_embedded"]
                if "contact" in embedded:
                    contact = embedded["contact"]
                    if "id" not in contact or not isinstance(contact["id"], int):
                        embedded_validations.append("Contact ID inválido")

                if "company" in embedded:
                    company = embedded["company"]
                    required_company_fields = ["id", "type", "name"]
                    missing_company = [
                        field
                        for field in required_company_fields
                        if field not in company
                    ]
                    if missing_company:
                        embedded_validations.append(
                            f"Company campos faltantes: {missing_company}"
                        )

            # Compilar resultados
            all_validations = optional_validations + embedded_validations

            if all_validations:
                logger.warning(f"⚠️ Validaciones fallidas: {all_validations}")
                return {
                    "success": False,
                    "folio_id": folio_id,
                    "message": f"Validaciones fallidas: {all_validations}",
                }
            else:
                logger.info(f"✅ Schema válido según documentación oficial")
                return {
                    "success": True,
                    "folio_id": folio_id,
                    "message": "Schema válido según documentación oficial",
                }

        except Exception as e:
            logger.error(f"❌ Error en validación de schema: {e}")
            return {
                "success": False,
                "folio_id": folio_id,
                "error": str(e),
                "message": "Error en validación de schema",
            }

    def run_comprehensive_test(self):
        """Ejecutar test comprehensivo de la tool get_folio"""
        logger.info("=" * 80)
        logger.info("TESTING COMPREHENSIVO DE LA TOOL GET_FOLIO")
        logger.info("=" * 80)

        # Paso 1: Buscar folio IDs válidos
        logger.info("\n1. BUSCANDO FOLIO IDs VÁLIDOS")
        logger.info("-" * 40)
        valid_folio_ids = self.find_valid_folio_ids(20)

        if not valid_folio_ids:
            logger.error("❌ No se encontraron folio IDs válidos para testing")
            return

        # Paso 2: Test de cada folio ID válido
        logger.info(f"\n2. TESTING CON {len(valid_folio_ids)} FOLIO IDs VÁLIDOS")
        logger.info("-" * 40)

        results = {"tool_tests": [], "api_tests": [], "schema_tests": []}

        for folio_id in valid_folio_ids[:5]:  # Testear solo los primeros 5
            logger.info(f"\n--- Testing Folio ID: {folio_id} ---")

            # Test de tool
            tool_result = self.test_folio_tool_directly(folio_id)
            results["tool_tests"].append(tool_result)

            # Test de API
            api_result = self.test_folio_api_directly(folio_id)
            results["api_tests"].append(api_result)

            # Test de schema
            schema_result = self.test_folio_schema_validation(folio_id)
            results["schema_tests"].append(schema_result)

        # Paso 3: Resumen de resultados
        logger.info(f"\n3. RESUMEN DE RESULTADOS")
        logger.info("-" * 40)

        tool_success = sum(1 for r in results["tool_tests"] if r["success"])
        api_success = sum(1 for r in results["api_tests"] if r["success"])
        schema_success = sum(1 for r in results["schema_tests"] if r["success"])

        total_tests = len(results["tool_tests"])

        logger.info(f"Tool get_folio: {tool_success}/{total_tests} exitosos")
        logger.info(f"API endpoint: {api_success}/{total_tests} exitosos")
        logger.info(f"Schema validation: {schema_success}/{total_tests} exitosos")

        # Paso 4: Test de casos de error
        logger.info(f"\n4. TESTING DE CASOS DE ERROR")
        logger.info("-" * 40)

        # Test con folio ID inexistente
        logger.info("Testing con folio ID inexistente (99999)")
        error_result = self.test_folio_tool_directly(99999)
        if not error_result["success"]:
            logger.info("✅ Manejo de error correcto para folio inexistente")
        else:
            logger.warning("⚠️ Debería fallar con folio inexistente")

        # Test con folio ID inválido
        logger.info("Testing con folio ID inválido (0)")
        try:
            invalid_result = self.test_folio_tool_directly(0)
            logger.warning("⚠️ Debería fallar con folio ID 0")
        except Exception as e:
            logger.info(f"✅ Validación correcta para folio ID 0: {e}")

        logger.info(f"\n" + "=" * 80)
        logger.info("TESTING COMPLETADO")
        logger.info("=" * 80)

        # Guardar resultados
        results_file = "folio_tool_test_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Resultados guardados en {results_file}")


def main():
    """Función principal"""
    # Obtener credenciales
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        logger.error("Credenciales no encontradas en archivo .env")
        return

    logger.info(f"Usando credenciales: {username} / {'*' * len(password)}")

    # Crear tester
    tester = FolioToolTester(base_url, username, password)

    # Ejecutar test comprehensivo
    tester.run_comprehensive_test()


if __name__ == "__main__":
    main()
