# Herramienta Search Reservations V2

## Descripción

La herramienta `search_reservations` ha sido completamente actualizada para aprovechar todas las capacidades de la API Search Reservations V2 de Track HS. Esta herramienta proporciona búsqueda avanzada de reservas con filtros completos, paginación robusta y soporte para grandes conjuntos de datos.

## Características Principales

### ✅ Compatibilidad Completa con API V2
- Endpoint: `/v2/pms/reservations`
- Todos los parámetros de la especificación V2
- Respuesta completa con todos los campos disponibles

### ✅ Paginación Avanzada
- **Paginación Estándar:** `page` y `size` para resultados limitados
- **Scroll de Elasticsearch:** Para grandes conjuntos de datos
- **Límites:** Máximo 10,000 resultados totales, 1,000 por página

### ✅ Filtros Completos
- **Filtros de Fecha:** bookedStart/End, arrivalStart/End, departureStart/End
- **Filtros por ID:** nodeId, unitId, contactId, reservationTypeId, etc.
- **Filtros Especiales:** inHouseToday, status, tags, groupId
- **Búsqueda de Texto:** search para búsqueda por substring

### ✅ Ordenamiento Avanzado
- **Columnas:** name, status, altConf, agreementStatus, type, guest, guests, unit, units, checkin, checkout, nights
- **Direcciones:** asc, desc

## Parámetros Disponibles

### Parámetros de Paginación

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `page` | int | Número de página | 1+ (default: 1) |
| `size` | int | Tamaño de página | 1-1000 (default: 10) |
| `scroll` | int/string | Scroll de Elasticsearch | 1 para empezar, string para continuar |

### Parámetros de Ordenamiento

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `sort_column` | string | Columna para ordenar | name, status, altConf, agreementStatus, type, guest, guests, unit, units, checkin, checkout, nights |
| `sort_direction` | string | Dirección de ordenamiento | asc, desc |

### Filtros de Búsqueda

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `search` | string | Búsqueda por substring en nombre o descripciones |
| `tags` | string | Búsqueda por ID de tag |
| `updated_since` | string | Filtro por fecha de actualización (ISO 8601) |

### Filtros por ID

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `node_id` | int/array | ID(s) del nodo específico |
| `unit_id` | int/array | ID(s) de la unidad específica |
| `reservation_type_id` | int/array | ID(s) del tipo de reserva específico |
| `contact_id` | int/array | ID(s) del contacto específico |
| `travel_agent_id` | int/array | ID(s) del agente de viajes específico |
| `campaign_id` | int/array | ID(s) de la campaña específica |
| `user_id` | int/array | ID(s) del usuario específico |
| `unit_type_id` | int/array | ID(s) del tipo de unidad específico |
| `rate_type_id` | int/array | ID(s) del tipo de tarifa específico |

### Filtros de Fecha

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `booked_start` | string | Fecha de inicio de reserva (ISO 8601) |
| `booked_end` | string | Fecha de fin de reserva (ISO 8601) |
| `arrival_start` | string | Fecha de inicio de llegada (ISO 8601) |
| `arrival_end` | string | Fecha de fin de llegada (ISO 8601) |
| `departure_start` | string | Fecha de inicio de salida (ISO 8601) |
| `departure_end` | string | Fecha de fin de salida (ISO 8601) |

### Filtros Especiales

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `in_house_today` | int | Filtrar por en casa hoy | 0 o 1 |
| `status` | string/array | Estado(s) de la reserva | Hold, Confirmed, Checked Out, Checked In, Cancelled |
| `group_id` | int | ID del grupo conectado |
| `checkin_office_id` | int | ID de la oficina de check-in |

## Ejemplos de Uso

### Búsqueda Básica

```python
# Búsqueda simple con paginación
result = await search_reservations(
    page=1,
    size=50,
    sort_column="name",
    sort_direction="asc"
)
```

### Búsqueda con Filtros de Fecha

```python
# Reservas confirmadas para 2024
result = await search_reservations(
    page=1,
    size=100,
    status="Confirmed",
    arrival_start="2024-01-01T00:00:00Z",
    arrival_end="2024-12-31T23:59:59Z"
)
```

### Búsqueda con Filtros Múltiples

```python
# Reservas en nodos específicos con filtros avanzados
result = await search_reservations(
    page=1,
    size=50,
    node_id=[123, 456],
    unit_type_id=[789],
    status=["Confirmed", "Checked In"],
    in_house_today=1,
    arrival_start="2024-01-01T00:00:00Z"
)
```

