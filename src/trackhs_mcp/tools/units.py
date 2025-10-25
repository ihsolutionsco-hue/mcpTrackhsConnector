from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SearchUnitsRequest(BaseModel):
    """Parámetros para buscar unidades disponibles"""
    page: int = Field(default=1, ge=1, description="Página (1-based)")
    size: int = Field(default=2, ge=1, le=25, description="Resultados. Voz: 2-3")
    bedrooms: Optional[str] = Field(None, description="Número de habitaciones")
    bathrooms: Optional[str] = Field(None, description="Número de baños")
    pets_friendly: Optional[str] = Field(None, pattern="^[01]$", description="Acepta mascotas: 1=si, 0=no")
    is_active: Optional[str] = Field(None, pattern="^[01]$", description="Unidad activa: 1=si, 0=no")

def register_unit_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def search_units(request: SearchUnitsRequest) -> dict:
        """Busca unidades disponibles con filtros.
        
        CUÁNDO USAR:
        - "¿Qué habitaciones hay disponibles?" → sin filtros
        - "Habitaciones con 2 dormitorios" → bedrooms="2"
        - "Unidades que aceptan mascotas" → pets_friendly="1"
        """
        logger.info("search_units_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/pms/units", 
                                     params=request.model_dump(exclude_none=True))
            logger.info("search_units_success")
            return result
        except Exception as e:
            logger.error("search_units_error", error=str(e))
            raise
