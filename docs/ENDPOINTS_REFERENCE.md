# 📡 Referencia de Endpoints TrackHS

## 🌐 Configuración Base

**Base URL**: `https://ihmvacations.trackhs.com` (sin `/api` al final)

### Variables de Entorno
```bash
TRACKHS_API_URL=https://ihmvacations.trackhs.com
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

**⚠️ IMPORTANTE**: La base URL NO debe incluir `/api` al final. Los endpoints incluyen la ruta completa con `/api/`.

---

## ✅ Endpoints Implementados

### 1. 🔍 Search Reservations (API V2)
- **Método**: `GET`
- **Endpoint**: `/api/v2/pms/reservations`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/v2/pms/reservations`
- **Herramienta MCP**: `search_reservations`
- **Archivo**: `src/trackhs_mcp/application/use_cases/search_reservations.py`

**Parámetros de búsqueda**:
- `page` (0-based indexing)
- `size` (1-100)
- `search` (texto libre)
- `status` (Hold, Confirmed, Cancelled, Checked In, Checked Out)
- `arrivalStart`, `arrivalEnd`
- `departureStart`, `departureEnd`
- `bookedStart`, `bookedEnd`
- `unitId`, `nodeId`, `contactId`
- Y más...

---

### 2. 📄 Get Reservation (API V2)
- **Método**: `GET`
- **Endpoint**: `/api/v2/pms/reservations/{reservationId}`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/v2/pms/reservations/12345`
- **Herramienta MCP**: `get_reservation`
- **Archivo**: `src/trackhs_mcp/application/use_cases/get_reservation.py`

**Parámetros**:
- `reservationId` (requerido): ID de la reserva

**Respuesta**: Objeto completo de reserva con datos embebidos (unit, contact, policies, etc.)

---

### 3. 💰 Get Folio
- **Método**: `GET`
- **Endpoint**: `/api/pms/folios/{folioId}`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/pms/folios/12345`
- **Herramienta MCP**: `get_folio`
- **Archivo**: `src/trackhs_mcp/application/use_cases/get_folio.py`

**Parámetros**:
- `folioId` (requerido): ID del folio

**Respuesta**: Objeto completo de folio con balances, comisiones, y datos embebidos

---

### 4. 🏠 Search Units (Channel API)
- **Método**: `GET`
- **Endpoint**: `/api/pms/units`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/pms/units`
- **Herramienta MCP**: `search_units`
- **Archivo**: `src/trackhs_mcp/application/use_cases/search_units.py`

**Parámetros de búsqueda**:
- `page` (1-based indexing)
- `size` (1-25)
- `search` (texto libre)
- `bedrooms`, `minBedrooms`, `maxBedrooms`
- `bathrooms`, `minBathrooms`, `maxBathrooms`
- `petsFriendly` (0/1)
- `isAccessible` (0/1)
- `arrival`, `departure` (disponibilidad)
- `unitStatus` (clean, dirty, occupied, inspection, inprogress)
- Y más...

**Respuesta**: Lista de unidades con descripciones, imágenes, rates, amenidades, y calendario de disponibilidad

---

### 5. 🎯 Search Amenities (Channel API)
- **Método**: `GET`
- **Endpoint**: `/api/pms/units/amenities`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/pms/units/amenities`
- **Herramienta MCP**: `search_amenities`
- **Archivo**: `src/trackhs_mcp/application/use_cases/search_amenities.py`

**Parámetros de búsqueda**:
- `page` (1-based indexing)
- `size` (1-1000)
- `search` (buscar en ID y nombre)
- `groupId` (filtrar por grupo de amenidades)
- `isPublic` (0=privado, 1=público)
- `publicSearchable` (0=no buscable, 1=buscable)
- `isFilterable` (0=no filtrable, 1=filtrable)
- `sortColumn` (id, order, isPublic, publicSearchable, isFilterable, createdAt)
- `sortDirection` (asc, desc)

**Respuesta**: Lista de amenidades con metadatos y grupos

---

### 6. 🔧 Create Maintenance Work Order
- **Método**: `POST`
- **Endpoint**: `/api/pms/maintenance/work-orders`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/pms/maintenance/work-orders`
- **Herramienta MCP**: `create_maintenance_work_order`
- **Archivo**: `src/trackhs_mcp/application/use_cases/create_work_order.py`

**Campos Requeridos**:
- `dateReceived` (ISO 8601: YYYY-MM-DD)
- `priority` (1=Low, 3=Medium, 5=High)
- `status` (open, not-started, in-progress, completed, etc.)
- `summary` (resumen del trabajo)
- `estimatedCost` (>= 0)
- `estimatedTime` (minutos, > 0)

**Campos Opcionales**:
- `dateScheduled`
- `userId`
- `vendorId`
- `unitId`
- `reservationId`
- `referenceNumber`
- `description`
- `workPerformed`
- `source` (Guest Request, Inspection, etc.)
- `sourceName`
- `sourcePhone`
- `actualTime`
- `blockCheckin`

**Ejemplo**:
```json
{
  "dateReceived": "2024-01-15",
  "priority": 5,
  "status": "open",
  "summary": "Reparar aire acondicionado",
  "estimatedCost": 150.00,
  "estimatedTime": 120,
  "unitId": 123
}
```

---

### 7. 🧹 Create Housekeeping Work Order
- **Método**: `POST`
- **Endpoint**: `/api/pms/housekeeping/work-orders`
- **URL Completa**: `https://ihmvacations.trackhs.com/api/pms/housekeeping/work-orders`
- **Herramienta MCP**: `create_housekeeping_work_order`
- **Archivo**: `src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py` (línea 548)

