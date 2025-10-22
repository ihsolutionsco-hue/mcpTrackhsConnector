# Especificaciones Técnicas: Corrección de Problemas MCP search_units

## Problema Principal: Incompatibilidad de Tipos Integer/Number

### Descripción del Problema

El cliente MCP (Cursor) envía valores numéricos como tipo `number` en JSON, pero el esquema Pydantic del servidor MCP espera tipo `integer`. Esto causa errores de validación para aproximadamente 15 parámetros críticos.

### Parámetros Afectados

```python
# Parámetros que fallan actualmente:
- bedrooms: int
- min_bedrooms: int
- max_bedrooms: int
- bathrooms: int
- min_bathrooms: int
- max_bathrooms: int
- is_active: int (0/1)
- is_bookable: int (0/1)
- pets_friendly: int (0/1)
- smoking_allowed: int (0/1)
- children_allowed: int (0/1)
- events_allowed: int (0/1)
- is_accessible: int (0/1)
- computed: int (0/1)
- inherited: int (0/1)
- limited: int (0/1)
- include_descriptions: int (0/1)
```

### Solución Recomendada

#### Opción 1: Conversión Automática en el Adaptador MCP

```python
# En el adaptador MCP, antes de la validación Pydantic:
def convert_number_to_integer(params: dict) -> dict:
    """Convierte valores number a integer para parámetros específicos"""
    integer_params = {
        'bedrooms', 'min_bedrooms', 'max_bedrooms', 'bathrooms',
        'min_bathrooms', 'max_bathrooms', 'is_active', 'is_bookable',
        'pets_friendly', 'smoking_allowed', 'children_allowed',
        'events_allowed', 'is_accessible', 'computed', 'inherited',
        'limited', 'include_descriptions'
    }

    for param in integer_params:
        if param in params and isinstance(params[param], (int, float)):
            params[param] = int(params[param])

    return params
```

#### Opción 2: Modificar el Esquema Pydantic

```python
# Cambiar de:
bedrooms: Optional[int] = None

# A:
bedrooms: Optional[Union[int, float]] = None

# Y agregar validación personalizada:
@validator('bedrooms', pre=True)
def convert_bedrooms_to_int(cls, v):
    if v is not None:
        return int(v)
    return v
```

#### Opción 3: Usar Coercion en Pydantic

```python
# En el modelo Pydantic:
class SearchUnitsParams(BaseModel):
    bedrooms: Optional[int] = Field(None, ge=0)

    class Config:
        # Permitir conversión automática
        use_enum_values = True
        validate_assignment = True

    @validator('*', pre=True)
    def convert_numbers_to_int(cls, v, field):
        if field.type_ == int and isinstance(v, (int, float)):
            return int(v)
        return v
```

### Implementación Recomendada

**Recomiendo la Opción 1** por las siguientes razones:

1. **Mínimo impacto**: No requiere cambios en el esquema Pydantic
2. **Compatibilidad**: Mantiene la validación estricta de tipos
3. **Mantenibilidad**: Centraliza la lógica de conversión
4. **Debugging**: Fácil de rastrear y debuggear

### Código de Implementación

```python
# En el archivo del adaptador MCP (search_units)
from typing import Dict, Any, Union

def preprocess_search_units_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocesa parámetros para convertir number a integer
    según la especificación OpenAPI de TrackHS
    """
    # Parámetros que deben ser integer según OpenAPI spec
    integer_fields = {
        'bedrooms', 'min_bedrooms', 'max_bedrooms',
        'bathrooms', 'min_bathrooms', 'max_bathrooms',
        'is_active', 'is_bookable', 'pets_friendly',
        'smoking_allowed', 'children_allowed', 'events_allowed',
        'is_accessible', 'computed', 'inherited', 'limited',
        'include_descriptions', 'calendar_id', 'role_id'
    }

    processed_params = params.copy()

    for field in integer_fields:
        if field in processed_params and processed_params[field] is not None:
            value = processed_params[field]
            # Convertir number a integer si es numérico
            if isinstance(value, (int, float)):
                processed_params[field] = int(value)
            # Manejar strings numéricos
            elif isinstance(value, str) and value.isdigit():
                processed_params[field] = int(value)

    return processed_params

# Aplicar antes de la validación Pydantic:
def search_units_handler(params: Dict[str, Any]) -> str:
    # Preprocesar parámetros
    processed_params = preprocess_search_units_params(params)

    # Validar con Pydantic (ahora debería funcionar)
    validated_params = SearchUnitsParams(**processed_params)

    # Continuar con la lógica normal...
```

