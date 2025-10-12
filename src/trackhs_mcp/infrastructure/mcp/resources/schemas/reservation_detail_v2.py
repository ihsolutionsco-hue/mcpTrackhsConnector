"""
Schema resources para Get Reservation V2
Información esencial del esquema de datos para obtener reserva individual
"""

from typing import Any, Dict

from ....application.ports.api_client_port import ApiClientPort


def register_reservation_detail_v2_schema(mcp, api_client: ApiClientPort):
    """Registra el schema de Get Reservation V2"""

    @mcp.resource(
        "trackhs://schema/reservation-detail-v2",
        name="Reservation Detail V2 Schema",
        description="Schema for Get Reservation V2 API",
        mime_type="application/json",
    )
    async def reservation_detail_v2_schema() -> Dict[str, Any]:
        """Schema esencial para Get Reservation V2"""
        return {
            "endpoint": "/v2/pms/reservations/{reservationId}",
            "method": "GET",
            "version": "2.0",
            "description": "Get individual reservation with enriched data",
            "fields": {
                "id": "integer - ID único de la reserva",
                "alternates": "array - IDs de confirmación alternativos",
                "currency": "string - Moneda de la reserva",
                "unitId": "integer - ID de la unidad",
                "arrivalDate": "string - Fecha de llegada (ISO 8601)",
                "departureDate": "string - Fecha de salida (ISO 8601)",
                "nights": "number - Número de noches",
                "status": "string - Hold|Confirmed|Checked In|Checked Out|Cancelled",
                "contactId": "integer - ID del contacto",
                "channelId": "integer - ID del canal",
                "userId": "integer - ID del usuario",
                "travelAgentId": "integer - ID del agente de viajes",
                "campaignId": "integer - ID de la campaña",
                "unitTypeId": "integer - ID del tipo de unidad",
                "rateTypeId": "integer - ID del tipo de tarifa",
                "reservationTypeId": "integer - ID del tipo de reserva",
                "createdAt": "string - Fecha de creación (ISO 8601)",
                "updatedAt": "string - Fecha de actualización (ISO 8601)",
                "bookedAt": "string - Fecha de reserva (ISO 8601)",
            },
            "financial_data": {
                "guestBreakdown": "object - Desglose financiero del huésped",
                "ownerBreakdown": "object - Desglose financiero del propietario",
                "securityDeposit": "object - Información del depósito de seguridad",
                "paymentPlan": "array - Plan de pagos programado",
            },
            "embedded_objects": {
                "unit": "object - Información completa de la unidad",
                "contact": "object - Información del contacto",
                "guaranteePolicy": "object - Política de garantía",
                "cancellationPolicy": "object - Política de cancelación",
                "user": "object - Usuario que creó/actualizó",
                "type": "object - Tipo de reservación",
                "rateType": "object - Tipo de tarifa",
            },
            "occupants": {
                "type": "array - Lista de ocupantes",
                "fields": {
                    "typeId": "integer - ID del tipo de ocupante",
                    "name": "string - Nombre del ocupante",
                    "quantity": "number - Cantidad",
                    "included": "boolean - Si está incluido en el precio",
                },
            },
            "error_codes": {
                "401": "No autorizado - Credenciales inválidas",
                "403": "Prohibido - Permisos insuficientes",
                "404": "No encontrado - Reserva no existe",
                "500": "Error interno del servidor",
            },
        }
