"""
Utilidades para normalización de tipos en herramientas MCP.

Este módulo proporciona funciones helper para convertir tipos JSON-RPC
(number, boolean, string) a tipos Python específicos (int, float, bool).

Problema que resuelve:
- Los clientes MCP envían datos en formato JSON con tipos genéricos (number)
- FastMCP valida contra type hints Python específicos (int, float)
- La conversión no es automática, causando errores de validación

Solución:
- Aceptar múltiples tipos en la signature (Union[int, float, str])
- Normalizar explícitamente al inicio de cada función
- Validar después de normalizar

Autor: Track HS MCP Team
Fecha: Octubre 2025
"""

from typing import Optional, Union

from ...domain.exceptions.api_exceptions import ValidationError


def normalize_int(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[int]:
    """
    Normaliza un valor a int desde múltiples representaciones.

    Soporta:
    - None → None (para parámetros opcionales)
    - int → int (directo)
    - float → int (si no tiene decimales)
    - str → int (parsing)
    - JSON number → int (desde FastMCP)

    Args:
        value: Valor a normalizar (puede ser None, int, float o str)
        param_name: Nombre del parámetro (para mensajes de error)

    Returns:
        int normalizado, o None si value es None

    Raises:
        ValidationError: Si el valor no puede convertirse a int

    Examples:
        >>> normalize_int(42, "page")
        42
        >>> normalize_int(42.0, "page")
        42
        >>> normalize_int("42", "page")
        42
        >>> normalize_int(None, "page")
        None
        >>> normalize_int(42.5, "page")
        ValidationError: page must be an integer, got float with decimals: 42.5
    """
    if value is None:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        # Validar que no tiene decimales significativos
        if value.is_integer():
            return int(value)
        raise ValidationError(
            f"{param_name} must be an integer, got float with decimals: {value}",
            param_name,
        )

    if isinstance(value, str):
        # Limpiar espacios
        value = value.strip()
        if not value:
            raise ValidationError(f"{param_name} cannot be empty string", param_name)

        try:
            # Intentar parsear como int
            return int(value)
        except ValueError:
            raise ValidationError(
                f"{param_name} must be a valid integer string, got: {value}",
                param_name,
            )

    # Tipo no soportado
    raise ValidationError(
        f"{param_name} must be int, float, or str, got: {type(value).__name__}",
        param_name,
    )


def normalize_binary_int(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[int]:
    """
    Normaliza un valor a 0 o 1 (para flags booleanos representados como int).

    Común en APIs que usan 0/1 en lugar de true/false para flags booleanos.
    Ejemplos: is_active, pets_friendly, in_house_today

    Args:
        value: Valor a normalizar (puede ser None, int, float o str)
        param_name: Nombre del parámetro (para mensajes de error)

    Returns:
        0 o 1, o None si value es None

    Raises:
        ValidationError: Si el valor no puede convertirse a 0 o 1

    Examples:
        >>> normalize_binary_int(0, "is_active")
        0
        >>> normalize_binary_int(1, "is_active")
        1
        >>> normalize_binary_int("1", "is_active")
        1
        >>> normalize_binary_int(None, "is_active")
        None
        >>> normalize_binary_int(2, "is_active")
        ValidationError: is_active must be 0 or 1, got: 2
    """
    if value is None:
        return None

    # Normalizar a int primero usando normalize_int
    int_value = normalize_int(value, param_name)

    # Si normalize_int devolvió None (caso edge), retornar None
    if int_value is None:
        return None

    # Validar que sea 0 o 1
    if int_value not in [0, 1]:
        raise ValidationError(
            f"{param_name} must be 0 or 1, got: {int_value}", param_name
        )

    return int_value


def normalize_bool(
    value: Optional[Union[bool, int, float, str]], param_name: str
) -> Optional[bool]:
    """
    Normaliza un valor a bool desde múltiples representaciones.

    Soporta:
    - None → None (para parámetros opcionales)
    - bool → bool (directo)
    - int → bool (0=False, cualquier otro=True)
    - float → bool (0.0=False, cualquier otro=True)
    - str → bool ("true", "1", "yes" = True; "false", "0", "no" = False)

    Args:
        value: Valor a normalizar (puede ser None, bool, int, float o str)
        param_name: Nombre del parámetro (para mensajes de error)

    Returns:
        bool normalizado, o None si value es None

    Raises:
        ValidationError: Si el valor no puede convertirse a bool

    Examples:
        >>> normalize_bool(True, "flag")
        True
        >>> normalize_bool(1, "flag")
        True
        >>> normalize_bool(0, "flag")
        False
        >>> normalize_bool("true", "flag")
        True
        >>> normalize_bool("yes", "flag")
        True
        >>> normalize_bool(None, "flag")
        None
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        # Limpiar y convertir a minúsculas
        value_lower = value.strip().lower()

        if value_lower in ("true", "1", "yes", "y", "t"):
            return True

        if value_lower in ("false", "0", "no", "n", "f"):
            return False

        raise ValidationError(
            f"{param_name} must be a valid boolean string (true/false/yes/no/1/0), got: {value}",
            param_name,
        )

    # Tipo no soportado
    raise ValidationError(
        f"{param_name} must be bool, int, float, or str, got: {type(value).__name__}",
        param_name,
    )


def normalize_float(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[float]:
    """
    Normaliza un valor a float desde múltiples representaciones.

    Soporta:
    - None → None (para parámetros opcionales)
    - float → float (directo)
    - int → float (conversión)
    - str → float (parsing)
    - JSON number → float (desde FastMCP)

    Args:
        value: Valor a normalizar (puede ser None, int, float o str)
        param_name: Nombre del parámetro (para mensajes de error)

    Returns:
        float normalizado, o None si value es None

    Raises:
        ValidationError: Si el valor no puede convertirse a float

    Examples:
        >>> normalize_float(42.5, "rate")
        42.5
        >>> normalize_float(42, "rate")
        42.0
        >>> normalize_float("42.5", "rate")
        42.5
        >>> normalize_float(None, "rate")
        None
    """
    if value is None:
        return None

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    if isinstance(value, str):
        # Limpiar espacios
        value = value.strip()
        if not value:
            raise ValidationError(f"{param_name} cannot be empty string", param_name)

        try:
            # Intentar parsear como float
            return float(value)
        except ValueError:
            raise ValidationError(
                f"{param_name} must be a valid float string, got: {value}",
                param_name,
            )

    # Tipo no soportado
    raise ValidationError(
        f"{param_name} must be int, float, or str, got: {type(value).__name__}",
        param_name,
    )


def normalize_positive_int(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[int]:
    """
    Normaliza un valor a int positivo (>= 0).

    Útil para parámetros que deben ser no negativos como:
    - page (número de página)
    - size (tamaño de página)
    - count (contadores)

    Args:
        value: Valor a normalizar (puede ser None, int, float o str)
        param_name: Nombre del parámetro (para mensajes de error)

    Returns:
        int positivo normalizado, o None si value es None

    Raises:
        ValidationError: Si el valor es negativo o no puede convertirse a int

    Examples:
        >>> normalize_positive_int(42, "page")
        42
        >>> normalize_positive_int(0, "page")
        0
        >>> normalize_positive_int(-1, "page")
        ValidationError: page must be >= 0, got: -1
    """
    if value is None:
        return None

    # Normalizar a int primero
    int_value = normalize_int(value, param_name)

    # Si normalize_int devolvió None (caso edge), retornar None
    if int_value is None:
        return None

    # Validar que sea positivo (>= 0)
    if int_value < 0:
        raise ValidationError(
            f"{param_name} must be >= 0, got: {int_value}", param_name
        )

    return int_value


def normalize_string_to_int(value: Union[int, str]) -> int:
    """
    Normaliza un valor string a int.

    Args:
        value: Valor a normalizar (int o str)

    Returns:
        int normalizado

    Raises:
        ValidationError: Si el valor no puede convertirse a int
    """
    if isinstance(value, int):
        return value

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise ValidationError(f"Invalid integer value: {value}")

    raise ValidationError(f"Expected int or str, got: {type(value).__name__}")


def normalize_string_to_float(value: Union[float, str]) -> float:
    """
    Normaliza un valor string a float.

    Args:
        value: Valor a normalizar (float o str)

    Returns:
        float normalizado

    Raises:
        ValidationError: Si el valor no puede convertirse a float
    """
    if isinstance(value, float):
        return value

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValidationError(f"Invalid float value: {value}")

    raise ValidationError(f"Expected float or str, got: {type(value).__name__}")


def normalize_string_to_bool(value: Union[bool, str]) -> bool:
    """
    Normaliza un valor string a bool.

    Args:
        value: Valor a normalizar (bool o str)

    Returns:
        bool normalizado

    Raises:
        ValidationError: Si el valor no puede convertirse a bool
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ("true", "1", "yes", "y", "t"):
            return True
        elif value_lower in ("false", "0", "no", "n", "f"):
            return False
        else:
            raise ValidationError(f"Invalid boolean value: {value}")

    raise ValidationError(f"Expected bool or str, got: {type(value).__name__}")
