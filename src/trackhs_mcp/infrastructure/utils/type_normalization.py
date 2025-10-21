"""
Utilidades de normalización de tipos para herramientas MCP.

Este módulo proporciona funciones para normalizar parámetros que llegan vía JSON-RPC
a tipos específicos de Python, resolviendo incompatibilidades entre tipos genéricos
de JSON (number, boolean) y tipos específicos de Python (int, float, bool).

Problema resuelto:
- JSON-RPC envía tipos genéricos: "number", "boolean"
- Python espera tipos específicos: int, float, bool
- FastMCP valida estrictamente antes de ejecutar la función
- La normalización debe ocurrir en type hints o decoradores

Autor: Equipo de Desarrollo
Fecha: 14 de Octubre, 2025
"""

from typing import Optional, Union

from ...domain.exceptions.api_exceptions import ValidationError


def normalize_int(value: Union[int, float, str], param_name: str) -> int:
    """
    Normaliza un valor a int desde múltiples representaciones.

    Soporta:
    - int → int (directo)
    - float → int (conversión si no tiene decimales)
    - str → int (parsing)
    - JSON number → int (desde FastMCP)

    Args:
        value: Valor a normalizar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        int: Valor normalizado como entero

    Raises:
        ValidationError: Si el valor no puede convertirse a int
    """
    if isinstance(value, int):
        return value

    if isinstance(value, float):
        # Validar que no tiene decimales significativos
        if value.is_integer():
            return int(value)
        raise ValidationError(
            f"El parámetro '{param_name}' debe ser un número entero (sin decimales). Recibido: {value}. Ejemplo válido: 123",
            param_name,
        )

    if isinstance(value, str):
        try:
            # Intentar parsear como int
            return int(value)
        except ValueError:
            raise ValidationError(
                f"El parámetro '{param_name}' debe ser un número entero válido. Recibido: '{value}'. Ejemplo válido: '123'",
                param_name,
            )

    # Tipo no soportado
    raise ValidationError(
        f"El parámetro '{param_name}' debe ser un número entero, decimal o texto. Tipo recibido: {type(value).__name__}. Ejemplo válido: 123, 123.0, o '123'",
        param_name,
    )


def normalize_optional_int(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[int]:
    """
    Normaliza un valor opcional a int.

    Args:
        value: Valor a normalizar (puede ser None)
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        Optional[int]: Valor normalizado o None
    """
    if value is None:
        return None
    return normalize_int(value, param_name)


def normalize_float(value: Union[int, float, str], param_name: str) -> float:
    """
    Normaliza un valor a float desde múltiples representaciones.

    Args:
        value: Valor a normalizar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        float: Valor normalizado como flotante
    """
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValidationError(
                f"{param_name} must be a valid float string, got: {value}", param_name
            )

    raise ValidationError(
        f"{param_name} must be int, float, or str, got: {type(value).__name__}",
        param_name,
    )


def normalize_optional_float(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[float]:
    """
    Normaliza un valor opcional a float.
    """
    if value is None:
        return None
    return normalize_float(value, param_name)


def normalize_bool(value: Union[bool, int, str], param_name: str) -> bool:
    """
    Normaliza un valor a bool desde múltiples representaciones.

    Soporta:
    - bool → bool (directo)
    - int → bool (0=False, otros=True)
    - str → bool (parsing de strings booleanos)

    Args:
        value: Valor a normalizar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        bool: Valor normalizado como booleano
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value != 0

    if isinstance(value, str):
        lower = value.lower()
        if lower in ("true", "1", "yes", "on"):
            return True
        if lower in ("false", "0", "no", "off"):
            return False
        raise ValidationError(
            f"{param_name} must be a valid boolean string, got: {value}", param_name
        )

    raise ValidationError(
        f"{param_name} must be bool, int, or str, got: {type(value).__name__}",
        param_name,
    )


def normalize_optional_bool(
    value: Optional[Union[bool, int, str]], param_name: str
) -> Optional[bool]:
    """
    Normaliza un valor opcional a bool.
    """
    if value is None:
        return None
    return normalize_bool(value, param_name)


def normalize_binary_int(value: Union[int, float, str], param_name: str) -> int:
    """
    Normaliza valor a 0 o 1 (para flags booleanos representados como int).

    Común en APIs que usan 0/1 en lugar de true/false.

    Args:
        value: Valor a normalizar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        int: 0 o 1

    Raises:
        ValidationError: Si el valor no puede convertirse a 0 o 1
    """
    # Normalizar a int primero
    int_value = normalize_int(value, param_name)

    # Validar que sea 0 o 1
    if int_value not in [0, 1]:
        raise ValidationError(
            f"El parámetro '{param_name}' debe ser 0 (No) o 1 (Sí). Recibido: {int_value}. Ejemplo válido: 0 o 1",
            param_name,
        )

    return int_value


def normalize_optional_binary_int(
    value: Optional[Union[int, float, str]], param_name: str
) -> Optional[int]:
    """
    Normaliza un valor opcional a 0 o 1.
    """
    if value is None:
        return None
    return normalize_binary_int(value, param_name)


def normalize_string(value: Union[str, int, float], param_name: str) -> str:
    """
    Normaliza un valor a string.

    Args:
        value: Valor a normalizar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        str: Valor normalizado como string
    """
    if isinstance(value, str):
        return value

    if isinstance(value, (int, float)):
        return str(value)

    raise ValidationError(
        f"{param_name} must be str, int, or float, got: {type(value).__name__}",
        param_name,
    )


def normalize_optional_string(
    value: Optional[Union[str, int, float]], param_name: str
) -> Optional[str]:
    """
    Normaliza un valor opcional a string.
    """
    if value is None:
        return None
    return normalize_string(value, param_name)
