"""
Resources MCP para TrackHS API V1 y V2
Basados en la documentación oficial de TrackHS
"""

from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort
from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_all_resources(mcp, api_client: ApiClientPort):
    """Registra los resources MCP esenciales para TrackHS V1 y V2"""

    # Schema para API V1
    @mcp.resource("trackhs://schema/reservations-v1")
    async def reservations_v1_schema() -> Dict[str, Any]:
        """Esquema completo de datos para reservas en TrackHS API V1"""
        return {
            "schema": {
                "id": {"type": "integer", "description": "ID único de la reserva"},
                "name": {"type": "string", "description": "Nombre de la reserva"},
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
                "unit_id": {"type": "integer", "description": "ID de la unidad"},
                "contact_id": {"type": "integer", "description": "ID del contacto"},
                "arrival_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de llegada (ISO 8601)",
                },
                "departure_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de salida (ISO 8601)",
                },
                "nights": {"type": "number", "description": "Número de noches"},
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de creación (ISO 8601)",
                },
                "updated_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de actualización (ISO 8601)",
                },
                "booked_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Fecha de reserva (ISO 8601)",
                },
                "guest_breakdown": {
                    "type": "object",
                    "description": "Desglose financiero del huésped",
                },
                "owner_breakdown": {
                    "type": "object",
                    "description": "Desglose financiero del propietario",
                },
                "_embedded": {"type": "object", "description": "Datos embebidos"},
                "_links": {"type": "object", "description": "Enlaces"},
            },
            "description": "Esquema de datos para reservas en TrackHS API V1",
            "version": "1.0.0",
            "api_endpoint": "/pms/reservations",
            "supported_operations": ["GET"],
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
                    "altConf",
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

    # Schema para API V2
    @mcp.resource("trackhs://schema/reservations-v2")
    async def reservations_v2_schema() -> Dict[str, Any]:
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
                "unitId": {
                    "type": "integer",
                    "description": "ID de la unidad (camelCase)",
                },
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
                    "items": {"$ref": "#/definitions/Occupant"},
                    "description": "Ocupantes",
                },
                "security_deposit": {
                    "$ref": "#/definitions/SecurityDeposit",
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
                    "$ref": "#/definitions/GuestBreakdown",
                    "description": "Desglose del huésped",
                },
                "owner_breakdown": {
                    "$ref": "#/definitions/OwnerBreakdown",
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
                    "items": {"$ref": "#/definitions/PaymentPlan"},
                    "description": "Plan de pagos",
                },
                "travel_insurance_products": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/TravelInsuranceProduct"},
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
                            "items": {"$ref": "#/definitions/Rate"},
                            "description": "Tarifas",
                        },
                        "guest_fees": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/GuestFee"},
                            "description": "Tarifas del huésped",
                        },
                        "taxes": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/Tax"},
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
                            "items": {"$ref": "#/definitions/OwnerFee"},
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

    # Documentación API V1
    @mcp.resource("trackhs://docs/api-v1")
    async def api_v1_documentation() -> str:
        """Documentación completa de la API de TrackHS V1"""
        return """# TrackHS API V1 Documentation

## Endpoint Principal
- `GET /pms/reservations` - Buscar reservas con API V1

## Características V1
- **Paginación**: Estándar con page/size
- **Scroll**: Elasticsearch scroll para grandes datasets
- **Filtros**: Búsqueda por texto, IDs, fechas, estado
- **Ordenamiento**: Múltiples columnas disponibles

## Parámetros Principales
- `page`: Número de página (0-based)
- `size`: Tamaño de página (máximo 1000)
- `sortColumn`: Columna para ordenar
- `sortDirection`: Dirección (asc/desc)
- `search`: Búsqueda por texto
- `status`: Estado de reserva
- `arrivalStart/End`: Rango de fechas de llegada
- `departureStart/End`: Rango de fechas de salida
- `nodeId`: ID del nodo/propiedad
- `unitId`: ID de la unidad
- `contactId`: ID del contacto

## Limitaciones V1
- Máximo 10,000 resultados totales
- Máximo 1,000 elementos por página
- Scroll timeout de 1 minuto
- Ordenamiento deshabilitado con scroll

## Ejemplos de Uso

### Búsqueda Básica
```
GET /pms/reservations?page=1&size=10&sortColumn=name&sortDirection=asc
```

### Búsqueda con Filtros
```
GET /pms/reservations?status=Confirmed&arrivalStart=2024-01-01&arrivalEnd=2024-12-31
```

### Scroll para Grandes Conjuntos
```
GET /pms/reservations?scroll=1&size=100
```
"""

    # Documentación API V2
    @mcp.resource("trackhs://docs/api-v2")
    async def api_v2_documentation() -> str:
        """Documentación completa de la API de TrackHS V2"""
        return """# TrackHS API V2 Documentation

## Endpoint Principal
- `GET /v2/pms/reservations` - Buscar reservas con API V2 (recomendado)

## Características V2
- **Paginación Avanzada**: Estándar + Elasticsearch scroll
- **Filtros Mejorados**: Más parámetros y mejor rendimiento
- **Datos Enriquecidos**: Información financiera detallada
- **Compatibilidad**: Mantiene compatibilidad con V1

## Parámetros Principales
- `page`: Número de página (0-based)
- `size`: Tamaño de página (máximo 1000)
- `sortColumn`: Columna para ordenar
- `sortDirection`: Dirección (asc/desc)
- `search`: Búsqueda por texto
- `status`: Estado de reserva (múltiples valores)
- `arrivalStart/End`: Rango de fechas de llegada
- `departureStart/End`: Rango de fechas de salida
- `nodeId`: ID del nodo/propiedad
- `unitId`: ID de la unidad
- `contactId`: ID del contacto
- `travelAgentId`: ID del agente de viajes
- `campaignId`: ID de la campaña
- `userId`: ID del usuario
- `unitTypeId`: ID del tipo de unidad
- `rateTypeId`: ID del tipo de tarifa
- `reservationTypeId`: ID del tipo de reserva
- `bookedStart/End`: Rango de fechas de reserva
- `updatedSince`: Actualizadas desde fecha
- `scroll`: Scroll de Elasticsearch
- `inHouseToday`: Filtro de huéspedes en casa
- `groupId`: ID del grupo
- `checkinOfficeId`: ID de la oficina de check-in

## Mejoras V2 vs V1
- **Más parámetros**: 25+ parámetros vs 20 en V1
- **Mejor rendimiento**: Optimizaciones de consulta
- **Datos enriquecidos**: Información financiera completa
- **Flexibilidad**: Múltiples valores para algunos parámetros

## Limitaciones V2
- Máximo 10,000 resultados totales
- Máximo 1,000 elementos por página
- Scroll timeout de 1 minuto
- Ordenamiento deshabilitado con scroll

## Ejemplos de Uso

### Búsqueda Básica
```
GET /v2/pms/reservations?page=1&size=10&sortColumn=name&sortDirection=asc
```

### Búsqueda con Filtros Múltiples
```
GET /v2/pms/reservations?status=Confirmed&arrivalStart=2024-01-01&arrivalEnd=2024-12-31&nodeId=1,2,3
```

### Scroll para Grandes Conjuntos
```
GET /v2/pms/reservations?scroll=1&size=100
```

### Búsqueda por Múltiples Estados
```
GET /v2/pms/reservations?status=Confirmed,Checked In&arrivalStart=2024-01-01
```
"""

    # Guía de migración V1 → V2
    @mcp.resource("trackhs://docs/migration-guide")
    async def migration_guide() -> str:
        """Guía de migración de API V1 a V2"""
        return """# Guía de Migración V1 → V2

## Cambios Principales

### Endpoints
- **V1**: `/pms/reservations`
- **V2**: `/v2/pms/reservations`

### Nuevos Parámetros en V2
- `travelAgentId`: ID del agente de viajes
- `campaignId`: ID de la campaña
- `userId`: ID del usuario
- `unitTypeId`: ID del tipo de unidad
- `rateTypeId`: ID del tipo de tarifa
- `reservationTypeId`: ID del tipo de reserva
- `bookedStart/End`: Rango de fechas de reserva
- `updatedSince`: Actualizadas desde fecha
- `groupId`: ID del grupo
- `checkinOfficeId`: ID de la oficina de check-in

### Mejoras en V2
- **Mejor rendimiento**: Consultas optimizadas
- **Datos enriquecidos**: Información financiera completa
- **Flexibilidad**: Múltiples valores para algunos parámetros
- **Compatibilidad**: Mantiene todos los parámetros de V1

## Migración Paso a Paso

### 1. Cambiar Endpoint
```python
# V1
endpoint = "/pms/reservations"

# V2
endpoint = "/v2/pms/reservations"
```

### 2. Aprovechar Nuevos Parámetros
```python
# V2 - Nuevos filtros disponibles
params = {
    "status": ["Confirmed", "Checked In"],  # Múltiples valores
    "travelAgentId": 123,
    "campaignId": 456,
    "unitTypeId": 789,
    "updatedSince": "2024-01-01T00:00:00Z"
}
```

### 3. Optimizar Consultas
```python
# V2 - Mejor rendimiento
params = {
    "arrivalStart": "2024-01-01",
    "arrivalEnd": "2024-12-31",
    "nodeId": "1,2,3",  # Múltiples IDs
    "status": "Confirmed"
}
```

## Compatibilidad
- Todos los parámetros de V1 funcionan en V2
- Misma estructura de respuesta
- Mismos códigos de error
- Misma autenticación

## Recomendaciones
1. **Usar V2 para nuevas implementaciones**
2. **Migrar gradualmente desde V1**
3. **Aprovechar nuevos parámetros para mejor rendimiento**
4. **Mantener V1 para compatibilidad legacy**
"""

    # Ejemplos de uso
    @mcp.resource("trackhs://docs/examples")
    async def usage_examples() -> str:
        """Ejemplos de uso para TrackHS API V1 y V2"""
        return """# Ejemplos de Uso TrackHS API

## Búsquedas Comunes

### 1. Reservas por Rango de Fechas
```python
# V1
search_reservations_v1(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    sort_column="checkin",
    sort_direction="asc"
)

# V2
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    sort_column="checkin",
    sort_direction="asc"
)
```

### 2. Reservas por Estado
```python
# V1
search_reservations_v1(
    status="Confirmed",
    sort_column="checkin",
    sort_direction="desc"
)

# V2 - Múltiples estados
search_reservations_v2(
    status=["Confirmed", "Checked In"],
    sort_column="checkin",
    sort_direction="desc"
)
```

### 3. Reservas por Unidad/Nodo
```python
# V1
search_reservations_v1(
    unit_id="123",
    node_id="456"
)

# V2 - Múltiples IDs
search_reservations_v2(
    unit_id="123,124,125",
    node_id="456,457"
)
```

### 4. Scroll para Grandes Datasets
```python
# V1 y V2 - Mismo comportamiento
search_reservations_v2(
    scroll=1,
    size=1000
)

# Continuar con scroll
search_reservations_v2(
    scroll="scroll_token_from_previous_response",
    size=1000
)
```

### 5. Búsqueda Combinada
```python
# V2 - Filtros múltiples
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    status=["Confirmed", "Checked In"],
    node_id="1,2,3",
    unit_type_id="10",
    sort_column="checkin",
    sort_direction="asc"
)
```

### 6. Reservas Actualizadas
```python
# V2 - Nuevo en V2
search_reservations_v2(
    updated_since="2024-01-01T00:00:00Z",
    sort_column="updated_at",
    sort_direction="desc"
)
```

## Casos de Uso Comunes

### Reportes Mensuales
```python
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    status="Confirmed",
    sort_column="checkin",
    sort_direction="asc"
)
```

### Huéspedes Actualmente en Casa
```python
search_reservations_v2(
    status="Checked In",
    in_house_today=1,
    sort_column="checkin",
    sort_direction="asc"
)
```

### Exportación Masiva
```python
search_reservations_v2(
    scroll=1,
    size=1000
)
```

### Análisis por Canal
```python
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    channel_id="1,2,3",  # Múltiples canales
    sort_column="channel_id",
    sort_direction="asc"
)
```
"""

    # Referencia de parámetros
    @mcp.resource("trackhs://reference/parameters")
    async def parameters_reference() -> Dict[str, Any]:
        """Referencia completa de parámetros para V1 y V2"""
        return {
            "v1_parameters": {
                "pagination": {
                    "page": {
                        "type": "integer",
                        "description": "Número de página (0-based)",
                        "max": 10000,
                    },
                    "size": {
                        "type": "integer",
                        "description": "Tamaño de página",
                        "max": 1000,
                    },
                },
                "sorting": {
                    "sortColumn": {
                        "type": "string",
                        "enum": [
                            "name",
                            "status",
                            "altConf",
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
                    },
                    "sortDirection": {"type": "string", "enum": ["asc", "desc"]},
                },
                "filtering": {
                    "search": {"type": "string", "description": "Búsqueda por texto"},
                    "tags": {"type": "string", "description": "Búsqueda por tags"},
                    "nodeId": {"type": "integer|array", "description": "ID del nodo"},
                    "unitId": {
                        "type": "integer|array",
                        "description": "ID de la unidad",
                    },
                    "contactId": {
                        "type": "integer|array",
                        "description": "ID del contacto",
                    },
                    "status": {
                        "type": "string|array",
                        "description": "Estado de reserva",
                    },
                    "arrivalStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de llegada inicio",
                    },
                    "arrivalEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de llegada fin",
                    },
                    "departureStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de salida inicio",
                    },
                    "departureEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de salida fin",
                    },
                    "bookedStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de reserva inicio",
                    },
                    "bookedEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de reserva fin",
                    },
                    "updatedSince": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Actualizadas desde",
                    },
                    "scroll": {
                        "type": "integer|string",
                        "description": "Scroll de Elasticsearch",
                    },
                    "inHouseToday": {
                        "type": "integer",
                        "enum": [0, 1],
                        "description": "Huéspedes en casa hoy",
                    },
                },
            },
            "v2_parameters": {
                "pagination": {
                    "page": {
                        "type": "integer",
                        "description": "Número de página (0-based)",
                        "max": 10000,
                    },
                    "size": {
                        "type": "integer",
                        "description": "Tamaño de página",
                        "max": 1000,
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
                    },
                    "sortDirection": {"type": "string", "enum": ["asc", "desc"]},
                },
                "filtering": {
                    "search": {"type": "string", "description": "Búsqueda por texto"},
                    "tags": {"type": "string", "description": "Búsqueda por tags"},
                    "nodeId": {"type": "integer|array", "description": "ID del nodo"},
                    "unitId": {
                        "type": "integer|array",
                        "description": "ID de la unidad",
                    },
                    "contactId": {
                        "type": "integer|array",
                        "description": "ID del contacto",
                    },
                    "travelAgentId": {
                        "type": "integer|array",
                        "description": "ID del agente de viajes",
                    },
                    "campaignId": {
                        "type": "integer|array",
                        "description": "ID de la campaña",
                    },
                    "userId": {
                        "type": "integer|array",
                        "description": "ID del usuario",
                    },
                    "unitTypeId": {
                        "type": "integer|array",
                        "description": "ID del tipo de unidad",
                    },
                    "rateTypeId": {
                        "type": "integer|array",
                        "description": "ID del tipo de tarifa",
                    },
                    "reservationTypeId": {
                        "type": "integer|array",
                        "description": "ID del tipo de reserva",
                    },
                    "status": {
                        "type": "string|array",
                        "description": "Estado de reserva",
                    },
                    "arrivalStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de llegada inicio",
                    },
                    "arrivalEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de llegada fin",
                    },
                    "departureStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de salida inicio",
                    },
                    "departureEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de salida fin",
                    },
                    "bookedStart": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de reserva inicio",
                    },
                    "bookedEnd": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Fecha de reserva fin",
                    },
                    "updatedSince": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Actualizadas desde",
                    },
                    "scroll": {
                        "type": "integer|string",
                        "description": "Scroll de Elasticsearch",
                    },
                    "inHouseToday": {
                        "type": "integer",
                        "enum": [0, 1],
                        "description": "Huéspedes en casa hoy",
                    },
                    "groupId": {"type": "integer", "description": "ID del grupo"},
                    "checkinOfficeId": {
                        "type": "integer",
                        "description": "ID de la oficina de check-in",
                    },
                },
            },
            "common_parameters": {
                "date_formats": [
                    "YYYY-MM-DD",
                    "YYYY-MM-DDTHH:MM:SSZ",
                    "YYYY-MM-DDTHH:MM:SS",
                ],
                "status_values": [
                    "Hold",
                    "Confirmed",
                    "Checked Out",
                    "Checked In",
                    "Cancelled",
                ],
                "sort_columns": [
                    "name",
                    "status",
                    "altConf",
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
                "sort_directions": ["asc", "desc"],
            },
        }

    # Valores válidos de status
    @mcp.resource("trackhs://reference/status-values")
    async def status_values() -> Dict[str, Any]:
        """Valores válidos para el parámetro status"""
        return {
            "valid_statuses": [
                {
                    "value": "Hold",
                    "description": "Reserva en espera de confirmación",
                    "color": "#FFA500",
                    "is_active": True,
                },
                {
                    "value": "Confirmed",
                    "description": "Reserva confirmada",
                    "color": "#28A745",
                    "is_active": True,
                },
                {
                    "value": "Checked In",
                    "description": "Huésped registrado",
                    "color": "#007BFF",
                    "is_active": True,
                },
                {
                    "value": "Checked Out",
                    "description": "Huésped salido",
                    "color": "#6C757D",
                    "is_active": False,
                },
                {
                    "value": "Cancelled",
                    "description": "Reserva cancelada",
                    "color": "#DC3545",
                    "is_active": False,
                },
            ],
            "usage_examples": {
                "single_status": "status=Confirmed",
                "multiple_statuses": "status=Confirmed,Checked In",
                "array_format": 'status=["Confirmed", "Checked In"]',
            },
        }

    # Formatos de fecha soportados
    @mcp.resource("trackhs://reference/date-formats")
    async def date_formats() -> Dict[str, Any]:
        """Formatos de fecha soportados por la API"""
        return {
            "supported_formats": [
                {
                    "format": "YYYY-MM-DD",
                    "example": "2024-01-01",
                    "description": "Solo fecha",
                    "usage": "Para rangos de fechas básicos",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SS",
                    "example": "2024-01-01T00:00:00",
                    "description": "Fecha y hora sin timezone",
                    "usage": "Para fechas específicas",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SSZ",
                    "example": "2024-01-01T00:00:00Z",
                    "description": "Fecha y hora con timezone UTC",
                    "usage": "Para fechas con timezone explícito",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SS+HH:MM",
                    "example": "2024-01-01T00:00:00+00:00",
                    "description": "Fecha y hora con offset",
                    "usage": "Para fechas con timezone específico",
                },
            ],
            "examples": {
                "arrival_start": "2024-01-01",
                "arrival_end": "2024-01-31T23:59:59Z",
                "booked_start": "2024-01-01T00:00:00",
                "updated_since": "2024-01-01T00:00:00Z",
            },
            "best_practices": [
                "Usar formato ISO 8601 completo para fechas específicas",
                "Usar solo fecha (YYYY-MM-DD) para rangos de días completos",
                "Especificar timezone cuando sea relevante",
                "Usar Z para UTC cuando no se especifique timezone",
            ],
        }
