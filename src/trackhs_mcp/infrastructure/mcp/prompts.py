"""
Prompts para el servidor MCP de TrackHS
"""

from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort


def create_search_reservations_prompt(
    filters: Dict[str, Any],
    include_financials: bool = False,
    scroll_mode: bool = False,
) -> Dict[str, Any]:
    """
    Crea un prompt para búsqueda de reservas con filtros múltiples

    Args:
        filters: Diccionario con los filtros de búsqueda
        include_financials: Si incluir información financiera
        scroll_mode: Si usar modo scroll para grandes conjuntos

    Returns:
        Diccionario con el prompt configurado
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
                    "text": f"""Búsqueda avanzada de reservas con filtros múltiples:

**Filtros Aplicados:**
{filters_text}
- Incluir información financiera: {'Sí' if include_financials else 'No'}
- Modo de búsqueda: {
        'Scroll (grandes conjuntos)' if scroll_mode else 'Paginación estándar'
    }

**Instrucciones:**
1. Usa search_reservations con todos los filtros proporcionados
2. {
        'Usa scroll=1 para grandes conjuntos' if scroll_mode
        else 'Usa paginación estándar (page=1, size=50)'
    }
3. Ordena por fecha de llegada (arrivalStart)
4. Incluye todos los campos relevantes según los filtros

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {
        'Desglose financiero completo (guest_breakdown, owner_breakdown)'
        if include_financials else 'Información básica de tarifas'
    }
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {
        'Análisis financiero consolidado' if include_financials
        else 'Métricas básicas de ocupación'
    }
- Recomendaciones basadas en los resultados""",
                },
            }
        ]
    }


def create_search_reservations_by_guest_prompt(
    guest_name: str,
    guest_email: str = None,
    include_financials: bool = False,
) -> Dict[str, Any]:
    """
    Crea un prompt para búsqueda de reservas por huésped

    Args:
        guest_name: Nombre del huésped
        guest_email: Email del huésped (opcional)
        include_financials: Si incluir información financiera

    Returns:
        Diccionario con el prompt configurado
    """
    email_filter = f"\n- Email: {guest_email}" if guest_email else ""

    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Búsqueda de reservas por huésped:

**Filtros Aplicados:**
- Nombre del huésped: {guest_name}{email_filter}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations con filtros de huésped
2. Busca por nombre exacto o parcial
3. Incluye reservas históricas y futuras
4. Ordena por fecha de llegada más reciente

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {
        'Desglose financiero completo'
        if include_financials else 'Información básica de tarifas'
    }
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {
        'Análisis financiero consolidado' if include_financials
        else 'Métricas básicas de ocupación'
    }
- Recomendaciones basadas en los resultados""",
                },
            }
        ]
    }


def create_search_reservations_by_unit_prompt(
    unit_id: str,
    unit_name: str = None,
    include_financials: bool = False,
) -> Dict[str, Any]:
    """
    Crea un prompt para búsqueda de reservas por unidad

    Args:
        unit_id: ID de la unidad
        unit_name: Nombre de la unidad (opcional)
        include_financials: Si incluir información financiera

    Returns:
        Diccionario con el prompt configurado
    """
    name_filter = f"\n- Nombre de unidad: {unit_name}" if unit_name else ""

    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Búsqueda de reservas por unidad:

**Filtros Aplicados:**
- ID de unidad: {unit_id}{name_filter}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:
1. Usa search_reservations con filtros de unidad
2. Busca por ID exacto de unidad
3. Incluye reservas históricas y futuras
4. Ordena por fecha de llegada más reciente

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {
        'Desglose financiero completo'
        if include_financials else 'Información básica de tarifas'
    }
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {
        'Análisis financiero consolidado' if include_financials
        else 'Métricas básicas de ocupación'
    }
- Recomendaciones basadas en los resultados""",
                },
            }
        ]
    }


def create_search_reservations_by_date_range_prompt(
    start_date: str,
    end_date: str,
    include_financials: bool = False,
) -> Dict[str, Any]:
    """
    Crea un prompt para búsqueda de reservas por rango de fechas

    Args:
        start_date: Fecha de inicio (YYYY-MM-DD)
        end_date: Fecha de fin (YYYY-MM-DD)
        include_financials: Si incluir información financiera

    Returns:
        Diccionario con el prompt configurado
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Búsqueda de reservas por rango de fechas:

**Filtros Aplicados:**
- Fecha de inicio: {start_date}
- Fecha de fin: {end_date}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations con filtros de fecha
2. Busca por rango de fechas de llegada
3. Incluye reservas en el rango especificado
4. Ordena por fecha de llegada

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {
        'Desglose financiero completo'
        if include_financials else 'Información básica de tarifas'
    }
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {
        'Análisis financiero consolidado' if include_financials
        else 'Métricas básicas de ocupación'
    }
- Recomendaciones basadas en los resultados""",
                },
            }
        ]
    }


def create_search_reservations_by_status_prompt(
    status: str,
    include_financials: bool = False,
) -> Dict[str, Any]:
    """
    Crea un prompt para búsqueda de reservas por estado

    Args:
        status: Estado de la reserva
        include_financials: Si incluir información financiera

    Returns:
        Diccionario con el prompt configurado
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Búsqueda de reservas por estado:

**Filtros Aplicados:**
- Estado: {status}
- Incluir información financiera: {'Sí' if include_financials else 'No'}

**Instrucciones:**
1. Usa search_reservations con filtros de estado
2. Busca por estado exacto
3. Incluye reservas históricas y futuras
4. Ordena por fecha de llegada más reciente

**Información a Incluir:**
- Datos básicos: ID, estado, fechas, huésped, unidad
- Información de contacto y ocupantes
- Detalles de unidad y nodo
- {
        'Desglose financiero completo'
        if include_financials else 'Información básica de tarifas'
    }
- Estado de acuerdos y políticas
- Productos adicionales (seguros, planes de pago)

**Formato de Respuesta:**
- Resumen ejecutivo con totales y métricas
- Lista detallada de reservas encontradas
- Análisis por nodo/tipo de unidad si aplica
- {
        'Análisis financiero consolidado' if include_financials
        else 'Métricas básicas de ocupación'
    }
- Recomendaciones basadas en los resultados""",
                },
            }
        ]
    }


def register_all_prompts(mcp, api_client: ApiClientPort):
    """Registra todos los prompts MCP para TrackHS"""

    # Los prompts básicos son funciones de utilidad que se pueden usar
    # para crear prompts dinámicos. Los prompts reales están en prompts_enhanced.py
    # que se registran automáticamente con el decorador @mcp.prompt

    # Importar y registrar prompts mejorados
    from .prompts_enhanced import register_enhanced_prompts

    register_enhanced_prompts(mcp)
