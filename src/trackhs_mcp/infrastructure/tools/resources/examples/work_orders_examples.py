"""
Examples resources para Work Orders
Ejemplos de uso para la herramienta create_maintenance_work_order
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_work_orders_examples(mcp, api_client: "ApiClientPort"):
    """Registra los ejemplos de work orders"""

    @mcp.resource(
        "trackhs://examples/work-orders",
        name="Work Orders Examples",
        description="Common work order creation examples",
        mime_type="text/plain",
    )
    async def work_orders_examples() -> str:
        """Ejemplos de creación de órdenes de trabajo"""
        return """# TrackHS Work Orders Examples

## ¿Qué son las Órdenes de Trabajo?

Las **órdenes de trabajo** son solicitudes de mantenimiento, reparación o servicios para propiedades. TrackHS las organiza por:

- **Prioridad**: Urgencia del trabajo usando prioridades textuales intuitivas (trivial, low, medium, high, critical)
- **Estado**: Progreso del trabajo (open, in-progress, completed, etc.)
- **Tipo**: Mantenimiento, housekeeping, emergencias
- **Asignación**: Usuario interno o proveedor externo
- **Servicio al Cliente**: Ideal para manejar llamadas de huéspedes, emergencias y mantenimiento

## Para Principiantes - Primeros Pasos

### 1. Mi Primera Orden (Más Simple)
```python
# Crear una orden básica de mantenimiento usando prioridades textuales
create_maintenance_work_order(
    date_received="2024-01-15",
    priority="medium",
    status="open",
    summary="Reparar aire acondicionado",
    estimated_cost=150.00,
    estimated_time=120
)
```
**¿Qué hace?** Crea una orden de mantenimiento básica usando prioridad textual intuitiva.
**¿Cuándo usarlo?** Para solicitudes simples de mantenimiento reportadas por huéspedes.

### 2. Orden con Unidad Específica
```python
# Orden relacionada con una unidad específica - caso típico de servicio al cliente
create_maintenance_work_order(
    date_received="2024-01-15",
    priority="high",
    status="open",
    summary="Fuga de agua en baño",
    estimated_cost=100.00,
    estimated_time=60,
    unit_id=101,
    source="Guest Request",
    source_name="Maria Garcia",
    source_phone="+1234567890"
)
```
**¿Qué hace?** Crea una orden para una unidad específica con información del huésped.
**¿Cuándo usarlo?** Cuando un huésped reporta un problema en su unidad.

### 3. Orden de Emergencia
```python
# Orden de emergencia que bloquea check-in - caso crítico de servicio al cliente
create_maintenance_work_order(
    date_received="2024-01-15T22:30:00Z",
    priority="critical",
    status="in-progress",
    summary="Emergencia: Sin agua caliente",
    estimated_cost=300.00,
    estimated_time=120,
    unit_id=205,
    block_checkin=1,
    source="Guest Request",
    source_name="John Smith",
    source_phone="+1987654321",
    description="Huésped reporta falta completa de agua caliente en toda la unidad"
)
```
**¿Qué hace?** Crea una orden de emergencia que impide nuevos check-ins.
**¿Cuándo usarlo?** Para problemas críticos que afectan la habitabilidad y requieren atención inmediata.

## Tabla de Estados Válidos

| Estado | Descripción | Cuándo Usarlo |
|--------|-------------|---------------|
| `"open"` | Orden abierta, pendiente de asignación | Nueva orden sin asignar |
| `"not-started"` | Orden asignada pero no iniciada | Orden programada para el futuro |
| `"in-progress"` | Trabajo en progreso | Orden siendo ejecutada |
| `"completed"` | Trabajo completado | Orden terminada exitosamente |
| `"processed"` | Orden procesada/cerrada | Orden finalizada administrativamente |
| `"vendor-assigned"` | Asignada a proveedor externo | Trabajo para terceros |
| `"vendor-accepted"` | Proveedor aceptó la orden | Proveedor confirmó el trabajo |
| `"vendor-rejected"` | Proveedor rechazó la orden | Proveedor no puede hacer el trabajo |
| `"vendor-completed"` | Proveedor completó el trabajo | Trabajo terminado por terceros |
| `"cancelled"` | Orden cancelada | Trabajo ya no es necesario |

## Tabla de Prioridades Textuales

