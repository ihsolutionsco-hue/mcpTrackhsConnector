"""
Resources MCP para Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort
from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_all_resources(mcp, api_client: ApiClientPort):
    """Registra todos los resources MCP"""

    @mcp.resource("trackhs://schema/reservations")
    async def reservations_schema() -> Dict[str, Any]:
        """Esquema completo de datos para reservas en TrackHS API V2"""
        return {
            "schema": {
                "id": {"type": "integer", "description": "ID único de la reserva"},
                "alternates": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs de confirmación alternativos",
                },
                "currency": {"type": "string", "description": "Moneda de la reserva"},
                "unit_id": {"type": "integer", "description": "ID de la unidad"},
                "unitId": {"type": "integer", "description": "ID de la unidad (camelCase)"},
                "is_unit_locked": {
                    "type": "boolean",
                    "description": "Si la unidad está bloqueada",
                },
                "is_unit_assigned": {
                    "type": "boolean",
                    "description": "Si la unidad está asignada",
                },
                "is_unit_type_locked": {
                    "type": "boolean",
                    "description": "Si el tipo de unidad está bloqueado",
                },
                "unit_type_id": {
                    "type": "integer",
                    "description": "ID del tipo de unidad",
                },
                "arrival_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de llegada (ISO 8601)",
                },
                "arrivalDate": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de llegada (camelCase)",
                },
                "departure_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de salida (ISO 8601)",
                },
                "departureDate": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de salida (camelCase)",
                },
                "early_arrival": {"type": "boolean", "description": "Llegada temprana"},
                "late_departure": {"type": "boolean", "description": "Salida tardía"},
                "arrival_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Hora de llegada (ISO 8601)",
                },
                "departure_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Hora de salida (ISO 8601)",
                },
                "nights": {"type": "number", "description": "Número de noches"},
                "status": {
                    "type": "string",
                    "enum": [
                        "Hold",
                        "Confirmed",
                        "Checked Out",
                        "Checked In",
                        "Cancelled",
                    ],
                    "description": "Estado de la reserva",
                },
                "cancelled_at": {
                    "type": "string",
                    "format": "date-time",
                    "nullable": True,
                    "description": "Fecha de cancelación (ISO 8601)",
                },
                "occupants": {
                    "type": "array",
                    "items": {"$re": "#/definitions/Occupant"},
                    "description": "Ocupantes",
                },
                "security_deposit": {
                    "$re": "#/definitions/SecurityDeposit",
                    "description": "Depósito de seguridad",
                },
                "updated_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de actualización (ISO 8601)",
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de creación (ISO 8601)",
                },
                "booked_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de reserva (ISO 8601)",
                },
                "guest_breakdown": {
                    "$re": "#/definitions/GuestBreakdown",
                    "description": "Desglose del huésped",
                },
                "owner_breakdown": {
                    "$re": "#/definitions/OwnerBreakdown",
                    "description": "Desglose del propietario",
                },
                "contact_id": {"type": "integer", "description": "ID del contacto"},
                "channel_id": {"type": "integer", "description": "ID del canal"},
                "sub_channel": {
                    "type": "string",
                    "nullable": True,
                    "description": "Subcanal",
                },
                "folio_id": {"type": "integer", "description": "ID del folio"},
                "guarantee_policy_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de la política de garantía",
                },
                "cancellation_policy_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de la política de cancelación",
                },
                "cancellation_reason_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de la razón de cancelación",
                },
                "user_id": {"type": "integer", "description": "ID del usuario"},
                "travel_agent_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID del agente de viajes",
                },
                "campaign_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de la campaña",
                },
                "type_id": {"type": "integer", "description": "ID del tipo"},
                "rate_type_id": {
                    "type": "integer",
                    "description": "ID del tipo de tarifa",
                },
                "unit_code_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID del código de unidad",
                },
                "cancelled_by_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de quien canceló",
                },
                "payment_method_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID del método de pago",
                },
                "quote_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID de la cotización",
                },
                "hold_expires_at": {
                    "type": "string",
                    "format": "date-time",
                    "nullable": True,
                    "description": "Fecha de expiración de la retención",
                },
                "is_taxable": {"type": "boolean", "description": "Si es gravable"},
                "invite_uuid": {
                    "type": "string",
                    "nullable": True,
                    "description": "UUID de la invitación",
                },
                "uuid": {"type": "string", "description": "UUID de la reserva"},
                "source": {"type": "string", "description": "Fuente de la reserva"},
                "is_channel_locked": {
                    "type": "boolean",
                    "description": "Si el canal está bloqueado",
                },
                "agreement_status": {
                    "type": "string",
                    "enum": ["not-needed", "not-sent", "sent", "viewed", "received"],
                    "description": "Estado del acuerdo",
                },
                "automate_payment": {
                    "type": "boolean",
                    "description": "Si el pago es automático",
                },
                "revenue_realized_method": {
                    "type": "string",
                    "description": "Método de realización de ingresos",
                },
                "schedule_type1": {
                    "type": "string",
                    "nullable": True,
                    "description": "Tipo de programación 1",
                },
                "schedule_percentage1": {
                    "type": "number",
                    "nullable": True,
                    "description": "Porcentaje de programación 1",
                },
                "schedule_type2": {
                    "type": "string",
                    "nullable": True,
                    "description": "Tipo de programación 2",
                },
                "schedule_percentage2": {
                    "type": "number",
                    "nullable": True,
                    "description": "Porcentaje de programación 2",
                },
                "promo_code_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID del código promocional",
                },
                "updated_by": {"type": "string", "description": "Actualizado por"},
                "created_by": {"type": "string", "description": "Creado por"},
                "group_id": {
                    "type": "integer",
                    "nullable": True,
                    "description": "ID del grupo",
                },
                "payment_plan": {
                    "type": "array",
                    "items": {"$re": "#/definitions/PaymentPlan"},
                    "description": "Plan de pagos",
                },
                "travel_insurance_products": {
                    "type": "array",
                    "items": {"$re": "#/definitions/TravelInsuranceProduct"},
                    "description": "Productos de seguro de viaje",
                },
                "_embedded": {"type": "object", "description": "Datos embebidos"},
                "_links": {"type": "object", "description": "Enlaces"},
            },
            "definitions": {
                "Occupant": {
                    "type": "object",
                    "properties": {
                        "type_id": {
                            "type": "integer",
                            "description": "ID del tipo de ocupante",
                        },
                        "name": {
                            "type": "string",
                            "description": "Nombre del ocupante",
                        },
                        "handle": {
                            "type": "string",
                            "description": "Handle del ocupante",
                        },
                        "quantity": {"type": "number", "description": "Cantidad"},
                        "included": {
                            "type": "boolean",
                            "description": "Si está incluido en el precio de renta",
                        },
                        "extra_quantity": {
                            "type": "number",
                            "description": "Cantidad extra permitida",
                        },
                        "rate_per_person_per_stay": {
                            "type": "string",
                            "description": "Tarifa por persona por estadía",
                        },
                        "rate_per_stay": {
                            "type": "string",
                            "description": "Tarifa por estadía",
                        },
                    },
                },
                "SecurityDeposit": {
                    "type": "object",
                    "properties": {
                        "required": {
                            "type": "string",
                            "description": "Monto total requerido del depósito",
                        },
                        "remaining": {
                            "type": "number",
                            "description": "Monto restante del depósito de seguridad",
                        },
                    },
                },
                "GuestBreakdown": {
                    "type": "object",
                    "properties": {
                        "gross_rent": {"type": "string", "description": "Renta bruta"},
                        "guest_gross_display_rent": {
                            "type": "string",
                            "description": "Renta bruta mostrada al huésped",
                        },
                        "discount": {"type": "string", "description": "Descuento"},
                        "promo_value": {
                            "type": "string",
                            "description": "Valor promocional",
                        },
                        "discount_total": {
                            "type": "number",
                            "description": "Total de descuentos",
                        },
                        "net_rent": {"type": "string", "description": "Renta neta"},
                        "guest_net_display_rent": {
                            "type": "string",
                            "description": "Renta neta mostrada al huésped",
                        },
                        "actual_adr": {"type": "string", "description": "ADR actual"},
                        "guest_adr": {
                            "type": "string",
                            "description": "ADR del huésped",
                        },
                        "total_guest_fees": {
                            "type": "string",
                            "description": "Total de tarifas del huésped",
                        },
                        "total_rent_fees": {
                            "type": "string",
                            "description": "Total de tarifas de renta",
                        },
                        "total_itemized_fees": {
                            "type": "string",
                            "description": "Total de tarifas detalladas",
                        },
                        "total_tax_fees": {
                            "type": "string",
                            "description": "Total de tarifas de impuestos",
                        },
                        "total_service_fees": {
                            "type": "string",
                            "description": "Total de tarifas de servicio",
                        },
                        "folio_charges": {
                            "type": "string",
                            "description": "Cargos del folio",
                        },
                        "subtotal": {"type": "string", "description": "Subtotal"},
                        "guest_subtotal": {
                            "type": "string",
                            "description": "Subtotal del huésped",
                        },
                        "total_taxes": {
                            "type": "string",
                            "description": "Total de impuestos",
                        },
                        "total_guest_taxes": {
                            "type": "string",
                            "description": "Total de impuestos del huésped",
                        },
                        "total": {"type": "string", "description": "Total"},
                        "grand_total": {"type": "string", "description": "Gran total"},
                        "net_payments": {
                            "type": "string",
                            "description": "Pagos netos",
                        },
                        "payments": {"type": "string", "description": "Pagos"},
                        "refunds": {"type": "string", "description": "Reembolsos"},
                        "net_transfers": {
                            "type": "string",
                            "description": "Transferencias netas",
                        },
                        "balance": {"type": "string", "description": "Balance"},
                        "rates": {
                            "type": "array",
                            "items": {"$re": "#/definitions/Rate"},
                            "description": "Tarifas",
                        },
                        "guest_fees": {
                            "type": "array",
                            "items": {"$re": "#/definitions/GuestFee"},
                            "description": "Tarifas del huésped",
                        },
                        "taxes": {
                            "type": "array",
                            "items": {"$re": "#/definitions/Tax"},
                            "description": "Impuestos",
                        },
                    },
                },
                "OwnerBreakdown": {
                    "type": "object",
                    "properties": {
                        "gross_rent": {
                            "type": "string",
                            "description": "Renta bruta del propietario",
                        },
                        "fee_revenue": {
                            "type": "string",
                            "description": "Ingresos por tarifas",
                        },
                        "gross_revenue": {
                            "type": "string",
                            "description": "Ingresos brutos",
                        },
                        "manager_commission": {
                            "type": "string",
                            "description": "Comisión del manager",
                        },
                        "agent_commission": {
                            "type": "string",
                            "description": "Comisión del agente",
                        },
                        "net_revenue": {
                            "type": "string",
                            "description": "Ingresos netos",
                        },
                        "owner_fees": {
                            "type": "array",
                            "items": {"$re": "#/definitions/OwnerFee"},
                            "description": "Tarifas del propietario",
                        },
                    },
                },
                "Rate": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "format": "date",
                            "description": "Fecha",
                        },
                        "rate": {"type": "string", "description": "Tarifa"},
                        "nights": {"type": "integer", "description": "Noches"},
                        "is_quoted": {
                            "type": "boolean",
                            "description": "Si está cotizada",
                        },
                    },
                },
                "GuestFee": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "ID de la tarifa"},
                        "name": {
                            "type": "string",
                            "description": "Nombre de la tarifa",
                        },
                        "display_as": {
                            "type": "string",
                            "enum": ["itemize", "rent", "tax", "service"],
                            "description": "Cómo mostrar",
                        },
                        "quantity": {"type": "string", "description": "Cantidad"},
                        "unit_value": {
                            "type": "string",
                            "description": "Valor unitario",
                        },
                        "value": {"type": "string", "description": "Valor"},
                    },
                },
                "Tax": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "ID del impuesto"},
                        "name": {
                            "type": "string",
                            "description": "Nombre del impuesto",
                        },
                        "amount": {
                            "type": "string",
                            "description": "Monto del impuesto",
                        },
                    },
                },
                "OwnerFee": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "ID de la tarifa"},
                        "name": {
                            "type": "string",
                            "description": "Nombre de la tarifa",
                        },
                        "display_as": {
                            "type": "string",
                            "enum": ["itemize", "rent", "tax", "service"],
                            "description": "Cómo mostrar",
                        },
                        "quantity": {"type": "string", "description": "Cantidad"},
                        "unit_value": {
                            "type": "string",
                            "description": "Valor unitario",
                        },
                        "value": {"type": "string", "description": "Valor"},
                    },
                },
                "PaymentPlan": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "format": "date",
                            "description": "Fecha",
                        },
                        "amount": {"type": "string", "description": "Monto"},
                    },
                },
                "TravelInsuranceProduct": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "ID del producto"},
                        "status": {
                            "type": "string",
                            "enum": ["optin", "funded", "cancelled"],
                            "description": "Estado",
                        },
                        "type": {
                            "type": "string",
                            "enum": [
                                "Travel Insurance",
                                "Master Cancel",
                                "Damage Deposit",
                            ],
                            "description": "Tipo",
                        },
                        "provider": {"type": "string", "description": "Proveedor"},
                        "provider_id": {
                            "type": "integer",
                            "description": "ID del proveedor",
                        },
                        "amount": {"type": "string", "description": "Monto"},
                    },
                },
            },
            "description": "Esquema completo de datos para reservas en TrackHS API V2",
            "version": "2.0.0",
            "api_endpoint": "/v2/pms/reservations",
            "supported_operations": ["GET", "POST", "PUT", "DELETE"],
            "pagination": {
                "supported": True,
                "modes": ["standard", "scroll"],
                "max_page_size": 1000,
                "max_total_results": 10000,
            },
            "filtering": {
                "supported_parameters": [
                    "search",
                    "tags",
                    "nodeId",
                    "unitId",
                    "reservationTypeId",
                    "contactId",
                    "travelAgentId",
                    "campaignId",
                    "userId",
                    "unitTypeId",
                    "rateTypeId",
                    "bookedStart",
                    "bookedEnd",
                    "arrivalStart",
                    "arrivalEnd",
                    "departureStart",
                    "departureEnd",
                    "updatedSince",
                    "scroll",
                    "inHouseToday",
                    "status",
                    "groupId",
                    "checkinOfficeId",
                ]
            },
            "sorting": {
                "supported_columns": [
                    "name",
                    "status",
                    "altCon",
                    "agreementStatus",
                    "type",
                    "guest",
                    "guests",
                    "unit",
                    "units",
                    "checkin",
                    "checkout",
                    "nights",
                ],
                "supported_directions": ["asc", "desc"],
            },
        }

    @mcp.resource("trackhs://schema/units")
    async def units_schema() -> Dict[str, Any]:
        """Esquema de datos para unidades en TrackHS"""
        return {
            "schema": {
                "id": "string",
                "name": "string",
                "type": "enum[apartment, house, room]",
                "capacity": "number",
                "status": "enum[available, occupied, maintenance]",
                "nodeId": "string",
                "amenities": "array[string]",
            },
            "description": "Estructura de datos para unidades en TrackHS",
        }

    @mcp.resource("trackhs://status/system")
    async def system_status() -> Dict[str, Any]:
        """Estado actual del sistema TrackHS y configuración"""
        return {
            "status": "operational",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0",
            "apiUrl": api_client.config.base_url,
            "toolsCount": 13,
            "capabilities": ["tools", "resources", "prompts"],
        }

    @mcp.resource("trackhs://docs/api")
    async def api_documentation() -> str:
        """Documentación completa de la API de TrackHS V2"""
        return """# TrackHS API V2 Documentation

