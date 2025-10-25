from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import logging
import time
from datetime import datetime

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
    
    @field_validator('arrival_start', 'arrival_end')
    @classmethod
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
        return v
    
    @field_validator('arrival_end')
    @classmethod
    def validate_date_range(cls, v, info):
        if v and 'arrival_start' in info.data and info.data['arrival_start']:
            start_date = datetime.strptime(info.data['arrival_start'], "%Y-%m-%d")
            end_date = datetime.strptime(v, "%Y-%m-%d")
            if end_date < start_date:
                raise ValueError("arrival_end debe ser posterior a arrival_start")
        return v

class GetReservationRequest(BaseModel):
    """Parámetros para obtener una reserva específica"""
    reservation_id: str = Field(..., pattern=r"^\d+$", description="ID de reserva")
    
    @field_validator('reservation_id')
    @classmethod
    def validate_reservation_id(cls, v):
        if not v.isdigit():
            raise ValueError("ID de reserva debe ser numérico")
        if len(v) > 20:
            raise ValueError("ID de reserva demasiado largo")
        return v

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
        start_time = time.time()
        logger.info("search_reservations_called", params=request.model_dump())
        
        try:
            result = await client.get("/api/v2/pms/reservations", 
                                     params=request.model_dump(exclude_none=True))
            
            duration = time.time() - start_time
            logger.info(
                "search_reservations_success",
                duration_ms=round(duration * 1000, 2),
                result_count=len(result.get("data", [])) if isinstance(result, dict) else 0
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "search_reservations_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                params=request.model_dump()
            )
            raise
    
    @mcp.tool()
    async def get_reservation(request: GetReservationRequest) -> dict:
        """Obtiene detalles completos de una reserva por ID.
        
        CUÁNDO USAR:
        - "Dame detalles de la reserva 12345" → reservation_id="12345"
        - Verificar información específica de una reserva
        """
        start_time = time.time()
        logger.info("get_reservation_called", reservation_id=request.reservation_id)
        
        try:
            result = await client.get(f"/api/v2/pms/reservations/{request.reservation_id}")
            
            duration = time.time() - start_time
            logger.info(
                "get_reservation_success",
                duration_ms=round(duration * 1000, 2),
                reservation_id=request.reservation_id,
                has_guest_info="guest" in result if isinstance(result, dict) else False
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "get_reservation_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                reservation_id=request.reservation_id
            )
            raise
