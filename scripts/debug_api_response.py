#!/usr/bin/env python3
"""
Debug de la estructura de respuesta de la API TrackHS
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


def debug_api_response():
    """Debug de la estructura de respuesta de la API"""

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
    logger.info("DEBUG DE ESTRUCTURA DE RESPUESTA API")
    logger.info("=" * 60)

    # Test 1: Respuesta básica
    logger.info("1. Respuesta básica sin filtros")
    url = f"{base_url}/api/pms/units"
    params = {"page": 1, "size": 5}

    try:
        response = session.get(url, params=params)
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Content-Type: {response.headers.get('content-type')}")

        if response.status_code == 200:
            data = response.json()

            # Mostrar estructura completa
            logger.info(f"Claves principales: {list(data.keys())}")

            # Buscar unidades en diferentes ubicaciones posibles
            units_found = False

            if "units" in data:
                units = data["units"]
                logger.info(f"Unidades en 'units': {len(units)}")
                units_found = True
            elif "_embedded" in data:
                embedded = data["_embedded"]
                logger.info(f"Claves en '_embedded': {list(embedded.keys())}")
                if "units" in embedded:
                    units = embedded["units"]
                    logger.info(f"Unidades en '_embedded.units': {len(units)}")
                    units_found = True
            elif "data" in data:
                data_section = data["data"]
                logger.info(f"Claves en 'data': {list(data_section.keys())}")
                if "units" in data_section:
                    units = data_section["units"]
                    logger.info(f"Unidades en 'data.units': {len(units)}")
                    units_found = True

            if not units_found:
                logger.warning(
                    "No se encontraron unidades en ninguna ubicación esperada"
                )
                logger.info("Estructura completa de la respuesta:")
                logger.info(
                    json.dumps(data, indent=2, ensure_ascii=False)[:1000] + "..."
                )
            else:
                # Mostrar información de las primeras unidades
                logger.info(f"\nPrimeras {min(3, len(units))} unidades:")
                for i, unit in enumerate(units[:3]):
                    logger.info(f"  {i+1}. ID: {unit.get('id')}")
                    logger.info(f"     Nombre: {unit.get('name', 'N/A')}")
                    logger.info(f"     isActive: {unit.get('isActive')}")
                    logger.info(f"     isBookable: {unit.get('isBookable')}")
                    logger.info(f"     bedrooms: {unit.get('bedrooms')}")
                    logger.info(f"     petsFriendly: {unit.get('petsFriendly')}")
                    logger.info("")

                # Verificar campos de paginación
                logger.info("Información de paginación:")
                logger.info(f"  - page: {data.get('page', 'N/A')}")
                logger.info(f"  - size: {data.get('size', 'N/A')}")
                logger.info(f"  - total_items: {data.get('total_items', 'N/A')}")
                logger.info(f"  - total_pages: {data.get('total_pages', 'N/A')}")

        else:
            logger.error(f"Error HTTP {response.status_code}: {response.text}")

    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")

    # Test 2: Diferentes tamaños de página
    logger.info("\n" + "=" * 60)
    logger.info("2. Diferentes tamaños de página")
    logger.info("=" * 60)

    sizes = [1, 5, 10, 20]
    for size in sizes:
        logger.info(f"\nProbando size={size}")
        params = {"page": 1, "size": size}

        try:
            response = session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                units = data.get("units", [])
                total_items = data.get("total_items", 0)
                logger.info(
                    f"  Resultado: {len(units)} unidades (total: {total_items})"
                )
            else:
                logger.error(f"  Error HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"  Error: {e}")

    # Test 3: Diferentes páginas
    logger.info("\n" + "=" * 60)
    logger.info("3. Diferentes páginas")
    logger.info("=" * 60)

    pages = [1, 2, 3, 10]
    for page in pages:
        logger.info(f"\nProbando page={page}")
        params = {"page": page, "size": 5}

        try:
            response = session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                units = data.get("units", [])
                total_items = data.get("total_items", 0)
                logger.info(
                    f"  Resultado: {len(units)} unidades (total: {total_items})"
                )
            else:
                logger.error(f"  Error HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"  Error: {e}")


if __name__ == "__main__":
    debug_api_response()
