"""
Utilidades de validación de fechas (ISO 8601) usadas por herramientas MCP.

Formato permitido (documentado):
- YYYY-MM-DD
- YYYY-MM-DDTHH:MM:SSZ
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

_DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_TIME_Z_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_DATE_TIME_NO_TZ_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$")
_DATE_TIME_OFFSET_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?[+-]\d{2}:\d{2}$"
)
_DATE_TIME_SPACE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$")


def is_valid_iso8601_date(date_string: Optional[str]) -> bool:
    """Valida fechas en formatos ISO 8601 soportados por la documentación.

    Acepta únicamente:
    - YYYY-MM-DD
    - YYYY-MM-DDTHH:MM:SSZ
    """
    if not date_string or not isinstance(date_string, str):
        return False

    if _DATE_ONLY_PATTERN.match(date_string):
        try:
            datetime.fromisoformat(date_string)
            return True
        except ValueError:
            return False

    if _DATE_TIME_Z_PATTERN.match(date_string):
        try:
            # Reemplazar Z por +00:00 para fromisoformat
            datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False

    if _DATE_TIME_NO_TZ_PATTERN.match(date_string) or _DATE_TIME_OFFSET_PATTERN.match(
        date_string
    ):
        try:
            datetime.fromisoformat(date_string)
            return True
        except ValueError:
            return False

    # Compatibilidad: aceptar 'YYYY-MM-DD HH:MM:SS' (con espacio)
    if _DATE_TIME_SPACE_PATTERN.match(date_string):
        try:
            datetime.fromisoformat(date_string)
            return True
        except ValueError:
            return False

    return False


def normalize_date_to_iso8601(date_string: str) -> str:
    """Normaliza una fecha a formato ISO 8601 estándar.

    Convierte formatos como 'YYYY-MM-DD HH:MM:SS' a 'YYYY-MM-DDTHH:MM:SSZ'

    Args:
        date_string: String de fecha en cualquier formato soportado

    Returns:
        String de fecha en formato ISO 8601 estándar

    Raises:
        ValueError: Si la fecha no es válida
    """
    if not date_string or not isinstance(date_string, str):
        raise ValueError("Date string cannot be empty or None")

    # Si ya está en formato ISO 8601 con T y Z, devolverlo tal como está
    if _DATE_TIME_Z_PATTERN.match(date_string):
        return date_string

    # Si es solo fecha, devolverla tal como está
    if _DATE_ONLY_PATTERN.match(date_string):
        return date_string

    # Si tiene formato con espacio, convertir a formato ISO 8601
    if _DATE_TIME_SPACE_PATTERN.match(date_string):
        # Reemplazar espacio por T y agregar Z
        iso_date = date_string.replace(" ", "T") + "Z"
        return iso_date

    # Si tiene formato ISO 8601 sin Z, agregar Z
    if _DATE_TIME_NO_TZ_PATTERN.match(date_string):
        return date_string + "Z"

    # Si tiene offset, mantenerlo
    if _DATE_TIME_OFFSET_PATTERN.match(date_string):
        return date_string

    # Si no coincide con ningún patrón, intentar parsear y convertir
    try:
        # Intentar parsear la fecha
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        # Convertir a formato ISO 8601 con Z
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}")
