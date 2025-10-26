"""
Validadores de reglas de negocio para TrackHS MCP Server.
Fase 3 - Validación: Reglas de negocio.
"""

from datetime import datetime
from typing import Optional


class BusinessValidationError(Exception):
    """Excepción para errores de validación de reglas de negocio"""

    pass


def validate_date_format(date_str: str, field_name: str = "fecha") -> bool:
    """
    Valida que una fecha tenga formato YYYY-MM-DD y sea válida.

    Args:
        date_str: String de fecha a validar
        field_name: Nombre del campo para mensajes de error

    Returns:
        True si es válida

    Raises:
        BusinessValidationError: Si el formato o fecha no son válidos
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError as e:
        raise BusinessValidationError(
            f"{field_name} debe tener formato YYYY-MM-DD y ser válida: {str(e)}"
        )


def validate_date_range(
    start_date: str,
    end_date: str,
    start_field: str = "fecha_inicio",
    end_field: str = "fecha_fin",
) -> bool:
    """
    Valida que end_date sea posterior a start_date.

    Args:
        start_date: Fecha de inicio (YYYY-MM-DD)
        end_date: Fecha de fin (YYYY-MM-DD)
        start_field: Nombre del campo de inicio
        end_field: Nombre del campo de fin

    Returns:
        True si el rango es válido

    Raises:
        BusinessValidationError: Si el rango no es válido
    """
    # Primero validar formatos
    validate_date_format(start_date, start_field)
    validate_date_format(end_date, end_field)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if end <= start:
        raise BusinessValidationError(
            f"{end_field} ({end_date}) debe ser posterior a {start_field} ({start_date})"
        )

    return True


def validate_positive_number(
    value: float,
    field_name: str = "valor",
    allow_zero: bool = False,
) -> bool:
    """
    Valida que un número sea positivo.

    Args:
        value: Valor a validar
        field_name: Nombre del campo
        allow_zero: Si se permite cero

    Returns:
        True si es válido

    Raises:
        BusinessValidationError: Si no es positivo
    """
    if allow_zero:
        if value < 0:
            raise BusinessValidationError(
                f"{field_name} debe ser mayor o igual a cero, recibido: {value}"
            )
    else:
        if value <= 0:
            raise BusinessValidationError(
                f"{field_name} debe ser mayor que cero, recibido: {value}"
            )

    return True


def validate_integer_range(
    value: int,
    min_value: int,
    max_value: int,
    field_name: str = "valor",
) -> bool:
    """
    Valida que un entero esté en un rango específico.

    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido (inclusive)
        max_value: Valor máximo permitido (inclusive)
        field_name: Nombre del campo

    Returns:
        True si está en el rango

    Raises:
        BusinessValidationError: Si está fuera del rango
    """
    if value < min_value or value > max_value:
        raise BusinessValidationError(
            f"{field_name} debe estar entre {min_value} y {max_value}, recibido: {value}"
        )

    return True


def validate_string_not_empty(value: str, field_name: str = "campo") -> bool:
    """
    Valida que un string no esté vacío o solo contenga espacios.

    Args:
        value: String a validar
        field_name: Nombre del campo

    Returns:
        True si no está vacío

    Raises:
        BusinessValidationError: Si está vacío
    """
    if not value or not value.strip():
        raise BusinessValidationError(f"{field_name} no puede estar vacío")

    return True


def validate_string_length(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    field_name: str = "campo",
) -> bool:
    """
    Valida que un string tenga una longitud específica.

    Args:
        value: String a validar
        min_length: Longitud mínima (opcional)
        max_length: Longitud máxima (opcional)
        field_name: Nombre del campo

    Returns:
        True si la longitud es válida

    Raises:
        BusinessValidationError: Si la longitud no es válida
    """
    length = len(value)

    if min_length is not None and length < min_length:
        raise BusinessValidationError(
            f"{field_name} debe tener al menos {min_length} caracteres, tiene: {length}"
        )

    if max_length is not None and length > max_length:
        raise BusinessValidationError(
            f"{field_name} debe tener máximo {max_length} caracteres, tiene: {length}"
        )

    return True


def validate_priority(priority: int) -> bool:
    """
    Valida que una prioridad sea 1, 3 o 5.

    Args:
        priority: Prioridad a validar

    Returns:
        True si es válida

    Raises:
        BusinessValidationError: Si no es válida
    """
    valid_priorities = {1, 3, 5}

    if priority not in valid_priorities:
        raise BusinessValidationError(
            f"Prioridad debe ser 1 (Baja), 3 (Media) o 5 (Alta), recibido: {priority}"
        )

    return True


def validate_reservation_dates(arrival: str, departure: str) -> bool:
    """
    Valida fechas de reserva (llegada y salida).

    Args:
        arrival: Fecha de llegada (YYYY-MM-DD)
        departure: Fecha de salida (YYYY-MM-DD)

    Returns:
        True si son válidas

    Raises:
        BusinessValidationError: Si no son válidas
    """
    return validate_date_range(
        arrival, departure, start_field="arrival", end_field="departure"
    )


def validate_unit_capacity(
    bedrooms: Optional[int] = None, bathrooms: Optional[int] = None
) -> bool:
    """
    Valida capacidad de una unidad (dormitorios y baños).

    Args:
        bedrooms: Número de dormitorios (opcional)
        bathrooms: Número de baños (opcional)

    Returns:
        True si son válidos

    Raises:
        BusinessValidationError: Si no son válidos
    """
    if bedrooms is not None:
        validate_integer_range(bedrooms, 0, 20, "bedrooms")

    if bathrooms is not None:
        validate_integer_range(bathrooms, 0, 20, "bathrooms")

    return True


def validate_cost(cost: float, field_name: str = "cost") -> bool:
    """
    Valida que un costo sea válido (positivo o cero).

    Args:
        cost: Costo a validar
        field_name: Nombre del campo

    Returns:
        True si es válido

    Raises:
        BusinessValidationError: Si no es válido
    """
    return validate_positive_number(cost, field_name, allow_zero=True)


def validate_work_order_summary(summary: str) -> bool:
    """
    Valida resumen de work order.

    Args:
        summary: Resumen a validar

    Returns:
        True si es válido

    Raises:
        BusinessValidationError: Si no es válido
    """
    validate_string_not_empty(summary, "summary")
    validate_string_length(summary, min_length=5, max_length=500, field_name="summary")

    return True


def validate_work_order_description(description: str) -> bool:
    """
    Valida descripción de work order.

    Args:
        description: Descripción a validar

    Returns:
        True si es válida

    Raises:
        BusinessValidationError: Si no es válida
    """
    validate_string_not_empty(description, "description")
    validate_string_length(
        description, min_length=10, max_length=5000, field_name="description"
    )

    return True
