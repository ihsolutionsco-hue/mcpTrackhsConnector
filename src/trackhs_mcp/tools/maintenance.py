from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import logging
import time
from datetime import datetime, date

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
    
    @field_validator('date_received')
    @classmethod
    def validate_date_received(cls, v):
        try:
            received_date = datetime.strptime(v, "%Y-%m-%d").date()
            today = date.today()
            if received_date > today:
                raise ValueError("Fecha de recepción no puede ser futura")
            if (today - received_date).days > 365:
                raise ValueError("Fecha de recepción no puede ser mayor a 1 año")
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            raise e
        return v
    
    @field_validator('estimated_cost')
    @classmethod
    def validate_estimated_cost(cls, v):
        if v > 100000:
            raise ValueError("Costo estimado demasiado alto (máximo $100,000)")
        return v
    
    @field_validator('estimated_time')
    @classmethod
    def validate_estimated_time(cls, v):
        if v > 1440:  # 24 horas en minutos
            raise ValueError("Tiempo estimado demasiado alto (máximo 24 horas)")
        return v

class CreateHousekeepingWORequest(BaseModel):
    """Parámetros para crear orden de trabajo de housekeeping"""
    scheduled_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha programada (YYYY-MM-DD)")
    status: str = Field(..., description="Estado: pending, in-progress, completed")
    unit_id: int = Field(..., ge=1, description="ID de la unidad")
    clean_type_id: Optional[int] = Field(None, description="ID del tipo de limpieza")
    is_inspection: Optional[bool] = Field(None, description="Es inspección: true/false")
    
    @field_validator('scheduled_at')
    @classmethod
    def validate_scheduled_at(cls, v):
        try:
            scheduled_date = datetime.strptime(v, "%Y-%m-%d").date()
            today = date.today()
            if scheduled_date < today:
                raise ValueError("Fecha programada no puede ser pasada")
            if (scheduled_date - today).days > 30:
                raise ValueError("Fecha programada no puede ser mayor a 30 días")
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            raise e
        return v
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid = ["pending", "not-started", "in-progress", "completed", "cancelled", "exception"]
        if v not in valid:
            raise ValueError(f"Status inválido. Válidos: {', '.join(valid)}")
        return v
    
    @field_validator('unit_id')
    @classmethod
    def validate_unit_id(cls, v):
        if v > 10000:
            raise ValueError("ID de unidad demasiado alto")
        return v
    
    @field_validator('clean_type_id')
    @classmethod
    def validate_clean_type_id(cls, v):
        if v is not None:
            if v < 1 or v > 20:
                raise ValueError("ID de tipo de limpieza debe estar entre 1 y 20")
        return v

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
        start_time = time.time()
        logger.info("create_maintenance_wo_called", params=request.model_dump())
        
        try:
            result = await client.post("/api/pms/maintenance/work-orders", 
                                      json=request.model_dump(exclude_none=True))
            
            duration = time.time() - start_time
            logger.info(
                "create_maintenance_wo_success",
                duration_ms=round(duration * 1000, 2),
                work_order_id=result.get("id") if isinstance(result, dict) else None,
                priority=request.priority,
                unit_id=request.unit_id
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "create_maintenance_wo_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                params=request.model_dump()
            )
            raise
    
    @mcp.tool()
    async def create_housekeeping_work_order(request: CreateHousekeepingWORequest) -> dict:
        """Crea orden de trabajo de housekeeping.
        
        CUÁNDO USAR:
        - "Limpiar habitación 101" → unit_id=101, status="pending"
        - "Inspección pre-checkin" → is_inspection=true
        - "Limpieza profunda" → clean_type_id=2
        """
        start_time = time.time()
        logger.info("create_housekeeping_wo_called", params=request.model_dump())
        
        try:
            result = await client.post("/api/pms/housekeeping/work-orders", 
                                      json=request.model_dump(exclude_none=True))
            
            duration = time.time() - start_time
            logger.info(
                "create_housekeeping_wo_success",
                duration_ms=round(duration * 1000, 2),
                work_order_id=result.get("id") if isinstance(result, dict) else None,
                unit_id=request.unit_id,
                is_inspection=request.is_inspection
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "create_housekeeping_wo_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                params=request.model_dump()
            )
            raise
