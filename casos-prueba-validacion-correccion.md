# Casos de Prueba para Validación de Corrección MCP search_units

## Objetivo

Validar que la corrección de tipos integer/number funciona correctamente y no introduce regresiones.

## Casos de Prueba Críticos

### 1. Parámetros Integer Básicos

```python
# Caso 1.1: Número de habitaciones
test_params = {
    "bedrooms": 3,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna unidades con 3 habitaciones

# Caso 1.2: Rango de habitaciones
test_params = {
    "min_bedrooms": 2,
    "max_bedrooms": 4,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna unidades entre 2-4 habitaciones

# Caso 1.3: Número exacto de baños
test_params = {
    "bathrooms": 2,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna unidades con 2 baños
```

### 2. Parámetros Booleanos (Integer 0/1)

```python
# Caso 2.1: Unidades activas
test_params = {
    "is_active": 1,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna solo unidades activas

# Caso 2.2: Unidades bookables
test_params = {
    "is_bookable": 1,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna solo unidades bookables

# Caso 2.3: Unidades pet-friendly
test_params = {
    "pets_friendly": 1,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna solo unidades pet-friendly

# Caso 2.4: Unidades accesibles
test_params = {
    "is_accessible": 1,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna solo unidades accesibles
```

### 3. Conversión de Tipos

```python
# Caso 3.1: Float a Integer
test_params = {
    "bedrooms": 3.0,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Se convierte a 3, sin errores

# Caso 3.2: String numérico a Integer
test_params = {
    "bedrooms": "3",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Se convierte a 3, sin errores

# Caso 3.3: Múltiples conversiones
test_params = {
    "bedrooms": 3.0,
    "bathrooms": "2",
    "is_active": 1.0,
    "page": 1,
    "size": 2
}
# Esperado: ✅ Todas las conversiones exitosas
```

### 4. Parámetro ID con Múltiples Valores

```python
# Caso 4.1: String separado por comas
test_params = {
    "id": "168,142,140",
    "page": 1,
    "size": 5
}
# Esperado: ✅ Retorna 3 unidades (IDs: 168, 142, 140)

# Caso 4.2: Array ya formateado
test_params = {
    "id": [168, 142, 140],
    "page": 1,
    "size": 5
}
# Esperado: ✅ Retorna 3 unidades

# Caso 4.3: ID único
test_params = {
    "id": "168",
    "page": 1,
    "size": 1
}
# Esperado: ✅ Retorna 1 unidad (ID: 168)
```

### 5. Combinaciones Complejas

```python
# Caso 5.1: Filtros múltiples con tipos mixtos
test_params = {
    "bedrooms": 3.0,
    "bathrooms": "2",
    "is_active": 1,
    "pets_friendly": 1,
    "arrival": "2025-11-01",
    "departure": "2025-11-07",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna unidades que cumplan todos los criterios

# Caso 5.2: Parámetros de ordenamiento con filtros
test_params = {
    "bedrooms": 4,
    "sort_column": "name",
    "sort_direction": "desc",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sin errores, retorna unidades de 4 habitaciones ordenadas por nombre desc
```

### 6. Casos Edge

```python
# Caso 6.1: Valores límite
test_params = {
    "bedrooms": 0,
    "page": 1,
    "size": 1
}
# Esperado: ✅ Sin errores (si hay unidades con 0 habitaciones)

# Caso 6.2: Valores negativos (deberían fallar en validación de rango)
test_params = {
    "bedrooms": -1,
    "page": 1,
    "size": 1
}
# Esperado: ❌ Error de validación de rango (no error de tipo)

# Caso 6.3: Valores muy grandes
test_params = {
    "bedrooms": 999999,
    "page": 1,
    "size": 1
}
# Esperado: ✅ Sin errores de tipo (puede retornar 0 resultados)
```

### 7. Regresiones - Funcionalidad Existente

