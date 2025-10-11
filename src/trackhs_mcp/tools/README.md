# Herramientas MCP TrackHS - API V2

Este directorio contiene la herramienta MCP principal para la API de Track HS V2. Se ha simplificado para incluir solo la herramienta más importante y completa: `search_reservations`.

## Estructura de Archivos

### Herramienta Principal

1. **`search_reservations.py`** - ⭐ **HERRAMIENTA PRINCIPAL** - Buscar reservas con filtros avanzados de API V2

### Archivo Principal

- **`all_tools.py`** - Registrador principal que importa y registra la herramienta search_reservations

## Patrón de Implementación

La herramienta search_reservations sigue el patrón estándar:

```python
def register_search_reservations(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta search_reservations V2"""
    
    @mcp.tool()
    async def search_reservations(...):
        """
        Search reservations in Track HS API V2 with comprehensive filtering options
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            # ... todos los parámetros de la API V2
        """
        # Implementación completa de la API V2
        pass
```

## Ventajas de esta Estructura Simplificada

1. **Enfoque**: Una sola herramienta poderosa y completa
2. **Simplicidad**: Fácil de mantener y actualizar
3. **Completitud**: Cubre todas las necesidades de búsqueda de reservas
4. **API V2**: Aprovecha al máximo las capacidades de la API V2
5. **Rendimiento**: Optimizada para grandes conjuntos de datos

## Mejoras de la API V2

### Herramienta `search_reservations` Mejorada

La herramienta `search_reservations` ha sido completamente actualizada para aprovechar todas las capacidades de la API V2:

#### Nuevos Parámetros Disponibles

**Filtros de Fecha:**
- `booked_start/end` - Fechas de reserva
- `arrival_start/end` - Fechas de llegada
- `departure_start/end` - Fechas de salida
- `updated_since` - Filtro por fecha de actualización

**Filtros por ID:**
- `reservation_type_id` - Tipo de reserva
- `travel_agent_id` - Agente de viajes
- `campaign_id` - Campaña
- `user_id` - Usuario
- `unit_type_id` - Tipo de unidad
- `rate_type_id` - Tipo de tarifa

**Filtros Especiales:**
- `in_house_today` - Reservas en casa hoy
- `scroll` - Scroll de Elasticsearch
- `group_id` - ID del grupo
- `checkin_office_id` - Oficina de check-in

#### Características Avanzadas

1. **Paginación Robusta:**
   - Paginación estándar con `page` y `size`
   - Scroll de Elasticsearch para grandes conjuntos
   - Límites: máximo 10k resultados, 1k por página

2. **Ordenamiento Avanzado:**
   - Columnas: name, status, altConf, agreementStatus, type, guest, guests, unit, units, checkin, checkout, nights
   - Direcciones: asc, desc

3. **Filtros Múltiples:**
   - Soporte para arrays de IDs
   - Filtros de fecha con formato ISO 8601
   - Búsqueda de texto con `search`

#### Ejemplo de Uso

```python
# Búsqueda básica
await search_reservations(
    page=1,
    size=50,
    sort_column="name",
    sort_direction="asc"
)

# Búsqueda con filtros avanzados
await search_reservations(
    page=1,
    size=100,
    status="Confirmed",
    arrival_start="2024-01-01T00:00:00Z",
    arrival_end="2024-12-31T23:59:59Z",
    node_id=[123, 456],
    unit_type_id=[789],
    in_house_today=1,
    scroll=1
)

# Búsqueda con scroll para grandes conjuntos
await search_reservations(
    scroll=1,
    size=100,
    status=["Confirmed", "Checked In"],
    arrival_start="2024-01-01T00:00:00Z"
)
```

#### Respuesta de la API V2

La respuesta incluye información completa de la API V2:

- **Datos de Reserva:** Todos los campos de la especificación V2
- **Desglose Financiero:** guest_breakdown, owner_breakdown
- **Información de Ocupantes:** Detalles completos de huéspedes
- **Productos Adicionales:** Seguros de viaje, planes de pago
- **Estado de Acuerdos:** agreement_status, políticas
- **Metadatos:** Paginación, enlaces, timestamps

## Utilidades de Soporte

### Paginación
- `PaginationUtility` - Manejo robusto de paginación
- Soporte para scroll de Elasticsearch
- Validación de límites y parámetros

### Logging
- `TrackHSLogger` - Logging avanzado con contexto
- Métricas de rendimiento
- Integración con MCP

### Completion
- `TrackHSCompletion` - Autocompletado inteligente
- Sugerencias de parámetros
- Cache inteligente

### Manejo de Errores
- `TrackHSErrorHandler` - Manejo robusto de errores
- Estrategias de reintento
- Respuestas estructuradas

## Uso

La herramienta se registra automáticamente cuando se importa `register_all_tools` en el servidor principal. La herramienta `search_reservations` está lista para usar con todas las capacidades de la API V2.

### Configuración Recomendada

Para aprovechar al máximo las mejoras de la API V2:

1. **Usar endpoint V2:** `/v2/pms/reservations`
2. **Configurar paginación:** Ajustar `size` según necesidades
3. **Implementar scroll:** Para conjuntos grandes de datos
4. **Usar filtros específicos:** Para mejorar rendimiento
5. **Manejar errores:** Implementar estrategias de reintento
