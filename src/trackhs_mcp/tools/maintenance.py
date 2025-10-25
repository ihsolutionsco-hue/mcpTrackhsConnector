from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import logging

logger = logging.getLogger(__name__)

# Schemas
class CreateMaintenanceWORequest(BaseModel):
    """Parámetros para crear orden de trabajo de mantenimiento"""
    summary: str = Field(..., min_length=1, max_length=500, description="Resumen del problema")
    status: str = Field(..., description="Estado: open, in-progress, completed")
    date_received: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de recepción (YYYY-MM-DD)")
    priority: Literal["trivial", "low", "medium", "high", "critical"] = Field(..., description="Prioridad del trabajo")
    estimated_cost: float = Field(..., ge=0, description="Costo estimado")
    estimated_time: int = Field(..., ge=1, description="Tiempo estimado en minutos")
    unit_id: Optional[int] = Field(default=1, description="ID de la unidad")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid = ["open", "not-started", "in-progress", "completed", "cancelled"]
        if v not in valid:
            raise ValueError(f"Status inválido. Válidos: {', '.join(valid)}")
        return v

class CreateHousekeepingWORequest(BaseModel):
    """Parámetros para crear orden de trabajo de housekeeping"""
    scheduled_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha programada (YYYY-MM-DD)")
    status: str = Field(..., description="Estado: pending, in-progress, completed")
    unit_id: int = Field(..., ge=1, description="ID de la unidad")
    clean_type_id: Optional[int] = Field(None, description="ID del tipo de limpieza")
    is_inspection: Optional[bool] = Field(None, description="Es inspección: true/false")

# Tools
def register_maintenance_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def create_maintenance_work_order(request: CreateMaintenanceWORequest) -> dict:
        """Crea orden de trabajo de mantenimiento.
        
        CUÁNDO USAR:
        - "El aire acondicionado no funciona" → summary="AC not working", priority="high"
        - "Fuga de agua en baño" → summary="Water leak in bathroom", priority="critical"
        - "Luz del pasillo fundida" → summary="Hallway light out", priority="low"
        """
        logger.info("create_maintenance_wo_called", params=request.model_dump())
        
        try:
            result = await client.post("/api/pms/maintenance/work-orders", 
                                      json=request.model_dump(exclude_none=True))
            logger.info("create_maintenance_wo_success")
            return result
        except Exception as e:
            logger.error("create_maintenance_wo_error", error=str(e))
            raise
    
    @mcp.tool()
    async def create_housekeeping_work_order(request: CreateHousekeepingWORequest) -> dict:
        """Crea orden de trabajo de housekeeping.
        
        CUÁNDO USAR:
        - "Limpiar habitación 101" → unit_id=101, status="pending"
        - "Inspección pre-checkin" → is_inspection=true
        - "Limpieza profunda" → clean_type_id=2
        """
        logger.info("create_housekeeping_wo_called", params=request.model_dump())
        
        try:
            result = await client.post("/api/pms/housekeeping/work-orders", 
                                      json=request.model_dump(exclude_none=True))
            logger.info("create_housekeeping_wo_success")
            return result
        except Exception as e:
            logger.error("create_housekeeping_wo_error", error=str(e))
            raise