**Campos Requeridos**:
- `scheduledAt` (ISO 8601: YYYY-MM-DD HH:MM:SS)
- **Exactamente uno de**:
  - `unitId` (ID de unidad)
  - `unitBlockId` (ID de bloque de unidades)
- **Exactamente uno de**:
  - `isInspection` (true/false)
  - `cleanTypeId` (ID de tipo de limpieza)

**Campos Opcionales**:
- `userId` (ID de usuario asignado)
- `vendorId` (ID de proveedor)
- `reservationId` (ID de reserva relacionada)
- `isTurn` (true/false)
- `chargeOwner` (true/false)
- `comments` (comentarios adicionales)
- `cost` (costo de la orden)

**Ejemplo**:
```json
{
  "scheduledAt": "2024-01-15 10:00:00",
  "unitId": 123,
  "cleanTypeId": 5,
  "userId": 789,
  "comments": "Limpieza de salida"
}
```

---

## 🔐 Autenticación

Todos los endpoints requieren **Basic Authentication**:

```http
Authorization: Basic base64(username:password)
```

Las credenciales se configuran mediante variables de entorno:
- `TRACKHS_USERNAME`
- `TRACKHS_PASSWORD`

---

## ⚙️ Configuración de Timeout

```bash
# Timeout general (default: 60 segundos)
TRACKHS_TIMEOUT=60

# Timeout para búsquedas complejas (default: 120 segundos)
TRACKHS_SEARCH_TIMEOUT=120
```

---

## 📊 Límites y Paginación

### Search Reservations
- **Indexing**: 0-based (page=0 es la primera página)
- **Size máximo**: 100 items por página
- **Total máximo**: 10,000 resultados

### Search Units
- **Indexing**: 1-based (page=1 es la primera página)
- **Size máximo**: 25 items por página
- **Total máximo**: 10,000 resultados

### Search Amenities
- **Indexing**: 1-based (page=1 es la primera página)
- **Size máximo**: 1,000 items por página
- **Total máximo**: 10,000 resultados

---

## 🚨 Códigos de Error Comunes

| Código | Descripción | Acción |
|--------|-------------|--------|
| 400 | Bad Request | Verificar parámetros de entrada |
| 401 | Unauthorized | Verificar credenciales |
| 403 | Forbidden | Verificar permisos de la cuenta |
| 404 | Not Found | Verificar que el ID exista |
| 422 | Unprocessable Entity | Verificar validación de datos |
| 500 | Internal Server Error | Reintentar más tarde |

---

## 🎯 Estructura de URLs

### Base URL
```
https://ihmvacations.trackhs.com
```

### Todos los endpoints incluyen `/api/` en su ruta:
```
/api/v2/pms/reservations
/api/pms/units
/api/pms/folios/{id}
/api/pms/maintenance/work-orders
/api/pms/housekeeping/work-orders
/api/pms/units/amenities
```

### Ejemplo de URL completa:
```
Base URL: https://ihmvacations.trackhs.com
Endpoint: /api/v2/pms/reservations
Resultado: https://ihmvacations.trackhs.com/api/v2/pms/reservations
```

---

## 📚 Referencias

- **Configuración Base**: `src/trackhs_mcp/infrastructure/adapters/config.py`
- **API Client**: `src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py`
- **Use Cases**: `src/trackhs_mcp/application/use_cases/`
- **Tools Registry**: `src/trackhs_mcp/infrastructure/tools/registry.py`

---

## 🔗 URLs de Prueba

### Ejemplos de URLs Completas

#### Búsqueda de Reservas
```
GET https://ihmvacations.trackhs.com/api/v2/pms/reservations?page=0&size=10&status=Confirmed
```

#### Obtener Reserva Específica
```
GET https://ihmvacations.trackhs.com/api/v2/pms/reservations/37152796
```

#### Búsqueda de Unidades
```
GET https://ihmvacations.trackhs.com/api/pms/units?page=1&size=10&bedrooms=3&petsFriendly=1
```

#### Búsqueda de Amenidades
```
GET https://ihmvacations.trackhs.com/api/pms/units/amenities?page=1&size=25&isPublic=1
```

#### Crear Work Order de Mantenimiento
```
POST https://ihmvacations.trackhs.com/api/pms/maintenance/work-orders
Content-Type: application/json

{
  "dateReceived": "2024-01-15",
  "priority": 5,
  "status": "open",
  "summary": "Reparar aire acondicionado",
  "estimatedCost": 150.00,
  "estimatedTime": 120,
  "unitId": 123
}
```

---

**Última actualización**: 24 de octubre, 2025
**Versión API**: V1 y V2
**Base URL**: `https://ihmvacations.trackhs.com` (sin `/api`)
