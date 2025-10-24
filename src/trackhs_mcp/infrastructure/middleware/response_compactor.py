"""
Middleware para compactar respuestas de API para uso con agentes de voz
Optimizado para ElevenLabs + Gemini 2.5 y otros sistemas con límites de contexto

Este middleware reduce el tamaño de las respuestas manteniendo la información esencial
para agentes de servicio al cliente que hablan por teléfono.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ResponseCompactor:
    """
    Compacta respuestas de API para optimizar uso de contexto en agentes de voz.

    Estrategias de compactación:
    1. Eliminar campos innecesarios para servicio al cliente
    2. Resumir listas largas
    3. Reducir descripciones largas
    4. Eliminar datos técnicos/administrativos
    """

    # Campos a mantener para cada tipo de entidad
    RESERVATION_ESSENTIAL_FIELDS = {
        "id",
        "name",
        "status",
        "checkin",
        "checkout",
        "nights",
        "guests",
        "guestName",
        "contact",  # Info básica de contacto
        "unit",  # Info básica de unidad
        "totalPrice",
        "balance",
        "phone",
        "email",
    }

    UNIT_ESSENTIAL_FIELDS = {
        "id",
        "name",
        "code",
        "bedrooms",
        "bathrooms",
        "maxOccupancy",
        "isActive",
        "isBookable",
        "shortDescription",  # Solo descripción corta
        "unitType",
        "node",
    }

    AMENITY_ESSENTIAL_FIELDS = {
        "id",
        "name",
        "group",
        "isPublic",
    }

    CONTACT_ESSENTIAL_FIELDS = {
        "id",
        "firstName",
        "lastName",
        "email",
        "phone",
        "mobilePhone",
    }

    @staticmethod
    def compact_reservation(reservation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compacta una reserva manteniendo solo información esencial para servicio al cliente.

        Args:
            reservation: Datos completos de la reserva

        Returns:
            Reserva compactada con información esencial
        """
        compacted = {}

        # Copiar campos esenciales
        for field in ResponseCompactor.RESERVATION_ESSENTIAL_FIELDS:
            if field in reservation:
                value = reservation[field]

                # Compactar sub-objetos
                if field == "contact" and isinstance(value, dict):
                    compacted[field] = ResponseCompactor.compact_contact(value)
                elif field == "unit" and isinstance(value, dict):
                    compacted[field] = ResponseCompactor._compact_unit_brief(value)
                else:
                    compacted[field] = value

        # Información financiera resumida
        if "guestBreakdown" in reservation:
            breakdown = reservation["guestBreakdown"]
            compacted["pricing"] = {
                "subtotal": breakdown.get("subtotal"),
                "tax": breakdown.get("tax"),
                "total": breakdown.get("total"),
            }

        return compacted

    @staticmethod
    def compact_reservation_list(
        reservations: List[Dict[str, Any]], max_items: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Compacta una lista de reservas.

        Args:
            reservations: Lista de reservas completas
            max_items: Máximo número de items a retornar (None = sin límite)

        Returns:
            Lista de reservas compactadas
        """
        items_to_process = reservations[:max_items] if max_items else reservations
        compacted_list = [
            ResponseCompactor.compact_reservation(res) for res in items_to_process
        ]

        # Advertencia si se truncaron resultados
        if max_items and len(reservations) > max_items:
            logger.warning(
                f"ResponseCompactor: Truncados {len(reservations) - max_items} "
                f"resultados de {len(reservations)} totales"
            )

        return compacted_list

    @staticmethod
    def compact_unit(unit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compacta una unidad manteniendo solo información esencial.

        Args:
            unit: Datos completos de la unidad

        Returns:
            Unidad compactada
        """
        compacted = {}

        # Copiar campos esenciales
        for field in ResponseCompactor.UNIT_ESSENTIAL_FIELDS:
            if field in unit:
                compacted[field] = unit[field]

        # Resumir amenidades (solo nombres, no toda la info)
        if "amenities" in unit and isinstance(unit["amenities"], list):
            compacted["amenities"] = [
                amenity.get("name", amenity.get("id", "Unknown"))
                for amenity in unit["amenities"][:10]  # Máximo 10 amenidades
            ]
            if len(unit["amenities"]) > 10:
                compacted["amenitiesCount"] = len(unit["amenities"])

        # Resumir imágenes (solo contar, no incluir URLs)
        if "images" in unit and isinstance(unit["images"], list):
            compacted["imageCount"] = len(unit["images"])

        return compacted

    @staticmethod
    def _compact_unit_brief(unit: Dict[str, Any]) -> Dict[str, Any]:
        """Versión ultra-compacta de unidad para embeds en reservas"""
        return {
            "id": unit.get("id"),
            "name": unit.get("name"),
            "code": unit.get("code"),
        }

    @staticmethod
    def compact_unit_list(
        units: List[Dict[str, Any]], max_items: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Compacta una lista de unidades.

        Args:
            units: Lista de unidades completas
            max_items: Máximo número de items a retornar

        Returns:
            Lista de unidades compactadas
        """
        items_to_process = units[:max_items] if max_items else units
        compacted_list = [
            ResponseCompactor.compact_unit(unit) for unit in items_to_process
        ]

        if max_items and len(units) > max_items:
            logger.warning(
                f"ResponseCompactor: Truncados {len(units) - max_items} "
                f"resultados de {len(units)} totales"
            )

        return compacted_list

    @staticmethod
    def compact_amenity(amenity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compacta una amenidad manteniendo solo información esencial.

        Args:
            amenity: Datos completos de la amenidad

        Returns:
            Amenidad compactada
        """
        compacted = {}

        for field in ResponseCompactor.AMENITY_ESSENTIAL_FIELDS:
            if field in amenity:
                value = amenity[field]
                # Simplificar grupo si es un objeto
                if field == "group" and isinstance(value, dict):
                    compacted[field] = value.get("name", value.get("id"))
                else:
                    compacted[field] = value

        return compacted

    @staticmethod
    def compact_amenity_list(
        amenities: List[Dict[str, Any]], max_items: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Compacta una lista de amenidades"""
        items_to_process = amenities[:max_items] if max_items else amenities
        compacted_list = [
            ResponseCompactor.compact_amenity(amenity) for amenity in items_to_process
        ]

        if max_items and len(amenities) > max_items:
            logger.warning(
                f"ResponseCompactor: Truncados {len(amenities) - max_items} "
                f"resultados de {len(amenities)} totales"
            )

        return compacted_list

    @staticmethod
    def compact_contact(contact: Dict[str, Any]) -> Dict[str, Any]:
        """Compacta información de contacto"""
        compacted = {}

        for field in ResponseCompactor.CONTACT_ESSENTIAL_FIELDS:
            if field in contact:
                compacted[field] = contact[field]

        return compacted

    @staticmethod
    def compact_api_response(
        response: Dict[str, Any], response_type: str, max_items: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Compacta una respuesta completa de API.

        Args:
            response: Respuesta completa de la API
            response_type: Tipo de respuesta ('reservations', 'units', 'amenities', etc.)
            max_items: Máximo número de items a retornar en listas

        Returns:
            Respuesta compactada
        """
        compacted_response = {}

        # Mantener metadata de paginación (importante para el agente)
        if "pagination" in response:
            compacted_response["pagination"] = response["pagination"]

        # Compactar datos según tipo
        if response_type == "reservations":
            if "data" in response and isinstance(response["data"], list):
                compacted_response["data"] = ResponseCompactor.compact_reservation_list(
                    response["data"], max_items
                )
                compacted_response["count"] = len(compacted_response["data"])

        elif response_type == "units":
            if "data" in response and isinstance(response["data"], list):
                compacted_response["data"] = ResponseCompactor.compact_unit_list(
                    response["data"], max_items
                )
                compacted_response["count"] = len(compacted_response["data"])

        elif response_type == "amenities":
            if "data" in response and isinstance(response["data"], list):
                compacted_response["data"] = ResponseCompactor.compact_amenity_list(
                    response["data"], max_items
                )
                compacted_response["count"] = len(compacted_response["data"])

        elif response_type == "reservation":
            # Respuesta de un solo objeto
            compacted_response = ResponseCompactor.compact_reservation(response)

        else:
            # Tipo desconocido, retornar tal cual pero con advertencia
            logger.warning(
                f"ResponseCompactor: Tipo de respuesta desconocido '{response_type}'"
            )
            compacted_response = response

        return compacted_response


# Funciones helper para uso directo
def compact_for_voice_agent(
    response: Dict[str, Any], response_type: str, max_items: int = 3
) -> Dict[str, Any]:
    """
    Función helper para compactar respuestas específicamente para agentes de voz.

    Por defecto limita a 3 items máximo.

    Args:
        response: Respuesta de la API
        response_type: Tipo de respuesta
        max_items: Máximo número de items (default: 3 para agentes de voz)

    Returns:
        Respuesta compactada y optimizada para voz
    """
    return ResponseCompactor.compact_api_response(
        response, response_type, max_items=max_items
    )


def estimate_token_count(data: Any) -> int:
    """
    Estima el número de tokens en una respuesta.

    Usa una heurística simple: ~4 caracteres por token

    Args:
        data: Datos a estimar

    Returns:
        Estimación de tokens
    """
    import json

    json_str = json.dumps(data, ensure_ascii=False)
    char_count = len(json_str)
    # Heurística: ~4 caracteres por token
    return char_count // 4


def should_compact_response(data: Any, max_tokens: int = 2000) -> bool:
    """
    Determina si una respuesta debería ser compactada.

    Args:
        data: Datos a evaluar
        max_tokens: Límite de tokens para considerar compactación

    Returns:
        True si debería compactarse
    """
    estimated_tokens = estimate_token_count(data)
    return estimated_tokens > max_tokens
