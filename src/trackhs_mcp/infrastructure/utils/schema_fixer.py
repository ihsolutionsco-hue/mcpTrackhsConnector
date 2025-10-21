"""
Módulo para corregir esquemas JSON MCP que han sido serializados incorrectamente.

Este módulo resuelve el problema donde FastMCP Cloud serializa valores numéricos
como strings en los esquemas JSON, causando incompatibilidad con clientes como ElevenLabs.

Problema:
- ❌ "minimum": "0", "maximum": "1", "type": "integer"
- ✅ "minimum": 0, "maximum": 1, "type": "integer"
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def fix_json_schema_types(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Corrige tipos serializados incorrectamente en esquemas JSON.

    Convierte strings numéricos a números nativos en:
    - minimum, maximum, minLength, maxLength
    - default (cuando es numérico)
    - Cualquier valor que debería ser numérico según el contexto

    Args:
        schema: Esquema JSON a corregir

    Returns:
        Esquema corregido con tipos nativos
    """
    if not isinstance(schema, dict):
        return schema

    # Crear copia para no modificar el original
    fixed_schema = schema.copy()

    # Lista de campos que deben ser numéricos
    numeric_fields = {
        "minimum",
        "maximum",
        "minLength",
        "maxLength",
        "minItems",
        "maxItems",
        "minProperties",
        "maxProperties",
    }

    # Lista de campos que pueden ser numéricos o strings
    flexible_fields = {"default"}

    # Procesar campos numéricos obligatorios
    for field in numeric_fields:
        if field in fixed_schema and isinstance(fixed_schema[field], str):
            try:
                # Intentar convertir a int primero
                if "." not in fixed_schema[field]:
                    fixed_schema[field] = int(fixed_schema[field])
                else:
                    fixed_schema[field] = float(fixed_schema[field])
                logger.debug(
                    f"Converted {field}: '{schema[field]}' -> {fixed_schema[field]}"
                )
            except (ValueError, TypeError):
                logger.warning(
                    f"Could not convert {field} '{fixed_schema[field]}' to number, keeping as string"
                )

    # Procesar campos flexibles (como default)
    for field in flexible_fields:
        if field in fixed_schema and isinstance(fixed_schema[field], str):
            # Solo convertir si parece ser un número
            if _is_numeric_string(fixed_schema[field]):
                try:
                    if "." not in fixed_schema[field]:
                        fixed_schema[field] = int(fixed_schema[field])
                    else:
                        fixed_schema[field] = float(fixed_schema[field])
                    logger.debug(
                        f"Converted {field}: '{schema[field]}' -> {fixed_schema[field]}"
                    )
                except (ValueError, TypeError):
                    logger.debug(f"Keeping {field} as string: '{fixed_schema[field]}'")

    # Procesar recursivamente objetos anidados
    for key, value in fixed_schema.items():
        if isinstance(value, dict):
            fixed_schema[key] = fix_json_schema_types(value)
        elif isinstance(value, list):
            fixed_schema[key] = _fix_list_schemas(value)

    return fixed_schema


def _is_numeric_string(s: str) -> bool:
    """
    Verifica si un string representa un número válido.

    Args:
        s: String a verificar

    Returns:
        True si el string es numérico, False en caso contrario
    """
    if not isinstance(s, str):
        return False

    # Permitir números enteros y decimales
    try:
        float(s)
        return True
    except ValueError:
        return False


def _fix_list_schemas(schema_list: List[Any]) -> List[Any]:
    """
    Corrige esquemas dentro de listas (como anyOf, oneOf, etc.).

    Args:
        schema_list: Lista de esquemas a corregir

    Returns:
        Lista con esquemas corregidos
    """
    if not isinstance(schema_list, list):
        return schema_list

    fixed_list = []
    for item in schema_list:
        if isinstance(item, dict):
            fixed_list.append(fix_json_schema_types(item))
        elif isinstance(item, list):
            fixed_list.append(_fix_list_schemas(item))
        else:
            fixed_list.append(item)

    return fixed_list


def validate_json_schema(schema: Dict[str, Any]) -> bool:
    """
    Valida que un esquema JSON sea válido según JSON Schema Draft 7.

    Args:
        schema: Esquema a validar

    Returns:
        True si el esquema es válido, False en caso contrario
    """
    try:
        # Verificar estructura básica
        if not isinstance(schema, dict):
            logger.error("Schema must be a dictionary")
            return False

        # Verificar que los tipos sean correctos
        if "type" in schema:
            valid_types = {
                "string",
                "number",
                "integer",
                "boolean",
                "array",
                "object",
                "null",
            }
            if schema["type"] not in valid_types:
                logger.error(f"Invalid type: {schema['type']}")
                return False

        # Verificar constraints numéricos
        numeric_constraints = ["minimum", "maximum", "minLength", "maxLength"]
        for constraint in numeric_constraints:
            if constraint in schema:
                value = schema[constraint]
                if not isinstance(value, (int, float)):
                    logger.error(
                        f"{constraint} must be numeric, got {type(value)}: {value}"
                    )
                    return False

        # Validar recursivamente
        for key, value in schema.items():
            if isinstance(value, dict):
                if not validate_json_schema(value):
                    return False
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        if not validate_json_schema(item):
                            return False

        return True

    except Exception as e:
        logger.error(f"Schema validation error: {e}")
        return False


def fix_and_validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Corrige y valida un esquema JSON.

    Args:
        schema: Esquema a corregir y validar

    Returns:
        Esquema corregido y validado

    Raises:
        ValueError: Si el esquema no puede ser corregido o es inválido
    """
    logger.info("Starting schema fix and validation")

    # Corregir tipos
    fixed_schema = fix_json_schema_types(schema)

    # Validar esquema corregido
    if not validate_json_schema(fixed_schema):
        logger.error("Schema validation failed after fixing")
        raise ValueError("Invalid JSON schema after correction")

    logger.info("Schema successfully fixed and validated")
    return fixed_schema


def compare_schemas(original: Dict[str, Any], fixed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compara esquemas original y corregido para mostrar diferencias.

    Args:
        original: Esquema original
        fixed: Esquema corregido

    Returns:
        Diccionario con las diferencias encontradas
    """
    differences = {"changes": [], "total_changes": 0}

    def _compare_recursive(orig: Any, fix: Any, path: str = ""):
        if isinstance(orig, dict) and isinstance(fix, dict):
            for key in set(orig.keys()) | set(fix.keys()):
                current_path = f"{path}.{key}" if path else key

                if key not in orig:
                    differences["changes"].append(
                        {
                            "path": current_path,
                            "action": "added",
                            "original": None,
                            "fixed": fix[key],
                        }
                    )
                elif key not in fix:
                    differences["changes"].append(
                        {
                            "path": current_path,
                            "action": "removed",
                            "original": orig[key],
                            "fixed": None,
                        }
                    )
                else:
                    _compare_recursive(orig[key], fix[key], current_path)
        elif orig != fix:
            differences["changes"].append(
                {"path": path, "action": "changed", "original": orig, "fixed": fix}
            )

    _compare_recursive(original, fixed)
    differences["total_changes"] = len(differences["changes"])

    return differences
