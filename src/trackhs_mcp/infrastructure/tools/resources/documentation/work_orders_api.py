"""
Documentation resources para Work Orders API
Información concisa de la documentación de la API de órdenes de trabajo
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_work_orders_api_documentation(mcp, api_client: "ApiClientPort"):
    """Registra la documentación de Work Orders API"""

    @mcp.resource(
        "trackhs://docs/work-orders-api",
        name="Work Orders API Documentation",
        description="Essential documentation for Maintenance Work Orders API",
        mime_type="text/plain",
    )
    async def work_orders_api_docs() -> str:
        """Documentación concisa de Work Orders API"""
        return """# TrackHS Work Orders API - Create Maintenance Work Order

## Endpoint
- **URL**: `POST /pms/maintenance/work-orders`
- **Versión**: 1.0
- **Autenticación**: Basic Auth

## Descripción
Crea nuevas órdenes de trabajo de mantenimiento en TrackHS con campos requeridos y opcionales.
Ideal para manejar llamadas de servicio al cliente, emergencias, mantenimiento preventivo y reparaciones.
Soporta prioridades textuales intuitivas que se mapean automáticamente a valores numéricos de la API.

## Campos Requeridos

### dateReceived (string, required)
- Fecha de recepción de la orden
- Formato: ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)
- Ejemplo: "2024-01-15" o "2024-01-15T10:30:00Z"

### priority (string, required)
- Prioridad de la orden usando valores textuales intuitivos
- Valores válidos:
  - "trivial": Problemas menores, cosméticos (mapea a 1)
  - "low": Mantenimiento rutinario (mapea a 1)
  - "medium": Reparaciones estándar (mapea a 3)
  - "high": Problemas de comodidad del huésped (mapea a 5)
  - "critical": Emergencias que afectan habitabilidad (mapea a 5)

### status (string, required)
- Estado de la orden
- Valores válidos:
  - "open": Abierta
  - "not-started": No iniciada
  - "in-progress": En progreso
  - "completed": Completada
  - "processed": Procesada
  - "vendor-assigned": Asignada a proveedor
  - "vendor-accepted": Aceptada por proveedor
  - "vendor-rejected": Rechazada por proveedor
  - "vendor-completed": Completada por proveedor
  - "cancelled": Cancelada

### summary (string, required)
- Resumen breve de la orden de trabajo
- Ejemplo: "Reparar aire acondicionado unidad 101"

### estimatedCost (number, required)
- Costo estimado de la reparación
- Debe ser >= 0
- Ejemplo: 150.00

### estimatedTime (integer, required)
- Tiempo estimado en minutos
- Debe ser > 0
- Ejemplo: 120 (2 horas)

## Campos Opcionales

### dateScheduled (string, optional)
- Fecha programada para realizar el trabajo
- Formato: ISO 8601
- Ejemplo: "2024-01-16T09:00:00Z"

### userId (integer, optional)
- ID del usuario responsable
- Debe ser > 0

### vendorId (integer, optional)
- ID del proveedor asignado
- Debe ser > 0

### unitId (integer, optional)
- ID de la unidad relacionada
- Debe ser > 0

### reservationId (integer, optional)
- ID de la reserva relacionada
- Debe ser > 0

### referenceNumber (string, optional)
- Número de referencia externo
- Ejemplo: "WO-2024-001"

### description (string, optional)
- Descripción detallada del problema
- Ejemplo: "El aire acondicionado no enfría adecuadamente"

### workPerformed (string, optional)
- Descripción del trabajo realizado
- Se usa cuando el status es "completed"

### source (string, optional)
- Fuente de la orden para tracking de servicio al cliente
- Valores comunes:
  - "Guest Request": Problema reportado por huésped
  - "Inspection": Inspección de rutina
  - "Preventive Maintenance": Mantenimiento programado
  - "Emergency": Emergencia reportada

### sourceName (string, optional)
- Nombre de la persona que reporta el problema
- Ejemplo: "Maria Garcia" (para solicitudes de huéspedes)
- Ejemplo: "Juan Pérez" (para personal interno)

### sourcePhone (string, optional)
- Teléfono de contacto de quien reporta
- Incluir código de país
- Ejemplo: "+1234567890" (US), "+34612345678" (España)

### actualTime (integer, optional)
- Tiempo real utilizado en minutos
- Debe ser > 0
- Se usa cuando el trabajo está completado

### blockCheckin (boolean, optional)
- Si debe bloquear el check-in de la unidad
- true: Bloquea check-in
- false: No bloquea check-in
- Usar true solo cuando sea absolutamente necesario

## Ejemplos de Uso

### Creación Básica
```json
{
  "dateReceived": "2024-01-15",
  "priority": 5,
  "status": "open",
  "summary": "Reparar aire acondicionado",
  "estimatedCost": 150.00,
  "estimatedTime": 120
}
```

