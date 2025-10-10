"""
Utilidad de completion para Track HS MCP Connector
Proporciona sugerencias y autocompletado inteligente para parámetros de API
"""

from typing import Dict, List, Any, Optional, Union, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import re
from datetime import datetime, timedelta
import json

class CompletionType(Enum):
    """Tipos de completion disponibles"""
    PARAMETER = "parameter"
    VALUE = "value"
    ENDPOINT = "endpoint"
    FILTER = "filter"
    SORT = "sort"
    DATE = "date"
    STATUS = "status"

@dataclass
class CompletionSuggestion:
    """Sugerencia de completion"""
    value: str
    label: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: int = 0
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class CompletionContext:
    """Contexto para completion"""
    current_input: str
    parameter_name: Optional[str] = None
    endpoint: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class TrackHSCompletion:
    """Sistema de completion para Track HS API"""
    
    def __init__(self, api_client=None):
        self.api_client = api_client
        self._cache: Dict[str, List[CompletionSuggestion]] = {}
        self._cache_ttl: Dict[str, datetime] = {}
        self._cache_duration = timedelta(hours=1)
    
    def _is_cache_valid(self, key: str) -> bool:
        """Verifica si el cache es válido"""
        if key not in self._cache_ttl:
            return False
        return datetime.now() < self._cache_ttl[key]
    
    def _set_cache(self, key: str, suggestions: List[CompletionSuggestion]):
        """Establece cache con TTL"""
        self._cache[key] = suggestions
        self._cache_ttl[key] = datetime.now() + self._cache_duration
    
    def _get_cache(self, key: str) -> Optional[List[CompletionSuggestion]]:
        """Obtiene del cache si es válido"""
        if self._is_cache_valid(key):
            return self._cache.get(key)
        return None
    
    def _filter_suggestions(self, suggestions: List[CompletionSuggestion], 
                           current_input: str) -> List[CompletionSuggestion]:
        """Filtra sugerencias basado en input actual"""
        if not current_input:
            return suggestions[:10]  # Top 10 si no hay input
        
        current_lower = current_input.lower()
        filtered = []
        
        for suggestion in suggestions:
            if (current_lower in suggestion.value.lower() or 
                current_lower in suggestion.label.lower()):
                filtered.append(suggestion)
        
        # Ordenar por prioridad y relevancia
        filtered.sort(key=lambda x: (-x.priority, x.value.lower().startswith(current_lower)))
        return filtered[:10]
    
    def get_parameter_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias de parámetros para la API V2"""
        suggestions = []
        
        # Parámetros básicos de paginación
        suggestions.extend([
            CompletionSuggestion("page", "Page", "Número de página", "pagination", 10),
            CompletionSuggestion("size", "Size", "Tamaño de página", "pagination", 10),
            CompletionSuggestion("sortColumn", "Sort Column", "Columna para ordenar", "sorting", 9),
            CompletionSuggestion("sortDirection", "Sort Direction", "Dirección de ordenamiento", "sorting", 9),
        ])
        
        # Parámetros de búsqueda
        suggestions.extend([
            CompletionSuggestion("search", "Search", "Búsqueda por texto", "search", 8),
            CompletionSuggestion("tags", "Tags", "Filtro por tags", "filter", 7),
            CompletionSuggestion("updatedSince", "Updated Since", "Filtro por fecha de actualización", "filter", 7),
        ])
        
        # Parámetros de filtrado por ID
        suggestions.extend([
            CompletionSuggestion("nodeId", "Node ID", "ID del nodo", "filter", 6),
            CompletionSuggestion("unitId", "Unit ID", "ID de la unidad", "filter", 6),
            CompletionSuggestion("contactId", "Contact ID", "ID del contacto", "filter", 6),
            CompletionSuggestion("reservationTypeId", "Reservation Type ID", "ID del tipo de reserva", "filter", 6),
            CompletionSuggestion("travelAgentId", "Travel Agent ID", "ID del agente de viajes", "filter", 6),
            CompletionSuggestion("campaignId", "Campaign ID", "ID de la campaña", "filter", 6),
            CompletionSuggestion("userId", "User ID", "ID del usuario", "filter", 6),
            CompletionSuggestion("unitTypeId", "Unit Type ID", "ID del tipo de unidad", "filter", 6),
            CompletionSuggestion("rateTypeId", "Rate Type ID", "ID del tipo de tarifa", "filter", 6),
        ])
        
        # Parámetros de fecha
        suggestions.extend([
            CompletionSuggestion("bookedStart", "Booked Start", "Fecha de inicio de reserva", "date", 5),
            CompletionSuggestion("bookedEnd", "Booked End", "Fecha de fin de reserva", "date", 5),
            CompletionSuggestion("arrivalStart", "Arrival Start", "Fecha de inicio de llegada", "date", 5),
            CompletionSuggestion("arrivalEnd", "Arrival End", "Fecha de fin de llegada", "date", 5),
            CompletionSuggestion("departureStart", "Departure Start", "Fecha de inicio de salida", "date", 5),
            CompletionSuggestion("departureEnd", "Departure End", "Fecha de fin de salida", "date", 5),
        ])
        
        # Parámetros especiales
        suggestions.extend([
            CompletionSuggestion("scroll", "Scroll", "Scroll de Elasticsearch", "special", 4),
            CompletionSuggestion("inHouseToday", "In House Today", "Filtrar por en casa hoy", "special", 4),
            CompletionSuggestion("status", "Status", "Estado de la reserva", "filter", 5),
            CompletionSuggestion("groupId", "Group ID", "ID del grupo", "filter", 4),
            CompletionSuggestion("checkinOfficeId", "Check-in Office ID", "ID de la oficina de check-in", "filter", 4),
        ])
        
        return self._filter_suggestions(suggestions, context.current_input)
    
    def get_sort_column_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias para sortColumn"""
        suggestions = [
            CompletionSuggestion("name", "Name", "Ordenar por nombre", "sort", 10),
            CompletionSuggestion("status", "Status", "Ordenar por estado", "sort", 9),
            CompletionSuggestion("altConf", "Alt Conf", "Ordenar por confirmación alternativa", "sort", 8),
            CompletionSuggestion("agreementStatus", "Agreement Status", "Ordenar por estado de acuerdo", "sort", 8),
            CompletionSuggestion("type", "Type", "Ordenar por tipo", "sort", 7),
            CompletionSuggestion("guest", "Guest", "Ordenar por huésped", "sort", 7),
            CompletionSuggestion("guests", "Guests", "Ordenar por huéspedes", "sort", 7),
            CompletionSuggestion("unit", "Unit", "Ordenar por unidad", "sort", 6),
            CompletionSuggestion("units", "Units", "Ordenar por unidades", "sort", 6),
            CompletionSuggestion("checkin", "Check-in", "Ordenar por check-in", "sort", 5),
            CompletionSuggestion("checkout", "Check-out", "Ordenar por check-out", "sort", 5),
            CompletionSuggestion("nights", "Nights", "Ordenar por noches", "sort", 5),
        ]
        
        return self._filter_suggestions(suggestions, context.current_input)
    
    def get_status_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias para status"""
        suggestions = [
            CompletionSuggestion("Hold", "Hold", "Reserva en espera", "status", 10),
            CompletionSuggestion("Confirmed", "Confirmed", "Reserva confirmada", "status", 10),
            CompletionSuggestion("Checked In", "Checked In", "Huésped registrado", "status", 9),
            CompletionSuggestion("Checked Out", "Checked Out", "Huésped salido", "status", 9),
            CompletionSuggestion("Cancelled", "Cancelled", "Reserva cancelada", "status", 8),
        ]
        
        return self._filter_suggestions(suggestions, context.current_input)
    
    def get_date_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias de fechas"""
        now = datetime.now()
        suggestions = []
        
        # Fechas comunes
        today = now.strftime("%Y-%m-%d")
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        next_week = (now + timedelta(days=7)).strftime("%Y-%m-%d")
        next_month = (now + timedelta(days=30)).strftime("%Y-%m-%d")
        
        suggestions.extend([
            CompletionSuggestion(today, f"Today ({today})", "Hoy", "date", 10),
            CompletionSuggestion(tomorrow, f"Tomorrow ({tomorrow})", "Mañana", "date", 9),
            CompletionSuggestion(next_week, f"Next Week ({next_week})", "Próxima semana", "date", 8),
            CompletionSuggestion(next_month, f"Next Month ({next_month})", "Próximo mes", "date", 7),
        ])
        
        # Patrones de fecha
        suggestions.extend([
            CompletionSuggestion("2024-", "2024-", "Año 2024", "date", 6),
            CompletionSuggestion("2025-", "2025-", "Año 2025", "date", 6),
        ])
        
        return self._filter_suggestions(suggestions, context.current_input)
    
    async def get_dynamic_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias dinámicas desde la API"""
        if not self.api_client:
            return []
        
        cache_key = f"dynamic_{context.parameter_name}_{context.endpoint}"
        cached = self._get_cache(cache_key)
        if cached:
            return self._filter_suggestions(cached, context.current_input)
        
        suggestions = []
        
        try:
            if context.parameter_name == "nodeId":
                # Obtener nodos disponibles
                response = await self.api_client.get("/nodes")
                if "_embedded" in response and "nodes" in response["_embedded"]:
                    for node in response["_embedded"]["nodes"]:
                        suggestions.append(CompletionSuggestion(
                            str(node["id"]),
                            f"{node.get('name', 'Node')} (ID: {node['id']})",
                            f"Node: {node.get('name', 'Unnamed')}",
                            "node",
                            5
                        ))
            
            elif context.parameter_name == "unitId":
                # Obtener unidades disponibles
                response = await self.api_client.get("/units")
                if "_embedded" in response and "units" in response["_embedded"]:
                    for unit in response["_embedded"]["units"]:
                        suggestions.append(CompletionSuggestion(
                            str(unit["id"]),
                            f"{unit.get('name', 'Unit')} (ID: {unit['id']})",
                            f"Unit: {unit.get('name', 'Unnamed')}",
                            "unit",
                            5
                        ))
            
            elif context.parameter_name == "contactId":
                # Obtener contactos disponibles
                response = await self.api_client.get("/contacts")
                if "_embedded" in response and "contacts" in response["_embedded"]:
                    for contact in response["_embedded"]["contacts"]:
                        suggestions.append(CompletionSuggestion(
                            str(contact["id"]),
                            f"{contact.get('name', 'Contact')} (ID: {contact['id']})",
                            f"Contact: {contact.get('name', 'Unnamed')}",
                            "contact",
                            5
                        ))
            
            if suggestions:
                self._set_cache(cache_key, suggestions)
                
        except Exception as e:
            # En caso de error, retornar sugerencias vacías
            pass
        
        return self._filter_suggestions(suggestions, context.current_input)
    
    async def get_completions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene completions basado en el contexto"""
        suggestions = []
        
        # Sugerencias basadas en el parámetro
        if context.parameter_name == "sortColumn":
            suggestions = self.get_sort_column_suggestions(context)
        elif context.parameter_name == "status":
            suggestions = self.get_status_suggestions(context)
        elif context.parameter_name in ["bookedStart", "bookedEnd", "arrivalStart", 
                                       "arrivalEnd", "departureStart", "departureEnd"]:
            suggestions = self.get_date_suggestions(context)
        elif context.parameter_name in ["nodeId", "unitId", "contactId", "reservationTypeId",
                                       "travelAgentId", "campaignId", "userId", "unitTypeId", "rateTypeId"]:
            suggestions = await self.get_dynamic_suggestions(context)
        else:
            # Sugerencias generales de parámetros
            suggestions = self.get_parameter_suggestions(context)
        
        return suggestions
    
    def get_endpoint_suggestions(self, context: CompletionContext) -> List[CompletionSuggestion]:
        """Obtiene sugerencias de endpoints"""
        suggestions = [
            CompletionSuggestion("/v2/pms/reservations", "Search Reservations V2", 
                               "Buscar reservas con API V2", "endpoint", 10),
            CompletionSuggestion("/reservations", "Search Reservations", 
                               "Buscar reservas (legacy)", "endpoint", 8),
            CompletionSuggestion("/units", "Units", "Listar unidades", "endpoint", 7),
            CompletionSuggestion("/contacts", "Contacts", "Listar contactos", "endpoint", 7),
            CompletionSuggestion("/nodes", "Nodes", "Listar nodos", "endpoint", 6),
        ]
        
        return self._filter_suggestions(suggestions, context.current_input)

# Funciones de conveniencia
async def get_parameter_completions(api_client, parameter_name: str, 
                                   current_input: str = "") -> List[CompletionSuggestion]:
    """Función de conveniencia para obtener completions de parámetros"""
    completion = TrackHSCompletion(api_client)
    context = CompletionContext(
        current_input=current_input,
        parameter_name=parameter_name
    )
    return await completion.get_completions(context)

async def get_endpoint_completions(current_input: str = "") -> List[CompletionSuggestion]:
    """Función de conveniencia para obtener completions de endpoints"""
    completion = TrackHSCompletion()
    context = CompletionContext(current_input=current_input)
    return completion.get_endpoint_suggestions(context)
