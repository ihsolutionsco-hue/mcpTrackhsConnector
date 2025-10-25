from fastmcp import FastMCP
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class GetFolioRequest(BaseModel):
    """Parámetros para obtener un folio específico"""
    folio_id: str = Field(..., pattern=r"^\d+$", description="ID del folio")

def register_folio_tools(mcp: FastMCP, client):
    
    @mcp.tool()
    async def get_folio(request: GetFolioRequest) -> dict:
        """Obtiene detalles de un folio por ID.
        
        CUÁNDO USAR:
        - "Dame el folio 12345" → folio_id="12345"
        - Verificar información financiera de un folio
        - Consultar pagos y saldos
        """
        logger.info("get_folio_called", folio_id=request.folio_id)
        
        try:
            result = await client.get(f"/api/pms/folios/{request.folio_id}")
            logger.info("get_folio_success")
            return result
        except Exception as e:
            logger.error("get_folio_error", error=str(e))
            raise
