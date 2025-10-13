"""
Ejemplos de uso para la API de Units
Proporciona ejemplos prácticos de cómo usar la herramienta search_units
"""

from typing import Any, Dict, List


class UnitsExamples:
    """Ejemplos de uso para la API de Units"""

    @staticmethod
    def get_basic_examples() -> List[Dict[str, Any]]:
        """Ejemplos básicos de uso"""
        return [
            {
                "name": "Búsqueda básica",
                "description": "Obtener las primeras 25 unidades",
                "parameters": {"page": 0, "size": 25},
                "expected_result": "Lista de 25 unidades con información básica",
            },
            {
                "name": "Búsqueda con ordenamiento",
                "description": "Ordenar unidades por nombre en orden descendente",
                "parameters": {
                    "sort_column": "name",
                    "sort_direction": "desc",
                    "size": 50,
                },
                "expected_result": "50 unidades ordenadas por nombre (Z-A)",
            },
            {
                "name": "Búsqueda por texto",
                "description": "Buscar unidades que contengan 'villa' en nombre o descripción",
                "parameters": {"search": "villa", "size": 10},
                "expected_result": "Unidades que contengan 'villa' en nombre o descripción",
            },
        ]

    @staticmethod
    def get_filtering_examples() -> List[Dict[str, Any]]:
        """Ejemplos de filtrado"""
        return [
            {
                "name": "Filtro por características físicas",
                "description": "Buscar unidades con 2 habitaciones, 2 baños, que permitan mascotas",
                "parameters": {
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "pets_friendly": 1,
                    "is_active": 1,
                },
                "expected_result": "Unidades con 2 habitaciones, 2 baños, que permitan mascotas y estén activas",
            },
            {
                "name": "Filtro por rango de habitaciones",
                "description": "Buscar unidades con entre 1 y 3 habitaciones",
                "parameters": {"min_bedrooms": 1, "max_bedrooms": 3, "is_active": 1},
                "expected_result": "Unidades con 1-3 habitaciones activas",
            },
            {
                "name": "Filtro por ubicación",
                "description": "Buscar unidades en nodos específicos",
                "parameters": {"node_id": "1,2,3", "is_active": 1},
                "expected_result": "Unidades activas en los nodos 1, 2 o 3",
            },
            {
                "name": "Filtro por amenidades",
                "description": "Buscar unidades con amenidades específicas",
                "parameters": {
                    "amenity_id": "1,2,3",
                    "pets_friendly": 1,
                    "events_allowed": 1,
                },
                "expected_result": "Unidades con amenidades 1, 2 o 3, que permitan mascotas y eventos",
            },
        ]

    @staticmethod
    def get_availability_examples() -> List[Dict[str, Any]]:
        """Ejemplos de búsqueda por disponibilidad"""
        return [
            {
                "name": "Disponibilidad para fechas específicas",
                "description": "Buscar unidades disponibles para una semana en enero",
                "parameters": {
                    "arrival": "2024-01-01",
                    "departure": "2024-01-07",
                    "is_bookable": 1,
                },
                "expected_result": "Unidades disponibles del 1 al 7 de enero de 2024",
            },
            {
                "name": "Unidades actualizadas recientemente",
                "description": "Buscar unidades actualizadas en los últimos 7 días",
                "parameters": {
                    "content_updated_since": "2024-01-01T00:00:00Z",
                    "is_active": 1,
                },
                "expected_result": "Unidades activas actualizadas desde el 1 de enero de 2024",
            },
        ]

    @staticmethod
    def get_advanced_examples() -> List[Dict[str, Any]]:
        """Ejemplos avanzados"""
        return [
            {
                "name": "Búsqueda compleja con múltiples filtros",
                "description": "Buscar unidades de lujo con múltiples criterios",
                "parameters": {
                    "bedrooms": 3,
                    "min_bathrooms": 2,
                    "pets_friendly": 1,
                    "events_allowed": 1,
                    "is_accessible": 1,
                    "is_active": 1,
                    "include_descriptions": 1,
                    "sort_column": "name",
                    "sort_direction": "asc",
                },
                "expected_result": "Unidades de lujo con 3 habitaciones, 2+ baños, accesibles, que permitan mascotas y eventos",
            },
            {
                "name": "Búsqueda por estado de unidad",
                "description": "Buscar unidades limpias y disponibles",
                "parameters": {
                    "unit_status": "clean",
                    "is_bookable": 1,
                    "is_active": 1,
                },
                "expected_result": "Unidades limpias, reservables y activas",
            },
            {
                "name": "Búsqueda con paginación grande",
                "description": "Obtener un gran conjunto de datos con paginación",
                "parameters": {
                    "page": 0,
                    "size": 1000,
                    "is_active": 1,
                    "sort_column": "id",
                    "sort_direction": "asc",
                },
                "expected_result": "1000 unidades activas ordenadas por ID",
            },
        ]

    @staticmethod
    def get_error_examples() -> List[Dict[str, Any]]:
        """Ejemplos de manejo de errores"""
        return [
            {
                "name": "Error de paginación",
                "description": "Intentar acceder a una página que excede el límite",
                "parameters": {"page": 100, "size": 100},
                "expected_error": "Total results (page * size) must be <= 10,000",
            },
            {
                "name": "Error de formato de fecha",
                "description": "Usar formato de fecha inválido",
                "parameters": {"arrival": "01/01/2024", "departure": "01/07/2024"},
                "expected_error": "Invalid date format. Use ISO 8601 format.",
            },
            {
                "name": "Error de valor booleano",
                "description": "Usar valor booleano incorrecto",
                "parameters": {"pets_friendly": True, "is_active": False},
                "expected_error": "Boolean values must be 0 or 1",
            },
            {
                "name": "Error de rango de habitaciones",
                "description": "Mínimo mayor que máximo",
                "parameters": {"min_bedrooms": 3, "max_bedrooms": 1},
                "expected_error": "min_bedrooms must be <= max_bedrooms",
            },
        ]

    @staticmethod
    def get_performance_examples() -> List[Dict[str, Any]]:
        """Ejemplos de optimización de rendimiento"""
        return [
            {
                "name": "Búsqueda optimizada con filtros específicos",
                "description": "Usar filtros específicos para reducir resultados",
                "parameters": {
                    "node_id": "1",
                    "is_active": 1,
                    "is_bookable": 1,
                    "size": 50,
                },
                "tip": "Usar filtros específicos reduce el tiempo de respuesta",
            },
            {
                "name": "Búsqueda con atributos limitados",
                "description": "Obtener solo información básica para listados",
                "parameters": {"limited": 1, "size": 100},
                "tip": "Usar limited=1 para obtener solo campos básicos (id, name, longitude, latitude, isActive)",
            },
            {
                "name": "Búsqueda sin descripciones",
                "description": "Excluir descripciones para mejorar rendimiento",
                "parameters": {"include_descriptions": 0, "size": 100},
                "tip": "Excluir descripciones mejora el rendimiento en listados grandes",
            },
        ]

    @staticmethod
    def get_integration_examples() -> List[Dict[str, Any]]:
        """Ejemplos de integración"""
        return [
            {
                "name": "Integración con sistema de reservas",
                "description": "Buscar unidades disponibles para reserva",
                "parameters": {
                    "arrival": "2024-01-01",
                    "departure": "2024-01-07",
                    "is_bookable": 1,
                    "is_active": 1,
                    "unit_status": "clean",
                },
                "use_case": "Sistema de reservas online",
            },
            {
                "name": "Integración con sistema de gestión",
                "description": "Obtener todas las unidades para gestión",
                "parameters": {
                    "is_active": 1,
                    "include_descriptions": 1,
                    "computed": 1,
                    "inherited": 1,
                },
                "use_case": "Panel de administración",
            },
            {
                "name": "Integración con canal de distribución",
                "description": "Sincronizar unidades con canal externo",
                "parameters": {
                    "content_updated_since": "2024-01-01T00:00:00Z",
                    "is_active": 1,
                    "include_descriptions": 1,
                },
                "use_case": "Sincronización con OTAs",
            },
        ]

    @staticmethod
    def get_response_examples() -> List[Dict[str, Any]]:
        """Ejemplos de respuestas"""
        return [
            {
                "name": "Respuesta básica",
                "description": "Estructura típica de respuesta",
                "response": {
                    "_embedded": {
                        "units": [
                            {
                                "id": 7,
                                "name": "Townhome 444",
                                "shortName": "TH444",
                                "unitCode": "TH444",
                                "nodeId": 81,
                                "bedrooms": 3,
                                "fullBathrooms": 3,
                                "maxOccupancy": 12,
                                "petsFriendly": True,
                                "maxPets": 1,
                                "eventsAllowed": False,
                                "smokingAllowed": False,
                                "childrenAllowed": True,
                                "minimumAgeLimit": 25,
                                "isAccessible": False,
                                "updatedAt": "2020-05-21T22:30:18-06:00",
                            }
                        ]
                    },
                    "page": 0,
                    "page_count": 13,
                    "page_size": 25,
                    "total_items": 304,
                    "_links": {
                        "self": {
                            "href": "https://api.example.com/api/pms/units/?page=0"
                        },
                        "first": {"href": "https://api.example.com/api/pms/units/"},
                        "last": {
                            "href": "https://api.example.com/api/pms/units/?page=12"
                        },
                        "next": {
                            "href": "https://api.example.com/api/pms/units/?page=1"
                        },
                    },
                },
            }
        ]
