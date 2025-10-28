"""
Utilities y helpers para limpieza y sanitización de datos
Extrae lógica reutilizable de los Services eliminados
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Datos sensibles que deben ser sanitizados en logs
SENSITIVE_KEYS = {
    "email",
    "phone",
    "telephone",
    "mobile",
    "password",
    "pwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "card",
    "credit",
    "creditcard",
    "ssn",
    "social_security",
    "address",
    "street",
    "postal",
    "zip",
    "payment",
}


def sanitize_for_log(data: Any, max_depth: int = 10) -> Any:
    """
    Sanitiza datos sensibles para logging seguro.

    Oculta valores de campos que puedan contener información personal
    o sensible como emails, teléfonos, direcciones, etc.

    Args:
        data: Datos a sanitizar (dict, list, str, etc.)
        max_depth: Profundidad máxima de recursión

    Returns:
        Datos sanitizados con valores sensibles reemplazados por '***REDACTED***'
    """
    if max_depth <= 0:
        return "***MAX_DEPTH***"

    if data is None:
        return None

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            # Verificar si la clave contiene alguna palabra sensible
            is_sensitive = any(sensitive in key_lower for sensitive in SENSITIVE_KEYS)

            if is_sensitive:
                sanitized[key] = "***REDACTED***"
            else:
                sanitized[key] = sanitize_for_log(value, max_depth - 1)
        return sanitized

    elif isinstance(data, (list, tuple)):
        return [sanitize_for_log(item, max_depth - 1) for item in data]

    elif isinstance(data, str):
        # Detectar si parece un email o teléfono en el string
        if "@" in data and "." in data:  # Posible email
            return "***EMAIL_REDACTED***"
        # No sanitizar otros strings por defecto
        return data

    else:
        # Para otros tipos (int, float, bool, etc.) retornar tal cual
        return data


def clean_unit_data(unit_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Limpia datos de unidad para evitar errores de esquema.

    MEJOR PRÁCTICA: Transformación automática de tipos problemáticos.

    Args:
        unit_data: Datos de unidad sin limpiar

    Returns:
        Datos de unidad limpios
    """
    cleaned = unit_data.copy()

    # Limpiar campo area específicamente - MEJORADO
    if "area" in cleaned:
        cleaned["area"] = normalize_area(cleaned["area"])

    # Limpiar campos numéricos - MEJORADO
    numeric_fields = ["bedrooms", "bathrooms", "max_occupancy", "floors"]
    for field in numeric_fields:
        if field in cleaned:
            cleaned[field] = normalize_numeric(cleaned[field])

    # Limpiar campos booleanos - MEJORADO
    boolean_fields = [
        "is_active",
        "is_bookable",
        "pet_friendly",
        "smoking_allowed",
        "children_allowed",
        "events_allowed",
        "is_accessible",
    ]
    for field in boolean_fields:
        if field in cleaned:
            cleaned[field] = normalize_boolean(cleaned[field])

    # Limpiar campos de tipo float - MEJORADO
    float_fields = ["longitude", "latitude"]
    for field in float_fields:
        if field in cleaned:
            cleaned[field] = normalize_float(cleaned[field])

    return cleaned


def normalize_area(area_value: Any) -> Optional[float]:
    """
    Normaliza el campo area a float | None de forma estricta.

    Garantiza que el output siempre sea float o None, nunca string.

    Args:
        area_value: Valor del área a normalizar

    Returns:
        float normalizado o None
    """
    # Casos nulos directos
    if area_value is None:
        return None

    # Si ya es float, validar y retornar
    if isinstance(area_value, float):
        if area_value != area_value or area_value in [float("inf"), float("-inf")]:
            return None
        return area_value if area_value >= 0 else None

    # Si es int, convertir a float
    if isinstance(area_value, int):
        return float(area_value) if area_value >= 0 else None

    # Si es string, intentar conversión
    if isinstance(area_value, str):
        area_value = area_value.strip()

        # Casos de valores nulos
        if not area_value or area_value.lower() in [
            "null",
            "none",
            "n/a",
            "undefined",
            "nan",
            "empty",
            "",
        ]:
            return None

        try:
            # Limpiar string de caracteres no numéricos
            cleaned_str = "".join(c for c in area_value if c.isdigit() or c in ".-")

            if not cleaned_str:
                return None

            result = float(cleaned_str)

            # Validar resultado
            if (
                result != result
                or result in [float("inf"), float("-inf")]
                or result < 0
            ):
                return None

            return result

        except (ValueError, TypeError):
            return None

    # Para otros tipos, intentar conversión directa
    try:
        result = float(area_value)
        if result != result or result in [float("inf"), float("-inf")] or result < 0:
            return None
        return result
    except (ValueError, TypeError):
        return None


def normalize_numeric(value: Any) -> Optional[int]:
    """
    Normaliza valores numéricos a int.

    Args:
        value: Valor a normalizar

    Returns:
        int normalizado o None
    """
    if value is None:
        return None

    try:
        if isinstance(value, (int, float)):
            return int(value)
        elif isinstance(value, str):
            # Limpiar string de caracteres no numéricos
            cleaned_str = "".join(c for c in value.strip() if c.isdigit())
            if cleaned_str:
                return int(cleaned_str)
            else:
                return None
        else:
            return None
    except (ValueError, TypeError, AttributeError):
        logger.warning(f"Could not normalize numeric value: {value}")
        return None


