# Mejores Prácticas MCP para TrackHS Connector

## Fecha
2025-10-20

## Resumen

Este documento establece las mejores prácticas para definir herramientas MCP compatibles con todos los clientes (Claude Desktop, MCP Inspector, ElevenLabs, etc.).

## 1. Type Annotations en Python

### ❌ Evitar: Union Types con Múltiples Tipos

```python
# MAL - Genera anyOf con múltiples tipos
def my_tool(
    page: Union[int, float, str] = 1,
    search: Union[str, None] = None,
):
```

### ✅ Usar: Tipos Específicos

```python
# BIEN - Genera schemas limpios
def my_tool(
    page: int = 1,
    search: Optional[str] = None,  # o str | None en Python 3.10+
):
```

### Tipos Recomendados por Caso

| Caso de Uso | Tipo Recomendado | Ejemplo |
|-------------|------------------|---------|
| Números enteros | `int` | `page: int = 1` |
| Números decimales | `float` | `price: float` |
| Texto | `str` | `name: str` |
| Booleanos | `bool` | `is_active: bool = False` |
| Fechas ISO | `str` con descripción | `date: str = Field(description="ISO 8601 date")` |
| Opcionales | `Optional[T]` o default | `search: Optional[str] = None` |
| Listas | `list[T]` | `tags: list[str]` |
| Enums | `Literal[...]` | `status: Literal["active", "inactive"]` |

## 2. Uso de Pydantic Field

### Agregar Descripciones

```python
from pydantic import Field

@mcp.tool()
def search_items(
    query: str = Field(description="Text to search for in items"),
    page: int = Field(default=1, description="Page number (1-indexed)", ge=1),
    size: int = Field(default=10, description="Items per page (max 100)", ge=1, le=100),
):
    """Search for items with pagination"""
    ...
```

### Validaciones Comunes

```python
# Rango de valores
age: int = Field(ge=0, le=150, description="Age in years")

# Longitud de string
name: str = Field(min_length=1, max_length=100)

# Patrón regex
email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')

# Lista con límites
tags: list[str] = Field(max_length=10, description="Up to 10 tags")
```

## 3. Parámetros Opcionales

### ✅ Opción 1: Usar Optional con None

```python
def search(
    search: Optional[str] = None,  # No requerido
    page: int = 1,                  # No requerido, tiene default
):
```

Genera:
```json
{
  "properties": {
    "search": {"type": "string"},
    "page": {"type": "integer", "default": 1}
  },
  "required": []
}
```

### ✅ Opción 2: Parámetros sin Default (Requeridos)

```python
def get_user(
    user_id: str,  # Requerido
):
```

Genera:
```json
{
  "properties": {
    "user_id": {"type": "string"}
  },
  "required": ["user_id"]
}
```

## 4. Fechas en ISO 8601

### ✅ Tipo Recomendado

```python
def search_by_date(
    start_date: str = Field(
        description="Start date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
        pattern=r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$',
        examples=["2024-01-01", "2024-01-01T00:00:00Z"]
    ),
):
```

### Validación en Runtime

```python
from datetime import datetime

def validate_iso_date(date_str: str) -> datetime:
    """Validate and parse ISO 8601 date"""
    try:
        # Try with time
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        try:
            # Try date only
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 date: {date_str}")
```

## 5. Enums y Literales

### ✅ Usar Literal para Opciones Fijas

```python
from typing import Literal

def sort_items(
    sort_by: Literal["name", "date", "price"] = "name",
    direction: Literal["asc", "desc"] = "asc",
):
```

Genera:
```json
{
  "sort_by": {
    "type": "string",
    "enum": ["name", "date", "price"],
    "default": "name"
  }
}
```

### Para Enums Largos

Si tienes más de 10 valores, considera:
1. Usar `str` sin enum
2. Documentar valores válidos en la descripción
3. Validar en runtime

```python
def filter_status(
    status: str = Field(
        default="all",
        description="Status filter. Valid values: all, active, inactive, pending, confirmed, cancelled, completed"
    ),
):
```

## 6. Listas y Arrays

### ✅ Listas Tipadas

```python
def filter_by_tags(
    tags: list[str] = Field(
        default=[],
        description="List of tag names to filter by",
        max_length=10
    ),
):
```

### ❌ Evitar: Strings con Delimitadores

```python
# MAL - Ambiguo para el AI
tags: str  # "tag1,tag2,tag3"

# BIEN - Explícito
tags: list[str]  # ["tag1", "tag2", "tag3"]
```

## 7. IDs y Referencias

### ✅ Tipos Consistentes

