# Get Folio API

## Descripción

La herramienta `get_folio` permite obtener un folio específico por ID desde la API de TrackHS. Un folio es un registro financiero que puede ser de tipo "guest" (huésped) o "master" (maestro), y contiene información sobre balances, comisiones, transacciones y datos embebidos de contacto, compañía y agente de viajes.

## Endpoint

```
GET /pms/folios/{folioId}
```

## Parámetros

### Parámetros de Entrada

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `folio_id` | string | Sí | ID único del folio (debe ser un entero positivo) |

### Ejemplo de Uso

```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "12345"
  }
}
```

## Respuesta

### Estructura de Respuesta

La respuesta incluye todos los campos del folio con datos embebidos:

```json
{
  "id": 12345,
  "status": "open",
  "type": "guest",
  "currentBalance": 150.00,
  "realizedBalance": 100.00,
  "startDate": "2024-01-15",
  "endDate": "2024-01-20",
  "closedDate": null,
  "contactId": 1,
  "companyId": 1,
  "reservationId": 37165851,
  "travelAgentId": 1,
  "name": "Guest Folio - John Doe",
  "taxEmpty": false,
  "hasException": false,
  "exceptionMessage": null,
  "agentCommission": 10.00,
  "ownerCommission": 5.00,
  "ownerRevenue": 500.00,
  "checkInDate": "2024-01-15",
  "checkOutDate": "2024-01-20",
  "masterFolioRuleId": null,
  "masterFolioId": null,
  "createdAt": "2024-01-10T10:00:00Z",
  "updatedAt": "2024-01-10T10:00:00Z",
  "createdBy": "system",
  "updatedBy": "system",
  "_embedded": {
    "contact": {
      "id": 1,
      "firstName": "John",
      "lastName": "Doe",
      "primaryEmail": "john@example.com",
      "homePhone": "+1234567890",
      "country": "US",
      "isVip": false,
      "isBlacklist": false
    },
    "travelAgent": {
      "id": 1,
      "type": "agent",
      "name": "Travel Agency Inc",
      "isActive": true,
      "email": "agent@example.com",
      "phone": "+1234567890"
    },
    "company": {
      "id": 1,
      "type": "company",
      "name": "Property Management Co",
      "isActive": true,
      "email": "company@example.com",
      "phone": "+1234567890"
    }
  },
  "_links": {
    "self": {
      "href": "/api/pms/folios/12345"
    },
    "logs": {
      "href": "/api/pms/folios/12345/logs"
    }
  }
}
```

### Campos Principales

#### Campos Requeridos
- `id`: ID único del folio
- `status`: Estado del folio ("open" o "closed")

#### Campos Opcionales Básicos
- `type`: Tipo de folio ("guest" o "master")
- `currentBalance`: Balance actual del folio
- `realizedBalance`: Balance realizado del folio
- `startDate`: Fecha de inicio (ISO 8601)
- `endDate`: Fecha de fin (ISO 8601)
- `closedDate`: Fecha de cierre (ISO 8601)
- `contactId`: ID del contacto
- `companyId`: ID de la compañía
- `reservationId`: ID de la reserva
- `travelAgentId`: ID del agente de viajes
- `name`: Nombre del folio
- `taxEmpty`: Si está exento de impuestos

#### Campos de Excepción
- `hasException`: Si tiene excepción
- `exceptionMessage`: Mensaje de excepción

#### Campos Financieros (visibles para ciertos tipos)
- `agentCommission`: Comisión del agente
- `ownerCommission`: Comisión del propietario
- `ownerRevenue`: Ingresos del propietario
- `checkInDate`: Fecha de check-in
- `checkOutDate`: Fecha de check-out

#### Campos de Folio Maestro
- `masterFolioRuleId`: ID de regla de folio maestro
- `masterFolioId`: ID de folio maestro

#### Metadatos
- `createdAt`: Fecha de creación
- `updatedAt`: Fecha de actualización
- `createdBy`: Creado por
- `updatedBy`: Actualizado por

#### Objetos Embebidos
- `_embedded`: Objetos embebidos (contact, travelAgent, company, masterFolioRule, masterFolio)
- `_links`: Enlaces relacionados

## Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 401 | No autorizado | Verificar credenciales de autenticación |
| 403 | Prohibido | Verificar permisos de acceso a folios |
| 404 | Folio no encontrado | Verificar que el ID del folio sea correcto |
| 500 | Error interno del servidor | Contactar soporte técnico |

## Casos de Uso Comunes

### 1. Verificar Balance de Folio
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "12345"
  }
}
```
**Uso**: Obtener el balance actual y realizado de un folio específico.

### 2. Análisis Financiero
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "67890"
  }
}
```
**Uso**: Analizar comisiones, ingresos y datos financieros de un folio.

### 3. Auditoría de Transacciones
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "11111"
  }
}
```
**Uso**: Revisar el historial de transacciones y cambios en un folio.

### 4. Información de Excepciones
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "22222"
  }
}
```
**Uso**: Verificar si un folio tiene excepciones y obtener detalles.

### 5. Datos de Contacto y Compañía
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "33333"
  }
}
```
**Uso**: Obtener información completa del contacto, agente de viajes y compañía asociados.

## Tipos de Folio

### Folio Guest (Huésped)
- Asociado a una reserva específica
- Contiene información del huésped
- Puede tener datos financieros detallados
- Incluye fechas de check-in/check-out

### Folio Master (Maestro)
- Folio consolidado para múltiples transacciones
- Puede tener reglas de folio maestro
- Generalmente para períodos específicos
- Puede incluir excepciones y mensajes especiales

## Notas Importantes

1. **Validación de ID**: El `folio_id` debe ser un string que represente un entero positivo válido.

2. **Campos Opcionales**: Muchos campos son opcionales y pueden estar ausentes según el tipo de folio.

3. **Datos Embebidos**: Los objetos embebidos (`_embedded`) contienen información detallada de contactos, compañías y reglas.

4. **Formato de Fechas**: Todas las fechas están en formato ISO 8601.

5. **Precisión Financiera**: Los valores financieros están en formato numérico para cálculos precisos.

6. **Manejo de Errores**: La herramienta proporciona mensajes de error descriptivos para facilitar la resolución de problemas.

## Ejemplos de Respuesta por Tipo

### Folio Guest
```json
{
  "id": 12345,
  "status": "open",
  "type": "guest",
  "currentBalance": 150.00,
  "realizedBalance": 100.00,
  "contactId": 1,
  "reservationId": 37165851,
  "checkInDate": "2024-01-15",
  "checkOutDate": "2024-01-20"
}
```

### Folio Master
```json
{
  "id": 67890,
  "status": "closed",
  "type": "master",
  "realizedBalance": 2500.00,
  "hasException": true,
  "exceptionMessage": "Payment processing delay",
  "masterFolioRuleId": 1
}
```

### Folio Mínimo
```json
{
  "id": 11111,
  "status": "open"
}
```