| Prioridad Textual | Valor API | Descripción | Tiempo Esperado | Casos de Uso |
|-------------------|-----------|-------------|-----------------|--------------|
| **trivial** | 1 | Problemas menores, cosméticos | 1-7 días | Cambio de bombillas, ajustes menores |
| **low** | 1 | Mantenimiento rutinario | 1-7 días | Limpieza programada, mantenimiento preventivo |
| **medium** | 3 | Reparaciones estándar | 1-3 días | WiFi lento, problemas de comodidad |
| **high** | 5 | Problemas de comodidad del huésped | Inmediato-24 horas | AC no funciona, problemas de habitabilidad |
| **critical** | 5 | Emergencias que afectan habitabilidad | Inmediato | Fugas de agua, problemas eléctricos, seguridad |

## Casos de Servicio al Cliente

### Llamadas Típicas de Huéspedes

#### 1. Problema de Aire Acondicionado
```python
# Huésped reporta AC no funciona
create_maintenance_work_order(
    date_received="2024-01-15T14:00:00Z",
    priority="high",
    status="open",
    summary="AC no funciona en habitación principal",
    estimated_cost=200.00,
    estimated_time=90,
    unit_id=101,
    reservation_id=37152796,
    description="Huésped reporta que el aire acondicionado no enfría la habitación",
    source="Guest Request",
    source_name="Maria Garcia",
    source_phone="+1234567890"
)
```

#### 2. Fuga de Agua (Emergencia)
```python
# Emergencia de fuga de agua
create_maintenance_work_order(
    date_received="2024-01-15T20:30:00Z",
    priority="critical",
    status="in-progress",
    summary="Fuga de agua en baño principal",
    estimated_cost=150.00,
    estimated_time=60,
    unit_id=205,
    block_checkin=1,
    source="Guest Request",
    source_name="John Smith",
    source_phone="+1987654321",
    description="Fuga importante que requiere atención inmediata"
)
```

#### 3. Problemas de WiFi
```python
# WiFi lento reportado por huésped
create_maintenance_work_order(
    date_received="2024-01-15T10:00:00Z",
    priority="medium",
    status="open",
    summary="WiFi lento en toda la unidad",
    estimated_cost=50.00,
    estimated_time=30,
    unit_id=103,
    source="Guest Request",
    source_name="Ana Rodriguez",
    source_phone="+34612345678"
)
```

#### 4. Mantenimiento Preventivo
```python
# Limpieza programada
create_maintenance_work_order(
    date_received="2024-01-15",
    priority="low",
    status="not-started",
    summary="Limpieza profunda programada",
    estimated_cost=0.00,
    estimated_time=120,
    unit_id=102,
    date_scheduled="2024-01-20T09:00:00Z",
    source="Preventive Maintenance",
    user_id=5
)
```

#### 5. Trabajo con Proveedor
```python
# Reparación asignada a proveedor externo
create_maintenance_work_order(
    date_received="2024-01-15",
    priority="medium",
    status="vendor-assigned",
    summary="Reemplazo de electrodoméstico",
    estimated_cost=400.00,
    estimated_time=180,
    vendor_id=789,
    unit_id=104,
    date_scheduled="2024-01-18T10:00:00Z",
    reference_number="VENDOR-2024-001",
    source="Inspection"
)
```

## Flujo de Trabajo Típico

### 1. Solicitud Inicial
```python
# Huésped reporta problema
create_maintenance_work_order(
    date_received="2024-01-15T14:00:00Z",
    priority=5,
    status="open",
    summary="Fuga de agua en baño principal",
    estimated_cost=100.00,
    estimated_time=60,
    unit_id=101,
    reservation_id=37152796,
    description="Fuga reportada por huésped en lavamanos",
    source="Guest Request",
    source_name="Maria Garcia",
    source_phone="+1987654321"
)
```

### 2. Asignación a Personal
```python
# Asignar a miembro del equipo
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="not-started",
    summary="Mantenimiento preventivo HVAC",
    estimated_cost=200.00,
    estimated_time=180,
    date_scheduled="2024-01-20T10:00:00Z",
    unit_id=205,
    user_id=10,
    description="Inspección de rutina del sistema de climatización",
    source="Preventive Maintenance"
)
```

### 3. Asignación a Proveedor
```python
# Asignar a proveedor externo
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="vendor-assigned",
    summary="Reemplazo de alfombra",
    estimated_cost=500.00,
    estimated_time=240,
    vendor_id=789,
    unit_id=103,
    date_scheduled="2024-01-25T09:00:00Z",
    description="Reemplazo completo de alfombra en sala y habitaciones",
    reference_number="VENDOR-2024-001",
    source="Inspection"
)
```