## Endpoints Principales

### Reservas V2
- `GET /v2/pms/reservations` - Buscar reservas con API V2 (recomendado)
- `GET /reservations` - Listar reservas (legacy)
- `GET /reservations/{id}` - Obtener reserva específica
- `GET /reservations/search` - Buscar reservas (legacy)

### Unidades
- `GET /units` - Listar unidades
- `GET /units/{id}` - Obtener unidad específica

### Contactos
- `GET /crm/contacts` - Listar contactos

### Contabilidad
- `GET /pms/accounting/accounts` - Listar cuentas contables
- `GET /pms/accounting/folios` - Listar folios

### Mantenimiento
- `GET /maintenance/work-orders` - Listar órdenes de trabajo

## API V2 - Características Principales

### Paginación Avanzada
- **Paginación estándar**: `page` y `size` para resultados limitados
- **Scroll de Elasticsearch**: Para grandes conjuntos de datos
- **Límites**: Máximo 10k resultados totales, 1k por página

### Filtrado Completo
- **Búsqueda de texto**: `search` para búsqueda por substring
- **Filtros por ID**: `nodeId`, `unitId`, `contactId`, etc.
- **Filtros de fecha**: `bookedStart`, `arrivalStart`, `departureStart`
- **Filtros especiales**: `inHouseToday`, `status`, `tags`

