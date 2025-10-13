# 📋 Parámetros Válidos para Units Collection API

## 🎯 Resumen

Este documento lista todos los parámetros válidos para la API de Units Collection de TrackHS, basado en la documentación oficial de la Channel API.

## ✅ Parámetros Soportados

### **Paginación y Ordenamiento**
- `page`: Número de página (1-based, máximo 10,000 resultados totales)
- `size`: Tamaño de página (máximo 1,000, limitado a 10,000 resultados totales)
- `sort_column`: Campo de ordenamiento (`id`, `name`, `nodeName`, `unitTypeName`)
- `sort_direction`: Dirección de ordenamiento (`asc`, `desc`)

### **Búsqueda de Texto**
- `search`: Búsqueda de texto en nombres/descripciones
- `term`: Búsqueda de subcadena coincidente
- `unit_code`: Búsqueda en unitCode (coincidencia exacta o usar % para wildcard)
- `short_name`: Búsqueda en shortName (coincidencia exacta o usar % para wildcard)

### **Filtros por ID**
- `node_id`: ID(s) de nodo - entero simple, separado por comas, o array
- `amenity_id`: ID(s) de amenidad - entero simple, separado por comas, o array
- `unit_type_id`: ID(s) de tipo de unidad - entero simple, separado por comas, o array
- `id`: Filtrar por IDs de unidad
- `calendar_id`: Retornar unidades que coincidan con el tipo de unidad con calendar group id
- `role_id`: Retornar unidades por roleId específico

### **Filtros por Características**
- `bedrooms`: Número exacto de habitaciones
- `min_bedrooms`: Número mínimo de habitaciones
- `max_bedrooms`: Número máximo de habitaciones
- `bathrooms`: Número exacto de baños
- `min_bathrooms`: Número mínimo de baños
- `max_bathrooms`: Número máximo de baños

### **Filtros Booleanos**
- `pets_friendly`: Unidades amigables con mascotas (0/1)
- `allow_unit_rates`: Unidades que permiten tarifas de unidad (0/1)
- `computed`: Valores computados adicionales (0/1)
- `inherited`: Atributos heredados adicionales (0/1)
- `limited`: Atributos muy limitados (0/1)
- `is_bookable`: Unidades reservables (0/1)
- `include_descriptions`: Incluir descripciones (0/1)
- `is_active`: Unidades activas (0/1)
- `events_allowed`: Permitir eventos (0/1)
- `smoking_allowed`: Permitir fumar (0/1)
- `children_allowed`: Permitir niños (0/1)
- `is_accessible`: Accesible (0/1)

### **Filtros por Fechas**
- `arrival`: Fecha de llegada (ISO 8601)
- `departure`: Fecha de salida (ISO 8601)
- `content_updated_since`: Cambios de contenido desde timestamp (ISO 8601)
- `updated_since`: Actualizado desde timestamp (ISO 8601) - deprecated

### **Filtros por Estado**
- `unit_status`: Estado de unidad (`clean`, `dirty`, `occupied`, `inspection`, `inprogress`)

## ❌ Parámetros NO Soportados

Los siguientes parámetros **NO están disponibles** en la API oficial y deben evitarse:

- `has_early_checkin` ❌
- `use_room_configuration` ❌
- `use_bed_types` ❌
- `folio_exception` ❌

## 🔧 Ejemplos de Uso

### **Búsqueda Básica**
```python
# Búsqueda simple
search_units()

# Con paginación
search_units(page=1, size=25)

# Con ordenamiento
search_units(sort_column="name", sort_direction="asc")
```

### **Filtros por Características**
```python
# Por habitaciones y baños
search_units(bedrooms=2, bathrooms=2)

# Por rango de habitaciones
search_units(min_bedrooms=2, max_bedrooms=4)

# Por características específicas
search_units(pets_friendly=1, is_active=1, is_bookable=1)
```

### **Filtros por Fechas**
```python
# Por disponibilidad
search_units(
    arrival="2024-01-01",
    departure="2024-01-07",
    is_bookable=1
)

# Por fecha de actualización
search_units(content_updated_since="2024-01-01T00:00:00Z")
```

### **Filtros por Ubicación**
```python
# Por nodo específico
search_units(node_id="1,2,3")

# Por amenidades
search_units(amenity_id="1,2,3", pets_friendly=1)

# Por tipo de unidad
search_units(unit_type_id="1,2,3")
```

### **Filtros por Estado**
```python
# Por estado de unidad
search_units(unit_status="clean")

# Por estado y características
search_units(
    unit_status="clean",
    is_active=1,
    is_bookable=1
)
```

## 🚨 Problemas Conocidos

### **Filtros Booleanos con Lógica Invertida**
Algunos filtros booleanos pueden retornar resultados con lógica invertida:

- `is_bookable=1` puede retornar unidades con `isBookable: false`
- `events_allowed=1` puede retornar unidades con `eventsAllowed: false`
- `smoking_allowed=1` puede retornar unidades con `smokingAllowed: false`
- `is_accessible=1` puede retornar unidades con `isAccessible: false`

**Solución**: Verificar los resultados y usar filtros adicionales para refinar la búsqueda.

### **Filtros de Rango**
Los filtros de rango (`min_bedrooms`, `max_bedrooms`, etc.) pueden no funcionar correctamente.

**Solución**: Usar filtros exactos (`bedrooms`, `bathrooms`) en su lugar.

## 📝 Notas Importantes

1. **Paginación**: La API usa paginación 1-based, pero el límite total es de 10,000 resultados
2. **Tipos de Datos**: Todos los parámetros numéricos deben ser enteros
3. **Fechas**: Usar formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)
4. **IDs**: Pueden ser enteros simples, separados por comas, o arrays
5. **Booleanos**: Solo aceptan valores 0 o 1

## 🔗 Referencias

- [Documentación Channel API](docs/trackhsDoc/get%20unit%20collection.md)
- [Reporte de Testing](TESTING_REPORT_UNITS_ENDPOINT.md)
- [Solución de Problemas](SOLUCION_ENDPOINT_UNITS.md)
