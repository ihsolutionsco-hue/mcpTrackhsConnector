"""
Mensajes de error amigables para usuarios no técnicos
"""


def format_date_error(param_name: str) -> str:
    """Genera mensaje de error de fecha con ejemplos"""
    return (
        f"Formato de fecha inválido en '{param_name}'. "
        f"Usa formato ISO 8601:\n"
        f"  - Solo fecha: '2025-01-01'\n"
        f"  - Fecha y hora: '2025-01-01T00:00:00Z'\n"
        f"Ejemplo: {param_name}='2025-01-15'"
    )


def format_type_error(param_name: str, expected_type: str, received_value: any) -> str:
    """Genera mensaje de error de tipo con sugerencia"""
    return (
        f"Valor inválido para '{param_name}': {received_value}\n"
        f"Se esperaba: {expected_type}\n"
        f"Ejemplo: {param_name}=1"
    )


def format_range_error(param_name: str, min_val: int, max_val: int) -> str:
    """Genera mensaje de error de rango"""
    return (
        f"Valor fuera de rango en '{param_name}'. "
        f"Debe estar entre {min_val} y {max_val}.\n"
        f"Ejemplo: {param_name}={min_val}"
    )


def format_required_error(param_name: str) -> str:
    """Genera mensaje de error para parámetros requeridos"""
    return f"Parámetro '{param_name}' es requerido.\n" f"Ejemplo: {param_name}=1"


def format_boolean_error(param_name: str, received_value: any) -> str:
    """Genera mensaje de error para parámetros booleanos (0/1)"""
    return (
        f"Valor inválido para '{param_name}': {received_value}\n"
        f"Usa 0 (No) o 1 (Sí)\n"
        f"Ejemplo: {param_name}=1"
    )


def format_id_list_error(param_name: str, received_value: any) -> str:
    """Genera mensaje de error para listas de IDs"""
    return (
        f"Formato inválido para '{param_name}': {received_value}\n"
        f"Usa: '1,2,3' o '[1,2,3]'\n"
        f"Ejemplo: {param_name}='1,2,3'"
    )
