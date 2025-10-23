# 🎯 MEJORES PRÁCTICAS MCP: Cómo Indicar a los LLMs el Uso Correcto de Parámetros Opcionales

## 📋 RESUMEN EJECUTIVO

Este documento analiza las mejores prácticas del protocolo MCP (Model Context Protocol) y JSON Schema para guiar a los LLMs en el uso correcto de parámetros opcionales en APIs.

### 🔍 Problema Identificado

Los LLMs a veces envían el string literal `"null"` en lugar de omitir parámetros opcionales:

```json
{
  "arrival_start": "null",  // ❌ INCORRECTO
  "arrival_end": "null"     // ❌ INCORRECTO
}
```

### ✅ Solución Implementada

Normalización automática de strings inválidos + descripciones mejoradas en el esquema JSON.

---

## 🎓 HALLAZGOS DE LA INVESTIGACIÓN MCP

### 1. **Parámetros Opcionales en MCP** (FastMCP Documentation)

Según la documentación oficial de FastMCP:

> "Parameters without default values are required, while those with default values are optional."

**Regla clave:**
- Parámetros **sin** valor por defecto → **REQUERIDOS**
- Parámetros **con** valor por defecto → **OPCIONALES**

```python
# ✅ CORRECTO según MCP
@mcp.tool
def search_products(
    query: str,                   # REQUERIDO - sin default
    max_results: int = 10,        # OPCIONAL - con default
    sort_by: str = "relevance",   # OPCIONAL - con default
    category: str | None = None   # OPCIONAL - puede ser None
) -> list[dict]:
    """Search the product catalog."""
    pass
```

### 2. **Descripciones de Parámetros para LLMs**

FastMCP enfatiza:

> "A good description is crucial for helping an LLM understand how to use a parameter correctly."

**Mejores prácticas identificadas:**

✅ **Usar descripciones explícitas y orientadas a LLMs:**
```python
arrival_start: Optional[str] = Field(
    default=None,
    description=(
        "Filter by arrival date start. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15'). "
        "To omit this filter, simply don't include this parameter. "
        "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
    ),
)
```

❌ **Evitar descripciones técnicas:**
```python
# ❌ Descripción para desarrolladores, no para LLMs
arrival_start: Optional[str] = Field(
    default=None,
    description="Arrival start date (ISO 8601)"
)
```

### 3. **Validación de Tipos Flexible vs Estricta**

FastMCP proporciona dos modos de validación:

**Modo flexible (default):**
```python
mcp = FastMCP("MyServer")  # Coerción automática de tipos
# "10" → 10 (string a int)
# "true" → True (string a bool)
```

**Modo estricto:**
```python
mcp = FastMCP("MyServer", strict_input_validation=True)
# "10" → ERROR (requiere int exacto)
```

**Recomendación:** Usar modo flexible + normalización manual para mejor compatibilidad con LLMs.

---

## 🎯 ESTRATEGIAS PARA GUIAR A LOS LLMs

### Estrategia 1: **Descripciones Explícitas con Ejemplos**

```python
Optional[str] = Field(
    default=None,
    description=(
        "📋 PURPOSE: Filter by arrival date start\n"
        "✅ CORRECT FORMAT: 'YYYY-MM-DD' (e.g., '2024-01-15')\n"
        "❌ WRONG: 'null', timestamps, empty strings\n"
        "💡 TO OMIT: Simply don't include this parameter\n"
        "📚 EXAMPLES:\n"
        "  - '2024-01-01' (January 1st)\n"
        "  - '2024-12-31' (December 31st)"
    ),
)
```

**Por qué funciona:**
- Emojis atraen atención del LLM
- Ejemplos específicos reducen ambigüedad
- Instrucción explícita de **NO usar** "null"

### Estrategia 2: **Normalización Defensiva en el Servidor**

```python
def normalize_optional_string(
    value: Optional[str], param_name: str
) -> Optional[str]:
    """
    Convierte valores inválidos a None automáticamente.

    Maneja:
    - None → None
    - "null" → None
    - "None" → None
    - "" → None
    - "  " → None
    """
    if value is None or not isinstance(value, str):
        return None

    value = value.strip()
    if not value or value.lower() in ["null", "none"]:
        return None

    return value
```

