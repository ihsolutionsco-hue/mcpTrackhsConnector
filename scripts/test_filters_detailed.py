#!/usr/bin/env python3
"""
Test detallado de filtros de la API TrackHS
Verifica si los filtros realmente se aplican correctamente
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

from utils.logger import get_logger

logger = get_logger(__name__)


class TrackHSFilterTester:
    """Tester detallado de filtros de la API TrackHS"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.timeout = 30

        logger.info(f"Tester inicializado para {base_url}")

    def search_units(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Hace búsqueda de unidades con parámetros dados"""
        url = f"{self.base_url}/api/pms/units"

        logger.info(f"Búsqueda con parámetros: {params}")

        try:
            response = self.session.get(url, params=params)

            if response.status_code != 200:
                logger.error(f"Error HTTP {response.status_code}: {response.text}")
                return {"error": f"HTTP {response.status_code}"}

            data = response.json()
            units = data.get("units", [])

            logger.info(f"Encontradas {len(units)} unidades")

            return {
                "units": units,
                "total_items": data.get("total_items", 0),
                "page": data.get("page", 1),
                "size": data.get("size", 10),
            }

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return {"error": str(e)}

    def test_bedrooms_filter(self):
        """Test específico para filtros de dormitorios"""
        logger.info("=" * 60)
        logger.info("TEST: Filtros de dormitorios")
        logger.info("=" * 60)

        # Test 1: Sin filtros (baseline)
        logger.info("1. Búsqueda sin filtros (baseline)")
        result_baseline = self.search_units({"page": 1, "size": 20})

        if "error" in result_baseline:
            logger.error(f"Error en baseline: {result_baseline['error']}")
            return

        baseline_units = result_baseline.get("units", [])
        baseline_bedrooms = [
            u.get("bedrooms") for u in baseline_units if u.get("bedrooms") is not None
        ]
        logger.info(f"Bedrooms en baseline: {set(baseline_bedrooms)}")

        # Test 2: Con filtro min_bedrooms=2 (camelCase)
        logger.info("2. Con minBedrooms=2 (camelCase)")
        result_min = self.search_units({"page": 1, "size": 20, "minBedrooms": 2})

        if "error" not in result_min:
            min_units = result_min.get("units", [])
            min_bedrooms = [
                u.get("bedrooms") for u in min_units if u.get("bedrooms") is not None
            ]
            logger.info(f"Bedrooms con minBedrooms=2: {set(min_bedrooms)}")

            # Verificar que todos tienen >= 2 bedrooms
            invalid_units = [u for u in min_units if u.get("bedrooms", 0) < 2]
            if invalid_units:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: {len(invalid_units)} unidades con < 2 bedrooms"
                )
                for unit in invalid_units[:3]:
                    logger.error(
                        f"   - ID: {unit.get('id')}, bedrooms: {unit.get('bedrooms')}"
                    )
            else:
                logger.info("✅ Filtro minBedrooms funciona correctamente")

        # Test 3: Con filtro max_bedrooms=3 (camelCase)
        logger.info("3. Con maxBedrooms=3 (camelCase)")
        result_max = self.search_units({"page": 1, "size": 20, "maxBedrooms": 3})

        if "error" not in result_max:
            max_units = result_max.get("units", [])
            max_bedrooms = [
                u.get("bedrooms") for u in max_units if u.get("bedrooms") is not None
            ]
            logger.info(f"Bedrooms con maxBedrooms=3: {set(max_bedrooms)}")

            # Verificar que todos tienen <= 3 bedrooms
            invalid_units = [u for u in max_units if u.get("bedrooms", 0) > 3]
            if invalid_units:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: {len(invalid_units)} unidades con > 3 bedrooms"
                )
                for unit in invalid_units[:3]:
                    logger.error(
                        f"   - ID: {unit.get('id')}, bedrooms: {unit.get('bedrooms')}"
                    )
            else:
                logger.info("✅ Filtro maxBedrooms funciona correctamente")

        # Test 4: Con rango min=2, max=3
        logger.info("4. Con minBedrooms=2, maxBedrooms=3")
        result_range = self.search_units(
            {"page": 1, "size": 20, "minBedrooms": 2, "maxBedrooms": 3}
        )

        if "error" not in result_range:
            range_units = result_range.get("units", [])
            range_bedrooms = [
                u.get("bedrooms") for u in range_units if u.get("bedrooms") is not None
            ]
            logger.info(f"Bedrooms con rango 2-3: {set(range_bedrooms)}")

            # Verificar que todos están en rango 2-3
            invalid_units = [
                u for u in range_units if not (2 <= u.get("bedrooms", 0) <= 3)
            ]
            if invalid_units:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: {len(invalid_units)} unidades fuera del rango 2-3"
                )
                for unit in invalid_units[:3]:
                    logger.error(
                        f"   - ID: {unit.get('id')}, bedrooms: {unit.get('bedrooms')}"
                    )
            else:
                logger.info("✅ Filtro de rango funciona correctamente")

    def test_pets_friendly_filter(self):
        """Test específico para filtro pets_friendly"""
        logger.info("=" * 60)
        logger.info("TEST: Filtro pets_friendly")
        logger.info("=" * 60)

        # Test 1: Sin filtro (baseline)
        logger.info("1. Búsqueda sin filtro pets_friendly")
        result_baseline = self.search_units({"page": 1, "size": 20})

        if "error" in result_baseline:
            logger.error(f"Error en baseline: {result_baseline['error']}")
            return

        baseline_units = result_baseline.get("units", [])
        pets_friendly_count = sum(
            1 for u in baseline_units if u.get("petsFriendly") is True
        )
        logger.info(
            f"Unidades pet-friendly en baseline: {pets_friendly_count}/{len(baseline_units)}"
        )

        # Test 2: Con filtro petsFriendly=1
        logger.info("2. Con petsFriendly=1 (camelCase)")
        result_pets = self.search_units({"page": 1, "size": 20, "petsFriendly": 1})

        if "error" not in result_pets:
            pets_units = result_pets.get("units", [])
            logger.info(f"Unidades encontradas con petsFriendly=1: {len(pets_units)}")

            # Verificar que todas son pet-friendly
            non_pets_units = [
                u for u in pets_units if u.get("petsFriendly") is not True
            ]
            if non_pets_units:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: {len(non_pets_units)} unidades no son pet-friendly"
                )
                for unit in non_pets_units[:3]:
                    logger.error(
                        f"   - ID: {unit.get('id')}, petsFriendly: {unit.get('petsFriendly')}"
                    )
            else:
                logger.info("✅ Filtro petsFriendly funciona correctamente")

    def test_is_active_filter(self):
        """Test específico para filtro is_active"""
        logger.info("=" * 60)
        logger.info("TEST: Filtro is_active")
        logger.info("=" * 60)

        # Test 1: Sin filtro (baseline)
        logger.info("1. Búsqueda sin filtro is_active")
        result_baseline = self.search_units({"page": 1, "size": 20})

        if "error" in result_baseline:
            logger.error(f"Error en baseline: {result_baseline['error']}")
            return

        baseline_units = result_baseline.get("units", [])
        active_count = sum(1 for u in baseline_units if u.get("isActive") is True)
        inactive_count = sum(1 for u in baseline_units if u.get("isActive") is False)
        logger.info(
            f"Unidades activas/inactivas en baseline: {active_count}/{inactive_count}"
        )

        # Test 2: Con filtro isActive=1
        logger.info("2. Con isActive=1 (camelCase)")
        result_active = self.search_units({"page": 1, "size": 20, "isActive": 1})

        if "error" not in result_active:
            active_units = result_active.get("units", [])
            logger.info(f"Unidades encontradas con isActive=1: {len(active_units)}")

            # Verificar que todas están activas
            inactive_units = [u for u in active_units if u.get("isActive") is not True]
            if inactive_units:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: {len(inactive_units)} unidades inactivas"
                )
                for unit in inactive_units[:3]:
                    logger.error(
                        f"   - ID: {unit.get('id')}, isActive: {unit.get('isActive')}"
                    )
            else:
                logger.info("✅ Filtro isActive funciona correctamente")

    def test_unit_ids_filter(self):
        """Test específico para filtro unit_ids"""
        logger.info("=" * 60)
        logger.info("TEST: Filtro unit_ids")
        logger.info("=" * 60)

        # Primero obtener algunas unidades para tener IDs válidos
        logger.info("1. Obteniendo unidades para tener IDs válidos")
        result_baseline = self.search_units({"page": 1, "size": 10})

        if "error" in result_baseline:
            logger.error(f"Error obteniendo baseline: {result_baseline['error']}")
            return

        baseline_units = result_baseline.get("units", [])
        if not baseline_units:
            logger.warning("No hay unidades disponibles para testear unit_ids")
            return

        # Tomar los primeros 3 IDs
        test_ids = [u.get("id") for u in baseline_units[:3] if u.get("id") is not None]
        logger.info(f"IDs a testear: {test_ids}")

        # Test 1: Con unit_ids como lista
        logger.info("2. Con unit_ids como lista")
        result_list = self.search_units({"page": 1, "size": 20, "unit_ids": test_ids})

        if "error" not in result_list:
            list_units = result_list.get("units", [])
            list_unit_ids = [u.get("id") for u in list_units]
            logger.info(f"IDs encontrados con lista: {list_unit_ids}")

            # Verificar que solo contiene los IDs solicitados
            invalid_ids = [uid for uid in list_unit_ids if uid not in test_ids]
            if invalid_ids:
                logger.error(
                    f"❌ FILTRO NO FUNCIONA: IDs no solicitados encontrados: {invalid_ids}"
                )
            else:
                logger.info("✅ Filtro unit_ids con lista funciona correctamente")

        # Test 2: Con unit_ids como string
        logger.info("3. Con unit_ids como string")
        result_string = self.search_units(
            {"page": 1, "size": 20, "unit_ids": str(test_ids)}
        )

        if "error" not in result_string:
            string_units = result_string.get("units", [])
            string_unit_ids = [u.get("id") for u in string_units]
            logger.info(f"IDs encontrados con string: {string_unit_ids}")
        else:
            logger.info(f"Error con string: {result_string['error']}")

    def run_all_tests(self):
        """Ejecuta todos los tests"""
        logger.info("INICIANDO TESTS DETALLADOS DE FILTROS")
        logger.info("=" * 80)

        self.test_bedrooms_filter()
        self.test_pets_friendly_filter()
        self.test_is_active_filter()
        self.test_unit_ids_filter()

        logger.info("=" * 80)
        logger.info("TESTS COMPLETADOS")
        logger.info("=" * 80)


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
    tester = TrackHSFilterTester(base_url, username, password)

    # Ejecutar tests
    tester.run_all_tests()


if __name__ == "__main__":
    main()
