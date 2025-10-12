"""
Prompts MCP mejorados para TrackHS con capacidades especializadas
Incluye prompts para análisis de ocupación, ingresos y gestión avanzada
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_enhanced_prompts(mcp):
    """Registra prompts mejorados para TrackHS"""

    # Prompt para análisis de ocupación
    @mcp.prompt
    def create_occupancy_analysis_prompt(
        period: str = "current_month",
        include_forecast: bool = True,
        group_by: str = "node",
        include_recommendations: bool = True,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para análisis detallado de ocupación.

        **Análisis Incluidos:**
        - Ocupación por período y nodo
        - Tendencias y patrones
        - Comparación con períodos anteriores
        - Previsión de ocupación
        - Recomendaciones de optimización
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis completo de ocupación para {period}:

**Objetivo:**
Realizar un análisis exhaustivo de ocupación que incluya métricas clave, tendencias y recomendaciones estratégicas.

**Datos a Analizar:**
1. **Ocupación Actual:**
   - Ocupación total por nodo
   - Ocupación por tipo de unidad
   - Ocupación por canal de reserva
   - Ocupación por período temporal

2. **Tendencias:**
   - Comparación con períodos anteriores
   - Análisis de estacionalidad
   - Patrones de ocupación por día de la semana
   - Tendencias de crecimiento/declive

3. **Métricas KPI:**
   - Tasa de ocupación promedio
   - ADR (Average Daily Rate)
   - RevPAR (Revenue Per Available Room)
   - Análisis de canales de reserva

4. **Previsión:**
   - Ocupación prevista para próximos 30 días
   - Análisis de demanda estacional
   - Identificación de períodos de alta/baja demanda

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con filtros de fecha apropiados
2. Agrupa resultados por {group_by}
3. Incluye métricas financieras (include_metrics=True)
4. {'Incluye previsión de demanda' if include_forecast else 'Enfócate en datos históricos'}
5. Genera recomendaciones basadas en los datos

**Formato de Respuesta:**
- Resumen ejecutivo con métricas clave
- Análisis detallado por nodo/tipo
- Gráficos de tendencias (descripción)
- Recomendaciones estratégicas
- Plan de acción para optimización

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://realtime/occupancy
- Recursos: trackhs://dashboard/kpi
- {'Recursos: trackhs://forecast/demand' if include_forecast else ''}

**Criterios de Éxito:**
- Análisis basado en datos reales
- Recomendaciones accionables
- Métricas comparativas
- Insights estratégicos""",
                    },
                }
            ]
        }

    # Prompt para análisis de ingresos
    @mcp.prompt
    def create_revenue_analysis_prompt(
        period: str = "current_month",
        include_breakdown: bool = True,
        include_forecast: bool = True,
        group_by: str = "channel",
    ) -> Dict[str, Any]:
        """
        Crea un prompt para análisis detallado de ingresos.

        **Análisis Incluidos:**
        - Ingresos totales y por canal
        - Análisis de ADR y RevPAR
        - Desglose de ingresos por tipo
        - Tendencias de ingresos
        - Previsión de ingresos
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis completo de ingresos para {period}:

**Objetivo:**
Realizar un análisis exhaustivo de ingresos que incluya desglose detallado, tendencias y previsión.

**Datos a Analizar:**
1. **Ingresos Totales:**
   - Ingresos brutos y netos
   - Ingresos por nodo/propiedad
   - Ingresos por tipo de unidad
   - Ingresos por canal de reserva

2. **Métricas Financieras:**
   - ADR (Average Daily Rate)
   - RevPAR (Revenue Per Available Room)
   - Ingresos por huésped
   - Ingresos por noche
   - Análisis de tarifas

3. **Desglose de Ingresos:**
   - Renta base vs. tarifas adicionales
   - Ingresos por impuestos
   - Ingresos por servicios
   - Comisiones por canal

4. **Análisis de Canales:**
   - Rendimiento por canal
   - Costo de adquisición por canal
   - Valor de vida del cliente por canal
   - Recomendaciones de canal

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con include_financials=True
2. Agrupa resultados por {group_by}
3. Incluye métricas avanzadas (include_metrics=True)
4. {'Incluye previsión de ingresos' if include_forecast else 'Enfócate en datos históricos'}
5. Analiza tendencias y patrones

**Formato de Respuesta:**
- Resumen ejecutivo financiero
- Desglose detallado de ingresos
- Análisis por canal y tipo
- Gráficos de tendencias
- Recomendaciones de optimización
- Plan de acción financiero

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://dashboard/kpi
- {'Recursos: trackhs://forecast/demand' if include_forecast else ''}

**Criterios de Éxito:**
- Análisis financiero completo
- Insights sobre canales
- Recomendaciones accionables
- Métricas comparativas""",
                    },
                }
            ]
        }

    # Prompt para análisis de huéspedes
    @mcp.prompt
    def create_guest_analysis_prompt(
        period: str = "current_month",
        include_segmentation: bool = True,
        include_loyalty: bool = True,
        include_recommendations: bool = True,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para análisis detallado de huéspedes.

        **Análisis Incluidos:**
        - Segmentación de huéspedes
        - Análisis de comportamiento
        - Análisis de lealtad
        - Recomendaciones personalizadas
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis completo de huéspedes para {period}:

**Objetivo:**
Realizar un análisis exhaustivo de huéspedes que incluya segmentación, comportamiento y recomendaciones.

**Datos a Analizar:**
1. **Segmentación de Huéspedes:**
   - Huéspedes nuevos vs. recurrentes
   - Segmentación por valor
   - Segmentación por duración de estadía
   - Segmentación por canal de reserva

2. **Comportamiento de Huéspedes:**
   - Patrones de reserva
   - Preferencias de tipo de unidad
   - Estacionalidad de reservas
   - Análisis de cancelaciones

3. **Análisis de Lealtad:**
   - Tasa de retorno
   - Valor de vida del cliente
   - Análisis de referidos
   - Satisfacción del cliente

4. **Recomendaciones Personalizadas:**
   - Estrategias de retención
   - Programas de lealtad
   - Marketing dirigido
   - Optimización de experiencia

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con filtros apropiados
2. Incluye análisis de contactos y reservas
3. Agrupa por tipo de huésped y comportamiento
4. {'Incluye análisis de lealtad' if include_loyalty else 'Enfócate en comportamiento'}
5. Genera recomendaciones personalizadas

**Formato de Respuesta:**
- Resumen de segmentación
- Análisis de comportamiento
- {'Análisis de lealtad' if include_loyalty else 'Análisis de patrones'}
- Recomendaciones estratégicas
- Plan de acción para retención

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://config/unit_types
- Recursos: trackhs://config/booking_channels

**Criterios de Éxito:**
- Segmentación clara
- Insights de comportamiento
- Recomendaciones accionables
- Estrategias de retención""",
                    },
                }
            ]
        }

    # Prompt para optimización de precios
    @mcp.prompt
    def create_pricing_optimization_prompt(
        period: str = "current_month",
        include_competition: bool = True,
        include_demand: bool = True,
        include_recommendations: bool = True,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para optimización de precios.

        **Análisis Incluidos:**
        - Análisis de precios actuales
        - Análisis de demanda
        - Análisis de competencia
        - Recomendaciones de pricing
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Optimización de precios para {period}:

**Objetivo:**
Realizar un análisis completo de precios que incluya optimización, demanda y recomendaciones estratégicas.

**Datos a Analizar:**
1. **Análisis de Precios Actuales:**
   - ADR por tipo de unidad
   - ADR por período temporal
   - ADR por canal de reserva
   - Análisis de elasticidad de precios

2. **Análisis de Demanda:**
   - Patrones de demanda por período
   - Análisis de estacionalidad
   - Identificación de períodos de alta/baja demanda
   - Análisis de ocupación vs. precios

3. **Análisis de Competencia:**
   - Comparación con precios del mercado
   - Análisis de posicionamiento
   - Identificación de oportunidades
   - Análisis de valor percibido

4. **Recomendaciones de Pricing:**
   - Estrategias de precios dinámicos
   - Recomendaciones por período
   - Estrategias por canal
   - Optimización de ingresos

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con include_financials=True
2. Incluye análisis de ADR y RevPAR
3. Agrupa por tipo de unidad y período
4. {'Incluye análisis de competencia' if include_competition else 'Enfócate en datos internos'}
5. Genera recomendaciones específicas

**Formato de Respuesta:**
- Análisis de precios actuales
- Análisis de demanda
- {'Análisis de competencia' if include_competition else 'Análisis de mercado'}
- Recomendaciones de pricing
- Plan de implementación

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://config/unit_types
- Recursos: trackhs://forecast/demand

**Criterios de Éxito:**
- Análisis de precios completo
- Recomendaciones específicas
- Plan de implementación
- Métricas de impacto""",
                    },
                }
            ]
        }

    # Prompt para análisis de canales
    @mcp.prompt
    def create_channel_analysis_prompt(
        period: str = "current_month",
        include_performance: bool = True,
        include_optimization: bool = True,
        include_recommendations: bool = True,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para análisis detallado de canales de reserva.

        **Análisis Incluidos:**
        - Rendimiento por canal
        - Análisis de costos
        - Análisis de conversión
        - Recomendaciones de canal
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Análisis completo de canales de reserva para {period}:

**Objetivo:**
Realizar un análisis exhaustivo de canales que incluya rendimiento, costos y recomendaciones estratégicas.

**Datos a Analizar:**
1. **Rendimiento por Canal:**
   - Reservas por canal
   - Ingresos por canal
   - ADR por canal
   - Ocupación por canal

2. **Análisis de Costos:**
   - Comisiones por canal
   - Costo de adquisición
   - ROI por canal
   - Análisis de rentabilidad

3. **Análisis de Conversión:**
   - Tasa de conversión por canal
   - Tiempo de conversión
   - Análisis de abandono
   - Optimización de conversión

4. **Recomendaciones de Canal:**
   - Estrategias por canal
   - Optimización de presupuesto
   - Diversificación de canales
   - Estrategias de retención

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con group_by="channel"
2. Incluye análisis financiero completo
3. Agrupa por canal y período
4. {'Incluye análisis de rendimiento' if include_performance else 'Enfócate en datos básicos'}
5. Genera recomendaciones específicas

**Formato de Respuesta:**
- Resumen de rendimiento por canal
- Análisis de costos y ROI
- {'Análisis de rendimiento' if include_performance else 'Análisis básico'}
- Recomendaciones estratégicas
- Plan de optimización

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://config/booking_channels
- Recursos: trackhs://dashboard/kpi

**Criterios de Éxito:**
- Análisis de canales completo
- Recomendaciones específicas
- Plan de optimización
- Métricas de impacto""",
                    },
                }
            ]
        }

    # Prompt para reporte ejecutivo
    @mcp.prompt
    def create_executive_report_prompt(
        period: str = "current_month",
        include_forecast: bool = True,
        include_recommendations: bool = True,
        include_action_plan: bool = True,
    ) -> Dict[str, Any]:
        """
        Crea un prompt para reporte ejecutivo completo.

        **Contenido del Reporte:**
        - Resumen ejecutivo
        - Métricas clave
        - Análisis de tendencias
        - Recomendaciones estratégicas
        - Plan de acción
        """
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Reporte ejecutivo completo para {period}:

**Objetivo:**
Crear un reporte ejecutivo comprensivo que incluya métricas clave, análisis estratégico y recomendaciones accionables.

**Contenido del Reporte:**
1. **Resumen Ejecutivo:**
   - Métricas clave del período
   - Comparación con períodos anteriores
   - Logros principales
   - Desafíos identificados

2. **Métricas Clave:**
   - Ocupación y ADR
   - Ingresos y RevPAR
   - Análisis de canales
   - Análisis de huéspedes

3. **Análisis Estratégico:**
   - Tendencias del mercado
   - Análisis de competencia
   - Oportunidades identificadas
   - Riesgos identificados

4. **Recomendaciones Estratégicas:**
   - Estrategias de crecimiento
   - Optimización de operaciones
   - Estrategias de marketing
   - Estrategias de precios

5. **Plan de Acción:**
   - Objetivos a corto plazo
   - Objetivos a largo plazo
   - Recursos necesarios
   - Cronograma de implementación

**Instrucciones Específicas:**
1. Usa search_reservations_advanced con análisis completo
2. Incluye todos los recursos disponibles
3. Agrupa por múltiples criterios
4. {'Incluye previsión y tendencias' if include_forecast else 'Enfócate en datos históricos'}
5. Genera recomendaciones estratégicas

**Formato de Respuesta:**
- Resumen ejecutivo
- Métricas clave con gráficos
- Análisis estratégico
- {'Recomendaciones estratégicas' if include_recommendations else 'Análisis básico'}
- {'Plan de acción detallado' if include_action_plan else 'Recomendaciones generales'}

**Herramientas a Usar:**
- search_reservations_advanced (principal)
- Recursos: trackhs://realtime/occupancy
- Recursos: trackhs://dashboard/kpi
- {'Recursos: trackhs://forecast/demand' if include_forecast else ''}

**Criterios de Éxito:**
- Reporte ejecutivo completo
- Métricas comparativas
- Recomendaciones estratégicas
- Plan de acción accionable""",
                    },
                }
            ]
        }