```python
# Si los IDs son numéricos en la API
user_id: int = Field(description="Unique user identifier")

# Si los IDs son strings/UUIDs
user_id: str = Field(
    description="User UUID",
    pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
)
```

### Normalización Interna

Si necesitas aceptar múltiples formatos internamente, normaliza DESPUÉS de recibir:

```python
def get_user(user_id: int):
    """Get user by ID"""
    # Normalizar internamente si viene como string de otro sistema
    normalized_id = int(user_id) if isinstance(user_id, str) else user_id
    return api.get_user(normalized_id)
```

## 8. Descripciones de Herramientas

### ✅ Estructura Recomendada

```python
@mcp.tool()
def search_items(
    query: str,
    page: int = 1,
) -> str:
    """
    Search for items with pagination and filtering.

    This tool provides comprehensive search capabilities with support for
    full-text search, pagination, and multiple filter options.

    Returns:
        JSON string with search results and pagination metadata.
    """
    ...
```

### Longitud Recomendada
- **Descripción principal**: 1-3 párrafos (máximo 500 caracteres)
- **Detalles de parámetros**: En `Field(description=...)`
- **Ejemplos**: En documentación separada o recursos MCP

## 9. Respuestas de Herramientas

### ✅ Retornar Contenido Estructurado

```python
from mcp.types import TextContent

def get_user(user_id: int):
    """Get user information"""
    user = api.get_user(user_id)

    # Opción 1: JSON string
    return json.dumps(user, indent=2)

    # Opción 2: Texto formateado
    return f"User: {user['name']}\nEmail: {user['email']}"
```

### Manejo de Errores

```python
def get_user(user_id: int):
    """Get user information"""
    try:
        user = api.get_user(user_id)
        return json.dumps(user, indent=2)
    except UserNotFoundError:
        return f"Error: User with ID {user_id} not found"
    except APIError as e:
        return f"API Error: {str(e)}"
```

## 10. Normalización Interna (Backward Compatibility)

### Patrón Recomendado

Cuando cambias de `Union[int, str]` a `int`, mantén normalización interna:

```python
# Función auxiliar de normalización
def normalize_int(value: Any) -> int:
    """Normalize value to integer"""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot convert '{value}' to integer")
    if isinstance(value, float):
        return int(value)
    raise TypeError(f"Expected int, got {type(value)}")

# Uso en la herramienta
@mcp.tool()
def search_items(page: int = 1):
    """Search items"""
    # Normalizar internamente por si viene de otro formato
    page_normalized = normalize_int(page)
    return api.search(page=page_normalized)
```

## 11. Checklist de Validación

Antes de considerar una herramienta lista:

- [ ] Tipos específicos (no `Union` innecesarios)
- [ ] Descripciones en todos los parámetros importantes
- [ ] Valores default apropiados
- [ ] Validaciones con `Field` donde corresponda
- [ ] Documentación clara y concisa
- [ ] Manejo de errores
- [ ] Normalización interna para BC (si aplica)
- [ ] Testing con diferentes clientes MCP

## 12. Ejemplo Completo

```python
from typing import Optional, Literal
from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TrackHS API")

@mcp.tool()
def search_reservations(
    page: int = Field(
        default=1,
        description="Page number (1-indexed)",
        ge=1,
        le=1000
    ),
    size: int = Field(
        default=10,
        description="Items per page",
        ge=1,
        le=100
    ),
    status: Optional[list[Literal["Confirmed", "Cancelled", "Pending"]]] = Field(
        default=None,
        description="Filter by reservation status"
    ),
    arrival_start: Optional[str] = Field(
        default=None,
        description="Filter by arrival date (ISO 8601: YYYY-MM-DD)",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    ),
    search: Optional[str] = Field(
        default=None,
        description="Full-text search in guest names and confirmation numbers",
        max_length=100
    ),
) -> str:
    """
    Search reservations with advanced filtering and pagination.

    Supports full-text search, status filtering, date ranges, and pagination.
    Returns reservations with guest and unit information.
    """
    # Implementación...
    pass
```

## Referencias

- [MCP Specification - Tools](../reference/mcp/05-referencias/especificacion/draft/server/tools.mdx)
- [FastMCP Examples](../reference/mcp/07-repositorios-originales/python-sdk/examples/fastmcp/)
- [Pydantic Field Validation](https://docs.pydantic.dev/latest/concepts/fields/)

## Conclusión

Siguiendo estas prácticas:
1. ✅ Mejora la compatibilidad con todos los clientes MCP
2. ✅ Reduce ambigüedad para modelos AI
3. ✅ Facilita el debugging
4. ✅ Mejora la documentación automática
5. ✅ Aumenta la confiabilidad del sistema
