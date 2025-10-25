from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SearchAmenitiesRequest(BaseModel):
    """Parámetros para buscar amenidades del hotel"""
    page: int = Field(default=1, ge=1, description="Página (1-based)")
    size: int = Field(default=10, ge=1, le=1000, description="Resultados por página")
    search: Optional[str] = Field(None, max_length=200, description="Búsqueda por nombre")
    group_id: Optional[int] = Field(None, description="ID del grupo de amenidades")
    is_public: Optional[int] = Field(None, ge=0, le=1, description="Amenidades públicas: 1=si, 0=no")

def register_amenity_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def search_amenities(request: SearchAmenitiesRequest) -> dict:
        """Busca amenidades del hotel.
        
        CUÁNDO USAR:
        - "¿Qué amenidades tiene el hotel?" → sin filtros
        - "Buscar piscina" → search="pool"
        - "Amenidades para familias" → group_id=4
        - "Amenidades públicas" → is_public=1
        """
        logger.info("search_amenities_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/pms/units/amenities", 
                                     params=request.model_dump(exclude_none=True))
            logger.info("search_amenities_success")
            return result
        except Exception as e:
            logger.error("search_amenities_error", error=str(e))
            raise
