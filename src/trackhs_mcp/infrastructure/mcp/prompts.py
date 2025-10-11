"""
Prompts MCP para Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

# datetime imports removed - not used
from typing import Any, Dict, List, Optional

from ...application.ports.api_client_port import ApiClientPort
from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_all_prompts(mcp, api_client: ApiClientPort):
    """Registra todos los prompts MCP"""

    @mcp.prompt("check-today-reservations")
    async def check_today_reservations(date: Optional[str] = None) -> Dict[str, Any]:
        """Revisar todas las reservas que llegan o salen hoy usando API V2"""
        from datetime import datetime, timezone

        target_date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Por favor, \
     revisa todas las reservas para la fecha {target_date} usando la API V2. Incluye:

**Información de Check-in (Llegadas):**
- Reservas con arrival_date = {target_date}
- Estado: Hold, Confirmed, Checked In
- Información de huéspedes y ocupantes
- Detalles de unidad y nodo
- Horarios de llegada (arrival_time)

**Información de Check-out (Salidas):**
- Reservas con departure_date = {target_date}
- Estado: Checked In, Checked Out
- Información de huéspedes y ocupantes
- Detalles de unidad y nodo
- Horarios de salida (departure_time)

**Reservas Activas:**
- Reservas que están en casa hoy (inHouseToday=1)
- Estado: Checked In
- Información de ocupación actual

**Resumen de Ocupación:**
- Por nodo (nodeId)
- Por tipo de unidad (unitTypeId)
- Por estado de reserva
- Métricas de ocupación

**Usa la herramienta search_reservations con:**
- arrivalStart/arrivalEnd para llegadas
- departureStart/departureEnd para salidas
- inHouseToday=1 para activas
- Parámetros de paginación apropiados
- Ordenamiento por fecha y hora

**Incluye también:**
- Información de desglose financiero (guest_breakdown)
- Estado de acuerdos (agreement_status)
- Productos de seguro de viaje
- Planes de pago""",
                    },
                }
            ]
        }

    @mcp.prompt("unit-availability")
    async def unit_availability(
        start_date: str, end_date: str, unit_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verificar disponibilidad de unidades para fechas específicas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito verificar la disponibilidad de unidades:
- Fecha inicio: {start_date}
- Fecha fin: {end_date}
{f'- Tipo de unidad: {unit_type}' if unit_type else ''}

Por favor:
1. Lista todas las unidades disponibles
2. Verifica si hay reservas conflictivas en esas fechas usando search_reservations
3. Proporciona un resumen de disponibilidad por tipo de unidad
4. Incluye información de capacidad y amenidades
5. Usa parámetros como unitId, nodeId para filtrar unidades específicas
6. Usa arrivalStart y arrivalEnd para filtrar por fechas de llegada""",
                    },
                }
            ]
        }

    @mcp.prompt("guest-contact-info")
    async def guest_contact_info(
        reservation_id: Optional[str] = None,
        search_term: Optional[str] = None,
        contact_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Obtener información de contacto de huéspedes para reservas específicas"""
        reservation_text = (
            f"- Para la reserva ID: {reservation_id}" if reservation_id else ""
        )
        search_text = f"- Filtrando por: {search_term}" if search_term else ""
        contact_text = f"- Contacto ID: {contact_id}" if contact_id else ""

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito obtener información de contacto de huéspedes:
{reservation_text}
{search_text}
{contact_text}

Por favor:
1. Obtén la información de contacto completa usando search_reservations
2. Incluye nombre, email, teléfono y dirección
3. Verifica si hay notas especiales o preferencias
4. Proporciona un resumen organizado por reserva
5. Usa contactId para filtrar contactos específicos""",
                    },
                }
            ]
        }

    @mcp.prompt("maintenance-summary")
    async def maintenance_summary(
        status: str = "all",
        days: int = 30,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Obtener resumen de órdenes de mantenimiento"""
        status_text = "Todas" if status == "all" else status
        date_text = (
            f"- Fechas: {start_date} a {end_date}"
            if start_date and end_date
            else f"- Período: Últimos {days} días"
        )

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito un resumen de las órdenes de mantenimiento:
- Estado: {status_text}
{date_text}

Por favor:
1. Lista todas las órdenes que coincidan con los criterios usando search_reservations
2. Agrupa por estado (pendiente, en progreso, completada)
3. Incluye información de prioridad y fecha de vencimiento
4. Proporciona estadísticas de completitud
5. Identifica órdenes urgentes o vencidas
6. Incluye información de unidades afectadas""",
                    },
                }
            ]
        }

    @mcp.prompt("financial-analysis")
    async def financial_analysis(
        period: str = "monthly",
        include_forecast: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        analysis_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Obtener un análisis financiero básico de reservas y cuentas"""
        period_text = f"- Tipo: {period}"
        forecast_text = f"- Incluir pronósticos: {'Sí' if include_forecast else 'No'}"
        date_text = (
            f"- Fechas: {start_date} a {end_date}" if start_date and end_date else ""
        )
        analysis_text = f"- Tipo de análisis: {analysis_type}" if analysis_type else ""

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis financiero de reservas:

**Período de Análisis:**
{period_text}
{forecast_text}
{date_text}
{analysis_text}

**Métricas a Calcular:**
1. **Ingresos Totales:**
   - Ingresos brutos (gross_rent)
   - Ingresos netos (net_rent)
   - Comparación con períodos anteriores

2. **Análisis de Tarifas:**
   - ADR (Average Daily Rate) por unidad
   - RevPAR (Revenue per Available Room)
   - Análisis de estacionalidad

3. **Rentabilidad por Reserva:**
   - Desglose de guest_breakdown
   - Análisis de owner_breakdown
   - Identificación de reservas más rentables

4. **Productos Adicionales:**
   - Seguros de viaje
   - Planes de pago
   - Servicios adicionales

**Usar search_reservations con:**
- Parámetros de fecha apropiados
- Incluir todos los campos financieros
- Agrupar por nodo y tipo de unidad
- Calcular métricas de ocupación

**Formato de Salida:**
- Dashboard financiero ejecutivo
- Gráficos de tendencias
- Análisis comparativo
- Recomendaciones estratégicas""",
                    },
                }
            ]
        }

    @mcp.prompt("advanced-reservation-search")
    async def advanced_reservation_search(
        search_term: Optional[str] = None,
        status: Optional[str] = None,
        date_range: Optional[str] = None,
        node_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        scroll_mode: bool = False,
        search_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Búsqueda avanzada de reservas usando API V2"""
        term_text = (
            f"- Término: {search_term}" if search_term else "- Sin término específico"
        )
        status_text = f"- Estado: {status}" if status else "- Todos"
        date_text = f"- Fechas: {date_range}" if date_range else "- Sin filtro"
        node_text = f"- Nodo: {node_id}" if node_id else "- Todos"
        unit_text = (
            f"- Tipo de unidad ID: {unit_type_id}"
            if unit_type_id
            else "- Todos los tipos"
        )
        contact_text = (
            f"- Contacto ID: {contact_id}" if contact_id else "- Todos los contactos"
        )

        criteria_text = ""
        if search_criteria:
            criteria_items = []
            for key, value in search_criteria.items():
                criteria_items.append(f"- {key}: {value}")
            criteria_text = "\n".join(criteria_items)

        # Construir sección de criterios adicionales
        additional_criteria_section = ""
        if criteria_text:
            additional_criteria_section = f"**Criterios Adicionales:**\n{criteria_text}"

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Realiza búsqueda avanzada de reservas con criterios:

**Criterios de Búsqueda:**
{term_text}
{status_text}
{date_text}
{node_text}
{unit_text}
{contact_text}
{additional_criteria_section}

**Configuración de Búsqueda:**
- Usar search_reservations con API V2: /v2/pms/reservations
- Modo de paginación: {'Scroll (para grandes conjuntos)' if scroll_mode else 'Estándar'}
- Ordenamiento: Por fecha de llegada (arrivalStart)
- Tamaño de página: {'100 (scroll)' if scroll_mode else '50 (estándar)'}

**Información a Incluir:**
1. **Datos Básicos:** ID, estado, fechas de llegada/salida, noches
2. **Información de Huésped:** Contacto, ocupantes, detalles de contacto
3. **Información de Unidad:** Unidad, nodo, tipo de unidad
4. **Desglose Financiero:** guest_breakdown, owner_breakdown, tarifas, impuestos
5. **Estado de Acuerdos:** agreement_status, políticas de garantía/cancelación
6. **Productos Adicionales:** Seguros de viaje, planes de pago
7. **Métricas:** ADR, ocupación, ingresos por tipo

**Filtros Adicionales a Considerar:**
- Filtros de fecha: bookedStart, bookedEnd, arrivalStart, arrivalEnd
- Filtros de ID: travelAgentId, campaignId, userId, rateTypeId
- Filtros especiales: inHouseToday, tags, groupId, checkinOfficeId
- Ordenamiento: name, status, altConf, agreementStatus, type, guest, guests
- Parámetros de búsqueda avanzada disponibles

**Formato de Respuesta:**
- Resumen ejecutivo con métricas clave
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad
- Información financiera consolidada
- Recomendaciones basadas en los datos""",
                    },
                }
            ]
        }

    @mcp.prompt("reservation-analytics")
    async def reservation_analytics(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: str = "node",
        include_financials: bool = True,
        include_occupancy: bool = True,
        metrics: Optional[List[str]] = None,
        period: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Análisis avanzado de reservas con métricas y KPIs"""
        date_text = (
            f"- Período: {start_date} a {end_date}"
            if start_date and end_date
            else "- Período: Sin especificar"
        )
        group_text = f"- Agrupación: {group_by} (node, unitType, status, channel)"
        financial_text = (
            f"- Incluir información financiera: {'Sí' if include_financials else 'No'}"
        )
        occupancy_text = (
            f"- Incluir análisis de ocupación: {'Sí' if include_occupancy else 'No'}"
        )
        metrics_text = (
            f"- Métricas específicas: {', '.join(metrics)}" if metrics else ""
        )
        period_text = f"- Período de análisis: {period}" if period else ""

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis de reservas:

**Parámetros de Análisis:**
{date_text}
{group_text}
{financial_text}
{occupancy_text}
{metrics_text}
{period_text}

**Métricas a Calcular:**
1. **Ocupación:**
   - Tasa de ocupación por nodo/tipo de unidad
   - Noches ocupadas vs. disponibles
   - Análisis de estacionalidad
   - Comparación con períodos anteriores

2. **Rendimiento Financiero:**
   - Ingresos totales (gross_rent, net_rent)
   - ADR (Average Daily Rate) por unidad/tipo
   - RevPAR (Revenue per Available Room)
   - Análisis de tarifas por temporada

3. **Análisis de Huéspedes:**
   - Distribución por canal de origen
   - Duración promedio de estadía
   - Análisis de ocupantes por reserva
   - Segmentación por tipo de huésped

4. **Operacional:**
   - Reservas por estado (Hold, Confirmed, Checked In, etc.)
   - Análisis de cancelaciones
   - Tiempo de respuesta por canal
   - Eficiencia de check-in/check-out

**Usar search_reservations con:**
- arrivalStart: {start_date or 'fecha_inicio'}
- arrivalEnd: {end_date or 'fecha_fin'}
- Parámetros de scroll para grandes conjuntos
- Ordenamiento por fecha y nodo
- Incluir todos los campos de desglose financiero

**Formato de Salida:**
- Dashboard ejecutivo con KPIs principales
- Gráficos de tendencias temporales
- Análisis comparativo por nodo/tipo
- Recomendaciones estratégicas
- Identificación de oportunidades de mejora
- Estadísticas detalladas de rendimiento""",
                    },
                }
            ]
        }

    @mcp.prompt("guest-experience-analysis")
    async def guest_experience_analysis(
        reservation_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        include_history: bool = True,
        focus_area: Optional[str] = None,
        time_period: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Análisis de experiencia del huésped con información completa de la API V2"""
        reservation_text = (
            f"- Reserva ID: {reservation_id}"
            if reservation_id
            else "- Sin reserva específica"
        )
        contact_text = (
            f"- Contacto ID: {contact_id}"
            if contact_id
            else "- Sin contacto específico"
        )
        history_text = (
            f"- Incluir historial completo: {'Sí' if include_history else 'No'}"
        )
        focus_text = f"- Área de enfoque: {focus_area}" if focus_area else ""
        time_text = f"- Período de tiempo: {time_period}" if time_period else ""

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis de experiencia:

**Identificación:**
{reservation_text}
{contact_text}
{history_text}
{focus_text}
{time_text}

**Información a Recopilar:**
1. **Datos de la Reserva:**
   - Información completa de la reserva (todos los campos V2)
   - Estado actual y historial de cambios
   - Fechas de llegada/salida y horarios
   - Información de ocupantes y huéspedes

2. **Experiencia Financiera:**
   - Desglose completo de tarifas (guest_breakdown)
   - Descuentos y promociones aplicadas
   - Productos de seguro de viaje
   - Plan de pagos y estado de pagos
   - Depósito de seguridad

3. **Información de Contacto:**
   - Datos completos del contacto
   - Historial de comunicaciones
   - Preferencias y notas especiales
   - Información de contacto de emergencia

4. **Detalles de la Unidad:**
   - Información completa de la unidad
   - Amenidades y características
   - Políticas de la unidad
   - Información de check-in/check-out

5. **Estado de Acuerdos:**
   - agreement_status actual
   - Políticas de garantía aplicadas
   - Políticas de cancelación
   - Documentos pendientes

**Análisis a Realizar:**
- Evaluación de la experiencia del huésped
- Identificación de problemas potenciales
- Recomendaciones de mejora
- Seguimiento de preferencias
- Análisis de satisfacción y comentarios basado en datos

**Usar herramientas:**
- search_reservations para datos de reserva
- get_contact para información de contacto
- get_unit para detalles de unidad
- Recursos de esquema para contexto completo""",
                    },
                }
            ]
        }
