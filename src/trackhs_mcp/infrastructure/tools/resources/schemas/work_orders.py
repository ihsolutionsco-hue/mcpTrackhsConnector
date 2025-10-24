"""
Schema resources para Work Orders (Maintenance)
Información esencial del esquema de datos para órdenes de trabajo de mantenimiento
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_work_orders_schema(mcp, api_client: "ApiClientPort"):
    """Registra el schema de Work Orders"""

    @mcp.resource(
        "trackhs://schema/work-orders",
        name="Work Orders Schema",
        description="Schema for Maintenance Work Orders API",
        mime_type="application/json",
    )
    async def work_orders_schema() -> Dict[str, Any]:
        """Schema esencial para Work Orders API"""
        return {
            "endpoint": "/api/pms/maintenance/work-orders",
            "method": "POST",
            "version": "1.0",
            "description": "Create maintenance work orders in TrackHS",
            "required_fields": {
                "dateReceived": "string - Fecha de recepción (ISO 8601: YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)",
                "priority": "integer - Prioridad (1=Baja, 3=Media, 5=Alta)",
                "status": "string - Estado de la orden (ver estados válidos)",
                "summary": "string - Resumen de la orden de trabajo",
                "estimatedCost": "number - Costo estimado (>= 0)",
                "estimatedTime": "integer - Tiempo estimado en minutos (> 0)",
            },
            "optional_fields": {
                "dateScheduled": "string - Fecha programada (ISO 8601)",
                "userId": "integer - ID del usuario responsable (> 0)",
                "vendorId": "integer - ID del proveedor asignado (> 0)",
                "unitId": "integer - ID de la unidad relacionada (> 0)",
                "reservationId": "integer - ID de la reserva relacionada (> 0)",
                "referenceNumber": "string - Número de referencia",
                "description": "string - Descripción detallada",
                "workPerformed": "string - Trabajo realizado",
                "source": "string - Fuente de la orden",
                "sourceName": "string - Nombre de la fuente",
                "sourcePhone": "string - Teléfono de la fuente",
                "actualTime": "integer - Tiempo real en minutos (> 0)",
                "blockCheckin": "boolean - Si debe bloquear el check-in",
            },
            "valid_statuses": {
                "open": "Abierta",
                "not-started": "No iniciada",
                "in-progress": "En progreso",
                "completed": "Completada",
                "processed": "Procesada",
                "vendor-assigned": "Asignada a proveedor",
                "vendor-accepted": "Aceptada por proveedor",
                "vendor-rejected": "Rechazada por proveedor",
                "vendor-completed": "Completada por proveedor",
                "cancelled": "Cancelada",
            },
            "valid_priorities": {
                "1": "Baja prioridad",
                "3": "Media prioridad",
                "5": "Alta prioridad",
            },
            "validation_rules": {
                "dateReceived": "Debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)",
                "dateScheduled": "Debe estar en formato ISO 8601 si se proporciona",
                "priority": "Debe ser 1, 3 o 5",
                "status": "Debe ser uno de los estados válidos listados arriba",
                "estimatedCost": "Debe ser >= 0",
                "estimatedTime": "Debe ser > 0",
                "userId": "Debe ser un entero positivo si se proporciona",
                "vendorId": "Debe ser un entero positivo si se proporciona",
                "unitId": "Debe ser un entero positivo si se proporciona",
                "reservationId": "Debe ser un entero positivo si se proporciona",
                "actualTime": "Debe ser > 0 si se proporciona",
                "blockCheckin": "Debe ser true o false",
            },
            "response_structure": {
                "success": "boolean - Indica si la operación fue exitosa",
                "work_order": "object - Objeto de la orden de trabajo creada",
                "message": "string - Mensaje descriptivo del resultado",
                "error": "string - Tipo de error si hubo fallo (opcional)",
            },
            "best_practices": [
                "Usar formato ISO 8601 completo para fechas con hora específica",
                "Validar IDs antes de enviar (usuario, proveedor, unidad, reserva)",
                "Proporcionar descripción detallada para mejor seguimiento",
                "Usar prioridad 5 (Alta) solo para emergencias",
                "Incluir información de contacto en source* para seguimiento",
                "Usar blockCheckin=true solo cuando sea absolutamente necesario",
                "Proporcionar estimaciones realistas de costo y tiempo",
            ],
        }
