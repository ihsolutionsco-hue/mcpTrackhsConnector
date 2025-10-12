# Get Reservation V2 - Documentación de API

## Descripción

La herramienta `get_reservation_v2` permite obtener información completa de una reserva específica desde la API TrackHS V2. Esta herramienta proporciona acceso a todos los datos de una reserva individual, incluyendo información financiera detallada, datos embebidos y metadatos.

## Endpoint de la API

- **Método**: `GET`
- **Path**: `/v2/pms/reservations/{reservationId}`
- **Versión**: API V2

## Parámetros

### Parámetros Requeridos

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `reservation_id` | `integer` | ID único de la reserva a obtener |

### Validaciones

- `reservation_id` debe ser un entero positivo mayor que 0
- El ID debe corresponder a una reserva existente en el sistema

## Respuesta

La herramienta retorna un objeto completo de reserva con la siguiente estructura:

### Datos Básicos

```json
{
  "id": 12345,
  "alternates": ["ALT123", "ALT456"],
  "currency": "USD",
  "unitId": 789,
  "status": "Confirmed",
  "arrivalDate": "2024-01-15",
  "departureDate": "2024-01-20",
  "nights": 5,
  "createdAt": "2024-01-01T10:00:00Z",
  "updatedAt": "2024-01-10T15:30:00Z"
}
```

### Información Financiera

```json
{
  "guestBreakdown": {
    "grossRent": "1000.00",
    "discount": "50.00",
    "netRent": "950.00",
    "totalTaxes": "95.00",
    "grandTotal": "1045.00",
    "balance": "0.00"
  },
  "ownerBreakdown": {
    "grossRent": "1000.00",
    "netRevenue": "850.00"
  },
  "securityDeposit": {
    "required": "200.00",
    "remaining": 200
  }
}
```

### Datos Embebidos

```json
{
  "_embedded": {
    "unit": {
      "id": 789,
      "name": "Casa de Playa",
      "streetAddress": "123 Ocean Drive",
      "maxOccupancy": 8,
      "bedrooms": 3,
      "fullBathrooms": 2
    },
    "contact": {
      "id": 456,
      "name": "Juan Pérez",
      "primaryEmail": "juan@email.com",
      "cellPhone": "+1234567890"
    },
    "guaranteePolicy": {
      "id": 1,
      "name": "Política Estándar",
      "type": "Guarantee"
    },
    "cancellationPolicy": {
      "id": 2,
      "name": "Cancelación Flexible",
      "chargeAs": "fee"
    }
  }
}
```

## Casos de Uso

### 1. Verificar Estado de Reserva

```python
# Obtener estado actual de una reserva
get_reservation_v2(reservation_id=12345)
```

### 2. Análisis Financiero

```python
# Analizar información financiera de una reserva
get_reservation_v2(reservation_id=12345)
# Usar templates para formatear desglose financiero
```

### 3. Información de Contacto

```python
# Obtener datos del huésped y contacto
get_reservation_v2(reservation_id=12345)
# Extraer información de _embedded.contact
```

### 4. Validación de Políticas

```python
# Verificar políticas de garantía y cancelación
get_reservation_v2(reservation_id=12345)
# Revisar _embedded.guaranteePolicy y _embedded.cancellationPolicy
```

## Templates Disponibles

### 1. Resumen de Reserva

```python
# Usar template para resumen ejecutivo
reservation_summary_template(reservation_data)
```

### 2. Desglose Financiero

```python
# Usar template para análisis financiero
financial_breakdown_template(reservation_data)
```

### 3. Información de Huésped

```python
# Usar template para datos del huésped
guest_information_template(reservation_data)
```

### 4. Políticas y Acuerdos

```python
# Usar template para políticas
policies_template(reservation_data)
```

### 5. Información de Unidad

```python
# Usar template para datos de la unidad
unit_information_template(reservation_data)
```

## Prompts Disponibles

