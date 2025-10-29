"""
Middleware personalizado para coerción de tipos de parámetros
Garantiza que los parámetros numéricos se conviertan correctamente
"""

import logging
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)


def coerce_numeric_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte parámetros numéricos de string a int/float cuando sea posible.

    Args:
        params: Diccionario de parámetros de entrada

    Returns:
        Diccionario con parámetros convertidos
    """
    if not isinstance(params, dict):
        return params

    # Parámetros que deben ser enteros
    integer_params = {
        "page",
        "size",
        "bedrooms",
        "bathrooms",
        "min_bedrooms",
        "max_bedrooms",
        "min_bathrooms",
        "max_bathrooms",
        "occupancy",
        "min_occupancy",
        "max_occupancy",
        "is_active",
        "is_bookable",
        "pets_friendly",
        "computed",
        "inherited",
        "limited",
        "include_descriptions",
        "calendar_id",
        "role_id",
        "promo_code_id",
        "owner_id",
        "company_id",
        "channel_id",
        "lodging_type_id",
        "bed_type_id",
        "unit_ids",
        "amenity_id",
        "unit_type_id",
        "node_id",
        "amenity_all",
    }

    # Parámetros que pueden ser enteros o listas de enteros
    integer_list_params = {
        "unit_ids",
        "amenity_id",
        "unit_type_id",
        "node_id",
        "amenity_all",
        "owner_id",
        "company_id",
        "channel_id",
        "lodging_type_id",
        "bed_type_id",
    }

    converted_params = {}

    for key, value in params.items():
        if value is None:
            converted_params[key] = None
            continue

        # Parámetros de enteros simples
        if key in integer_params and key not in integer_list_params:
            try:
                if isinstance(value, str) and value.strip():
                    converted_params[key] = int(value)
                    logger.debug(f"🔄 Convertido {key}: '{value}' → {int(value)}")
                else:
                    converted_params[key] = value
            except (ValueError, TypeError):
                logger.warning(f"⚠️ No se pudo convertir {key}='{value}' a entero")
                converted_params[key] = value

        # Parámetros que pueden ser listas de enteros
        elif key in integer_list_params:
            if isinstance(value, list):
                try:
                    converted_list = []
                    for item in value:
                        if isinstance(item, str) and item.strip():
                            converted_list.append(int(item))
                        else:
                            converted_list.append(item)
                    converted_params[key] = converted_list
                    logger.debug(
                        f"🔄 Convertida lista {key}: {value} → {converted_list}"
                    )
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ No se pudo convertir lista {key}={value}")
                    converted_params[key] = value
            else:
                # Si no es lista, tratar como entero simple
                try:
                    if isinstance(value, str) and value.strip():
                        converted_params[key] = int(value)
                        logger.debug(f"🔄 Convertido {key}: '{value}' → {int(value)}")
                    else:
                        converted_params[key] = value
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ No se pudo convertir {key}='{value}' a entero")
                    converted_params[key] = value
        else:
            converted_params[key] = value

    return converted_params


def validate_and_coerce_tool_input(
    tool_name: str, params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Valida y convierte parámetros de entrada para herramientas específicas.

    Args:
        tool_name: Nombre de la herramienta
        params: Parámetros de entrada

    Returns:
        Parámetros convertidos y validados
    """
    logger.info(f"🔧 Aplicando middleware de coerción para {tool_name}")

    # Aplicar coerción de tipos
    converted_params = coerce_numeric_parameters(params)

    # Log de cambios
    changes = []
    for key in converted_params:
        if key in params and params[key] != converted_params[key]:
            changes.append(f"{key}: '{params[key]}' → {converted_params[key]}")

    if changes:
        logger.info(f"✅ Parámetros convertidos: {', '.join(changes)}")
    else:
        logger.info("✅ No se requirieron conversiones de tipos")

    return converted_params
