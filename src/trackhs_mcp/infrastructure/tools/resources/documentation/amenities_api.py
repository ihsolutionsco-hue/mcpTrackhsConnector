"""
Documentation resources para Amenities API
Información concisa de la documentación de la API de Amenidades
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_amenities_api_documentation(mcp, api_client: "ApiClientPort"):
    """Registra la documentación de Amenities API"""

    @mcp.resource(
        "trackhs://docs/amenities-api",
        name="Amenities API Documentation",
        description="Essential documentation for Amenities API",
        mime_type="text/plain",
    )
    async def amenities_api_docs() -> str:
        """Documentación concisa de Amenities API"""
        return """# TrackHS Amenities API - Get Unit Amenities Collection

## Endpoint
- **URL**: `GET /pms/units/amenities`
- **Versión**: 1.0
- **API**: Channel API
- **Autenticación**: Basic Auth o HMAC

## Descripción
Obtiene la colección de amenidades disponibles en el sistema con opciones de filtrado y ordenamiento.

## Parámetros Principales

### Paginación
- `page`: Número de página (1-based, max 10k total)
- `size`: Tamaño de página (max 1000)

### Filtros
- `search`: Búsqueda por texto en id y/o nombre de amenidad
- `groupId`: Filtrar por ID de grupo específico
- `isPublic`: Amenidades públicas (0/1)
- `publicSearchable`: Amenidades buscables públicamente (0/1)
- `isFilterable`: Amenidades filtrables (0/1)

### Ordenamiento
- `sortColumn`: id, order, isPublic, publicSearchable, isFilterable, createdAt
- `sortDirection`: asc, desc (default: asc)

## Límites
- Máximo 10,000 resultados totales (page * size)
- Máximo 1,000 amenidades por página
- Paginación 1-based (page=1 es la primera página)

## Ejemplos de Uso

### Búsqueda Básica
```
GET /pms/units/amenities?page=1&size=25&sortColumn=order&sortDirection=asc
```

### Búsqueda con Filtros
```
GET /pms/units/amenities?isPublic=1&publicSearchable=1&groupId=1
```

### Búsqueda por Texto
```
GET /pms/units/amenities?search=pool&sortColumn=name&sortDirection=asc
```

### Amenidades Filtrables
```
GET /pms/units/amenities?isFilterable=1&isPublic=1
```

## Estructura de Respuesta

```json
{
  "_embedded": {
    "amenities": [
      {
        "id": 1,
        "name": "Pool",
        "order": 1,
        "isPublic": true,
        "publicSearchable": true,
        "isFilterable": true,
        "groupId": 5,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-15T12:30:00Z"
      }
    ]
  },
  "page": 1,
  "page_count": 5,
  "page_size": 25,
  "total_items": 120,
  "_links": {
    "self": {"href": "/pms/units/amenities?page=1"},
    "first": {"href": "/pms/units/amenities?page=1"},
    "last": {"href": "/pms/units/amenities?page=5"},
    "next": {"href": "/pms/units/amenities?page=2"}
  }
}
```

## Códigos de Error

- **400**: Bad Request - Parámetros inválidos
- **401**: Unauthorized - Credenciales inválidas o expiradas
- **403**: Forbidden - Permisos insuficientes
- **500**: Internal Server Error - Error temporal del servidor

## Mejores Prácticas

1. **Usar paginación** para grandes conjuntos de datos
2. **Validar valores booleanos** - usar 0 o 1, no true/false
3. **Filtrar por grupo** para resultados más específicos
4. **Ordenar por 'order'** para obtener amenidades en el orden de visualización
5. **Usar isPublic=1** para amenidades visibles al público
6. **Implementar caché** para consultas frecuentes
7. **Manejar errores apropiadamente** con reintentos para 500

## Casos de Uso Comunes

### Listar Amenidades Públicas
Obtener todas las amenidades visibles para usuarios públicos:
```
GET /pms/units/amenities?isPublic=1&publicSearchable=1&sortColumn=order
```

### Amenidades para Filtros de Búsqueda
Obtener amenidades que se pueden usar como filtros:
```
GET /pms/units/amenities?isFilterable=1&isPublic=1
```

### Buscar Amenidades Específicas
Buscar amenidades por nombre o características:
```
GET /pms/units/amenities?search=wifi&isPublic=1
```

### Amenidades por Grupo
Obtener amenidades de un grupo específico:
```
GET /pms/units/amenities?groupId=1&sortColumn=order&sortDirection=asc
```
"""
