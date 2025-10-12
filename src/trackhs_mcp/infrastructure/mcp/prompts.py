"""
Prompts MCP para TrackHS API V1 y V2
Basados en la documentación oficial de TrackHS
"""

from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort


def register_all_prompts(mcp, api_client: ApiClientPort):
    """Registra todos los prompts MCP para TrackHS V1 y V2"""

    # Prompt para búsqueda por rango de fechas
    @mcp.prompt
    def create_date_range_search_prompt(
        start_date: str,
        end_date: str,
        api_version: str = "v2",
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por rango de fechas.

        **Casos de Uso:**
        - Reportes mensuales/trimestrales
        - Análisis de ocupación por período
        - Auditoría de reservas en fechas específicas
        """
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

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
- API Version: {api_version.upper()}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con arrival_start="{start_date}" y arrival_end="{end_date}"
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
        api_version: str = "v2",
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por estado.

        **Casos de Uso:**
        - Reservas confirmadas pendientes
        - Reservas canceladas para análisis
        - Huéspedes actualmente en casa
        """
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas por estado:

**Parámetros:**
- Estado: {status}
- API Version: {api_version.upper()}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con status="{status}"
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
        api_version: str = "v2",
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas por unidad o nodo.

        **Casos de Uso:**
        - Historial de una unidad específica
        - Reservas de una propiedad (nodo)
        - Análisis de rendimiento por unidad
        """
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

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
- API Version: {api_version.upper()}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con {filter_text}
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
        api_version: str = "v2",
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
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda con scroll para grandes datasets:

**Parámetros:**
- API Version: {api_version.upper()}
- Tamaño de página: {size}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con scroll=1 y size={size}
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
        api_version: str = "v2",
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda con múltiples filtros combinados.

        **Casos de Uso:**
        - Análisis complejo con múltiples criterios
        - Reportes específicos por período y estado
        - Búsquedas personalizadas
        """
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

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
- API Version: {api_version.upper()}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con todos los filtros proporcionados
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
        api_version: str = "v2",
        include_financials: bool = False,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para búsqueda de reservas actualizadas desde una fecha.

        **Casos de Uso:**
        - Sincronización de datos
        - Auditoría de cambios
        - Monitoreo de actualizaciones
        """
        tool_name = (
            f"search_reservations_{api_version}"
            if api_version == "v1"
            else "search_reservations_v2"
        )

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Búsqueda de reservas actualizadas:

**Parámetros:**
- Actualizadas desde: {updated_since}
- API Version: {api_version.upper()}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa {tool_name} con updated_since="{updated_since}"
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