### Creación Completa
```json
{
  "dateReceived": "2024-01-15T10:30:00Z",
  "priority": 3,
  "status": "in-progress",
  "summary": "Mantenimiento preventivo HVAC",
  "estimatedCost": 200.50,
  "estimatedTime": 180,
  "dateScheduled": "2024-01-16T09:00:00Z",
  "unitId": 123,
  "vendorId": 456,
  "description": "Mantenimiento programado del sistema HVAC",
  "source": "Preventive Maintenance",
  "sourceName": "Juan Pérez",
  "sourcePhone": "+1234567890",
  "blockCheckin": true
}
```

### Solicitud de Huésped
```json
{
  "dateReceived": "2024-01-15T14:00:00Z",
  "priority": 5,
  "status": "open",
  "summary": "Fuga de agua en baño principal",
  "estimatedCost": 100.00,
  "estimatedTime": 60,
  "unitId": 101,
  "reservationId": 37152796,
  "description": "Fuga reportada por huésped en lavamanos",
  "source": "Guest Request",
  "sourceName": "Maria Garcia",
  "sourcePhone": "+1987654321",
  "blockCheckin": false
}
```

## Estructura de Respuesta

### Éxito
```json
{
  "success": true,
  "work_order": {
    "id": 12345,
    "dateReceived": "2024-01-15",
    "priority": 5,
    "status": "open",
    "summary": "Reparar aire acondicionado",
    "estimatedCost": 150.00,
    "estimatedTime": 120,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  },
  "message": "Orden de trabajo creada exitosamente"
}
```

### Error
```json
{
  "success": false,
  "error": "Datos inválidos",
  "message": "La prioridad debe ser 1 (Baja), 3 (Media) o 5 (Alta)",
  "work_order": null
}
```

## Códigos de Error

- **400**: Bad Request - Datos inválidos
- **401**: Unauthorized - Credenciales inválidas
- **403**: Forbidden - Permisos insuficientes
- **500**: Internal Server Error - Error temporal del servidor

## Mejores Prácticas

1. **Fechas**: Usar formato ISO 8601 completo para precisión
2. **Prioridades**: Usar prioridad 5 solo para emergencias
3. **Validación**: Validar IDs antes de enviar
4. **Descripción**: Proporcionar descripción detallada
5. **Contacto**: Incluir información de contacto en source*
6. **BlockCheckin**: Usar true solo cuando sea necesario
7. **Estimaciones**: Proporcionar estimaciones realistas
8. **Referencias**: Usar referenceNumber para tracking

## Casos de Uso de Servicio al Cliente

### Llamada de Huésped - AC No Funciona
```json
{
  "dateReceived": "2024-01-15T14:00:00Z",
  "priority": "high",
  "status": "open",
  "summary": "AC no funciona en habitación principal",
  "estimatedCost": 200.00,
  "estimatedTime": 90,
  "unitId": 101,
  "reservationId": 37152796,
  "description": "Huésped reporta que el aire acondicionado no enfría la habitación",
  "source": "Guest Request",
  "sourceName": "Maria Garcia",
  "sourcePhone": "+1234567890"
}
```

### Emergencia - Fuga de Agua
```json
{
  "dateReceived": "2024-01-15T20:30:00Z",
  "priority": "critical",
  "status": "in-progress",
  "summary": "Fuga de agua en baño principal",
  "estimatedCost": 150.00,
  "estimatedTime": 60,
  "unitId": 205,
  "blockCheckin": true,
  "source": "Guest Request",
  "sourceName": "John Smith",
  "sourcePhone": "+1987654321",
  "description": "Fuga importante que requiere atención inmediata"
}
```

### Problema de WiFi
```json
{
  "dateReceived": "2024-01-15T10:00:00Z",
  "priority": "medium",
  "status": "open",
  "summary": "WiFi lento en toda la unidad",
  "estimatedCost": 50.00,
  "estimatedTime": 30,
  "unitId": 103,
  "source": "Guest Request",
  "sourceName": "Ana Rodriguez",
  "sourcePhone": "+34612345678"
}
```

## Casos de Uso Comunes

### Mantenimiento Preventivo
```json
{
  "dateReceived": "2024-01-15",
  "priority": 3,
  "status": "not-started",
  "summary": "Inspección mensual HVAC",
  "estimatedCost": 0,
  "estimatedTime": 30,
  "dateScheduled": "2024-01-20T10:00:00Z",
  "source": "Preventive Maintenance"
}
```

### Emergencia
```json
{
  "dateReceived": "2024-01-15T22:30:00Z",
  "priority": 5,
  "status": "open",
  "summary": "Emergencia: Sin agua caliente",
  "estimatedCost": 300.00,
  "estimatedTime": 120,
  "unitId": 205,
  "reservationId": 12345,
  "blockCheckin": true,
  "source": "Guest Request"
}
```

### Con Proveedor Externo
```json
{
  "dateReceived": "2024-01-15",
  "priority": 3,
  "status": "vendor-assigned",
  "summary": "Reemplazo de alfombra",
  "estimatedCost": 500.00,
  "estimatedTime": 240,
  "vendorId": 789,
  "unitId": 103,
  "referenceNumber": "VENDOR-2024-001"
}
```
"""
