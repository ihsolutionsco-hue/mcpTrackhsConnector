"""
Prompts MCP para TrackHS API V1 y V2
Basados en la documentación oficial de TrackHS
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort


def register_all_prompts(mcp, api_client: "ApiClientPort"):
    """
    Registra todos los prompts MCP para TrackHS

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS

    Raises:
        TypeError: Si api_client es None
    """
    if api_client is None:
        raise TypeError("api_client cannot be None")

    # Prompt para búsqueda por rango de fechas
    @mcp.prompt
    def create_date_range_search_prompt(
        start_date: str,
        end_date: str,
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por rango de fechas.

        **Casos de Uso:**
        - Reportes mensuales/trimestrales
        - Análisis de ocupación por período
        - Auditoría de reservas en fechas específicas
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas por rango de fechas:

**Parámetros:**
- Fecha de inicio: {start_date}
- Fecha de fin: {end_date}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con arrival_start="{start_date}" y arrival_end="{end_date}"
2. Ordena por fecha de llegada (sort_column="checkin")
3. Incluye todos los campos relevantes
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas
- Análisis por nodo/tipo de unidad
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para búsqueda por estado
    @mcp.prompt
    def create_status_search_prompt(
        status: str,
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por estado.

        **Casos de Uso:**
        - Reservas confirmadas pendientes
        - Reservas canceladas para análisis
        - Huéspedes actualmente en casa
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas por estado:

**Parámetros:**
- Estado: {status}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con status="{status}"
2. Ordena por fecha de llegada más reciente
3. Incluye reservas históricas y futuras
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas
- Análisis por nodo/tipo de unidad
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para búsqueda por unidad/nodo
    @mcp.prompt
    def create_unit_search_prompt(
        unit_id: str = None,
        node_id: str = None,
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por unidad o nodo.

        **Casos de Uso:**
        - Historial de una unidad específica
        - Reservas de una propiedad (nodo)
        - Análisis de rendimiento por unidad
        """
        filters = []
        if unit_id:
            filters.append(f'unit_id="{unit_id}"')
        if node_id:
            filters.append(f'node_id="{node_id}"')

        filter_text = ", ".join(filters) if filters else "sin filtros específicos"

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas por unidad/nodo:

**Parámetros:**
- Filtros: {filter_text}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con {filter_text}
2. Ordena por fecha de llegada más reciente
3. Incluye reservas históricas y futuras
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas
- Análisis por nodo/tipo de unidad
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para búsqueda con scroll (grandes datasets)
    @mcp.prompt
    def create_scroll_search_prompt(
        size: int = 1000,
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda con scroll para grandes datasets.

        **Casos de Uso:**
        - Exportación masiva de datos
        - Análisis de grandes volúmenes
        - Sincronización de datos
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda con scroll para grandes datasets:

**Parámetros:**
- Tamaño de página: {size}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con scroll=1 y size={size}
2. NO uses sort_column ni sort_direction (deshabilitados con scroll)
3. Para continuar, usa el valor de _links.next como scroll
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas
- Información de paginación (_links.next para continuar)
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para búsqueda combinada
    @mcp.prompt
    def create_combined_search_prompt(
        filters: Dict[str, Any],
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda con múltiples filtros combinados.

        **Casos de Uso:**
        - Análisis complejo con múltiples criterios
        - Reportes específicos por período y estado
        - Búsquedas personalizadas
        """
        # Construir texto de filtros
        filters_text = ""
        for key, value in filters.items():
            if value is not None:
                filters_text += f"- {key}: {value}\n"

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda combinada de reservas:

**Filtros Aplicados:**
{filters_text}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con todos los filtros proporcionados
2. Ordena por fecha de llegada (sort_column="checkin")
3. Incluye todos los campos relevantes
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas
- Análisis por nodo/tipo de unidad
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para reservas actualizadas
    @mcp.prompt
    def create_updated_since_prompt(
        updated_since: str,
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas actualizadas desde una fecha.

        **Casos de Uso:**
        - Sincronización de datos
        - Auditoría de cambios
        - Monitoreo de actualizaciones
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas actualizadas:

**Parámetros:**
- Actualizadas desde: {updated_since}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations_v2 con updated_since="{updated_since}"
2. Ordena por fecha de actualización más reciente
3. Incluye solo reservas modificadas desde la fecha especificada
4. {'Incluye desglose financiero completo' if include_financials else 'Enfócate en datos básicos'}

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas
- Fecha de última actualización

**Formato de Respuesta:**
- Resumen ejecutivo con totales
- Lista detallada de reservas actualizadas
- Análisis de cambios por tipo
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}""",
                    },
                }
            ]
        }

    # Prompt para obtener detalles de reserva
    @mcp.prompt
    def create_get_reservation_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para obtener detalles completos de una reserva específica.

        **Casos de Uso:**
        - Verificar estado de una reserva específica
        - Obtener información completa de reserva
        - Validar datos de reserva antes de procesamiento
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Obtener detalles completos de reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation_v2 con reservation_id={reservation_id}
2. Extrae toda la información disponible de la reserva
3. Incluye datos embebidos (unit, contact, policies, user, etc.)
4. Proporciona análisis completo de la información

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información financiera: guest_breakdown, owner_breakdown, security_deposit
- Datos embebidos: unit, contact, guaranteePolicy, cancellationPolicy, user, type, rateType
- Ocupantes y políticas
- Estado de acuerdos y pagos
- Enlaces y metadatos

