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

## Creación Básica

### 1. Orden Simple
```python
# Crear una orden básica de mantenimiento
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="open",
    summary="Reparar aire acondicionado",
    estimated_cost=150.00,
    estimated_time=120
)
```

### 2. Orden con Fecha Programada
```python
# Orden con fecha específica de ejecución
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="not-started",
    summary="Mantenimiento preventivo HVAC",
    estimated_cost=200.00,
    estimated_time=180,
    date_scheduled="2024-01-20T09:00:00Z"
)
```

### 3. Orden con Unidad Específica
```python
# Orden relacionada con una unidad
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=5,
    status="open",
    summary="Fuga de agua en baño",
    estimated_cost=100.00,
    estimated_time=60,
    unit_id=101
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

### Emergencia
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

### Con Proveedor Externo
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

### Trabajo Completado
```python
# Orden completada con tiempo real registrado
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

## Ejemplos por Prioridad

### Prioridad Baja (1)
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

### Prioridad Media (3)
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

### Prioridad Alta (5)
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

## Ejemplos por Estado

### Open (Abierta)
```python
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="open",
    summary="Revisar termostato",
    estimated_cost=0,
    estimated_time=15,
    unit_id=105
)
```

### In Progress (En Progreso)
```python
create_maintenance_work_order(
    date_received="2024-01-15T10:00:00Z",
    priority=3,
    status="in-progress",
    summary="Reparación de lavavajillas",
    estimated_cost=120.00,
    estimated_time=90,
    unit_id=106,
    user_id=12
)
```

### Vendor Assigned (Asignada a Proveedor)
```python
create_maintenance_work_order(
    date_received="2024-01-15",
    priority=3,
    status="vendor-assigned",
    summary="Servicio de piscina",
    estimated_cost=150.00,
    estimated_time=120,
    vendor_id=25,
    reference_number="POOL-2024-001"
)
```

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

## Respuesta Esperada

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

## Manejo de Errores

```python
# La herramienta valida automáticamente y retorna errores descriptivos
result = create_maintenance_work_order(
    date_received="invalid-date",  # Error: formato inválido
    priority=10,  # Error: debe ser 1, 3 o 5
    status="invalid-status",  # Error: estado no válido
    summary="",  # Error: resumen requerido
    estimated_cost=-10,  # Error: debe ser >= 0
    estimated_time=0  # Error: debe ser > 0
)

# Resultado:
# {
#   "success": false,
#   "error": "Datos inválidos",
#   "message": "La fecha de recepción debe estar en formato ISO 8601",
#   "work_order": null
# }
```
"""
