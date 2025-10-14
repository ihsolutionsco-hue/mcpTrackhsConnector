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

    return False
