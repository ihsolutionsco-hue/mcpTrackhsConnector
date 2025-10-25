from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

class SearchUnitsRequest(BaseModel):
    """Parámetros para buscar unidades disponibles"""
    page: int = Field(default=1, ge=1, description="Página (1-based)")
    size: int = Field(default=2, ge=1, le=25, description="Resultados. Voz: 2-3")
    bedrooms: Optional[str] = Field(None, description="Número de habitaciones")
    bathrooms: Optional[str] = Field(None, description="Número de baños")
    pets_friendly: Optional[str] = Field(None, pattern="^[01]$", description="Acepta mascotas: 1=si, 0=no")
    is_active: Optional[str] = Field(None, pattern="^[01]$", description="Unidad activa: 1=si, 0=no")
    
    @field_validator('bedrooms', 'bathrooms')
    @classmethod
    def validate_numeric_fields(cls, v):
        if v is not None:
            try:
                num = int(v)
                if num < 0 or num > 20:
                    raise ValueError("Valor fuera del rango válido (0-20)")
            except ValueError:
                raise ValueError("Debe ser un número válido")
        return v
    
    @field_validator('bedrooms')
    @classmethod
    def validate_bedrooms_logic(cls, v, info):
        if v is not None and 'bathrooms' in info.data and info.data['bathrooms'] is not None:
            bedrooms = int(v)
            bathrooms = int(info.data['bathrooms'])
            if bedrooms > 0 and bathrooms == 0:
                raise ValueError("Unidades con dormitorios deben tener al menos 1 baño")
        return v

def register_unit_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def search_units(request: SearchUnitsRequest) -> dict:
        """Busca unidades disponibles con filtros.
        
        CUÁNDO USAR:
        - "¿Qué habitaciones hay disponibles?" → sin filtros
        - "Habitaciones con 2 dormitorios" → bedrooms="2"
        - "Unidades que aceptan mascotas" → pets_friendly="1"
        """
        start_time = time.time()
        logger.info("search_units_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/pms/units", 
                                     params=request.model_dump(exclude_none=True))
            
            duration = time.time() - start_time
            logger.info(
                "search_units_success",
                duration_ms=round(duration * 1000, 2),
                result_count=len(result.get("data", [])) if isinstance(result, dict) else 0,
                filters_applied=len([k for k, v in request.model_dump().items() if v is not None])
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "search_units_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                params=request.model_dump()
            )
            raise
