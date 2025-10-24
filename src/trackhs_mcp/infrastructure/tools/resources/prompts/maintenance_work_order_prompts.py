"""
Prompts y guías para el protocolo MCP de create_maintenance_work_order
Optimizado para casos de servicio al cliente y hospitalidad
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_maintenance_work_order_prompts(mcp, api_client: "ApiClientPort"):
    """Registra los prompts y guías para create_maintenance_work_order"""

    @mcp.resource(
        "trackhs://prompts/maintenance-work-order",
        name="Maintenance Work Order Prompts",
        description="Guías y prompts para crear órdenes de trabajo de mantenimiento en TrackHS",
        mime_type="text/plain",
    )
    async def maintenance_work_order_prompts() -> str:
        """Prompts y guías para create_maintenance_work_order"""
        return """# TrackHS Maintenance Work Order - MCP Prompts & Guidelines

## 🎯 Propósito del Tool
El tool `create_maintenance_work_order` está diseñado específicamente para manejar llamadas de servicio al cliente en el sector de hospitalidad. Permite crear órdenes de trabajo de mantenimiento con prioridades textuales intuitivas y seguimiento completo del cliente.

## 📞 Casos de Uso Principales

### 1. Llamadas de Huéspedes
**Cuándo usar:** Cuando un huésped reporta un problema en su unidad
**Prioridad típica:** high, critical
**Campos importantes:** source="Guest Request", source_name, source_phone, unit_id

### 2. Emergencias
**Cuándo usar:** Problemas que afectan la habitabilidad
**Prioridad típica:** critical
**Campos importantes:** block_checkin=1, status="in-progress"

### 3. Mantenimiento Preventivo
**Cuándo usar:** Trabajos programados de rutina
**Prioridad típica:** low, medium
**Campos importantes:** source="Preventive Maintenance", date_scheduled

### 4. Reparaciones con Proveedores
**Cuándo usar:** Trabajos que requieren especialistas externos
**Prioridad típica:** medium, high
**Campos importantes:** vendor_id, status="vendor-assigned", reference_number

## 🎨 Prioridades Textuales Intuitivas

### trivial
- **Descripción:** Problemas menores, cosméticos
- **Ejemplos:** Cambio de bombillas, ajustes menores, limpieza de manchas
- **Tiempo esperado:** 1-7 días
- **API Value:** 1

### low
- **Descripción:** Mantenimiento rutinario
- **Ejemplos:** Limpieza programada, mantenimiento preventivo, inspecciones
- **Tiempo esperado:** 1-7 días
- **API Value:** 1

### medium
- **Descripción:** Reparaciones estándar
- **Ejemplos:** WiFi lento, problemas de comodidad, reparaciones menores
- **Tiempo esperado:** 1-3 días
- **API Value:** 3

### high
- **Descripción:** Problemas de comodidad del huésped
- **Ejemplos:** AC no funciona, problemas de habitabilidad, comodidad
- **Tiempo esperado:** Inmediato-24 horas
- **API Value:** 5

### critical
- **Descripción:** Emergencias que afectan habitabilidad
- **Ejemplos:** Fugas de agua, problemas eléctricos, seguridad
- **Tiempo esperado:** Inmediato
- **API Value:** 5

## 📋 Guía de Campos por Escenario

### Llamada de Huésped - AC No Funciona
```python
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

### Emergencia - Fuga de Agua
```python
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

### Mantenimiento Preventivo
```python
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

## 🔧 Mejores Prácticas para MCP

### 1. Siempre Incluir Información del Cliente
- **source:** Identificar el origen (Guest Request, Inspection, etc.)
- **source_name:** Nombre de quien reporta
- **source_phone:** Teléfono de contacto
- **description:** Detalles del problema reportado

### 2. Usar Prioridades Apropiadas
- **critical:** Solo para emergencias reales
- **high:** Problemas de comodidad del huésped
- **medium:** Reparaciones estándar
- **low:** Mantenimiento rutinario
- **trivial:** Problemas menores

### 3. Configurar Block Check-in Correctamente
- **block_checkin=1:** Solo cuando la unidad no es habitable
- **block_checkin=0:** Para problemas que no afectan habitabilidad

### 4. Asignar Responsables
- **user_id:** Para personal interno
- **vendor_id:** Para proveedores externos
- **status:** Reflejar el estado actual del trabajo

## 📊 Estados y Flujos de Trabajo

### Flujo Típico de Llamada de Huésped
1. **open** → Orden creada, pendiente de asignación
2. **in-progress** → Trabajo iniciado
3. **completed** → Trabajo terminado
4. **processed** → Orden cerrada administrativamente

### Flujo con Proveedor Externo
1. **vendor-assigned** → Asignada a proveedor
2. **vendor-accepted** → Proveedor aceptó
3. **vendor-completed** → Proveedor terminó
4. **completed** → Orden finalizada

## 🚨 Manejo de Errores Comunes

### Error: "Priority is invalid"
- **Causa:** Usar valores numéricos en lugar de textuales
- **Solución:** Usar "trivial", "low", "medium", "high", "critical"

### Error: "A unit is required with a work order"
- **Causa:** No incluir unit_id
- **Solución:** Siempre incluir unit_id (default: 1)

### Error: "Invalid date format"
- **Causa:** Formato de fecha incorrecto
- **Solución:** Usar ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)

## 💡 Tips para Servicio al Cliente

### 1. Capturar Información Completa
- Siempre pedir nombre y teléfono del huésped
- Obtener detalles específicos del problema
- Identificar la unidad afectada

### 2. Priorizar Correctamente
- **critical:** Emergencias de seguridad o habitabilidad
- **high:** Problemas que afectan la comodidad del huésped
- **medium:** Reparaciones que pueden esperar
- **low:** Mantenimiento programado

### 3. Seguimiento
- Usar reference_number para tracking
- Actualizar status según progreso
- Documentar work_performed cuando se complete

## 🎯 Ejemplos de Prompts para AI

### Para Llamada de Huésped
```
"Un huésped llama reportando que el aire acondicionado no funciona en su habitación.
Crea una orden de trabajo con prioridad alta, incluyendo la información del huésped
y asegurándote de que se asigne a la unidad correcta."
```

### Para Emergencia
```
"Hay una fuga de agua importante en la unidad 205. El huésped está muy preocupado
y necesita atención inmediata. Crea una orden de emergencia que bloquee el check-in
hasta que se resuelva el problema."
```

### Para Mantenimiento Preventivo
```
"Es hora de hacer la limpieza profunda programada de la unidad 102. Crea una orden
de mantenimiento preventivo para la próxima semana."
```

## 📈 Métricas y Seguimiento

### Campos Importantes para Reportes
- **source:** Para identificar origen de órdenes
- **priority:** Para análisis de urgencia
- **status:** Para seguimiento de progreso
- **estimated_cost vs actual_time:** Para análisis de eficiencia

### Indicadores Clave
- Tiempo promedio de resolución por prioridad
- Número de órdenes por fuente
- Costo promedio por tipo de problema
- Satisfacción del huésped (basado en follow-up)

## 🔄 Integración con Otros Tools

### Con search_reservations
- Buscar reserva del huésped para obtener unit_id
- Verificar estado de la reserva
- Obtener información de contacto

### Con search_units
- Verificar disponibilidad de la unidad
- Obtener detalles de la propiedad
- Confirmar amenities afectados

### Con get_reservation
- Obtener detalles completos de la reserva
- Verificar fechas de check-in/check-out
- Identificar huésped principal
"""
