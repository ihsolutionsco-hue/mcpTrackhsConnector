#!/usr/bin/env python3
"""
Script de validación directa de la API TrackHS
Hace llamados HTTP directos para verificar el comportamiento de los filtros
sin pasar por MCP/FastMCP
"""

import json
import os
import sys
from typing import Any, Dict, List
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.logger import get_logger

logger = get_logger(__name__)


class TrackHSDirectValidator:
    """Validador directo de la API TrackHS"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.timeout = 30

        logger.info(f"Validador inicializado para {base_url}")

    def test_endpoint(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hace un llamado directo al endpoint con los parámetros dados

        Args:
            endpoint: Endpoint de la API (ej: "api/pms/units")
            params: Parámetros de consulta

        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info(f"Llamando a {url}")
        logger.info(f"Parámetros: {params}")

        try:
            response = self.session.get(url, params=params)

            logger.info(f"Status: {response.status_code}")
            logger.info(f"Headers: {dict(response.headers)}")

            if response.status_code == 401:
                logger.error("Error 401: Credenciales inválidas")
                return {"error": "authentication_failed", "status_code": 401}

            if response.status_code == 403:
                logger.error("Error 403: Sin permisos")
                return {"error": "authorization_failed", "status_code": 403}

            if not response.ok:
                logger.error(f"Error HTTP {response.status_code}: {response.text}")
                return {
                    "error": "http_error",
                    "status_code": response.status_code,
                    "text": response.text,
                }

            try:
                data = response.json()
                logger.info(f"Respuesta JSON válida con {len(data)} claves")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Error parseando JSON: {e}")
                return {"error": "json_parse_error", "text": response.text}

        except requests.RequestError as e:
            logger.error(f"Error de conexión: {e}")
            return {"error": "connection_error", "message": str(e)}

    def test_units_search_snake_case(self) -> Dict[str, Any]:
        """Test con parámetros en snake_case (formato incorrecto)"""
        logger.info("=" * 60)
        logger.info("TEST 1: Parámetros en snake_case (formato incorrecto)")
        logger.info("=" * 60)

        params = {
            "page": 1,
            "size": 5,
            "is_active": True,
            "is_bookable": True,
            "min_bedrooms": 2,
            "max_bedrooms": 3,
            "pets_friendly": True,
        }

        result = self.test_endpoint("api/pms/units", params)

        if "error" in result:
            logger.error(f"Test snake_case falló: {result}")
            return result

        # Analizar respuesta
        units = result.get("units", [])
        logger.info(f"Unidades encontradas: {len(units)}")

        if units:
            # Verificar si los filtros se aplicaron
            active_units = [u for u in units if u.get("isActive") is True]
            inactive_units = [u for u in units if u.get("isActive") is False]

            logger.info(f"Unidades activas: {len(active_units)}")
            logger.info(f"Unidades inactivas: {len(inactive_units)}")

            # Verificar bedrooms
            bedrooms_found = [
                u.get("bedrooms") for u in units if u.get("bedrooms") is not None
            ]
            logger.info(f"Bedrooms encontrados: {set(bedrooms_found)}")

            # Verificar pets_friendly
            pets_friendly = [u for u in units if u.get("petsFriendly") is True]
            logger.info(f"Unidades pet-friendly: {len(pets_friendly)}")

        return result

    def test_units_search_camel_case(self) -> Dict[str, Any]:
        """Test con parámetros en camelCase (formato correcto)"""
        logger.info("=" * 60)
        logger.info("TEST 2: Parámetros en camelCase (formato correcto)")
        logger.info("=" * 60)

        params = {
            "page": 1,
            "size": 5,
            "isActive": 1,  # camelCase + 1/0
            "isBookable": 1,
            "minBedrooms": 2,
            "maxBedrooms": 3,
            "petsFriendly": 1,
        }

        result = self.test_endpoint("api/pms/units", params)

        if "error" in result:
            logger.error(f"Test camelCase falló: {result}")
            return result

        # Analizar respuesta
        units = result.get("units", [])
        logger.info(f"Unidades encontradas: {len(units)}")

        if units:
            # Verificar si los filtros se aplicaron
            active_units = [u for u in units if u.get("isActive") is True]
            inactive_units = [u for u in units if u.get("isActive") is False]

            logger.info(f"Unidades activas: {len(active_units)}")
            logger.info(f"Unidades inactivas: {len(inactive_units)}")

            # Verificar bedrooms
            bedrooms_found = [
                u.get("bedrooms") for u in units if u.get("bedrooms") is not None
            ]
            logger.info(f"Bedrooms encontrados: {set(bedrooms_found)}")

            # Verificar pets_friendly
            pets_friendly = [u for u in units if u.get("petsFriendly") is True]
            logger.info(f"Unidades pet-friendly: {len(pets_friendly)}")

        return result

    def test_unit_ids_formats(self) -> Dict[str, Any]:
        """Test diferentes formatos para unit_ids"""
        logger.info("=" * 60)
        logger.info("TEST 3: Diferentes formatos para unit_ids")
        logger.info("=" * 60)

        # Test 1: Array como lista
        logger.info("Test 3.1: unit_ids como lista [2, 3]")
        params = {"page": 1, "size": 5, "unit_ids": [2, 3]}

        result1 = self.test_endpoint("api/pms/units", params)
        logger.info(f"Resultado lista: {result1.get('error', 'OK')}")

        # Test 2: Array como string
        logger.info("Test 3.2: unit_ids como string '[2,3]'")
        params = {"page": 1, "size": 5, "unit_ids": "[2,3]"}

        result2 = self.test_endpoint("api/pms/units", params)
        logger.info(f"Resultado string: {result2.get('error', 'OK')}")

        # Test 3: Array como string con comillas
        logger.info('Test 3.3: unit_ids como string con comillas \'["2","3"]\'')
        params = {"page": 1, "size": 5, "unit_ids": '["2","3"]'}

        result3 = self.test_endpoint("api/pms/units", params)
        logger.info(f"Resultado string con comillas: {result3.get('error', 'OK')}")

        return {"lista": result1, "string": result2, "string_quoted": result3}

    def test_availability_filters(self) -> Dict[str, Any]:
        """Test filtros de disponibilidad"""
        logger.info("=" * 60)
        logger.info("TEST 4: Filtros de disponibilidad")
        logger.info("=" * 60)

        params = {
            "page": 1,
            "size": 5,
            "arrival": "2025-12-15",
            "departure": "2025-12-22",
            "isActive": 1,
            "isBookable": 1,
        }

        result = self.test_endpoint("api/pms/units", params)

        if "error" in result:
            logger.error(f"Test disponibilidad falló: {result}")
            return result

        units = result.get("units", [])
        logger.info(f"Unidades disponibles: {len(units)}")

        return result

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Ejecuta todos los tests"""
        logger.info("INICIANDO VALIDACIÓN COMPREHENSIVA DE API TRACKHS")
        logger.info("=" * 80)

        results = {}

        # Test 1: snake_case
        results["snake_case"] = self.test_units_search_snake_case()

        # Test 2: camelCase
        results["camel_case"] = self.test_units_search_camel_case()

        # Test 3: unit_ids
        results["unit_ids"] = self.test_unit_ids_formats()

        # Test 4: disponibilidad
        results["availability"] = self.test_availability_filters()

        # Resumen
        logger.info("=" * 80)
        logger.info("RESUMEN DE RESULTADOS")
        logger.info("=" * 80)

        for test_name, result in results.items():
            if isinstance(result, dict) and "error" in result:
                logger.error(f"{test_name}: FALLÓ - {result['error']}")
            else:
                logger.info(f"{test_name}: OK")

        return results


def main():
    """Función principal"""
    # Obtener credenciales de variables de entorno (cargadas desde .env)
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        logger.error(
            "Credenciales no encontradas en archivo .env. Verifique que exista el archivo .env con TRACKHS_USERNAME y TRACKHS_PASSWORD"
        )
        return

    logger.info(f"Usando credenciales: {username} / {'*' * len(password)}")
    logger.info(f"URL base: {base_url}")

    # Crear validador
    validator = TrackHSDirectValidator(base_url, username, password)

    # Ejecutar tests
    results = validator.run_comprehensive_test()

    # Guardar resultados
    output_file = "api_validation_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Resultados guardados en {output_file}")


if __name__ == "__main__":
    main()
