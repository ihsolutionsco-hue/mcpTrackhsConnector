# Correcciones Realizadas en Work Orders

## Fecha: 2025-10-21

## Resumen

Se identificaron y corrigieron problemas críticos en las herramientas MCP de work orders (`create_maintenance_work_order` y `create_housekeeping_work_order`) relacionados con el manejo asíncrono de las llamadas a la API.

## Problemas Identificados

### 1. **Método `execute` no era asíncrono**
- **Archivo**: `src/trackhs_mcp/application/use_cases/create_work_order.py`
- **Problema**: El método `execute` del caso de uso no era `async`, pero llamaba a métodos asíncronos del cliente API
- **Error**: `'coroutine' object has no attribute 'pop'`

### 2. **Herramienta MCP no era asíncrona**
- **Archivo**: `src/trackhs_mcp/infrastructure/mcp/create_maintenance_work_order.py`
- **Problema**: La función decorada con `@mcp.tool` no era `async`
- **Síntoma**: Las llamadas a la herramienta no esperaban correctamente las respuestas

### 3. **Método `from_api_response` modificaba el diccionario original**
- **Archivo**: `src/trackhs_mcp/domain/entities/work_orders.py`
- **Problema**: Usaba `data.pop()` en lugar de crear una copia del diccionario
- **Riesgo**: Modificación de datos originales y posibles efectos secundarios

## Correcciones Aplicadas

### 1. Hacer el caso de uso asíncrono

**Antes:**
```python
def execute(self, params: CreateWorkOrderParams) -> WorkOrderResponse:
    # ...
    response_data = self.api_client.post(
        "/pms/maintenance/work-orders", data=payload
    )
```

**Después:**
```python
async def execute(self, params: CreateWorkOrderParams) -> WorkOrderResponse:
    # ...
    response_data = await self.api_client.post(
        "/pms/maintenance/work-orders", data=payload
    )
```

### 2. Hacer la herramienta MCP asíncrona

**Antes:**
```python
@mcp.tool(
    name="create_maintenance_work_order",
    description="Crear una nueva orden de trabajo de mantenimiento en TrackHS",
)
def create_maintenance_work_order(...):
    # ...
    response = use_case.execute(params)
```

**Después:**
```python
@mcp.tool(
    name="create_maintenance_work_order",
    description="Crear una nueva orden de trabajo de mantenimiento en TrackHS",
)
async def create_maintenance_work_order(...):
    # ...
    response = await use_case.execute(params)
```

### 3. Copiar el diccionario antes de modificarlo

**Antes:**
```python
@classmethod
def from_api_response(cls, data: Dict[str, Any]) -> "WorkOrder":
    """Crear instancia desde respuesta de API."""
    # Extraer campos embebidos si existen
    embedded = data.pop("_embedded", None)
    links = data.pop("_links", None)
```

**Después:**
```python
@classmethod
def from_api_response(cls, data: Dict[str, Any]) -> "WorkOrder":
    """Crear instancia desde respuesta de API."""
    # Crear una copia del diccionario para no modificar el original
    data_copy = data.copy()

    # Extraer campos embebidos si existen
    embedded = data_copy.pop("_embedded", None)
    links = data_copy.pop("_links", None)
```

### 4. Agregar verificación adicional en el cliente API

**Agregado en** `src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py`:
```python
# Realizar petición usando endpoint relativo
response = await self.client.request(method, endpoint, **request_kwargs)

# Asegurar que response no sea una corrutina
if hasattr(response, '__await__'):
    response = await response
```

## Formato de Respuesta de la API

Según la documentación oficial (`docs/trackhsDoc/post maintanance wo.md`), la API de maintenance work orders:

- **Endpoint**: `POST /pms/maintenance/work-orders`
- **Respuesta exitosa**: Status `201 Created`
- **Formato**: Devuelve **directamente** el objeto del work order, no un objeto wrapper

```json
{
  "id": 12345,
  "dateReceived": "2024-01-15",
  "priority": 3,
  "status": "open",
  "summary": "Reparar aire acondicionado",
  "estimatedCost": 150.00,
  "estimatedTime": 120,
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z",
  "_embedded": { ... },
  "_links": { ... }
}
```

## Archivos Modificados

1. ✅ `src/trackhs_mcp/application/use_cases/create_work_order.py`
   - Método `execute` ahora es `async`
   - Agregado `await` en la llamada al cliente API

2. ✅ `src/trackhs_mcp/infrastructure/mcp/create_maintenance_work_order.py`
   - Función `create_maintenance_work_order` ahora es `async`
   - Agregado `await` en la llamada al caso de uso

3. ✅ `src/trackhs_mcp/domain/entities/work_orders.py`
   - Método `from_api_response` ahora copia el diccionario antes de modificarlo

4. ✅ `src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py`
   - Agregada verificación adicional para asegurar que la respuesta no sea una corrutina

## Estado Actual

- ✅ Correcciones implementadas
- ⏳ Pendiente: Pruebas exhaustivas con la API real
- ⏳ Pendiente: Verificar que `create_housekeeping_work_order` también funcione correctamente

## Notas Adicionales

### Herramientas Similares

La herramienta `create_housekeeping_work_order` ya era asíncrona desde el principio, por lo que no requirió correcciones en ese aspecto. Sin embargo, se debe verificar que el caso de uso correspondiente también sea asíncrono.

### Patrón de Implementación

Todas las herramientas MCP que interactúan con la API deben seguir este patrón:

1. La función decorada con `@mcp.tool` debe ser `async`
2. Los casos de uso deben tener métodos `async execute`
3. Todas las llamadas al cliente API deben usar `await`
4. Los métodos que procesan respuestas no deben modificar los datos originales

## Próximos Pasos

1. ✅ Completar las correcciones en `create_maintenance_work_order`
2. ⏳ Verificar `create_housekeeping_work_order`
3. ⏳ Ejecutar pruebas exhaustivas
4. ⏳ Actualizar documentación de mejores prácticas

## Referencias

- Documentación oficial: `docs/trackhsDoc/post maintanance wo.md`
- Documentación oficial: `docs/trackhsDoc/post housekeeping wo.md`
- Mejores prácticas MCP: `docs/MEJORES_PRACTICAS_MCP.md`