```python
# Caso 7.1: Parámetros string (no deben cambiar)
test_params = {
    "search": "Orlando",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sigue funcionando igual

# Caso 7.2: Parámetros de fecha
test_params = {
    "arrival": "2025-11-01",
    "departure": "2025-11-07",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sigue funcionando igual

# Caso 7.3: Parámetros de amenidades
test_params = {
    "amenity_id": "1,9,13",
    "page": 1,
    "size": 2
}
# Esperado: ✅ Sigue funcionando igual
```

## Script de Testing Automatizado

```python
import pytest
from mcp_ihmTrackhs_search_units import search_units

class TestSearchUnitsCorrection:

    def test_integer_parameters_work(self):
        """Prueba que parámetros integer funcionan correctamente"""
        params = {
            "bedrooms": 3,
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result
        assert "units" in result["_embedded"]

    def test_float_conversion(self):
        """Prueba conversión de float a integer"""
        params = {
            "bedrooms": 3.0,
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result

    def test_string_conversion(self):
        """Prueba conversión de string numérico a integer"""
        params = {
            "bedrooms": "3",
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result

    def test_boolean_parameters(self):
        """Prueba parámetros booleanos (0/1)"""
        params = {
            "is_active": 1,
            "is_bookable": 1,
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result

    def test_id_multiple_values(self):
        """Prueba parámetro ID con múltiples valores"""
        params = {
            "id": "168,142,140",
            "page": 1,
            "size": 5
        }
        result = search_units(**params)
        assert "_embedded" in result
        # Verificar que retorna múltiples unidades
        units = result["_embedded"]["units"]
        assert len(units) > 1

    def test_complex_combination(self):
        """Prueba combinación compleja de parámetros"""
        params = {
            "bedrooms": 3.0,
            "bathrooms": "2",
            "is_active": 1,
            "pets_friendly": 1,
            "arrival": "2025-11-01",
            "departure": "2025-11-07",
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result

    def test_existing_functionality_unchanged(self):
        """Prueba que funcionalidad existente no se ve afectada"""
        params = {
            "search": "Orlando",
            "page": 1,
            "size": 2
        }
        result = search_units(**params)
        assert "_embedded" in result
        assert "units" in result["_embedded"]

    def test_error_handling(self):
        """Prueba manejo de errores"""
        # Parámetro inválido
        params = {
            "bedrooms": "invalid",
            "page": 1,
            "size": 2
        }
        with pytest.raises(ValueError):
            search_units(**params)
```

## Criterios de Aceptación

### ✅ Éxito
- [ ] Todos los parámetros integer funcionan sin errores de tipo
- [ ] Conversión automática de number a integer funciona
- [ ] Parámetro ID con múltiples valores retorna todos los resultados
- [ ] Funcionalidad existente no se ve afectada
- [ ] Casos edge se manejan correctamente

### ❌ Fallo
- [ ] Cualquier error de tipo "must be one of types [integer, null], got number"
- [ ] Regresiones en funcionalidad existente
- [ ] Parámetro ID con múltiples valores no funciona
- [ ] Conversión de tipos falla

## Métricas de Validación

1. **Cobertura de Parámetros**: 100% de parámetros integer probados
2. **Tasa de Éxito**: 100% de casos de prueba deben pasar
3. **Performance**: No degradación > 5% en tiempo de respuesta
4. **Regresiones**: 0 regresiones en funcionalidad existente

## Plan de Ejecución

### Fase 1: Testing Unitario
- [ ] Ejecutar casos de prueba 1-3
- [ ] Verificar conversión de tipos
- [ ] Validar manejo de errores

### Fase 2: Testing de Integración
- [ ] Ejecutar casos de prueba 4-6
- [ ] Probar combinaciones complejas
- [ ] Validar casos edge

### Fase 3: Testing de Regresión
- [ ] Ejecutar casos de prueba 7
- [ ] Comparar resultados con versión anterior
- [ ] Validar performance

### Fase 4: Testing de Aceptación
- [ ] Ejecutar todos los casos de prueba
- [ ] Validar criterios de aceptación
- [ ] Documentar resultados
