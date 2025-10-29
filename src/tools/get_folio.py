"""
Herramienta para obtener folio financiero
"""

from typing import Any, Dict

from pydantic import BaseModel

from ..schemas.folio import FolioResponse
from ..utils.exceptions import TrackHSAPIError, TrackHSNotFoundError
from ..utils.validators import validate_positive_integer
from .base import BaseTool


class GetFolioParams(BaseModel):
    """Parámetros para obtener folio"""

    reservation_id: int


class GetFolioTool(BaseTool):
    """Herramienta para obtener folio financiero de una reserva"""

    @property
    def name(self) -> str:
        return "get_folio"

    @property
    def description(self) -> str:
        return """
        Obtener el folio financiero completo de una reserva.

        Proporciona información detallada sobre:
        - Items del folio (cargos, créditos, impuestos, tarifas)
        - Desglose por categorías (huésped, propietario)
        - Montos totales y balance
        - Información de pagos

        Args:
            reservation_id: ID de la reserva para obtener su folio financiero

        Returns:
            Folio financiero completo de la reserva
        """

    @property
    def input_schema(self) -> type:
        return GetFolioParams

    @property
    def output_schema(self) -> type:
        return FolioResponse

    def _execute_logic(self, validated_input: GetFolioParams) -> Dict[str, Any]:
        """
        Ejecuta la obtención del folio

        Args:
            validated_input: Parámetros validados

        Returns:
            Folio financiero
        """
        reservation_id = validated_input.reservation_id

        # Validar ID de reserva
        try:
            validated_id = validate_positive_integer(reservation_id, "reservation_id")
        except Exception as e:
            self.logger.error(
                f"ID de reserva inválido: {reservation_id}",
                extra={"reservation_id": reservation_id, "error": str(e)},
            )
            raise

        # Realizar llamada a la API
        try:
            result = self.api_client.get(f"api/pms/reservations/{validated_id}/folio")

            # Procesar resultado
            processed_result = self._process_api_response(result, validated_id)

            return processed_result

        except TrackHSNotFoundError:
            # Re-lanzar error de no encontrado
            raise
        except Exception as e:
            self.logger.error(
                f"Error obteniendo folio de reserva {validated_id}",
                extra={
                    "reservation_id": validated_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise TrackHSAPIError(f"Error obteniendo folio: {str(e)}")

    def _process_api_response(
        self, api_result: Dict[str, Any], reservation_id: int
    ) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API

        Args:
            api_result: Respuesta de la API
            reservation_id: ID de la reserva

        Returns:
            Folio procesado
        """
        # Procesar items del folio
        items = api_result.get("items", [])
        processed_items = []

        for item in items:
            processed_item = {
                "id": item.get("id"),
                "description": item.get("description"),
                "amount": item.get("amount"),
                "currency": item.get("currency"),
                "category": item.get("category"),
                "type": item.get("type"),
                "date": item.get("date"),
            }
            processed_items.append(processed_item)

        # Mapear campos principales
        processed = {
            "reservation_id": reservation_id,
            "total_amount": api_result.get("totalAmount", 0.0),
            "currency": api_result.get("currency", "USD"),
            "balance": api_result.get("balance", 0.0),
            "items": processed_items,
            "guest_charges": api_result.get("guestCharges"),
            "owner_charges": api_result.get("ownerCharges"),
            "taxes": api_result.get("taxes"),
            "fees": api_result.get("fees"),
            "created_at": api_result.get("createdAt"),
            "updated_at": api_result.get("updatedAt"),
            "links": api_result.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}