**Beneficios:**
- ✅ Tolera errores comunes de LLMs
- ✅ Mantiene API robusta
- ✅ Reduce frustración del usuario

### Estrategia 3: **JSON Schema Optimizado**

Según el estándar JSON Schema Draft 2020-12:

```json
{
  "type": "object",
  "properties": {
    "arrival_start": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Arrival start date. Use YYYY-MM-DD format like '2024-01-15'. To omit this filter, simply don't include this parameter in your request. Do NOT use the string 'null'.",
      "examples": ["2024-01-15", "2024-12-31"],
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    }
  },
  "required": []
}
```

**Elementos clave:**
- `"type": ["string", "null"]` - Acepta string o null (JSON null, no string "null")
- `"description"` - Instrucciones explícitas
- `"examples"` - Ejemplos concretos
- `"pattern"` - Validación de formato

---

## 📊 COMPARACIÓN DE ENFOQUES

| Enfoque | Pros | Contras | Recomendado |
|---------|------|---------|-------------|
| **Solo descripciones** | Simple, estándar | LLMs pueden ignorar | ⚠️ Insuficiente |
| **Solo validación estricta** | Cumple estándar | Muchos errores | ❌ No recomendado |
| **Normalización automática** | Robusto, tolerante | Código adicional | ✅ **SÍ** |
| **Descripciones + Normalización** | Mejor experiencia | Más mantenimiento | ✅✅ **IDEAL** |

---

## 🛠️ IMPLEMENTACIÓN RECOMENDADA

### Paso 1: Actualizar Descripciones de Parámetros

```python
arrival_start: Optional[str] = Field(
    default=None,
    description=(
        "Filter by arrival date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
        "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. "
        "⚠️ IMPORTANT: To omit this filter, DO NOT include this parameter in your request. "
        "❌ DO NOT use 'null' as a string value. "
        "✅ CORRECT: omit the parameter entirely if you don't want to filter by arrival date. "
        "💡 EXAMPLES: '2024-03-01' (March 1st, 2024), '2024-12-31' (December 31st, 2024)"
    ),
)
```

### Paso 2: Agregar Normalización

```python
from ..utils.type_normalization import normalize_optional_string

# Normalizar TODOS los parámetros string opcionales
arrival_start = normalize_optional_string(arrival_start, "arrival_start")
arrival_end = normalize_optional_string(arrival_end, "arrival_end")
search = normalize_optional_string(search, "search")
# etc...
```

### Paso 3: Validar DESPUÉS de Normalizar

```python
# Después de normalizar, validar formato
if arrival_start is not None:
    if not is_valid_iso8601_date(arrival_start):
        raise ValidationError(
            f"Invalid date format for arrival_start: '{arrival_start}'. "
            f"Use ISO 8601 format like '2024-03-01'.",
            "arrival_start"
        )
```

---

## 📈 MEJORAS ESPECÍFICAS IMPLEMENTADAS

### ✅ Mejora 1: Nueva función `normalize_optional_string`

**Ubicación:** `src/trackhs_mcp/infrastructure/utils/type_normalization.py`

```python
def normalize_optional_string(
    value: Optional[str], param_name: str
) -> Optional[str]:
    """
    Normaliza un parámetro string opcional, convirtiendo valores inválidos a None.

    Esta función es especialmente útil para manejar casos donde LLMs pasan
    el string literal "null" en lugar de omitir el parámetro.

    Convierte a None:
    - None (ya es None)
    - "null" (string literal)
    - "None" (string literal)
    - "" (string vacío)
    - "  " (solo espacios)
    """
    if _is_field_info(value) or value is None:
        return None

    if not isinstance(value, str):
        raise ValidationError(
            f"{param_name} must be a string or None, got: {type(value).__name__}",
            param_name,
        )

    value = value.strip()
    if not value or value.lower() in ["null", "none"]:
        return None

    return value
```

