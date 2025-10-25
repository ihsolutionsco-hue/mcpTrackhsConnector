from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
import logging
import time

logger = logging.getLogger(__name__)

class GetFolioRequest(BaseModel):
    """Parámetros para obtener un folio específico"""
    folio_id: str = Field(..., pattern=r"^\d+$", description="ID del folio")
    
    @field_validator('folio_id')
    @classmethod
    def validate_folio_id(cls, v):
        if not v.isdigit():
            raise ValueError("ID de folio debe ser numérico")
        if len(v) > 20:
            raise ValueError("ID de folio demasiado largo")
        if int(v) <= 0:
            raise ValueError("ID de folio debe ser positivo")
        return v

def register_folio_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def get_folio(request: GetFolioRequest) -> dict:
        """Obtiene detalles de un folio por ID.
        
        CUÁNDO USAR:
        - "Dame el folio 12345" → folio_id="12345"
        - Verificar información financiera de un folio
        - Consultar pagos y saldos
        """
        start_time = time.time()
        logger.info("get_folio_called", folio_id=request.folio_id)
        
        try:
            result = await client.get(f"/api/pms/folios/{request.folio_id}")
            
            duration = time.time() - start_time
            logger.info(
                "get_folio_success",
                duration_ms=round(duration * 1000, 2),
                folio_id=request.folio_id,
                has_balance="balance" in result if isinstance(result, dict) else False
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "get_folio_error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                folio_id=request.folio_id
            )
            raise
