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
        - Preparación para check-in de huéspedes
        - Análisis financiero y operacional
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
1. Usa get_reservation con reservation_id="{reservation_id}"
2. Extrae toda la información disponible de la reserva
3. Incluye datos embebidos (unit, contact, policies, user, etc.)
4. Proporciona análisis completo orientado al cliente

**INFORMACIÓN DEL HUÉSPED:**
- Datos de contacto completos (nombre, email, teléfono, dirección)
- Preferencias especiales y notas del huésped
- Información de ocupantes (adultos, niños, mascotas)
- Historial de reservas y referencias

**DETALLES DE LA ESTANCIA:**
- Fechas exactas de llegada y salida (con horarios)
- Unidad asignada (dirección, características, amenidades)
- Políticas de check-in/check-out
- Servicios incluidos y adicionales
- Instrucciones especiales de acceso

**INFORMACIÓN FINANCIERA:**
- Total de la reserva y desglose de costos
- Estado de pagos (pagado, pendiente, balance)
- Depósitos de seguridad y garantías
- Tarifas por noche y servicios adicionales
- Políticas de cancelación y reembolso

**SEGUIMIENTO OPERATIVO:**
- Estado actual de la reserva
- Preparación necesaria para la unidad
- Servicios adicionales contratados
- Notas importantes para el personal
- Próximos pasos y acciones requeridas

**Formato de Respuesta:**
- Resumen ejecutivo orientado al cliente
- Información práctica para operaciones
- Análisis de estado y recomendaciones
- Datos de contacto y comunicación
- Desglose financiero claro y accionable""",
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
1. Usa get_reservation con reservation_id="{reservation_id}"
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

    # Prompt para preparación de check-in
    @mcp.prompt
    def create_checkin_preparation_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para preparación de check-in de huéspedes.

        **Casos de Uso:**
        - Preparación operacional para llegada de huéspedes
        - Verificación de servicios y amenidades
        - Coordinación de servicios adicionales
        - Preparación de documentación y acceso
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Preparación de check-in para reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation con reservation_id="{reservation_id}"
2. Enfócate en información operacional para check-in
3. Identifica servicios y preparaciones necesarias
4. Proporciona checklist de preparación

**INFORMACIÓN DEL HUÉSPED:**
- Nombre completo y datos de contacto
- Hora estimada de llegada
- Número de ocupantes (adultos, niños, mascotas)
- Preferencias especiales o solicitudes

**DETALLES DE LA UNIDAD:**
- Dirección exacta y código de acceso
- Características especiales (piscina, spa, BBQ, etc.)
- Servicios incluidos y adicionales
- Instrucciones de WiFi y amenidades
- Políticas de mascotas y reglas especiales

**PREPARACIÓN OPERACIONAL:**
- Servicios adicionales contratados (limpieza, calentamiento de piscina, etc.)
- Verificaciones necesarias (piscina, spa, BBQ, WiFi)
- Documentación requerida
- Horarios de check-in/check-out
- Contacto de emergencia

**Formato de Respuesta:**
- Checklist de preparación paso a paso
- Información de contacto del huésped
- Instrucciones específicas de la unidad
- Servicios a verificar y preparar
- Próximos pasos operacionales""",
                    },
                }
            ]
        }

    # Prompt para análisis financiero detallado
    @mcp.prompt
    def create_financial_analysis_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para análisis financiero detallado de una reserva.

        **Casos de Uso:**
        - Reconciliación financiera
        - Análisis de rentabilidad
        - Verificación de pagos y balances
        - Auditoría financiera
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis financiero detallado de reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation con reservation_id="{reservation_id}"
2. Enfócate en información financiera completa
3. Analiza rentabilidad y estado de pagos
4. Proporciona recomendaciones financieras

**DESGLOSE FINANCIERO DEL HUÉSPED:**
- Renta bruta y neta
- Tarifas por noche y total de noches
- Servicios adicionales y tarifas
- Descuentos y promociones aplicadas
- Impuestos y cargos adicionales
- Total pagado vs balance pendiente

**DESGLOSE FINANCIERO DEL PROPIETARIO:**
- Ingresos brutos y netos
- Comisiones de gestión y agente
- Tarifas del propietario
- Ingresos netos reales

**ESTADO DE PAGOS:**
- Pagos realizados y fechas
- Balance pendiente (si aplica)
- Método de pago utilizado
- Próximos pagos programados

**ANÁLISIS DE RENTABILIDAD:**
- Margen de ganancia
- Comparación con tarifas estándar
- Efectividad de servicios adicionales
- Recomendaciones de optimización

**Formato de Respuesta:**
- Resumen financiero ejecutivo
- Desglose detallado de costos
- Estado de pagos y balances
- Análisis de rentabilidad
- Recomendaciones financieras""",
                    },
                }
            ]
        }

    # Prompt para comunicación con huéspedes
    @mcp.prompt
    def create_guest_communication_prompt(reservation_id: int) -> Dict[str, Any]:
        """
        Crea un prompt para comunicación efectiva con huéspedes.

        **Casos de Uso:**
        - Preparación de comunicaciones con huéspedes
        - Información de contacto y preferencias
        - Coordinación de servicios especiales
        - Gestión de solicitudes especiales
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Comunicación con huésped de reserva:

**Parámetros:**
- ID de Reserva: {reservation_id}

**Instrucciones:**
1. Usa get_reservation con reservation_id="{reservation_id}"
2. Enfócate en información de comunicación
3. Identifica preferencias y necesidades especiales
4. Proporciona guía de comunicación efectiva

**DATOS DE CONTACTO:**
- Nombre completo del huésped principal
- Email principal y secundario
- Teléfonos (celular, trabajo, casa)
- Dirección postal completa
- Preferencias de comunicación

**INFORMACIÓN DE LA ESTANCIA:**
- Fechas y horarios de llegada/salida
- Unidad asignada y características
- Servicios contratados y adicionales
- Políticas y reglas importantes

**PREFERENCIAS ESPECIALES:**
- Solicitudes especiales del huésped
- Notas importantes de reservas anteriores
- Preferencias de servicios
- Restricciones o limitaciones

**GUÍA DE COMUNICACIÓN:**
- Mejor método de contacto
- Horarios preferidos de comunicación
- Información importante a comunicar
- Servicios adicionales a ofrecer

**Formato de Respuesta:**
- Datos de contacto completos
- Información clave para comunicar
- Preferencias y necesidades especiales
- Recomendaciones de comunicación
- Servicios adicionales a ofrecer""",
                    },
                }
            ]
        }