### Búsqueda con Scroll (Grandes Conjuntos)

```python
# Usar scroll para grandes conjuntos de datos
result = await search_reservations(
    scroll=1,
    size=100,
    status="Confirmed",
    arrival_start="2024-01-01T00:00:00Z"
)
```

### Búsqueda de Texto

```python
# Búsqueda por nombre o descripción
result = await search_reservations(
    page=1,
    size=20,
    search="John",
    sort_column="name"
)
```

## Respuesta de la API V2

### Estructura de Respuesta

```json
{
  "_embedded": {
    "reservations": [
      {
        "id": 12345,
        "alternates": ["ALT123", "ALT456"],
        "currency": "USD",
        "unit_id": 789,
        "arrival_date": "2024-01-15",
        "departure_date": "2024-01-20",
        "status": "Confirmed",
        "occupants": [...],
        "security_deposit": {...},
        "guest_breakdown": {...},
        "owner_breakdown": {...},
        "travel_insurance_products": [...],
        "payment_plan": [...],
        "_embedded": {...},
        "_links": {...}
      }
    ]
  },
  "page": 1,
  "page_count": 10,
  "page_size": 50,
  "total_items": 500,
  "_links": {
    "self": {...},
    "first": {...},
    "last": {...},
    "next": {...},
    "prev": {...}
  }
}
```

### Campos Principales de Reserva

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | int | ID único de la reserva |
| `alternates` | array | IDs de confirmación alternativos |
| `currency` | string | Moneda de la reserva |
| `unit_id` | int | ID de la unidad |
| `arrival_date` | string | Fecha de llegada (ISO 8601) |
| `departure_date` | string | Fecha de salida (ISO 8601) |
| `status` | string | Estado de la reserva |
| `occupants` | array | Información de ocupantes |
| `security_deposit` | object | Depósito de seguridad |
| `guest_breakdown` | object | Desglose financiero del huésped |
| `owner_breakdown` | object | Desglose financiero del propietario |
| `travel_insurance_products` | array | Productos de seguro de viaje |
| `payment_plan` | array | Plan de pagos |

## Mejores Prácticas

### 1. Paginación Eficiente

```python
# Para conjuntos pequeños (< 1000 resultados)
result = await search_reservations(
    page=1,
    size=50,
    # ... otros filtros
)

# Para conjuntos grandes (> 1000 resultados)
result = await search_reservations(
    scroll=1,
    size=100,
    # ... otros filtros
)
```

### 2. Filtros Específicos

```python
# Usar filtros específicos para mejorar rendimiento
result = await search_reservations(
    node_id=123,  # Filtro específico
    status="Confirmed",  # Estado específico
    arrival_start="2024-01-01T00:00:00Z",  # Rango de fecha
    # ... otros filtros
)
```

### 3. Manejo de Errores

```python
try:
    result = await search_reservations(...)
    if "error" in result:
        # Manejar error de API
        print(f"Error: {result['error']}")
    else:
        # Procesar resultados
        reservations = result["_embedded"]["reservations"]
except Exception as e:
    # Manejar error de conexión
    print(f"Error de conexión: {str(e)}")
```

### 4. Procesamiento de Grandes Conjuntos

```python
# Usar scroll para procesar grandes conjuntos
scroll_id = 1
all_reservations = []

while True:
    result = await search_reservations(
        scroll=scroll_id,
        size=100,
        # ... otros filtros
    )

    if not result["_embedded"]["reservations"]:
        break

    all_reservations.extend(result["_embedded"]["reservations"])
    scroll_id = result.get("_scroll_id")

    if not scroll_id:
        break
```

## Limitaciones

- **Máximo 10,000 resultados totales** por consulta
- **Máximo 1,000 elementos por página**
- **Scroll timeout de 1 minuto**
- **Rate limiting** según configuración del servidor

## Troubleshooting

### Error de Paginación
```
Error: Total de resultados solicitados (15000) excede el límite máximo (10000)
```
**Solución:** Usar scroll en lugar de paginación estándar para grandes conjuntos.

### Error de Scroll
```
Error: Scroll timeout
```
**Solución:** Reducir el tamaño de página o procesar más rápido.

### Error de Filtros
```
Error: Invalid parameter value
```
**Solución:** Verificar formato de fechas (ISO 8601) y tipos de datos.

## Recursos Adicionales

- [Documentación de la API V2](../resources.py)
- [Modelos de Datos](../types/reservations.py)
- [Utilidades de Soporte](../core/)
- [Ejemplos de Uso](../prompts.py)
