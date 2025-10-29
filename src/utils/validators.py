"""
Validadores comunes para TrackHS MCP Server
"""

from datetime import date, datetime
from typing import Any, Dict, Optional, Tuple

from .exceptions import TrackHSValidationError
from .logger import get_logger


def validate_date_range(
    start_date: Optional[str], end_date: Optional[str], field_prefix: str = "date"
) -> Tuple[Optional[date], Optional[date]]:
    """
    Valida un rango de fechas

    Args:
        start_date: Fecha de inicio (formato YYYY-MM-DD)
        end_date: Fecha de fin (formato YYYY-MM-DD)
        field_prefix: Prefijo para los nombres de campo

    Returns:
        Tupla con las fechas parseadas

    Raises:
        TrackHSValidationError: Si las fechas son inválidas
    """
    logger = get_logger(__name__)

    parsed_start = None
    parsed_end = None

    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(
                f"Formato de fecha inválido para {field_prefix}_start: {start_date}",
                extra={
                    "field": f"{field_prefix}_start",
                    "value": start_date,
                    "expected_format": "YYYY-MM-DD",
                },
            )
            raise TrackHSValidationError(
                f"{field_prefix}_start",
                start_date,
                "Formato de fecha inválido. Use YYYY-MM-DD",
            )

    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(
                f"Formato de fecha inválido para {field_prefix}_end: {end_date}",
                extra={
                    "field": f"{field_prefix}_end",
                    "value": end_date,
                    "expected_format": "YYYY-MM-DD",
                },
            )
            raise TrackHSValidationError(
                f"{field_prefix}_end",
                end_date,
                "Formato de fecha inválido. Use YYYY-MM-DD",
            )

    # Validar que start_date <= end_date
    if parsed_start and parsed_end and parsed_start > parsed_end:
        logger.warning(
            f"Fecha de inicio mayor que fecha de fin: {start_date} > {end_date}",
            extra={"start_date": start_date, "end_date": end_date},
        )
        raise TrackHSValidationError(
            f"{field_prefix}_start",
            start_date,
            f"Fecha de inicio debe ser menor o igual que fecha de fin ({end_date})",
        )

    return parsed_start, parsed_end


def validate_pagination_params(
    page: int, size: int, max_size: int = 100
) -> Tuple[int, int]:
    """
    Valida parámetros de paginación

    Args:
        page: Número de página
        size: Tamaño de página
        max_size: Tamaño máximo de página

    Returns:
        Tupla con los parámetros validados

    Raises:
        TrackHSValidationError: Si los parámetros son inválidos
    """
    logger = get_logger(__name__)

    if page < 1:
        logger.warning(
            f"Número de página inválido: {page}",
            extra={"field": "page", "value": page, "min_value": 1},
        )
        raise TrackHSValidationError(
            "page", page, "Número de página debe ser mayor o igual a 1"
        )

    if size < 1:
        logger.warning(
            f"Tamaño de página inválido: {size}",
            extra={"field": "size", "value": size, "min_value": 1},
        )
        raise TrackHSValidationError(
            "size", size, "Tamaño de página debe ser mayor o igual a 1"
        )

    if size > max_size:
        logger.warning(
            f"Tamaño de página excede el máximo: {size} > {max_size}",
            extra={"field": "size", "value": size, "max_value": max_size},
        )
        raise TrackHSValidationError(
            "size", size, f"Tamaño de página no puede exceder {max_size}"
        )

    return page, size


def validate_positive_integer(value: Any, field_name: str, min_value: int = 1) -> int:
    """
    Valida que un valor sea un entero positivo

    Args:
        value: Valor a validar
        field_name: Nombre del campo
        min_value: Valor mínimo permitido

    Returns:
        Valor validado como entero

    Raises:
        TrackHSValidationError: Si el valor es inválido
    """
    logger = get_logger(__name__)

    try:
        int_value = int(value)
    except (ValueError, TypeError):
        logger.warning(
            f"Valor no es un entero válido: {value}",
            extra={"field": field_name, "value": value, "expected_type": "int"},
        )
        raise TrackHSValidationError(field_name, value, f"Debe ser un entero válido")

    if int_value < min_value:
        logger.warning(
            f"Valor menor al mínimo permitido: {int_value} < {min_value}",
            extra={"field": field_name, "value": int_value, "min_value": min_value},
        )
        raise TrackHSValidationError(
            field_name, int_value, f"Debe ser mayor o igual a {min_value}"
        )

    return int_value


def validate_string_length(
    value: str, field_name: str, max_length: int, min_length: int = 1
) -> str:
    """
    Valida la longitud de una cadena

    Args:
        value: Valor a validar
        field_name: Nombre del campo
        max_length: Longitud máxima
        min_length: Longitud mínima

    Returns:
        Valor validado

    Raises:
        TrackHSValidationError: Si el valor es inválido
    """
    logger = get_logger(__name__)

    if not isinstance(value, str):
        logger.warning(
            f"Valor no es una cadena: {value}",
            extra={"field": field_name, "value": value, "expected_type": "str"},
        )
        raise TrackHSValidationError(field_name, value, "Debe ser una cadena de texto")

    if len(value) < min_length:
        logger.warning(
            f"Cadena muy corta: {len(value)} < {min_length}",
            extra={"field": field_name, "value": value, "min_length": min_length},
        )
        raise TrackHSValidationError(
            field_name, value, f"Debe tener al menos {min_length} caracteres"
        )

    if len(value) > max_length:
        logger.warning(
            f"Cadena muy larga: {len(value)} > {max_length}",
            extra={"field": field_name, "value": value, "max_length": max_length},
        )
        raise TrackHSValidationError(
            field_name, value, f"No puede exceder {max_length} caracteres"
        )

    return value
