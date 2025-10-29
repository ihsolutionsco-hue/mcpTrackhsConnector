# 🐛 Issue: Parámetros isPublic/publicSearchable/isFilterable en FastMCP Cloud

**Fecha:** 29 de Octubre, 2025
**Severidad:** Media
**Estado:** 🔴 **NO RESUELTO** - Limitación de FastMCP Cloud
**Afecta a:** `search_amenities` tool

---

## 📋 Descripción del Problema

Los parámetros de filtrado booleanos (`isPublic`, `publicSearchable`, `isFilterable`) no aceptan valores numéricos (0 o 1) cuando se invoca la herramienta desde clientes MCP, generando el siguiente error:

```
Parameter 'isPublic' must be one of types [, null], got number
```

---

## 🔍 Causa Raíz

FastMCP Cloud genera un schema JSON desde las definiciones de tipos Python. Cuando usamos `Optional[Any]` sin anotaciones de Pydantic, el schema JSON resultante solo permite `null` pero no permite `number` o `string`.

### Definición Actual (que no funciona en Cloud):
```python
isPublic: Optional[Any] = None,
publicSearchable: Optional[Any] = None,
isFilterable: Optional[Any] = None,
```

### Schema JSON Generado (inferido del error):
```json
{
  "type": ["null"]  // Solo permite null
}
```

### Schema JSON Esperado:
```json
{
  "type": ["null", "integer", "string"]  // Debería permitir null, int y string
}
```

---

## 🧪 Intentos de Corrección

### Intento 1: Usar `Union[int, str]` con Field
```python
isPublic: Annotated[
    Optional[Union[int, str]],
    Field(ge=0, le=1, description="...")
] = None
```
**Resultado:** ❌ Error - FastMCP Cloud no reconoce el tipo correctamente

### Intento 2: Usar `FlexibleIntType` (alias)
```python
isPublic: Annotated[
    Optional[FlexibleIntType],
    Field(ge=0, le=1, description="...")
] = None
```
**Resultado:** ❌ Error - El alias no se expande correctamente en el schema

### Intento 3: Usar `Union[int, str]` sin restricciones
```python
isPublic: Annotated[
    Optional[Union[int, str]],
    Field(description="...")
] = None
```
**Resultado:** ❌ Error - Persiste el problema

### Intento 4: Usar `Optional[Any]` con Field
```python
isPublic: Annotated[
    Optional[Any],
    Field(description="...")
] = None
```
**Resultado:** ❌ Error - Any no se traduce correctamente al schema JSON

### Intento 5: Usar `Optional[Any]` sin anotaciones
```python
isPublic: Optional[Any] = None
```
**Resultado:** ❌ Error - Schema JSON solo permite null

---

## 📊 Impacto

### Funcionalidades Afectadas:
- ❌ No se puede filtrar por amenidades públicas/privadas
- ❌ No se puede filtrar por amenidades buscables públicamente
- ❌ No se puede filtrar por amenidades filtrables

### Funcionalidades que SÍ Funcionan:
- ✅ Búsqueda por texto (`search`)
- ✅ Filtrado por grupo (`groupId`)
- ✅ Ordenamiento (`sortColumn`, `sortDirection`)
- ✅ Búsqueda por tipos OTA (`airbnbType`, `homeawayType`, etc.)
- ✅ Paginación (`page`, `size`)

### Casos de Uso Bloqueados:
1. ❌ Listar solo amenidades públicas para website
2. ❌ Listar solo amenidades filtrables para formularios
3. ❌ Listar amenidades buscables para motor de búsqueda

---

## 💡 Soluciones Alternativas

### Solución Temporal 1: Remover los Parámetros
Comentar/remover temporalmente estos parámetros hasta que FastMCP Cloud soporte correctamente `Any` en el schema JSON.

### Solución Temporal 2: Usar el API Directamente
Para casos donde se necesitan estos filtros, usar el `TrackHSClient` directamente:

