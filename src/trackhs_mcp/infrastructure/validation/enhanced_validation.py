"""
Validación mejorada para parámetros de MCP con mensajes de error descriptivos
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass


class ReservationStatus(Enum):
    """Estados válidos para reservas"""
    HOLD = "Hold"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"


class SortColumn(Enum):
    """Columnas válidas para ordenamiento"""
    NAME = "name"
    STATUS = "status"
    ALT_CONF = "altConf"
    AGREEMENT_STATUS = "agreementStatus"
    TYPE = "type"
    GUEST = "guest"
    GUESTS = "guests"
    UNIT = "unit"
    UNITS = "units"
    CHECKIN = "checkin"
    CHECKOUT = "checkout"
    NIGHTS = "nights"


class SortDirection(Enum):
    """Direcciones válidas para ordenamiento"""
    ASC = "asc"
    DESC = "desc"


def validate_date_parameter(value: Any, param_name: str) -> Optional[str]:
    """
    Valida parámetros de fecha con formato ISO 8601

    Args:
        value: Valor a validar
        param_name: Nombre del parámetro para mensajes de error

    Returns:
        Fecha validada o None si es None

    Raises:
        ValidationError: Si el formato es inválido
    """
    if value is None:
        return None

    if isinstance(value, str):
        # Rechazar strings que representan null
        if value.lower() in ['null', 'none', '']:
            raise ValidationError(
                f"❌ Invalid date parameter '{param_name}': '{value}' is not a valid date.\n"
                f"✅ Use ISO 8601 format like '2024-03-01' or omit the parameter entirely.\n"
                f"💡 Example: {param_name}='2024-03-01' (not 'null' or empty string)"
            )

        # Validar formato ISO 8601
        iso_pattern = r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$'
        if not re.match(iso_pattern, value):
            raise ValidationError(
                f"❌ Invalid date format for '{param_name}': '{value}'.\n"
                f"✅ Use ISO 8601 format like '2024-03-01' or '2024-03-01T10:00:00Z'\n"
                f"💡 Example: {param_name}='2024-03-01'"
            )

        # Validar que la fecha sea válida
        try:
            if 'T' in value:
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            else:
                datetime.fromisoformat(value)
        except ValueError:
            raise ValidationError(
                f"❌ Invalid date value for '{param_name}': '{value}'.\n"
                f"✅ Use valid ISO 8601 date format\n"
                f"💡 Example: {param_name}='2024-03-01'"
            )

    return str(value)


def validate_enum_parameter(value: Any, param_name: str, enum_class: Enum, allow_multiple: bool = False) -> Optional[str]:
    """
    Valida parámetros enum con valores permitidos

    Args:
        value: Valor a validar
        param_name: Nombre del parámetro
        enum_class: Clase enum con valores válidos
        allow_multiple: Si permite múltiples valores separados por coma

    Returns:
        Valor validado o None si es None

    Raises:
        ValidationError: Si el valor no es válido
    """
    if value is None:
        return None

    valid_values = [e.value for e in enum_class]

    if isinstance(value, str):
        if allow_multiple:
            # Permitir múltiples valores separados por coma
            values = [v.strip() for v in value.split(',')]
            for v in values:
                if v not in valid_values:
                    raise ValidationError(
                        f"❌ Invalid {param_name} '{v}'.\n"
                        f"✅ Valid values: {', '.join(valid_values)}\n"
                        f"💡 Example: {param_name}='{valid_values[0]}' or {param_name}='{valid_values[0]},{valid_values[1]}'"
                    )
        else:
            if value not in valid_values:
                raise ValidationError(
                    f"❌ Invalid {param_name} '{value}'.\n"
                    f"✅ Valid values: {', '.join(valid_values)}\n"
                    f"💡 Example: {param_name}='{valid_values[0]}'"
                )

    return str(value)


def validate_integer_parameter(value: Any, param_name: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Optional[int]:
    """
    Valida parámetros enteros con rangos

    Args:
        value: Valor a validar
        param_name: Nombre del parámetro
        min_val: Valor mínimo permitido
        max_val: Valor máximo permitido

    Returns:
        Entero validado o None si es None

    Raises:
        ValidationError: Si el valor no es válido
    """
    if value is None:
        return None

    # Convertir string a int si es posible
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            raise ValidationError(
                f"❌ Invalid {param_name} '{value}'.\n"
                f"✅ Use integer values only\n"
                f"💡 Example: {param_name}=1"
            )

    if not isinstance(value, int):
        raise ValidationError(
            f"❌ Invalid {param_name} '{value}'.\n"
            f"✅ Use integer values only\n"
            f"💡 Example: {param_name}=1"
        )

    if min_val is not None and value < min_val:
        raise ValidationError(
            f"❌ Invalid {param_name} '{value}'.\n"
            f"✅ Minimum value: {min_val}\n"
            f"💡 Example: {param_name}={min_val}"
        )

    if max_val is not None and value > max_val:
        raise ValidationError(
            f"❌ Invalid {param_name} '{value}'.\n"
            f"✅ Maximum value: {max_val}\n"
            f"💡 Example: {param_name}={max_val}"
        )

    return value


def validate_id_list_parameter(value: Any, param_name: str) -> Optional[str]:
    """
    Valida parámetros de lista de IDs (separados por coma)

    Args:
        value: Valor a validar
        param_name: Nombre del parámetro

    Returns:
        String validado o None si es None

    Raises:
        ValidationError: Si el formato es inválido
    """
    if value is None:
        return None

    if isinstance(value, str):
        # Dividir por comas y validar cada ID
        ids = [id_val.strip() for id_val in value.split(',')]
        for id_val in ids:
            if not re.match(r'^\d+$', id_val):
                raise ValidationError(
                    f"❌ Invalid {param_name} '{id_val}'.\n"
                    f"✅ Use numeric IDs only\n"
                    f"💡 Example: {param_name}='123' or {param_name}='123,456'"
                )

    return str(value)


def validate_search_reservations_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validación completa y mejorada para parámetros de search_reservations

    Args:
        params: Diccionario de parámetros a validar

    Returns:
        Diccionario con parámetros validados

    Raises:
        ValidationError: Si hay errores de validación
    """
    validated_params = {}
    errors = []

    try:
        # Validar parámetros de paginación
        if 'page' in params:
            validated_params['page'] = validate_integer_parameter(
                params['page'], 'page', min_val=0, max_val=10000
            )

        if 'size' in params:
            validated_params['size'] = validate_integer_parameter(
                params['size'], 'size', min_val=1, max_val=100
            )

        # Validar parámetros de ordenamiento
        if 'sort_column' in params:
            validated_params['sort_column'] = validate_enum_parameter(
                params['sort_column'], 'sort_column', SortColumn
            )

        if 'sort_direction' in params:
            validated_params['sort_direction'] = validate_enum_parameter(
                params['sort_direction'], 'sort_direction', SortDirection
            )

        # Validar parámetros de búsqueda
        if 'search' in params and params['search'] is not None:
            search = params['search']
            if isinstance(search, str) and len(search) > 200:
                raise ValidationError(
                    f"❌ Invalid search parameter: too long ({len(search)} characters).\n"
                    f"✅ Maximum length: 200 characters\n"
                    f"💡 Example: search='John Smith'"
                )
            validated_params['search'] = search

        # Validar parámetros de fecha
        date_params = [
            'booked_start', 'booked_end', 'arrival_start', 'arrival_end',
            'departure_start', 'departure_end', 'updated_since'
        ]
        for param in date_params:
            if param in params:
                validated_params[param] = validate_date_parameter(params[param], param)

        # Validar parámetros de ID
        id_params = [
            'tags', 'node_id', 'unit_id', 'contact_id', 'travel_agent_id',
            'campaign_id', 'user_id', 'unit_type_id', 'rate_type_id', 'reservation_type_id'
        ]
        for param in id_params:
            if param in params:
                validated_params[param] = validate_id_list_parameter(params[param], param)

        # Validar status
        if 'status' in params:
            validated_params['status'] = validate_enum_parameter(
                params['status'], 'status', ReservationStatus, allow_multiple=True
            )

        # Validar in_house_today
        if 'in_house_today' in params:
            value = params['in_house_today']
            if value is not None:
                # Convertir string a int si es necesario
                if isinstance(value, str):
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValidationError(
                            f"❌ Invalid in_house_today '{params['in_house_today']}'.\n"
                            f"✅ Use integer values: 0 (not in house) or 1 (in house)\n"
                            f"💡 Example: in_house_today=1"
                        )

                if value not in [0, 1]:
                    raise ValidationError(
                        f"❌ Invalid in_house_today '{value}'.\n"
                        f"✅ Use integer values: 0 (not in house) or 1 (in house)\n"
                        f"💡 Example: in_house_today=1"
                    )

                validated_params['in_house_today'] = value

        # Validar otros parámetros enteros
        if 'group_id' in params:
            validated_params['group_id'] = validate_integer_parameter(params['group_id'], 'group_id')

        if 'checkin_office_id' in params:
            validated_params['checkin_office_id'] = validate_integer_parameter(params['checkin_office_id'], 'checkin_office_id')

        # Parámetros que no requieren validación especial
        simple_params = ['scroll']
        for param in simple_params:
            if param in params:
                validated_params[param] = params[param]

    except ValidationError as e:
        raise e
    except Exception as e:
        raise ValidationError(f"❌ Unexpected validation error: {str(e)}")

    return validated_params


def get_usage_examples() -> Dict[str, Dict[str, Any]]:
    """
    Retorna ejemplos de uso para la documentación

    Returns:
        Diccionario con ejemplos de uso
    """
    return {
        "basic_search": {
            "description": "Basic reservation search",
            "example": {
                "size": 10,
                "page": 0
            }
        },
        "search_by_guest": {
            "description": "Search by guest name",
            "example": {
                "search": "John Smith",
                "size": 5
            }
        },
        "filter_by_status": {
            "description": "Filter by reservation status",
            "example": {
                "status": "Confirmed",
                "size": 10
            }
        },
        "filter_by_dates": {
            "description": "Filter by arrival date range",
            "example": {
                "arrival_start": "2024-01-01",
                "arrival_end": "2024-12-31",
                "size": 10
            }
        },
        "filter_in_house": {
            "description": "Find guests currently checked in",
            "example": {
                "in_house_today": 1,
                "size": 5
            }
        },
        "complex_filter": {
            "description": "Complex filtering with multiple parameters",
            "example": {
                "status": "Confirmed",
                "arrival_start": "2024-03-01",
                "arrival_end": "2024-03-31",
                "unit_id": "58",
                "size": 5
            }
        }
    }
