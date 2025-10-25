from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

class SearchAmenitiesRequest(BaseModel):
    """Parámetros para buscar amenidades del hotel"""
    page: int = Field(default=1, ge=1, description="Página (1-based)")
    size: int = Field(default=10, ge=1, le=1000, description="Resultados por página")
    search: Optional[str] = Field(None, max_length=200, description="Búsqueda por nombre")
    group_id: Optional[int] = Field(None, description="ID del grupo de amenidades")
    is_public: Optional[int] = Field(None, ge=0, le=1, description="Amenidades públicas: 1=si, 0=no")
    
    @field_validator('search')
    @classmethod
    def validate_search_term(cls, v):
        if v is not None:
            if len(v.strip()) < 2:
                raise ValueError("Término de búsqueda debe tener al menos 2 caracteres")
            if len(v) > 200:
                raise ValueError("Término de búsqueda demasiado largo")
        return v
    
    @field_validator('group_id')
    @classmethod
    def validate_group_id(cls, v):
        if v is not None:
            if v < 1 or v > 1000:
                raise ValueError("ID de grupo debe estar entre 1 y 1000")
        return v

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
        start_time = time.time()
        logger.info("search_amenities_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/pms/units/amenities", 
                                     params=request.model_dump(exclude_none=True))
            
            duration = time.time() - start_time
            logger.info(
                "search_amenities_success",
                duration_ms=round(duration * 1000, 2),
                result_count=len(result.get("data", [])) if isinstance(result, dict) else 0,
                search_term=request.search,
                group_filter=request.group_id
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "search_amenities_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                params=request.model_dump()
            )
            raise