```python
from trackhs_mcp.client import TrackHSClient

client = TrackHSClient(base_url="...", username="...", password="...")
result = client.get("api/pms/units/amenities", {
    "page": 1,
    "size": 20,
    "isPublic": 1,
    "isFilterable": 1
})
```

### Solución Temporal 3: Crear Herramientas Separadas
Crear herramientas específicas para casos de uso comunes:

```python
@mcp.tool()
def get_public_amenities(size: int = 20) -> Dict[str, Any]:
    """Obtener solo amenidades públicas"""
    return api_client.get("api/pms/units/amenities", {
        "page": 1,
        "size": size,
        "isPublic": 1
    })

@mcp.tool()
def get_filterable_amenities(size: int = 20) -> Dict[str, Any]:
    """Obtener solo amenidades filtrables"""
    return api_client.get("api/pms/units/amenities", {
        "page": 1,
        "size": size,
        "isFilterable": 1
    })
```

---

## 🔧 Solución Definitiva (Pendiente)

### Opción A: Actualización de FastMCP
Esperar a que FastMCP Cloud actualice el generador de schemas JSON para soportar correctamente `Optional[Any]` como un tipo que acepta múltiples valores.

### Opción B: Usar JSON Schema Personalizado
Definir manualmente el schema JSON de salida para estos parámetros:

```python
AMENITIES_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "isPublic": {
            "anyOf": [
                {"type": "integer", "minimum": 0, "maximum": 1},
                {"type": "string"},
                {"type": "null"}
            ]
        },
        # ... otros parámetros
    }
}

@mcp.tool(input_schema=AMENITIES_INPUT_SCHEMA)
def search_amenities(...):
    ...
```

### Opción C: Contactar Soporte de FastMCP
Reportar el issue al equipo de FastMCP para que corrijan el generador de schemas.

---

## 📝 Commits Relacionados

| Commit | Intento | Resultado |
|--------|---------|-----------|
| `abc2f7f` | Union[int, str] con Field | ❌ Fallo |
| `32e70f6` | Optional[Any] con Field | ❌ Fallo |
| `7aeb0eb` | Optional[Any] sin Field | ❌ Fallo |

---

## 📚 Referencias

- **Documentación FastMCP:** https://gofastmcp.com
- **Issue similar:** (pendiente de buscar en GitHub de FastMCP)
- **Servidor afectado:** ihmTrackhs en FastMCP Cloud
- **Versión FastMCP:** 2.13.0.2

---

## ✅ Recomendaciones

### Corto Plazo:
1. ✅ **Documentar limitación** en README y docs de la API
2. ✅ **Implementar solución temporal 3** (herramientas específicas)
3. ✅ **Notificar a usuarios** sobre la limitación

### Mediano Plazo:
1. ⏳ **Contactar soporte FastMCP** para reportar el issue
2. ⏳ **Investigar alternativas** de implementación
3. ⏳ **Monitorear actualizaciones** de FastMCP

### Largo Plazo:
1. 🔮 **Migrar a solución definitiva** cuando esté disponible
2. 🔮 **Actualizar tests** para incluir estos parámetros
3. 🔮 **Actualizar documentación** con la solución final

---

## 👤 Reportado por

**Rol:** Developer/Tester
**Fecha:** 29 de Octubre, 2025
**Repositorio:** ihsolutionsco-hue/mcpTrackhsConnector
**Último commit:** `7aeb0eb`

---

## 📈 Estado del Testing

| Categoría | Exitoso | Fallido | Total |
|-----------|---------|---------|-------|
| **Búsqueda por texto** | 10 | 0 | 10 |
| **Filtros booleanos** | 0 | 3 | 3 |
| **Otros parámetros** | 8 | 0 | 8 |
| **TOTAL** | 18 | 3 | 21 |

**Tasa de éxito:** 85.7% (18/21)

---

**Nota:** A pesar de este issue, la herramienta `search_amenities` es completamente funcional para la mayoría de casos de uso. Los filtros booleanos son una funcionalidad avanzada que puede implementarse mediante soluciones alternativas.