def normalize_boolean(value: Any) -> Optional[bool]:
    """
    Normaliza valores booleanos.

    Args:
        value: Valor a normalizar

    Returns:
        bool normalizado o None
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value
    elif isinstance(value, int):
        return bool(value)
    elif isinstance(value, str):
        return value.lower() in ["true", "1", "yes", "on", "enabled"]
    else:
        return None


def normalize_float(value: Any) -> Optional[float]:
    """
    Normaliza valores a float.

    Args:
        value: Valor a normalizar

    Returns:
        float normalizado o None
    """
    if value is None:
        return None

    try:
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            # Limpiar string de caracteres no numéricos
            cleaned_str = "".join(c for c in value.strip() if c.isdigit() or c in ".-")
            if cleaned_str:
                return float(cleaned_str)
            else:
                return None
        else:
            return None
    except (ValueError, TypeError, AttributeError):
        logger.warning(f"Could not normalize float value: {value}")
        return None


def build_units_search_params(**kwargs) -> Dict[str, Any]:
    """
    Construir parámetros para la API de búsqueda de unidades.

    Convierte parámetros de Python a formato esperado por la API de TrackHS.
    Implementa todos los parámetros disponibles según la especificación OpenAPI.

    Args:
        **kwargs: Parámetros de búsqueda

    Returns:
        Diccionario de parámetros para la API
    """
    params = {}

    # Función helper para convertir strings a int
    def safe_int(value):
        """Convertir string a int de forma segura"""
        if value is None or value == "":
            return None
        try:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                cleaned = value.strip()
                if not cleaned:
                    return None
                return int(cleaned)
            return int(value)
        except (ValueError, TypeError, AttributeError):
            logger.warning(f"No se pudo convertir '{value}' a int")
            return None

    # Parámetros de paginación
    if kwargs.get("page") is not None:
        params["page"] = kwargs["page"]
    if kwargs.get("size") is not None:
        params["size"] = kwargs["size"]

    # Parámetros de ordenamiento
    if kwargs.get("sort_column") is not None:
        params["sortColumn"] = kwargs["sort_column"]
    if kwargs.get("sort_direction") is not None:
        params["sortDirection"] = kwargs["sort_direction"]

    # Parámetros de búsqueda de texto
    if kwargs.get("search") is not None:
        params["search"] = kwargs["search"]
    if kwargs.get("term") is not None:
        params["term"] = kwargs["term"]
    if kwargs.get("unit_code") is not None:
        params["unitCode"] = kwargs["unit_code"]
    if kwargs.get("short_name") is not None:
        params["shortName"] = kwargs["short_name"]

    # Parámetros de filtros por ID (convertir arrays a formato API)
    for param_name, api_name in [
        ("node_id", "nodeId"),
        ("amenity_id", "amenityId"),
        ("unit_type_id", "unitTypeId"),
        ("owner_id", "ownerId"),
        ("company_id", "companyId"),
        ("channel_id", "channelId"),
        ("lodging_type_id", "lodgingTypeId"),
        ("bed_type_id", "bedTypeId"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            # Convertir a lista si es un solo valor
            if isinstance(value, (int, str)):
                params[api_name] = [value]
            elif isinstance(value, list):
                params[api_name] = value
            else:
                logger.warning(f"Tipo no soportado para {param_name}: {type(value)}")

    if kwargs.get("amenity_all") is not None:
        params["amenityAll"] = kwargs["amenity_all"]
    if kwargs.get("unit_ids") is not None:
        params["id"] = kwargs["unit_ids"]

    # Parámetros de dormitorios
    for param_name, api_name in [
        ("bedrooms", "bedrooms"),
        ("min_bedrooms", "minBedrooms"),
        ("max_bedrooms", "maxBedrooms"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    # Parámetros de baños
    for param_name, api_name in [
        ("bathrooms", "bathrooms"),
        ("min_bathrooms", "minBathrooms"),
        ("max_bathrooms", "maxBathrooms"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    # Parámetros de capacidad
    for param_name, api_name in [
        ("occupancy", "occupancy"),
        ("min_occupancy", "minOccupancy"),
        ("max_occupancy", "maxOccupancy"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    # Parámetros de fechas
    if kwargs.get("arrival") is not None:
        params["arrival"] = kwargs["arrival"]
    if kwargs.get("departure") is not None:
        params["departure"] = kwargs["departure"]
    if kwargs.get("content_updated_since") is not None:
        params["contentUpdatedSince"] = kwargs["content_updated_since"]

    # Parámetros de estado y características
    for param_name, api_name in [
        ("is_active", "isActive"),
        ("is_bookable", "isBookable"),
        ("pets_friendly", "petsFriendly"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    if kwargs.get("unit_status") is not None:
        params["unitStatus"] = kwargs["unit_status"]

    # Parámetros de funcionalidad adicional
    for param_name, api_name in [
        ("computed", "computed"),
        ("inherited", "inherited"),
        ("limited", "limited"),
        ("include_descriptions", "includeDescriptions"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    # Parámetros de filtros adicionales
    for param_name, api_name in [
        ("calendar_id", "calendarId"),
        ("role_id", "roleId"),
        ("promo_code_id", "promoCodeId"),
    ]:
        value = kwargs.get(param_name)
        if value is not None:
            params[api_name] = value

    return params
