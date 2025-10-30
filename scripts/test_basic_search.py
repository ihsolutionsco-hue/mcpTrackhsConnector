#!/usr/bin/env python3
"""
Test básico de búsqueda sin filtros para obtener datos de la API
"""

import json
import os
import sys
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.logger import get_logger

logger = get_logger(__name__)


def test_basic_search():
    """Test básico para obtener datos de la API"""

    # Configurar credenciales
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        logger.error("Credenciales no encontradas en archivo .env")
        return

    # Crear sesión
    session = requests.Session()
    session.auth = (username, password)
    session.timeout = 30

    logger.info("=" * 60)
    logger.info("TEST BÁSICO DE BÚSQUEDA SIN FILTROS")
    logger.info("=" * 60)

    # Test 1: Búsqueda básica sin filtros
    logger.info("1. Búsqueda básica sin filtros")
    url = f"{base_url}/api/pms/units"
    params = {"page": 1, "size": 10}

    try:
        response = session.get(url, params=params)
        logger.info(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            units = data.get("units", [])
            total_items = data.get("total_items", 0)

            logger.info(f"Total de unidades disponibles: {total_items}")
            logger.info(f"Unidades en esta página: {len(units)}")

            if units:
                # Mostrar información de las primeras unidades
                logger.info("\nPrimeras 3 unidades:")
                for i, unit in enumerate(units[:3]):
                    logger.info(f"  {i+1}. ID: {unit.get('id')}")
                    logger.info(f"     Nombre: {unit.get('name', 'N/A')}")
                    logger.info(f"     isActive: {unit.get('isActive')}")
                    logger.info(f"     isBookable: {unit.get('isBookable')}")
                    logger.info(f"     bedrooms: {unit.get('bedrooms')}")
                    logger.info(f"     petsFriendly: {unit.get('petsFriendly')}")
                    logger.info("")

                # Analizar distribución de datos
                logger.info("ANÁLISIS DE DATOS:")

                # isActive
                active_count = sum(1 for u in units if u.get("isActive") is True)
                inactive_count = sum(1 for u in units if u.get("isActive") is False)
                logger.info(f"  - Unidades activas: {active_count}")
                logger.info(f"  - Unidades inactivas: {inactive_count}")

                # isBookable
                bookable_count = sum(1 for u in units if u.get("isBookable") is True)
                not_bookable_count = sum(
                    1 for u in units if u.get("isBookable") is False
                )
                logger.info(f"  - Unidades reservables: {bookable_count}")
                logger.info(f"  - Unidades no reservables: {not_bookable_count}")

                # petsFriendly
                pets_count = sum(1 for u in units if u.get("petsFriendly") is True)
                no_pets_count = sum(1 for u in units if u.get("petsFriendly") is False)
                logger.info(f"  - Unidades pet-friendly: {pets_count}")
                logger.info(f"  - Unidades no pet-friendly: {no_pets_count}")

                # bedrooms
                bedrooms = [
                    u.get("bedrooms") for u in units if u.get("bedrooms") is not None
                ]
                if bedrooms:
                    logger.info(f"  - Bedrooms encontrados: {set(bedrooms)}")
                    logger.info(
                        f"  - Rango de bedrooms: {min(bedrooms)} - {max(bedrooms)}"
                    )
                else:
                    logger.info("  - No hay datos de bedrooms")

                # bathrooms
                bathrooms = [
                    u.get("bathrooms") for u in units if u.get("bathrooms") is not None
                ]
                if bathrooms:
                    logger.info(f"  - Bathrooms encontrados: {set(bathrooms)}")
                    logger.info(
                        f"  - Rango de bathrooms: {min(bathrooms)} - {max(bathrooms)}"
                    )
                else:
                    logger.info("  - No hay datos de bathrooms")

            else:
                logger.warning("No se encontraron unidades")

        else:
            logger.error(f"Error HTTP {response.status_code}: {response.text}")

    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")

    # Test 2: Búsqueda con parámetros básicos
    logger.info("\n" + "=" * 60)
    logger.info("2. Búsqueda con parámetros básicos")
    logger.info("=" * 60)

    # Probar diferentes combinaciones de parámetros
    test_cases = [
        {"name": "Solo isActive=1", "params": {"page": 1, "size": 10, "isActive": 1}},
        {
            "name": "Solo isBookable=1",
            "params": {"page": 1, "size": 10, "isBookable": 1},
        },
        {
            "name": "isActive=1 + isBookable=1",
            "params": {"page": 1, "size": 10, "isActive": 1, "isBookable": 1},
        },
        {
            "name": "Con search='pool'",
            "params": {"page": 1, "size": 10, "search": "pool"},
        },
        {
            "name": "Con search='luxury'",
            "params": {"page": 1, "size": 10, "search": "luxury"},
        },
    ]

    for test_case in test_cases:
        logger.info(f"\nTest: {test_case['name']}")
        logger.info(f"Parámetros: {test_case['params']}")

        try:
            response = session.get(url, params=test_case["params"])
            if response.status_code == 200:
                data = response.json()
                units = data.get("units", [])
                total_items = data.get("total_items", 0)
                logger.info(
                    f"  Resultado: {len(units)} unidades (total: {total_items})"
                )

                if units:
                    # Mostrar características de las unidades encontradas
                    active = sum(1 for u in units if u.get("isActive") is True)
                    bookable = sum(1 for u in units if u.get("isBookable") is True)
                    pets = sum(1 for u in units if u.get("petsFriendly") is True)
                    bedrooms = [
                        u.get("bedrooms")
                        for u in units
                        if u.get("bedrooms") is not None
                    ]

                    logger.info(f"    - Activas: {active}/{len(units)}")
                    logger.info(f"    - Reservables: {bookable}/{len(units)}")
                    logger.info(f"    - Pet-friendly: {pets}/{len(units)}")
                    if bedrooms:
                        logger.info(f"    - Bedrooms: {set(bedrooms)}")
            else:
                logger.error(f"  Error HTTP {response.status_code}")

        except Exception as e:
            logger.error(f"  Error: {e}")


if __name__ == "__main__":
    test_basic_search()