### ✅ Mejora 2: Normalización en `search_reservations_v2`

**Ubicación:** `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`

```python
# Normalizar todos los parámetros string opcionales
# Esto convierte "null", "None", "", etc. a None real ANTES de validar
arrival_start = normalize_optional_string(arrival_start, "arrival_start")
arrival_end = normalize_optional_string(arrival_end, "arrival_end")
departure_start = normalize_optional_string(departure_start, "departure_start")
departure_end = normalize_optional_string(departure_end, "departure_end")
updated_since = normalize_optional_string(updated_since, "updated_since")
booked_start = normalize_optional_string(booked_start, "booked_start")
booked_end = normalize_optional_string(booked_end, "booked_end")
search = normalize_optional_string(search, "search")
tags = normalize_optional_string(tags, "tags")
# ... etc para todos los parámetros string opcionales
```

---

## 🎯 RECOMENDACIONES FINALES

### Para el Esquema JSON (Descripción):

1. ✅ **Usar instrucciones explícitas**
   - "To omit this filter, simply don't include this parameter"
   - "Do NOT use 'null' as a string"

2. ✅ **Incluir ejemplos concretos**
   - "Example: '2024-01-15'"
   - "Examples: '2024-03-01' (March 1st), '2024-12-31' (December 31st)"

3. ✅ **Usar emojis estratégicamente**
   - ⚠️ para advertencias
   - ❌ para errores
   - ✅ para formato correcto
   - 💡 para ejemplos

4. ✅ **Especificar formato claramente**
   - "ISO 8601: YYYY-MM-DD"
   - "Not YYYY-MM-DDTHH:MM:SSZ"

### Para el Código (Validación):

1. ✅ **Normalizar primero, validar después**
   ```python
   value = normalize_optional_string(value, "param")
   if value is not None:
       validate_format(value)
   ```

2. ✅ **Ser tolerante con errores comunes**
   - Aceptar "null", "None", ""
   - Convertir automáticamente a None
   - Solo fallar en valores realmente inválidos

3. ✅ **Mensajes de error informativos**
   ```python
   raise ValidationError(
       f"❌ Invalid date: '{value}'. "
       f"✅ Use: '2024-03-01'. "
       f"💡 Or omit the parameter entirely.",
       param_name
   )
   ```

---

## 📚 REFERENCIAS

1. **FastMCP Documentation - Optional Arguments**
   - https://gofastmcp.com/servers/tools#optional-arguments

2. **FastMCP Documentation - Tool Transformation**
   - https://gofastmcp.com/patterns/tool-transformation

3. **FastMCP Documentation - Validation Modes**
   - https://gofastmcp.com/servers/tools#validation-modes

4. **JSON Schema Specification**
   - https://json-schema.org/draft/2020-12/json-schema-validation

5. **MCP Protocol Specification**
   - Model Context Protocol Official Documentation

---

## ✅ ESTADO DE IMPLEMENTACIÓN

### ✅ Completado:
- [x] Función `normalize_optional_string` creada
- [x] Normalización integrada en `search_reservations_v2`
- [x] Descripciones de parámetros actualizadas
- [x] Validación después de normalización

### 📋 Recomendaciones Futuras:
- [ ] Aplicar mismo patrón a otras herramientas MCP
- [ ] Crear test suite para casos edge
- [ ] Documentar patrones en README
- [ ] Considerar middleware de normalización global

---

## 🎓 CONCLUSIÓN

**La mejor forma de indicar a los LLMs cómo usar parámetros opcionales es:**

1. **Descripciones explícitas** con ejemplos y advertencias claras
2. **Normalización defensiva** que tolere errores comunes
3. **Validación informativa** con mensajes claros de error
4. **Esquema JSON optimizado** con types, patterns y examples

**Esta combinación proporciona:**
- ✅ Mejor experiencia para LLMs
- ✅ API más robusta y tolerante
- ✅ Menos errores de validación
- ✅ Usuarios más satisfechos

---

**Fecha:** 23 de octubre de 2025
**Autor:** Track HS MCP Team
**Versión:** 1.0