### 4. Trabajo Completado
```python
# Orden completada con tiempo real
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="completed",
    summary="Reparación de puerta",
    estimated_cost=50.00,
    estimated_time=30,
    actual_time=45,
    unit_id=101,
    description="Reparación de bisagra de puerta principal",
    work_performed="Se reemplazó bisagra dañada y se ajustó la puerta",
    source="Inspection",
    user_id=8
)
```

## Casos de Uso Comunes

### Solicitud de Huésped
```python
# Orden creada por solicitud de un huésped
create_maintenance_work_order(
    date_received="2024-01-15T14:00:00Z",
    priority=5,
    status="open",
    summary="Fuga de agua en baño principal",
    estimated_cost=100.00,
    estimated_time=60,
    unit_id=101,
    reservation_id=37152796,
    description="Fuga reportada por huésped en lavamanos",
    source="Guest Request",
    source_name="Maria Garcia",
    source_phone="+1987654321",
    block_checkin=False
)
```
**¿Qué hace?** Crea orden por solicitud directa del huésped.
**¿Cuándo usarlo?** Cuando un huésped reporta un problema.

### Mantenimiento Preventivo
```python
# Mantenimiento programado regular
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="not-started",
    summary="Inspección mensual HVAC",
    estimated_cost=0,
    estimated_time=30,
    date_scheduled="2024-01-20T10:00:00Z",
    unit_id=205,
    description="Inspección de rutina del sistema de climatización",
    source="Preventive Maintenance",
    user_id=10
)
```
**¿Qué hace?** Programa mantenimiento preventivo regular.
**¿Cuándo usarlo?** Para mantenimiento programado (mensual, trimestral, etc.).

### Emergencia Crítica
```python
# Orden de emergencia que bloquea check-in
create_maintenance_work_order(
    date_received="2024-01-15T22:30:00Z",
    priority=5,
    status="in-progress",
    summary="Emergencia: Sin agua caliente",
    estimated_cost=300.00,
    estimated_time=120,
    unit_id=205,
    reservation_id=12345,
    description="Sistema de agua caliente completamente inoperativo",
    source="Guest Request",
    source_name="John Doe",
    source_phone="+1234567890",
    block_checkin=True,
    user_id=5
)
```
**¿Qué hace?** Crea orden de emergencia que impide nuevos check-ins.
**¿Cuándo usarlo?** Para problemas que hacen la unidad inhabitable.

### Trabajo con Proveedor Externo
```python
# Orden asignada a proveedor externo
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="vendor-assigned",
    summary="Reemplazo de alfombra",
    estimated_cost=500.00,
    estimated_time=240,
    vendor_id=789,
    unit_id=103,
    date_scheduled="2024-01-25T09:00:00Z",
    description="Reemplazo completo de alfombra en sala y habitaciones",
    reference_number="VENDOR-2024-001",
    source="Inspection"
)
```
**¿Qué hace?** Asigna trabajo a proveedor externo.
**¿Cuándo usarlo?** Para trabajos especializados o que requieren terceros.

## Ejemplos por Prioridad

### Prioridad Baja (1) - Mantenimiento No Urgente
```python
# Mantenimiento no urgente
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=1,
    status="not-started",
    summary="Pintura de retoque en pasillo",
    estimated_cost=25.00,
    estimated_time=15,
    unit_id=102,
    description="Pequeños retoques de pintura en paredes del pasillo"
)
```
**¿Qué hace?** Crea orden de baja prioridad.
**¿Cuándo usarlo?** Para mejoras estéticas o mantenimiento no crítico.

### Prioridad Media (3) - Mantenimiento Estándar
```python
# Mantenimiento estándar
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="open",
    summary="Cambio de filtros de aire",
    estimated_cost=30.00,
    estimated_time=20,
    unit_id=103,
    source="Preventive Maintenance"
)
```
**¿Qué hace?** Crea orden de prioridad media.
**¿Cuándo usarlo?** Para mantenimiento regular o problemas menores.

### Prioridad Alta (5) - Emergencia
```python
# Emergencia o problema crítico
create_maintenance_work_order(
    date_received="2024-01-15T20:00:00Z",
    priority=5,
    status="in-progress",
    summary="Falla eléctrica completa",
    estimated_cost=400.00,
    estimated_time=180,
    unit_id=104,
    description="Unidad sin energía eléctrica",
    block_checkin=True,
    user_id=1
)
```
**¿Qué hace?** Crea orden de alta prioridad.
**¿Cuándo usarlo?** Para emergencias que afectan la habitabilidad.

