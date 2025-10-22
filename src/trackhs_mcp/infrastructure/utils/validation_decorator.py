"""
Decorador de validación automática para herramientas MCP.

Este módulo proporciona un decorador que valida y normaliza automáticamente
los parámetros de entrada antes de ejecutar las funciones de herramientas MCP.

Autor: Track HS MCP Team
Fecha: Enero 2025
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

from ...domain.exceptions.api_exceptions import ValidationError
from .type_normalization import normalize_binary_int, normalize_int

logger = logging.getLogger(__name__)


def validate_mcp_parameters(
    binary_params: Optional[list] = None,
    int_params: Optional[list] = None,
    float_params: Optional[list] = None,
    string_params: Optional[list] = None,
) -> Callable:
    """
    Decorador para validar y normalizar automáticamente parámetros MCP.

    Args:
        binary_params: Lista de parámetros que deben ser 0 o 1
        int_params: Lista de parámetros que deben ser enteros
        float_params: Lista de parámetros que deben ser flotantes
        string_params: Lista de parámetros que deben ser strings

    Returns:
        Decorador que valida y normaliza parámetros automáticamente

    Examples:
        @validate_mcp_parameters(
            binary_params=['in_house_today', 'is_active'],
            int_params=['page', 'size', 'group_id']
        )
        async def search_reservations(page, size, in_house_today, ...):
            # Los parámetros ya están validados y normalizados
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                # Normalizar parámetros binarios
                if binary_params:
                    for param in binary_params:
                        if param in kwargs and kwargs[param] is not None:
                            try:
                                kwargs[param] = normalize_binary_int(
                                    kwargs[param], param
                                )
                            except ValidationError as e:
                                logger.warning(
                                    f"Error normalizando parámetro binario {param}: {e}"
                                )
                                raise ValidationError(
                                    f"Parámetro {param} debe ser 0, 1, '0', '1', o None. "
                                    f"Valor recibido: {kwargs[param]}",
                                    param,
                                )

                # Normalizar parámetros enteros
                if int_params:
                    for param in int_params:
                        if param in kwargs and kwargs[param] is not None:
                            try:
                                kwargs[param] = normalize_int(kwargs[param], param)
                            except ValidationError as e:
                                logger.warning(
                                    f"Error normalizando parámetro entero {param}: {e}"
                                )
                                raise ValidationError(
                                    f"Parámetro {param} debe ser un entero válido. "
                                    f"Valor recibido: {kwargs[param]}",
                                    param,
                                )

                # Normalizar parámetros flotantes
                if float_params:
                    for param in float_params:
                        if param in kwargs and kwargs[param] is not None:
                            try:
                                from .type_normalization import normalize_float

                                kwargs[param] = normalize_float(kwargs[param], param)
                            except ValidationError as e:
                                logger.warning(
                                    f"Error normalizando parámetro flotante {param}: {e}"
                                )
                                raise ValidationError(
                                    f"Parámetro {param} debe ser un número flotante válido. "
                                    f"Valor recibido: {kwargs[param]}",
                                    param,
                                )

                # Normalizar parámetros string
                if string_params:
                    for param in string_params:
                        if param in kwargs and kwargs[param] is not None:
                            if not isinstance(kwargs[param], str):
                                kwargs[param] = str(kwargs[param])
                            # Limpiar espacios
                            kwargs[param] = kwargs[param].strip()

                logger.debug(f"Parámetros normalizados para {func.__name__}: {kwargs}")

                # Ejecutar la función con parámetros normalizados
                return await func(*args, **kwargs)

            except Exception as e:
                logger.error(
                    f"Error en validación de parámetros para {func.__name__}: {e}"
                )
                raise

        return wrapper

    return decorator


def validate_search_reservations_params(func: Callable) -> Callable:
    """
    Decorador mejorado para validar parámetros de search_reservations.

    Aplica validación robusta con mensajes de error descriptivos
    y validación de tipos estricta.
    """
    from ..validation.enhanced_validation import (
        ValidationError,
        validate_search_reservations_parameters,
    )

    async def wrapper(*args, **kwargs):
        try:
            # Extraer parámetros de kwargs
            params = {k: v for k, v in kwargs.items() if k != 'api_client'}

            # Aplicar validación mejorada
            validated_params = validate_search_reservations_parameters(params)

            # Actualizar kwargs con parámetros validados
            for key, value in validated_params.items():
                if key in kwargs:
                    kwargs[key] = value

            # Ejecutar función original
            return await func(*args, **kwargs)

        except ValidationError as e:
            # Re-lanzar ValidationError con mensaje mejorado
            raise ValueError(str(e))
        except Exception as e:
            # Manejar otros errores
            raise ValueError(f"❌ Error validating search_reservations parameters: {str(e)}")

    return wrapper


def validate_search_units_params(func: Callable) -> Callable:
    """
    Decorador específico para validar parámetros de search_units.

    Aplica validación automática para los parámetros más comunes
    en búsquedas de unidades.
    """
    return validate_mcp_parameters(
        binary_params=["pets_friendly", "is_active", "is_bookable", "is_accessible"],
        int_params=[
            "page",
            "size",
            "bedrooms",
            "bathrooms",
            "min_bedrooms",
            "max_bedrooms",
        ],
        string_params=["search", "term", "unit_code", "short_name", "node_id"],
    )(func)


def validate_work_order_params(func: Callable) -> Callable:
    """
    Decorador específico para validar parámetros de órdenes de trabajo.

    Aplica validación automática para los parámetros más comunes
    en creación de órdenes de trabajo.
    """
    return validate_mcp_parameters(
        int_params=[
            "priority",
            "estimated_time",
            "actual_time",
            "user_id",
            "vendor_id",
            "unit_id",
        ],
        float_params=["estimated_cost", "cost"],
        string_params=["summary", "description", "status", "source"],
    )(func)
