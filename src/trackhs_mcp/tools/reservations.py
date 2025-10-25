from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import logging

logger = logging.getLogger(__name__)

# Schemas
class SearchReservationsRequest(BaseModel):
    """Parámetros para buscar reservas"""
    page: int = Field(default=0, ge=0, description="Página (0-based)")
    size: int = Field(default=3, ge=1, le=100, description="Resultados. Voz: 3-5")
    search: Optional[str] = Field(None, max_length=200, description="Nombre huésped")
    status: Optional[str] = Field(None, description="Confirmed, Checked In, Cancelled")
    arrival_start: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    arrival_end: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v:
            valid = ["Hold", "Confirmed", "Cancelled", "Checked In", "Checked Out"]
            statuses = [s.strip() for s in v.split(",")]
            if not all(s in valid for s in statuses):
                raise ValueError(f"Status inválido. Válidos: {', '.join(valid)}")
        return v

class GetReservationRequest(BaseModel):
    """Parámetros para obtener una reserva específica"""
    reservation_id: str = Field(..., pattern=r"^\d+$", description="ID de reserva")

# Tools
def register_reservation_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def search_reservations(request: SearchReservationsRequest) -> dict:
        """Busca reservas en TrackHS.
        
        CUÁNDO USAR:
        - "¿Tengo una reserva?" → search="nombre"
        - "Reservas de hoy" → arrival_start=hoy
        - "¿Quién está en el hotel?" → status="Checked In"
        """
        logger.info("search_reservations_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/v2/pms/reservations", 
                                     params=request.model_dump(exclude_none=True))
            logger.info("search_reservations_success")
            return result
        except Exception as e:
            logger.error("search_reservations_error", error=str(e))
            raise
    
    @mcp.tool()
    async def get_reservation(request: GetReservationRequest) -> dict:
        """Obtiene detalles completos de una reserva por ID.
        
        CUÁNDO USAR:
        - "Dame detalles de la reserva 12345" → reservation_id="12345"
        - Verificar información específica de una reserva
        """
        logger.info("get_reservation_called", reservation_id=request.reservation_id)
        
        try:
            result = await client.get(f"/api/v2/pms/reservations/{request.reservation_id}")
            logger.info("get_reservation_success")
            return result
        except Exception as e:
            logger.error("get_reservation_error", error=str(e))
            raise