### Ordenamiento
- **Columnas disponibles**: name, status, altConf, agreementStatus, type, guest, guests
- **Direcciones**: asc, desc

### Parámetros de Fecha
- **Formato**: ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)
- **Parámetros**: bookedStart, bookedEnd, arrivalStart, arrivalEnd, updatedSince

## Autenticación
Todas las peticiones requieren autenticación Basic Auth.

## Ejemplos de Uso

### Búsqueda Básica
```
GET /v2/pms/reservations?page=1&size=10&sortColumn=name&sortDirection=asc
```

### Búsqueda con Filtros
```
GET /v2/pms/reservations?status=Confirmed&arrivalStart=2024-01-01&arrivalEnd=2024-12-31
```

### Scroll para Grandes Conjuntos
```
GET /v2/pms/reservations?scroll=1&size=100
```

## Respuesta de la API V2

La respuesta incluye:
- `_embedded.reservations`: Array de reservas
- `page`, `page_count`, `page_size`, `total_items`: Información de paginación
- `_links`: Enlaces de navegación (self, first, last, next, prev)

## Limitaciones

- Máximo 10,000 resultados totales por consulta
- Máximo 1,000 elementos por página
- Scroll timeout de 1 minuto
- Rate limiting según configuración del servidor
"""

    @mcp.resource("trackhs://api/v2/endpoints")
    async def api_v2_endpoints() -> Dict[str, Any]:
        """Endpoints disponibles en la API V2"""
        return {
            "version": "2.0.0",
            "base_url": api_client.config.base_url,
            "endpoints": {
                "reservations": {
                    "search": {
                        "method": "GET",
                        "path": "/v2/pms/reservations",
                        "description": "Buscar reservas con filtros avanzados",
                        "parameters": {
                            "pagination": ["page", "size", "scroll"],
                            "sorting": ["sortColumn", "sortDirection"],
                            "filtering": [
                                "search",
                                "tags",
                                "nodeId",
                                "unitId",
                                "reservationTypeId",
                                "contactId",
                                "travelAgentId",
                                "campaignId",
                                "userId",
                                "unitTypeId",
                                "rateTypeId",
                                "bookedStart",
                                "bookedEnd",
                                "arrivalStart",
                                "arrivalEnd",
                                "departureStart",
                                "departureEnd",
                                "updatedSince",
                                "inHouseToday",
                                "status",
                                "groupId",
                                "checkinOfficeId",
                            ],
                        },
                        "response_format": "application/json",
                        "pagination_modes": ["standard", "scroll"],
                        "max_page_size": 1000,
                        "max_total_results": 10000,
                    }
                }
            },
            "authentication": {
                "type": "Basic Auth",
                "required": True,
                "headers": ["Authorization"],
            },
            "rate_limits": {"requests_per_minute": 100, "requests_per_hour": 1000},
        }

    @mcp.resource("trackhs://api/v2/parameters")
    async def api_v2_parameters() -> Dict[str, Any]:
        """Parámetros disponibles en la API V2"""
        return {
            "pagination": {
                "page": {
                    "type": "integer",
                    "description": "Número de página",
                    "default": 1,
                    "minimum": 1,
                },
                "size": {
                    "type": "integer",
                    "description": "Tamaño de página",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 1000,
                },
                "scroll": {
                    "type": "string|integer",
                    "description": "Scroll de Elasticsearch (1 para empezar)",
                    "example": "1",
                },
            },
            "sorting": {
                "sortColumn": {
                    "type": "string",
                    "enum": [
                        "name",
                        "status",
                        "altCon",
                        "agreementStatus",
                        "type",
                        "guest",
                        "guests",
                        "unit",
                        "units",
                        "checkin",
                        "checkout",
                        "nights",
                    ],
                    "default": "name",
                    "description": "Columna para ordenar",
                },
                "sortDirection": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "default": "asc",
                    "description": "Dirección de ordenamiento",
                },
            },
            "filtering": {
                "search": {
                    "type": "string",
                    "description": "Búsqueda por substring en nombre o descripciones",
                },
                "tags": {"type": "string", "description": "Búsqueda por ID de tag"},
                "nodeId": {
                    "type": "integer|array",
                    "description": "ID(s) del nodo específico",
                },
                "unitId": {
                    "type": "integer|array",
                    "description": "ID(s) de la unidad específica",
                },
                "contactId": {
                    "type": "integer|array",
                    "description": "ID(s) del contacto específico",
                },
                "status": {
                    "type": "string|array",
                    "enum": [
                        "Hold",
                        "Confirmed",
                        "Checked Out",
                        "Checked In",
                        "Cancelled",
                    ],
                    "description": "Estado(s) de la reserva",
                },
                "inHouseToday": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Filtrar por en casa hoy",
                },
            },
            "date_filters": {
                "bookedStart": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de inicio de reserva (ISO 8601)",
                },
                "bookedEnd": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de fin de reserva (ISO 8601)",
                },
                "arrivalStart": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de inicio de llegada (ISO 8601)",
                },
                "arrivalEnd": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de fin de llegada (ISO 8601)",
                },
                "departureStart": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de inicio de salida (ISO 8601)",
                },
                "departureEnd": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de fin de salida (ISO 8601)",
                },
                "updatedSince": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de actualización desde (ISO 8601)",
                },
            },
        }

    @mcp.resource("trackhs://api/v2/examples")
    async def api_v2_examples() -> Dict[str, Any]:
        """Ejemplos de uso de la API V2"""
        return {
            "basic_search": {
                "description": "Búsqueda básica de reservas",
                "url": "/v2/pms/reservations?page=1&size=10&sortColumn=name",
                "parameters": {
                    "page": 1,
                    "size": 10,
                    "sortColumn": "name",
                    "sortDirection": "asc",
                },
            },
            "filtered_search": {
                "description": "Búsqueda con filtros de fecha y estado",
                "url": "/v2/pms/reservations?status=Confirmed&arrivalStart=2024-01-01",
                "parameters": {
                    "status": "Confirmed",
                    "arrivalStart": "2024-01-01T00:00:00Z",
                    "arrivalEnd": "2024-12-31T23:59:59Z",
                    "page": 1,
                    "size": 50,
                },
            },
            "scroll_search": {
                "description": "Búsqueda con scroll para grandes conjuntos",
                "url": "/v2/pms/reservations?scroll=1&size=100",
                "parameters": {"scroll": 1, "size": 100},
            },
            "text_search": {
                "description": "Búsqueda por texto",
                "url": "/v2/pms/reservations?search=John&page=1&size=20",
                "parameters": {"search": "John", "page": 1, "size": 20},
            },
            "multi_filter": {
                "description": "Búsqueda con múltiples filtros",
                "url": "/v2/pms/reservations?nodeId=123&status=Confirmed",
                "parameters": {
                    "nodeId": 123,
                    "unitTypeId": 456,
                    "status": "Confirmed",
                    "inHouseToday": 1,
                },
            },
        }
