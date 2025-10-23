"""
Documentación completa de la API de Units
Proporciona información detallada sobre el endpoint /pms/units
"""

from typing import Any, Dict, List


class UnitsAPIDocumentation:
    """Documentación completa de la API de Units"""

    @staticmethod
    def get_endpoint_info() -> Dict[str, Any]:
        """Información del endpoint"""
        return {
            "endpoint": "/pms/units",
            "method": "GET",
            "api": "Channel API",
            "authentication": "Basic Auth o HMAC",
            "description": "Obtiene la colección de unidades disponibles",
            "base_url": "{customerDomain}/api",
            "version": "1.0",
        }

    @staticmethod
    def get_parameters() -> Dict[str, Any]:
        """Documentación completa de parámetros"""
        return {
            "pagination": {
                "page": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "maximum": 400,
                    "description": "Número de página (1-based). Max total results: 10,000 (400 pages × 25 results max)",
                    "max_total_results": 10000,
                },
                "size": {
                    "type": "integer",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 25,
                    "description": "Tamaño de página (1-25)",
                },
            },
            "sorting": {
                "sortColumn": {
                    "type": "string",
                    "enum": ["id", "name", "nodeName", "unitTypeName"],
                    "default": "name",
                    "description": "Columna para ordenar",
                },
                "sortDirection": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "default": "asc",
                    "description": "Dirección de ordenamiento",
                },
            },
            "search": {
                "search": {
                    "type": "string",
                    "description": "Búsqueda por nombre o descripción",
                },
                "term": {"type": "string", "description": "Búsqueda por término"},
                "unitCode": {
                    "type": "string",
                    "description": "Búsqueda por código de unidad (exacto o con % para wildcard)",
                },
                "shortName": {
                    "type": "string",
                    "description": "Búsqueda por nombre corto (exacto o con % para wildcard)",
                },
            },
            "filters": {
                "nodeId": {
                    "type": "integer|array",
                    "description": "ID(s) del nodo específico",
                },
                "amenityId": {
                    "type": "integer|array",
                    "description": "ID(s) de amenidad específica",
                },
                "unitTypeId": {
                    "type": "integer|array",
                    "description": "ID(s) del tipo de unidad específico",
                },
                "id": {"type": "array", "description": "IDs específicos de unidades"},
                "calendarId": {"type": "integer", "description": "ID del calendario"},
                "roleId": {"type": "integer", "description": "ID del rol"},
            },
            "rooms_bathrooms": {
                "bedrooms": {
                    "type": "integer",
                    "description": "Número exacto de habitaciones",
                },
                "minBedrooms": {
                    "type": "integer",
                    "description": "Mínimo de habitaciones",
                },
                "maxBedrooms": {
                    "type": "integer",
                    "description": "Máximo de habitaciones",
                },
                "bathrooms": {
                    "type": "integer",
                    "description": "Número exacto de baños",
                },
                "minBathrooms": {"type": "integer", "description": "Mínimo de baños"},
                "maxBathrooms": {"type": "integer", "description": "Máximo de baños"},
            },
            "boolean_filters": {
                "petsFriendly": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Permite mascotas (0/1)",
                },
                "allowUnitRates": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Permite tarifas de unidad (0/1)",
                },
                "computed": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Valores computados adicionales (0/1)",
                },
                "inherited": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Atributos heredados (0/1)",
                },
                "limited": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Atributos limitados (0/1)",
                },
                "isBookable": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Es reservable (0/1)",
                },
                "includeDescriptions": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Incluir descripciones (0/1)",
                },
                "isActive": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Está activo (0/1)",
                },
            },
            "dates": {
                "arrival": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de llegada (ISO 8601)",
                },
                "departure": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha de salida (ISO 8601)",
                },
                "contentUpdatedSince": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Actualización de contenido desde (ISO 8601)",
                },
                "updatedSince": {
                    "type": "string",
                    "format": "date",
                    "description": "Actualización desde (ISO 8601) - deprecated",
                },
            },
            "status": {
                "unitStatus": {
                    "type": "string",
                    "enum": ["clean", "dirty", "occupied", "inspection", "inprogress"],
                    "description": "Estado de la unidad",
                }
            },
        }

    @staticmethod
    def get_response_structure() -> Dict[str, Any]:
        """Estructura de la respuesta"""
        return {
            "_embedded": {
                "units": [
                    {
                        "id": "integer",
                        "name": "string",
                        "shortName": "string (optional)",
                        "unitCode": "string (optional)",
                        "headline": "string (optional)",
                        "shortDescription": "string (optional)",
                        "longDescription": "string (optional)",
                        "houseRules": "string (optional)",
                        "nodeId": "integer",
                        "unitType": "object (deprecated)",
                        "lodgingType": "object",
                        "directions": "string (optional)",
                        "checkinDetails": "string (optional)",
                        "timezone": "string",
                        "checkinTime": "string",
                        "hasEarlyCheckin": "boolean",
                        "earlyCheckinTime": "string (optional)",
                        "checkoutTime": "string",
                        "hasLateCheckout": "boolean",
                        "lateCheckoutTime": "string (optional)",
                        "minBookingWindow": "integer (optional)",
                        "maxBookingWindow": "integer (optional)",
                        "website": "string (optional)",
                        "phone": "string (optional)",
                        "streetAddress": "string",
                        "extendedAddress": "string (optional)",
                        "locality": "string",
                        "region": "string",
                        "postal": "string",
                        "country": "string",
                        "latitude": "number (optional)",
                        "longitude": "number (optional)",
                        "petsFriendly": "boolean",
                        "maxPets": "integer (optional)",
                        "eventsAllowed": "boolean",
                        "smokingAllowed": "boolean",
                        "childrenAllowed": "boolean",
                        "minimumAgeLimit": "integer (optional)",
                        "isAccessible": "boolean",
                        "area": "integer (optional)",
                        "floors": "integer (optional)",
                        "maxOccupancy": "integer",
                        "securityDeposit": "string (optional)",
                        "bedrooms": "integer",
                        "fullBathrooms": "integer",
                        "threeQuarterBathrooms": "integer (optional)",
                        "halfBathrooms": "integer",
                        "bedTypes": "array (optional)",
                        "rooms": "array (optional)",
                        "amenities": "array (optional)",
                        "amenityDescription": "string (optional)",
                        "custom": "object (optional)",
                        "coverImage": "string (optional, deprecated)",
                        "taxId": "string (optional)",
                        "localOffice": "object (optional)",
                        "regulations": "array (optional, deprecated)",
                        "updatedAt": "string",
                    }
                ]
            },
            "page": "integer",
            "page_count": "integer",
            "page_size": "integer",
            "total_items": "integer",
            "_links": {
                "self": "object",
                "first": "object",
                "last": "object",
                "next": "object (optional)",
                "prev": "object (optional)",
            },
        }

    @staticmethod
    def get_error_codes() -> Dict[str, Any]:
        """Códigos de error posibles"""
        return {
            "400": {
                "description": "Bad Request",
                "causes": [
                    "Invalid parameter format",
                    "Invalid date format",
                    "Invalid ID format",
                    "Invalid boolean value (must be 0 or 1)",
                ],
            },
            "401": {
                "description": "Unauthorized",
                "causes": ["Invalid credentials", "Expired authentication"],
            },
            "403": {
                "description": "Forbidden",
                "causes": [
                    "Insufficient permissions",
                    "Account not authorized for Channel API",
                ],
            },
            "404": {
                "description": "Not Found",
                "causes": ["Endpoint not found", "Invalid API URL"],
            },
            "500": {
                "description": "Internal Server Error",
                "causes": ["API temporarily unavailable", "Server error"],
            },
        }

    @staticmethod
    def get_usage_examples() -> List[Dict[str, Any]]:
        """Ejemplos de uso"""
        return [
            {
                "name": "Búsqueda básica",
                "description": "Obtener las primeras 25 unidades",
                "parameters": {"page": 0, "size": 25},
            },
            {
                "name": "Búsqueda por características",
                "description": "Buscar unidades con 2 habitaciones, 2 baños, que permitan mascotas",
                "parameters": {
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "petsFriendly": 1,
                    "isActive": 1,
                },
            },
            {
                "name": "Búsqueda por disponibilidad",
                "description": "Buscar unidades disponibles para fechas específicas",
                "parameters": {
                    "arrival": "2024-01-01",
                    "departure": "2024-01-07",
                    "isBookable": 1,
                },
            },
            {
                "name": "Búsqueda por amenidades",
                "description": "Buscar unidades con amenidades específicas",
                "parameters": {
                    "amenityId": "1,2,3",
                    "petsFriendly": 1,
                    "eventsAllowed": 1,
                },
            },
            {
                "name": "Búsqueda por ubicación",
                "description": "Buscar unidades en nodos específicos",
                "parameters": {"nodeId": "1,2,3", "locality": "Miami"},
            },
            {
                "name": "Búsqueda con ordenamiento",
                "description": "Ordenar por nombre en orden descendente",
                "parameters": {
                    "sortColumn": "name",
                    "sortDirection": "desc",
                    "size": 50,
                },
            },
        ]

    @staticmethod
    def get_limitations() -> Dict[str, Any]:
        """Limitaciones de la API"""
        return {
            "pagination": {
                "max_page_size": 1000,
                "max_total_results": 10000,
                "default_page_size": 3,
            },
            "rate_limits": {
                "requests_per_minute": "Varies by account",
                "concurrent_requests": "Varies by account",
            },
            "data_limitations": {
                "deprecated_fields": [
                    "unitType",
                    "coverImage",
                    "regulations",
                    "updatedSince",
                ],
                "unstable_fields": ["unitType", "customData"],
            },
            "authentication": {
                "supported_methods": ["Basic Auth", "HMAC"],
                "session_timeout": "Varies by configuration",
            },
        }

    @staticmethod
    def get_best_practices() -> List[str]:
        """Mejores prácticas"""
        return [
            "Usar paginación para grandes conjuntos de datos",
            "Implementar caché para consultas frecuentes",
            "Validar formatos de fecha ISO 8601",
            "Manejar errores de autenticación apropiadamente",
            "Usar filtros específicos para reducir resultados",
            "Evitar campos deprecated (unitType, coverImage, regulations)",
            "Usar contentUpdatedSince en lugar de updatedSince",
            "Implementar reintentos para errores 500",
            "Validar límites de paginación (10k máximo)",
            "Usar valores booleanos 0/1 en lugar de true/false",
        ]