## Mejores Prácticas

### 1. Información Completa
```python
# Siempre proporcionar toda la información disponible
create_maintenance_work_order(
    date_received="2024-01-15T10:30:00Z",
    priority=3,
    status="open",
    summary="Mantenimiento sistema HVAC",
    estimated_cost=200.00,
    estimated_time=120,
    date_scheduled="2024-01-18T09:00:00Z",
    unit_id=107,
    description="Mantenimiento completo: limpieza, filtros, revisión",
    source="Preventive Maintenance",
    user_id=5,
    reference_number="MAINT-2024-015"
)
```
**¿Qué hace?** Incluye toda la información relevante.
**¿Cuándo usarlo?** Para órdenes importantes que requieren seguimiento.

### 2. BlockCheckin Apropiado
```python
# Usar block_checkin solo cuando sea realmente necesario
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=5,
    status="in-progress",
    summary="Reparación mayor: piso dañado",
    estimated_cost=1000.00,
    estimated_time=480,
    unit_id=108,
    description="Daño significativo en piso de habitación principal",
    block_checkin=True,  # Bloquea porque la unidad no es habitable
    date_scheduled="2024-01-16T08:00:00Z"
)
```
**¿Qué hace?** Bloquea check-ins cuando la unidad no es habitable.
**¿Cuándo usarlo?** Solo para problemas que impiden el uso de la unidad.

### 3. Referencias Externas
```python
# Incluir número de referencia para tracking
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="vendor-assigned",
    summary="Instalación de electrodoméstico",
    estimated_cost=300.00,
    estimated_time=120,
    vendor_id=50,
    unit_id=109,
    reference_number="PO-2024-12345",
    description="Instalación de refrigerador nuevo"
)
```
**¿Qué hace?** Incluye referencia externa para seguimiento.
**¿Cuándo usarlo?** Para órdenes con proveedores o sistemas externos.

## Respuestas Esperadas

### Respuesta Exitosa
```json
{
  "success": true,
  "work_order": {
    "id": 12345,
    "dateReceived": "2024-01-15",
    "priority": 3,
    "status": "open",
    "summary": "Reparar aire acondicionado",
    "estimatedCost": 150.00,
    "estimatedTime": 120,
    "unitId": 101,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  },
  "message": "Orden de trabajo creada exitosamente"
}
```

### Respuesta con Error
```json
{
  "success": false,
  "error": "Datos inválidos",
  "message": "La fecha de recepción debe estar en formato ISO 8601",
  "work_order": null
}
```

## Errores Comunes y Soluciones

### Error: "Invalid date format"
```python
# ❌ Incorrecto
create_maintenance_work_order(date_received="01/15/2024")

# ✅ Correcto
create_maintenance_work_order(date_received="2024-01-15")
```

### Error: "Priority must be 1, 3, or 5"
```python
# ❌ Incorrecto
create_maintenance_work_order(priority=2)

# ✅ Correcto
create_maintenance_work_order(priority=3)
```

### Error: "Invalid status value"
```python
# ❌ Incorrecto
create_maintenance_work_order(status="pending")

# ✅ Correcto
create_maintenance_work_order(status="open")
```

### Error: "Summary is required"
```python
# ❌ Incorrecto
create_maintenance_work_order(summary="")

# ✅ Correcto
create_maintenance_work_order(summary="Reparar aire acondicionado")
```

## Parámetros Obligatorios

- `date_received` - Fecha de recepción (ISO 8601)
- `priority` - Prioridad (1, 3, o 5)
- `status` - Estado válido
- `summary` - Resumen del trabajo
- `estimated_cost` - Costo estimado (>= 0)
- `estimated_time` - Tiempo estimado en minutos (> 0)

## Parámetros Opcionales

- `date_scheduled` - Fecha programada
- `unit_id` - ID de la unidad
- `reservation_id` - ID de la reserva
- `user_id` - ID del usuario asignado
- `vendor_id` - ID del proveedor
- `description` - Descripción detallada
- `source` - Origen de la orden
- `source_name` - Nombre de quien reportó
- `source_phone` - Teléfono de contacto
- `reference_number` - Número de referencia
- `work_performed` - Trabajo realizado
- `actual_time` - Tiempo real empleado
- `block_checkin` - Bloquear check-in (true/false)
"""
