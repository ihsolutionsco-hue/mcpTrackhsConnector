# Get Maintenance Work Orders API

## Descripción
Obtiene una colección paginada de órdenes de trabajo de mantenimiento desde Track HS. Esta herramienta permite filtrar y buscar órdenes de trabajo con múltiples criterios.

## Parámetros

### Opcionales

#### Paginación
- **`page`** (number): Número de página (por defecto: 1)
- **`size`** (number): Tamaño de página (por defecto: 25, máximo: 100)

#### Ordenamiento
- **`sortColumn`** (string): Columna para ordenar
  - Valores: `id`, `scheduledAt`, `status`, `priority`, `dateReceived`, `unitId`, `vendorId`, `userId`, `summary`
  - Por defecto: `id`
- **`sortDirection`** (string): Dirección del ordenamiento
  - Valores: `asc`, `desc`
  - Por defecto: `asc`

#### Filtros de Búsqueda
- **`search`** (string): Buscar por ID (número) o resumen, unit.name, vendor.name o user.name (string)
- **`updatedSince`** (string): Filtrar por fecha de actualización en formato ISO 8601

#### Filtros Específicos
- **`isScheduled`** (number): Filtrar por programado (0 o 1)
- **`unitId`** (string): Filtrar por ID de unidad (CSV)
- **`userId`** (number[]): Filtrar por ID de usuario
- **`nodeId`** (number): Filtrar por ID de nodo
- **`roleId`** (number): Filtrar por ID de rol
- **`ownerId`** (number): Filtrar por ID de propietario
- **`priority`** (number[]): Filtrar por prioridad (enteros)
- **`reservationId`** (number): Filtrar por ID de reservación
- **`vendorId`** (number): Filtrar por ID de proveedor
- **`status`** (string[]): Filtrar por estado
  - Valores: `open`, `not-started`, `in-progress`, `completed`, `processed`, 
    `vendor-not-start`, `vendor-assigned`, `vendor-declined`, 
    `vendor-completed`, `user-completed`, `cancelled`
- **`dateScheduled`** (string): Filtrar por fecha programada (ISO 8601)
- **`startDate`** (string): Filtrar por fecha de inicio (ISO 8601)
- **`endDate`** (string): Filtrar por fecha de fin (ISO 8601)
- **`problems`** (number[]): Filtrar por IDs de problemas

## Ejemplos de Uso

### Obtener todas las órdenes de trabajo
```json
{}
```

### Filtrar por estado y prioridad
```json
{
  "status": ["open", "in-progress"],
  "priority": [5, 3],
  "page": 1,
  "size": 50
}
```

### Buscar órdenes específicas
```json
{
  "search": "reparación",
  "unitId": "1,2,3",
  "sortColumn": "dateReceived",
  "sortDirection": "desc"
}
```

### Filtrar por fechas
```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "status": ["completed"]
}
```

### Obtener órdenes actualizadas recientemente
```json
{
  "updatedSince": "2024-01-15T00:00:00Z",
  "page": 1,
  "size": 100
}
```

### Filtrar por unidad y proveedor
```json
{
  "unitId": "5",
  "vendorId": 123,
  "status": ["vendor-assigned", "vendor-completed"]
}
```

### Buscar órdenes de alta prioridad
```json
{
  "priority": [5],
  "status": ["open", "in-progress"],
  "sortColumn": "priority",
  "sortDirection": "desc"
}
```

## Respuesta

La respuesta incluye:
- **`_embedded.workOrders`**: Array de órdenes de trabajo
- **`page`**: Página actual
- **`page_count`**: Total de páginas
- **`page_size`**: Tamaño de página
- **`total_items`**: Total de elementos
- **`_links`**: Enlaces de navegación (self, first, last, next, prev)

## Campos de Orden de Trabajo

Cada orden de trabajo incluye:

### Campos Básicos
- **`id`**: ID único de la orden
- **`dateReceived`**: Fecha de recepción (ISO 8601)
- **`priority`**: Prioridad (5=Alta, 3=Media, 1=Baja)
- **`status`**: Estado actual de la orden
- **`summary`**: Resumen del trabajo
- **`description`**: Descripción detallada del problema
- **`referenceNumber`**: Número de referencia

