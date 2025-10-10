"""
Prompts MCP para Track HS API
"""

from typing import Dict, Any, Optional
from .core.api_client import TrackHSApiClient

def register_all_prompts(mcp, api_client: TrackHSApiClient):
    """Registra todos los prompts MCP"""
    
    @mcp.prompt("check-today-reservations")
    async def check_today_reservations(date: Optional[str] = None) -> Dict[str, Any]:
        """Revisar todas las reservas que llegan o salen hoy"""
        target_date = date or "hoy"
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Por favor, revisa todas las reservas para la fecha {target_date}. Incluye:
1. Reservas que llegan hoy (check-in)
2. Reservas que salen hoy (check-out)
3. Reservas que están activas hoy
4. Un resumen de ocupación por nodo/unidad

Usa las herramientas disponibles para obtener esta información."""
                    }
                }
            ]
        }
    
    @mcp.prompt("unit-availability")
    async def unit_availability(check_in: str, check_out: str, node_id: Optional[str] = None) -> Dict[str, Any]:
        """Verificar disponibilidad de unidades para fechas específicas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito verificar la disponibilidad de unidades para las fechas:
- Entrada: {check_in}
- Salida: {check_out}
{f'- Nodo específico: {node_id}' if node_id else ''}

Por favor:
1. Lista todas las unidades disponibles
2. Verifica si hay reservas conflictivas en esas fechas
3. Proporciona un resumen de disponibilidad por tipo de unidad
4. Incluye información de capacidad y amenidades"""
                    }
                }
            ]
        }
    
    @mcp.prompt("guest-contact-info")
    async def guest_contact_info(reservation_id: Optional[str] = None, search_term: Optional[str] = None) -> Dict[str, Any]:
        """Obtener información de contacto de huéspedes para reservas específicas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito obtener información de contacto de huéspedes:
{f'- Para la reserva ID: {reservation_id}' if reservation_id else ''}
{f'- Filtrando por: {search_term}' if search_term else ''}

Por favor:
1. Obtén la información de contacto completa
2. Incluye nombre, email, teléfono y dirección
3. Verifica si hay notas especiales o preferencias
4. Proporciona un resumen organizado por reserva"""
                    }
                }
            ]
        }
    
    @mcp.prompt("maintenance-summary")
    async def maintenance_summary(status: str = "all", days: int = 30) -> Dict[str, Any]:
        """Obtener un resumen de las órdenes de mantenimiento pendientes y completadas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito un resumen de las órdenes de mantenimiento:
- Estado: {status if status != 'all' else 'Todas'}
- Período: Últimos {days} días

Por favor:
1. Lista todas las órdenes que coincidan con los criterios
2. Agrupa por estado (pendiente, en progreso, completada)
3. Incluye información de prioridad y fecha de vencimiento
4. Proporciona estadísticas de completitud
5. Identifica órdenes urgentes o vencidas"""
                    }
                }
            ]
        }
    
    @mcp.prompt("financial-analysis")
    async def financial_analysis(period: str, include_forecast: bool = False) -> Dict[str, Any]:
        """Obtener un análisis financiero básico de reservas y cuentas"""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Necesito un análisis financiero para el período: {period}
{f'- Incluir proyecciones futuras' if include_forecast else ''}

Por favor:
1. Obtén datos de reservas para el período
2. Calcula ingresos totales y promedio por reserva
3. Analiza ocupación y tarifas
4. Incluye información de cuentas contables relevantes
5. Proporciona métricas clave de rendimiento
{f'6. Incluye proyecciones basadas en tendencias' if include_forecast else ''}"""
                    }
                }
            ]
        }
