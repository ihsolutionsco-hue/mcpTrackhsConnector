"""
Prompts MCP para Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

# datetime imports removed - not used
from typing import Any, Dict, Optional

from trackhs_mcp.application.ports.api_client_port import ApiClientPort
from trackhs_mcp.infrastructure.utils.logging import get_logger

logger = get_logger(__name__)


def register_all_prompts(mcp, api_client: ApiClientPort):
    """Registra todos los prompts MCP"""

    @mcp.prompt("check-today-reservations")
    async def check_today_reservations(date: Optional[str] = None) -> Dict[str, Any]:
        """Revisar todas las reservas que llegan o salen hoy usando API V2"""
        # target_date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Por favor, \
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
        check_in: str, check_out: str, node_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verificar disponibilidad de unidades para fechas específicas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Necesito verificar la disponibilidad de unidades:
- Entrada: {check_in}
- Salida: {check_out}
{f'- Nodo específico: {node_id}' if node_id else ''}

Por favor:
1. Lista todas las unidades disponibles
2. Verifica si hay reservas conflictivas en esas fechas
3. Proporciona un resumen de disponibilidad por tipo de unidad
4. Incluye información de capacidad y amenidades""",
                    },
                }
            ]
        }

    @mcp.prompt("guest-contact-info")
    async def guest_contact_info(
        reservation_id: Optional[str] = None, search_term: Optional[str] = None
    ) -> Dict[str, Any]:
        """Obtener información de contacto de huéspedes para reservas específicas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Necesito obtener información de contacto:
{f'- Para la reserva ID: {reservation_id}' if reservation_id else ''}
{f'- Filtrando por: {search_term}' if search_term else ''}

Por favor:
1. Obtén la información de contacto completa
2. Incluye nombre, email, teléfono y dirección
3. Verifica si hay notas especiales o preferencias
4. Proporciona un resumen organizado por reserva""",
                    },
                }
            ]
        }

    @mcp.prompt("maintenance-summary")
    async def maintenance_summary(
        status: str = "all", days: int = 30
    ) -> Dict[str, Any]:
        """Obtener resumen de órdenes de mantenimiento"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Necesito un resumen de las órdenes de mantenimiento:
- Estado: {status if status != 'all' else 'Todas'}
- Período: Últimos {days} días

Por favor:
1. Lista todas las órdenes que coincidan con los criterios
2. Agrupa por estado (pendiente, en progreso, completada)
3. Incluye información de prioridad y fecha de vencimiento
4. Proporciona estadísticas de completitud
5. Identifica órdenes urgentes o vencidas""",
                    },
                }
            ]
        }

    @mcp.prompt("financial-analysis")
    async def financial_analysis(
        period: str, include_forecast: bool = False
    ) -> Dict[str, Any]:
        """Obtener un análisis financiero básico de reservas y cuentas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Necesito análisis financiero para: {period}
{f'- Incluir proyecciones futuras' if include_forecast else ''}

Por favor:
1. Obtén datos de reservas para el período
2. Calcula ingresos totales y promedio por reserva
3. Analiza ocupación y tarifas
4. Incluye información de cuentas contables relevantes
5. Proporciona métricas clave de rendimiento
{f'6. Incluye proyecciones basadas en tendencias' if include_forecast else ''}""",
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
    ) -> Dict[str, Any]:
        """Búsqueda avanzada de reservas usando API V2"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Realiza búsqueda avanzada de reservas con criterios:

**Criterios de Búsqueda:**
{f'- Término: {search_term}' if search_term else '- Sin término específico'}
{f'- Estado: {status}' if status else '- Todos'}
{f'- Fechas: {date_range}' if date_range else '- Sin filtro'}
{f'- Nodo: {node_id}' if node_id else '- Todos'}
{f'- Tipo de unidad ID: {unit_type_id}' if unit_type_id else '- Todos los tipos'}
{f'- Contacto ID: {contact_id}' if contact_id else '- Todos los contactos'}

**Configuración de Búsqueda:**
- Usar API V2: /v2/pms/reservations
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
        start_date: str,
        end_date: str,
        group_by: str = "node",
        include_financials: bool = True,
        include_occupancy: bool = True,
    ) -> Dict[str, Any]:
        """Análisis avanzado de reservas con métricas y KPIs"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Análisis de reservas para {start_date} a {end_date}:

**Parámetros de Análisis:**
- Período: {start_date} a {end_date}
- Agrupación: {group_by} (node, unitType, status, channel)
- Incluir información financiera: {'Sí' if include_financials else 'No'}
- Incluir análisis de ocupación: {'Sí' if include_occupancy else 'No'}

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

**Usar API V2 con:**
- arrivalStart: {start_date}
- arrivalEnd: {end_date}
- Parámetros de scroll para grandes conjuntos
- Ordenamiento por fecha y nodo
- Incluir todos los campos de desglose financiero

**Formato de Salida:**
- Dashboard ejecutivo con KPIs principales
- Gráficos de tendencias temporales
- Análisis comparativo por nodo/tipo
- Recomendaciones estratégicas
- Identificación de oportunidades de mejora""",
                    },
                }
            ]
        }

    @mcp.prompt("guest-experience-analysis")
    async def guest_experience_analysis(
        reservation_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        include_history: bool = True,
    ) -> Dict[str, Any]:
        """Análisis de experiencia del huésped con información completa de la API V2"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": """Análisis de experiencia:

**Identificación:**
{f'- Reserva ID: {reservation_id}' if reservation_id else '- Sin reserva específica'}
{f'- Contacto ID: {contact_id}' if contact_id else '- Sin contacto específico'}
{f'- Incluir historial completo: {"Sí" if include_history else "No"}'}

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
- Análisis de satisfacción basado en datos

**Usar herramientas:**
- search_reservations para datos de reserva
- get_contact para información de contacto
- get_unit para detalles de unidad
- Recursos de esquema para contexto completo""",
                    },
                }
            ]
        }