### 1. Obtener Detalles Completos

```python
create_get_reservation_prompt(reservation_id=12345)
```

### 2. Análisis Financiero

```python
create_reservation_analysis_prompt(reservation_id=12345)
```

### 3. Resumen Ejecutivo

```python
create_reservation_summary_prompt(reservation_id=12345)
```

## Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 401 | No autorizado | Verificar credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD |
| 403 | Prohibido | Verificar permisos de acceso a la reserva |
| 404 | No encontrado | Verificar que el ID de reserva sea correcto |
| 500 | Error interno | Reintentar más tarde o contactar soporte |

## Ejemplos de Uso

### Ejemplo 1: Obtener Reserva Básica

```python
# Obtener información básica de una reserva
result = get_reservation_v2(reservation_id=12345)

# Extraer información clave
reservation_id = result["id"]
status = result["status"]
arrival_date = result["arrivalDate"]
departure_date = result["departureDate"]
total = result["guestBreakdown"]["grandTotal"]
```

### Ejemplo 2: Análisis Financiero

```python
# Obtener reserva y analizar información financiera
result = get_reservation_v2(reservation_id=12345)

# Usar template para formatear desglose financiero
financial_summary = financial_breakdown_template(result)
print(financial_summary)
```

### Ejemplo 3: Información de Contacto

```python
# Obtener datos del huésped
result = get_reservation_v2(reservation_id=12345)

# Extraer información de contacto
contact = result["_embedded"]["contact"]
guest_name = contact["name"]
guest_email = contact["primaryEmail"]
guest_phone = contact["cellPhone"]
```

### Ejemplo 4: Verificar Políticas

```python
# Obtener reserva y verificar políticas
result = get_reservation_v2(reservation_id=12345)

# Verificar política de garantía
guarantee_policy = result["_embedded"]["guaranteePolicy"]
policy_name = guarantee_policy["name"]
policy_type = guarantee_policy["type"]

# Verificar política de cancelación
cancellation_policy = result["_embedded"]["cancellationPolicy"]
cancel_charge = cancellation_policy["chargeAs"]
```

## Mejores Prácticas

### 1. Validación de ID

```python
# Siempre validar que el ID sea válido antes de hacer la petición
if reservation_id > 0:
    result = get_reservation_v2(reservation_id=reservation_id)
else:
    print("ID de reserva inválido")
```

### 2. Manejo de Errores

```python
try:
    result = get_reservation_v2(reservation_id=12345)
except ValidationError as e:
    print(f"Error de validación: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
```

### 3. Uso de Templates

```python
# Usar templates para formatear respuestas
result = get_reservation_v2(reservation_id=12345)

# Aplicar template de resumen
summary = reservation_summary_template(result)
print(summary)
```

### 4. Extracción de Datos Embebidos

```python
# Acceder a datos embebidos de forma segura
result = get_reservation_v2(reservation_id=12345)
embedded = result.get("_embedded", {})

# Verificar que los datos existan antes de acceder
if "contact" in embedded:
    contact = embedded["contact"]
    guest_name = contact.get("name", "N/A")
```

## Limitaciones

1. **ID Requerido**: El parámetro `reservation_id` es obligatorio
2. **Permisos**: Requiere permisos de acceso a la reserva específica
3. **Disponibilidad**: Depende de la disponibilidad de la API TrackHS
4. **Rate Limiting**: Sujeto a límites de velocidad de la API

## Recursos Relacionados

- [Search Reservations V2](./search-reservations-v2.md)
- [TrackHS API Documentation](https://docs.trackhs.com)
- [Schema de Reserva Individual](../schema/reservation-detail-v2.md)

## Soporte

Para soporte técnico o preguntas sobre esta herramienta:

- **Email**: support@trackhs.com
- **Documentación**: https://docs.trackhs.com
- **Issues**: Reportar problemas en el repositorio del proyecto
