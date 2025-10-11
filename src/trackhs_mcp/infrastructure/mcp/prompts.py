"""
Prompts MCP para Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
Enfocado en casos de uso reales de búsqueda de reservas
"""

from typing import Any, Dict, Optional

from ...application.ports.api_client_port import ApiClientPort
from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_all_prompts(mcp, api_client: ApiClientPort):
    """Registra todos los prompts MCP enfocados en búsqueda de reservas"""

    @mcp.prompt("search-reservations-by-dates")
    async def search_reservations_by_dates(
        start_date: str, end_date: str, date_type: str = "arrival"
    ) -> Dict[str, Any]:
        """
        Buscar reservas por rango de fechas usando la API V2.

        Args:
            start_date: Fecha de inicio (formato: YYYY-MM-DD)
            end_date: Fecha de fin (formato: YYYY-MM-DD)
            date_type: Tipo de fecha a filtrar (arrival, departure, booked)
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Buscar reservas por rango de fechas:

**Parámetros de Búsqueda:**
- Fecha inicio: {start_date}
- Fecha fin: {end_date}
- Tipo de fecha: {date_type}

**Instrucciones:**
1. Usa la herramienta search_reservations con los parámetros de fecha apropiados
2. Para {date_type}: usa {date_type}Start y {date_type}End
3. Incluye información básica: ID, estado, fechas, huésped, unidad
4. Ordena por fecha de {date_type}
5. Limita a 50 resultados para mejor rendimiento

**Información a Incluir:**
- ID de reserva y estado
- Fechas de llegada y salida
- Información del huésped principal
- Unidad asignada y nodo
- Número de noches
- Estado de acuerdos (agreement_status)

**Formato de Respuesta:**
- Lista organizada por fecha
- Resumen de totales por estado
- Identificación de reservas especiales o problemáticas""",
                    },
                }
            ]
        }

    @mcp.prompt("search-reservations-by-guest")
    async def search_reservations_by_guest(
        guest_name: Optional[str] = None,
        contact_id: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Buscar reservas por información de huésped usando la API V2.

        Args:
            guest_name: Nombre del huésped a buscar
            contact_id: ID específico del contacto
            email: Email del huésped
            phone: Teléfono del huésped
        """
        search_criteria = []
        if guest_name:
            search_criteria.append(f"- Nombre: {guest_name}")
        if contact_id:
            search_criteria.append(f"- Contacto ID: {contact_id}")
        if email:
            search_criteria.append(f"- Email: {email}")
        if phone:
            search_criteria.append(f"- Teléfono: {phone}")

        criteria_text = (
            "\n".join(search_criteria)
            if search_criteria
            else "- Sin criterios específicos"
        )

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Buscar reservas por información de huésped:

**Criterios de Búsqueda:**
{criteria_text}

**Instrucciones:**
1. Usa search_reservations con parámetros de búsqueda de texto
2. Si tienes contactId específico, úsalo directamente
3. Para búsqueda por nombre/email, usa el parámetro 'search'
4. Incluye información completa del contacto y reservas
5. Ordena por fecha de llegada más reciente

**Información a Incluir:**
- Datos completos del contacto (nombre, email, teléfono)
- Historial de reservas del huésped
- Estado actual de reservas activas
- Preferencias y notas especiales
- Información de facturación

**Formato de Respuesta:**
- Información del contacto principal
- Lista de reservas con fechas y estados
- Resumen de actividad del huésped
- Notas especiales o preferencias identificadas""",
                    },
                }
            ]
        }

    @mcp.prompt("search-reservations-advanced")
    async def search_reservations_advanced(
        search_term: Optional[str] = None,
        status: Optional[str] = None,
        node_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        include_financials: bool = False,
        scroll_mode: bool = False,
    ) -> Dict[str, Any]:
        """
        Búsqueda avanzada de reservas con múltiples filtros usando la API V2.

        Args:
            search_term: Término de búsqueda en nombres/descripciones
            status: Estado de reserva (Hold, Confirmed, Checked In, etc.)
            node_id: ID del nodo específico
            unit_type_id: ID del tipo de unidad
            include_financials: Incluir información financiera detallada
            scroll_mode: Usar modo scroll para grandes conjuntos de datos
        """
        filters = []
        if search_term:
            filters.append(f"- Término de búsqueda: {search_term}")
        if status:
            filters.append(f"- Estado: {status}")
        if node_id:
            filters.append(f"- Nodo ID: {node_id}")
        if unit_type_id:
            filters.append(f"- Tipo de unidad ID: {unit_type_id}")

        filters_text = "\n".join(filters) if filters else "- Sin filtros específicos"

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda avanzada de reservas con filtros múltiples:

**Filtros Aplicados:**
{filters_text}
- Incluir información financiera: {'Sí' if include_financials else 'No'}
- Modo de búsqueda: {'Scroll (grandes conjuntos)' if scroll_mode else 'Paginación estándar'}

**Instrucciones:**
1. Usa search_reservations con todos los filtros proporcionados
2. {'Usa scroll=1 para grandes conjuntos' if scroll_mode else 'Usa paginación estándar (page=1, size=50)'}
3. Ordena por fecha de llegada (arrivalStart)
4. Incluye todos los campos relevantes según los filtros

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {'Desglose financiero completo (guest_breakdown, owner_breakdown)' if include_financials else 'Información básica de tarifas'}
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {'Análisis financiero consolidado' if include_financials else 'Métricas básicas de ocupación'}
- Recomendaciones basadas en los resultados""",
                    },
                }
            ]
        }