### Campos de Tiempo y Costo
- **`estimatedCost`**: Costo estimado del trabajo
- **`estimatedTime`**: Tiempo estimado en minutos
- **`actualTime`**: Tiempo real empleado en minutos
- **`dateCompleted`**: Fecha de finalización (ISO 8601)
- **`dateProcessed`**: Fecha de procesamiento (ISO 8601)

### Campos de Asignación
- **`userId`**: ID del usuario asignado
- **`vendorId`**: ID del proveedor asignado
- **`unitId`**: ID de la unidad afectada
- **`ownerId`**: ID del propietario
- **`reservationId`**: ID de la reservación relacionada
- **`assignees`**: Array de personas asignadas

### Campos de Seguimiento
- **`completedById`**: ID de quien completó el trabajo
- **`processedById`**: ID de quien procesó la orden
- **`workPerformed`**: Descripción del trabajo realizado

### Campos de Origen
- **`source`**: Fuente de la orden
- **`sourceName`**: Nombre de la fuente
- **`sourcePhone`**: Teléfono de la fuente
- **`blockCheckin`**: Si bloquea el check-in

### Campos de Problemas
- **`problems`**: Array de problemas asociados
  - `id`: ID del problema
  - `name`: Nombre del problema

### Campos de Auditoría
- **`createdAt`**: Fecha de creación (ISO 8601)
- **`createdBy`**: Usuario que creó la orden
- **`updatedAt`**: Fecha de última actualización (ISO 8601)
- **`updatedBy`**: Usuario que actualizó la orden

### Datos Relacionados (`_embedded`)
- **`unit`**: Información de la unidad
- **`vendor`**: Información del proveedor
- **`owner`**: Información del propietario

### Enlaces (`_links`)
- **`self`**: Enlace a la orden
- **`contacts`**: Enlace a contactos relacionados
- **`licences`**: Enlace a licencias relacionadas

## Estados de Órdenes de Trabajo

- **`open`**: Abierta - Orden creada pero no iniciada
- **`not-started`**: No iniciada - Orden asignada pero no comenzada
- **`in-progress`**: En progreso - Trabajo en curso
- **`completed`**: Completada - Trabajo finalizado
- **`processed`**: Procesada - Orden procesada administrativamente
- **`vendor-not-start`**: Proveedor no inició - Asignada a proveedor pero no comenzada
- **`vendor-assigned`**: Proveedor asignado - Asignada a proveedor
- **`vendor-declined`**: Proveedor declinó - Proveedor rechazó la orden
- **`vendor-completed`**: Proveedor completó - Proveedor finalizó el trabajo
- **`user-completed`**: Usuario completó - Usuario finalizó el trabajo
- **`cancelled`**: Cancelada - Orden cancelada

## Niveles de Prioridad

- **5**: Alta prioridad - Requiere atención inmediata
- **3**: Media prioridad - Atención normal
- **1**: Baja prioridad - Puede esperar

## Casos de Uso Comunes

### 1. Dashboard de Mantenimiento
```json
{
  "status": ["open", "in-progress"],
  "sortColumn": "priority",
  "sortDirection": "desc",
  "page": 1,
  "size": 20
}
```

### 2. Órdenes Pendientes por Unidad
```json
{
  "unitId": "10",
  "status": ["open", "not-started", "in-progress"]
}
```

### 3. Órdenes Completadas en un Período
```json
{
  "status": ["completed"],
  "startDate": "2024-01-01",
  "endDate": "2024-01-31"
}
```

### 4. Órdenes de Alta Prioridad
```json
{
  "priority": [5],
  "status": ["open", "in-progress", "not-started"]
}
```

### 5. Órdenes Asignadas a un Proveedor
```json
{
  "vendorId": 456,
  "status": ["vendor-assigned", "vendor-not-start"]
}
```

## Notas de Implementación

- La API soporta paginación completa con enlaces de navegación
- Los filtros pueden combinarse para búsquedas complejas
- El campo `search` permite búsqueda de texto libre
- Los arrays de filtros (como `status`, `priority`) permiten múltiples valores
- Las fechas deben estar en formato ISO 8601
- El campo `unitId` acepta valores CSV para múltiples unidades
- La respuesta incluye metadatos de paginación y enlaces de navegación
