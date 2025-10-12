"""
Herramienta MCP para obtener una reserva específica por ID en TrackHS API V2
Basado en el endpoint GET /v2/pms/reservations/{reservationId}
"""

from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort
from ...application.use_cases.get_reservation import GetReservationUseCase
from ...domain.entities.reservations import GetReservationParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler


def register_get_reservation_v2(mcp, api_client: ApiClientPort):
    """Registra la herramienta get_reservation_v2"""

    @mcp.tool
    @error_handler("get_reservation_v2")
    async def get_reservation_v2(reservation_id: int) -> Dict[str, Any]:
        """
        Obtiene una reserva específica por ID desde TrackHS API V2.

        Esta herramienta MCP permite obtener todos los detalles de una reserva
        individual, incluyendo información financiera completa, datos embebidos
        de unidad, contacto, políticas y más.

        **Características Principales:**
        - ✅ Obtiene reserva completa por ID
        - ✅ Incluye datos embebidos (unit, contact, policies, user, etc.)
        - ✅ Información financiera detallada (guest_breakdown, owner_breakdown)
        - ✅ Datos de ocupantes y políticas
        - ✅ Manejo robusto de errores
        - ✅ Optimizado para integración con modelos de IA

        **Casos de Uso:**
        - Verificar detalles de una reserva específica
        - Análisis financiero de reserva individual
        - Validación de estado y políticas
        - Extracción de información de contacto
        - Auditoría de reservas

        **Ejemplos de Uso:**

        # Obtener reserva por ID
        get_reservation_v2(reservation_id=12345)

        # Verificar estado de reserva
        get_reservation_v2(reservation_id=67890)

        # Análisis financiero
        get_reservation_v2(reservation_id=11111)

        **Parámetros:**
        - reservation_id: ID único de la reserva (entero positivo requerido)

        **Respuesta:**
        Objeto completo de reserva con:
        - Datos básicos: ID, estado, fechas, huésped, unidad
        - Información financiera: breakdowns, tarifas, impuestos, pagos
        - Datos embebidos: unit, contact, policies, user, type, rateType
        - Ocupantes y políticas de garantía/cancelación
        - Enlaces y metadatos

        **Manejo de Errores:**
        - 401: Credenciales inválidas o expiradas
        - 403: Permisos insuficientes para acceder a la reserva
        - 404: Reserva no encontrada con el ID especificado
        - 500: Error interno del servidor de TrackHS

        **Notas Importantes:**
        - El ID debe ser un entero positivo válido
        - La respuesta incluye todos los datos embebidos disponibles
        - Los datos financieros están en formato de string para precisión
        - Las fechas están en formato ISO 8601
        """
        # Validar parámetros de entrada
        if not reservation_id or reservation_id <= 0:
            raise ValidationError(
                "reservation_id debe ser un entero positivo mayor que 0",
                "reservation_id",
            )

        try:
            # Crear caso de uso
            use_case = GetReservationUseCase(api_client)

            # Crear parámetros
            params = GetReservationParams(reservation_id=reservation_id)

            # Ejecutar caso de uso
            reservation = await use_case.execute(params)

            # Convertir a diccionario para respuesta MCP
            return reservation.model_dump(by_alias=True, exclude_none=True)

        except Exception as e:
            # Manejar errores específicos de la API
            if hasattr(e, "status_code"):
                if e.status_code == 401:
                    raise ValidationError(
                        "No autorizado: Credenciales de autenticación inválidas. "
                        "Por favor verifica que TRACKHS_USERNAME y TRACKHS_PASSWORD "
                        "sean correctos y no hayan expirado.",
                        "auth",
                    )
                elif e.status_code == 403:
                    raise ValidationError(
                        "Prohibido: Permisos insuficientes para acceder a esta reserva. "
                        "Por favor verifica que tu cuenta tenga acceso a "
                        "los endpoints de PMS/Reservations.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Reserva no encontrada: No existe una reserva con ID {reservation_id}. "
                        "Por favor verifica que el ID sea correcto y que la reserva exista.",
                        "reservation_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API de TrackHS está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte técnico.",
                        "api",
                    )

            # Re-lanzar otros errores con contexto
            raise ValidationError(f"Error al obtener la reserva: {str(e)}", "api")