## Problema Secundario: Parámetro ID con Múltiples Valores

### Descripción

El parámetro `id` con valores separados por comas ("168,142,140") solo retorna 1 resultado en lugar de 3.

### Análisis

Según la documentación OpenAPI, el parámetro `id` acepta:
```json
{
  "schema": {
    "type": "array",
    "items": {
      "type": "integer"
    }
  }
}
```

### Solución

```python
# En el preprocesamiento:
def preprocess_id_parameter(params: Dict[str, Any]) -> Dict[str, Any]:
    """Convierte string separado por comas a array de integers"""
    if 'id' in params and isinstance(params['id'], str):
        # Dividir por comas y convertir a integers
        id_list = [int(x.strip()) for x in params['id'].split(',') if x.strip().isdigit()]
        params['id'] = id_list
    return params
```

## Testing de la Solución

### Casos de Prueba

```python
def test_integer_conversion():
    """Prueba conversión de number a integer"""
    test_cases = [
        # (input, expected_output)
        ({"bedrooms": 3}, {"bedrooms": 3}),
        ({"bedrooms": 3.0}, {"bedrooms": 3}),
        ({"is_active": 1}, {"is_active": 1}),
        ({"is_active": 1.0}, {"is_active": 1}),
        ({"bedrooms": "3"}, {"bedrooms": 3}),
    ]

    for input_params, expected in test_cases:
        result = preprocess_search_units_params(input_params)
        assert result == expected

def test_id_parameter_conversion():
    """Prueba conversión de ID string a array"""
    test_cases = [
        ({"id": "168,142,140"}, {"id": [168, 142, 140]}),
        ({"id": "168"}, {"id": [168]}),
        ({"id": [168, 142]}, {"id": [168, 142]}),  # Ya es array
    ]

    for input_params, expected in test_cases:
        result = preprocess_id_parameter(input_params)
        assert result == expected
```

## Validación Post-Implementación

### Pruebas de Regresión

1. **Probar todos los parámetros integer que fallaban antes**
2. **Verificar que parámetros string siguen funcionando**
3. **Confirmar que validaciones de rango siguen activas**
4. **Probar casos edge (valores negativos, muy grandes, etc.)**

### Métricas de Éxito

- ✅ 0 errores de tipo "must be one of types [integer, null], got number"
- ✅ Parámetro `id` con múltiples valores retorna todos los resultados
- ✅ Todos los filtros numéricos funcionan correctamente
- ✅ No se introducen regresiones en funcionalidad existente

## Cronograma de Implementación

### Fase 1: Implementación (1-2 días)
- [ ] Implementar función de preprocesamiento
- [ ] Aplicar a todos los endpoints afectados
- [ ] Testing unitario

### Fase 2: Testing (1 día)
- [ ] Testing de integración
- [ ] Pruebas de regresión
- [ ] Validación con casos reales

### Fase 3: Despliegue (1 día)
- [ ] Deploy a ambiente de testing
- [ ] Validación con cliente MCP real
- [ ] Deploy a producción

## Notas Adicionales

### Consideraciones de Performance

La función de preprocesamiento es O(1) por parámetro, por lo que el impacto en performance es mínimo.

### Compatibilidad

Esta solución mantiene compatibilidad total con:
- Clientes que ya envían integers correctos
- Clientes que envían strings numéricos
- Clientes que envían floats

### Monitoreo

Recomiendo agregar logging para monitorear:
- Frecuencia de conversiones
- Tipos de parámetros que requieren conversión
- Errores de conversión (si los hay)
