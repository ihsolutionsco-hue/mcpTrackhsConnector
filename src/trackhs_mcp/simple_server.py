"""
Servidor MCP simplificado para TrackHS
Solo las funciones esenciales, sin complejidad innecesaria
"""

import logging
from typing import Dict, Any, Optional
from fastmcp import FastMCP
import httpx

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración simple
API_BASE_URL = "https://ihmvacations.trackhs.com"
API_USERNAME = "aba99777416466b6bdc1a25223192ccb"
API_PASSWORD = "a8b8c8d8e8f8g8h8i8j8k8l8m8n8o8p8"

# Cliente HTTP simple
class SimpleTrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = httpx.BasicAuth(username, password)
        self.client = httpx.Client(auth=self.auth, timeout=30)

    def get(self, endpoint: str, params: dict = None):
        """Hacer petición GET a la API"""
        url = f"{self.base_url}/{endpoint}"
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Cerrar el cliente HTTP"""
        self.client.close()

# Crear cliente
api_client = SimpleTrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)

# Crear servidor MCP simple
mcp = FastMCP(
    name="TrackHS Simple",
    instructions="Servidor MCP simple para TrackHS API",
    strict_input_validation=False
)

@mcp.tool
def search_units(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    is_active: Optional[int] = None,
    is_bookable: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Buscar unidades de alojamiento en TrackHS.

    Args:
        page: Número de página (1-based)
        size: Tamaño de página (1-100)
        search: Búsqueda de texto
        bedrooms: Número de dormitorios
        bathrooms: Número de baños
        is_active: Unidades activas (1) o inactivas (0)
        is_bookable: Unidades disponibles (1) o no (0)

    Returns:
        Resultado de la búsqueda de unidades
    """
    try:
        # Construir parámetros simples
        params = {
            "page": page,
            "size": size
        }

        if search:
            params["search"] = search
        if bedrooms is not None:
            params["bedrooms"] = bedrooms
        if bathrooms is not None:
            params["bathrooms"] = bathrooms
        if is_active is not None:
            params["isActive"] = is_active
        if is_bookable is not None:
            params["isBookable"] = is_bookable

        logger.info(f"Buscando unidades con parámetros: {params}")

        # Llamar a la API
        result = api_client.get("api/pms/units", params)

        logger.info(f"Encontradas {result.get('total_items', 0)} unidades")

        return result

    except Exception as e:
        logger.error(f"Error buscando unidades: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