**Formato de Respuesta:**
- Resumen ejecutivo de la reserva
- Información detallada por sección
- Análisis de estado y políticas
- Información de contacto y unidad
- Desglose financiero completo""",
                    },
                }
            ]
        }

    # Prompt para análisis financiero de reserva
    @mcp.prompt
    def create_reservation_analysis_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para análisis financiero detallado de una reserva.

        **Casos de Uso:**
        - Análisis de rentabilidad de reserva
        - Verificación de pagos y balances
        - Auditoría financiera de reserva específica
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis financiero de reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation_v2 con reservation_id={reservation_id}
2. Enfócate en la información financiera de la reserva
3. Analiza guest_breakdown y owner_breakdown
4. Verifica pagos, balances y depósitos

**Análisis Financiero a Incluir:**
- Desglose del huésped: renta bruta, descuentos, renta neta, impuestos, total
- Desglose del propietario: renta bruta, comisiones, ingresos netos
- Depósito de seguridad: requerido vs restante
- Plan de pagos: fechas y montos programados
- Balance actual y estado de pagos
- Productos de seguro de viaje

**Formato de Respuesta:**
- Resumen financiero ejecutivo
- Análisis de rentabilidad
- Estado de pagos y balances
- Recomendaciones financieras""",
                    },
                }
            ]
        }

    # Prompt para resumen ejecutivo de reserva
    @mcp.prompt
    def create_reservation_summary_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para generar un resumen ejecutivo de una reserva.

        **Casos de Uso:**
        - Reportes ejecutivos de reserva
        - Resúmenes para stakeholders
        - Información de alto nivel para toma de decisiones
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Resumen ejecutivo de reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation_v2 con reservation_id={reservation_id}
2. Crea un resumen ejecutivo conciso y claro
3. Incluye solo la información más relevante
4. Enfócate en métricas clave y estado actual

**Información Clave a Incluir:**
- Estado actual de la reserva
- Fechas de llegada y salida
- Información del huésped principal
- Unidad asignada
- Total financiero y balance
- Estado de políticas y acuerdos
- Métricas de ocupación

**Formato de Respuesta:**
- Resumen ejecutivo en formato ejecutivo
- Métricas clave destacadas
- Estado actual y próximos pasos
- Alertas o recomendaciones importantes""",
                    },
                }
            ]
        }
