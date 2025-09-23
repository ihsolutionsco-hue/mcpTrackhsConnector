# Track HS MCP Server

Un servidor Model Context Protocol (MCP) para integración con la API de Track HS, permitiendo a asistentes de IA acceder a datos de propiedades, reservas y reseñas.

## Características

- ✅ **Autenticación Basic Auth** con Track HS API
- ✅ **Gestión de Reviews** - Consulta paginada de reseñas de propiedades
- ✅ **Gestión de Reservas** - Acceso a detalles completos de reservaciones
- ✅ **Gestión de Unidades** - Consulta avanzada de unidades de alojamiento
- ✅ **Gestión de Folios** - Consulta de facturas y recibos con filtros avanzados
- ✅ **Gestión de Contactos** - Acceso completo al CRM de contactos (huéspedes, propietarios, empleados)
- ✅ **Arquitectura Escalable** - Fácil adición de nuevos endpoints
- ✅ **Manejo de Errores** - Gestión robusta de errores de API

## Herramientas Disponibles

### `get_reviews`
Recupera una colección paginada de reseñas de propiedades desde Track HS.

**Parámetros:**
- `page` (number, opcional): Número de página
- `size` (number, opcional): Tamaño de página
- `sortColumn` (string, opcional): Columna de ordenamiento (solo 'id')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc')
- `search` (string, opcional): Búsqueda por ID de reseña y contenido público
- `updatedSince` (string, opcional): Filtrar por fecha de actualización (ISO 8601)

### `get_reservation`
Obtiene información detallada de una reservación específica por ID.

**Parámetros:**
- `reservationId` (string, requerido): ID de la reservación a recuperar

### `search_reservations`
Búsqueda avanzada de reservaciones con múltiples filtros y opciones de paginación.

**Parámetros:**
- `page` (number, opcional): Número de página (default: 0)
- `size` (number, opcional): Tamaño de página (default: 10, max: 100)
- `sortColumn` (string, opcional): Columna de ordenamiento
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc')
- `search` (string, opcional): Búsqueda por nombre o descripciones
- `tags` (string, opcional): Búsqueda por ID de tag
- `updatedSince` (string, opcional): Filtrar por fecha de actualización (ISO 8601)
- `nodeId` (number/array, opcional): ID(s) de nodo
- `unitId` (number/array, opcional): ID(s) de unidad
- `reservationTypeId` (number/array, opcional): ID(s) de tipo de reservación
- `contactId` (number/array, opcional): ID(s) de contacto
- `travelAgentId` (number/array, opcional): ID(s) de agente de viajes
- `campaignId` (number/array, opcional): ID(s) de campaña
- `userId` (number/array, opcional): ID(s) de usuario
- `unitTypeId` (number/array, opcional): ID(s) de tipo de unidad
- `rateTypeId` (number/array, opcional): ID(s) de tipo de tarifa
- `bookedStart` (string, opcional): Fecha de reserva inicio (ISO 8601)
- `bookedEnd` (string, opcional): Fecha de reserva fin (ISO 8601)
- `arrivalStart` (string, opcional): Fecha de llegada inicio (ISO 8601)
- `arrivalEnd` (string, opcional): Fecha de llegada fin (ISO 8601)
- `departureStart` (string, opcional): Fecha de salida inicio (ISO 8601)
- `departureEnd` (string, opcional): Fecha de salida fin (ISO 8601)
- `inHouseToday` (number, opcional): Filtrar por huéspedes actuales (0 o 1)
- `status` (string/array, opcional): Estado(s) de reservación

### `get_units`
Obtener colección de unidades de alojamiento con filtros avanzados incluyendo paginación, ordenamiento, filtros por ID, búsqueda de texto, filtros físicos, políticas y disponibilidad.

**Parámetros:**
- `page` (number, opcional): Número de página (default: 0)
- `size` (number, opcional): Tamaño de página (default: 10, max: 100)
- `sortColumn` (string, opcional): Columna de ordenamiento ('id', 'name', 'nodeName', 'unitTypeName')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc')
- `search` (string, opcional): Búsqueda por nombre o descripciones
- `term` (string, opcional): Búsqueda por término
- `unitCode` (string, opcional): Búsqueda por código de unidad
- `shortName` (string, opcional): Búsqueda por nombre corto
- `contentUpdatedSince` (string, opcional): Filtrar por fecha de actualización de contenido (ISO 8601)
- `nodeId` (number/array, opcional): ID(s) de nodo
- `unitTypeId` (number/array, opcional): ID(s) de tipo de unidad
- `amenityId` (number/array, opcional): ID(s) de amenidad
- `bedrooms` (number, opcional): Número exacto de dormitorios
- `minBedrooms` (number, opcional): Mínimo número de dormitorios
- `maxBedrooms` (number, opcional): Máximo número de dormitorios
- `bathrooms` (number, opcional): Número exacto de baños
- `minBathrooms` (number, opcional): Mínimo número de baños
- `maxBathrooms` (number, opcional): Máximo número de baños
- `petsFriendly` (number, opcional): Unidades que permiten mascotas (0 o 1)
- `eventsAllowed` (number, opcional): Unidades que permiten eventos (0 o 1)
- `smokingAllowed` (number, opcional): Unidades que permiten fumar (0 o 1)
- `childrenAllowed` (number, opcional): Unidades que permiten niños (0 o 1)
- `arrival` (string, opcional): Fecha de llegada para filtro de disponibilidad (ISO 8601)
- `departure` (string, opcional): Fecha de salida para filtro de disponibilidad (ISO 8601)
- `isActive` (number, opcional): Unidades activas (0 o 1)
- `isBookable` (number, opcional): Unidades reservables (0 o 1)
- `unitStatus` (string, opcional): Estado de la unidad ('clean', 'dirty', 'occupied', 'inspection', 'inprogress')
- `computed` (number, opcional): Incluir valores computados (0 o 1)
- `inherited` (number, opcional): Incluir atributos heredados (0 o 1)
- `limited` (number, opcional): Respuesta limitada (0 o 1)
- `includeDescriptions` (number, opcional): Incluir descripciones (0 o 1)
- `allowUnitRates` (number, opcional): Unidades que permiten tarifas por unidad (0 o 1)
- `calendarId` (number, opcional): ID del calendario
- `roleId` (number, opcional): ID del rol
- `id` (array, opcional): IDs específicos de unidades

### `get_folios_collection`
Obtener colección de folios (facturas/recibos) con filtros avanzados, paginación y ordenamiento.

**Parámetros:**
- `page` (number, opcional): Número de página (minimum: 1)
- `size` (number, opcional): Tamaño de página (minimum: 1, maximum: 100)
- `sortColumn` (string, opcional): Columna de ordenamiento ('id', 'name', 'status', 'type', 'startDate', 'endDate', 'contactName', 'companyName', 'reservationId', 'currentBalance', 'realizedBalance', 'masterFolioRule')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc')
- `search` (string, opcional): Búsqueda por ID, nombre, nombre de empresa, nombre de contacto, ID de reservación, ID de unidad o nombre de unidad
- `type` (string, opcional): Tipo de folio ('guest', 'master', 'guest-sub-folio', 'master-sub-folio')
- `status` (string, opcional): Estado del folio ('open', 'closed')
- `masterFolioId` (number, opcional): ID del folio maestro (minimum: 1)
- `contactId` (number, opcional): ID del contacto/huésped (minimum: 1)
- `companyId` (number, opcional): ID de la empresa (minimum: 1)

### `get_contacts`
Obtener todos los contactos del sistema CRM de Track HS. Incluye huéspedes, propietarios y empleados de proveedores con información completa de contacto, direcciones, teléfonos, emails y datos personalizados.

**Parámetros:**
- `sortColumn` (string, opcional): Columna de ordenamiento ('id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc', default: 'asc')
- `search` (string, opcional): Búsqueda por nombre, apellido, email, teléfonos con wildcard derecho
- `term` (string, opcional): Búsqueda por valor preciso como ID o nombre
- `email` (string, opcional): Búsqueda por email primario o secundario
- `page` (number, opcional): Número de página
- `size` (number, opcional): Tamaño de página (máximo 100)
- `updatedSince` (string, opcional): Fecha en formato ISO 8601 para filtrar contactos actualizados desde esa fecha

## Instalación

### Prerrequisitos

- Node.js 18+ 
- Credenciales de Track HS (usuario y contraseña)
- Acceso a la API de Track HS

### Configuración

1. **Clonar e instalar dependencias:**
```bash
git clone <repository-url>
cd trackhs-mcp-server
npm install
```

2. **Compilar el proyecto:**
```bash
npm run build
```

3. **Configurar variables de entorno:**
```bash
export TRACKHS_API_URL="https://api-integration-example.tracksandbox.io/api"
export TRACKHS_USERNAME="your_username"
export TRACKHS_PASSWORD="your_password"
```

## Uso con Claude Desktop

Agregar la siguiente configuración a tu archivo de configuración de Claude Desktop:

### Configuración Manual

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "node",
      "args": ["path/to/trackhs-mcp-server/dist/index.js"],
      "env": {
        "TRACKHS_API_URL": "https://api-integration-example.tracksandbox.io/api",
        "TRACKHS_USERNAME": "your_username", 
        "TRACKHS_PASSWORD": "your_password"
      }
    }
  }
}
```

### Configuración con NPX (Próximamente)

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "npx",
      "args": ["trackhs-mcp-server"],
      "env": {
        "TRACKHS_API_URL": "https://api-integration-example.tracksandbox.io/api",
        "TRACKHS_USERNAME": "your_username",
        "TRACKHS_PASSWORD": "your_password"
      }
    }
  }
}
```

## Ejemplos de Uso

### Consultar Reseñas
```
"Muéstrame las últimas 10 reseñas de propiedades"
"Busca reseñas que contengan 'excelente' en los comentarios"
"Obtén reseñas actualizadas desde el 2024-01-01"
```

### Consultar Reservaciones
```
"Muestra los detalles de la reservación #12345"
"¿Cuál es el estado de la reserva con ID 98765?"
"Dame información completa de la reservación ABC123"
```

### Buscar Reservaciones
```
"Busca todas las reservaciones confirmadas"
"Encuentra reservaciones de llegada entre el 1 y 15 de enero de 2024"
"Muéstrame reservaciones del nodo 123 con estado 'Checked In'"
"Busca reservaciones que contengan 'VIP' en el nombre"
"Encuentra reservaciones de la unidad 456 ordenadas por fecha de llegada"
"Busca reservaciones actualizadas desde ayer"
"Muéstrame reservaciones de huéspedes actuales (inHouseToday)"
```

### Consultar Unidades
```
"Muéstrame todas las unidades disponibles"
"Busca unidades con 3 dormitorios o más"
"Encuentra unidades que permitan mascotas"
"Muéstrame unidades del nodo 456"
"Busca unidades disponibles entre el 1 y 15 de marzo de 2024"
"Encuentra unidades con piscina (amenidad específica)"
"Muéstrame unidades activas y reservables"
"Busca unidades que permitan eventos"
"Encuentra unidades con código 'TH444'"
"Muéstrame unidades actualizadas desde ayer"
```

### Consultar Folios
```
"Muéstrame todos los folios abiertos"
"Busca folios del huésped con ID 12345"
"Encuentra folios de tipo 'guest' ordenados por balance actual"
"Muéstrame folios de la empresa 789"
"Busca folios que contengan 'VIP' en el nombre"
"Encuentra folios cerrados del último mes"
"Muéstrame folios con balance negativo"
"Busca folios del folio maestro 456"
"Encuentra folios de reservación 999"
"Muéstrame folios ordenados por fecha de inicio"
```

### Consultar Contactos
```
"Muéstrame todos los contactos VIP"
"Busca contactos por email 'john@example.com'"
"Encuentra contactos que contengan 'Smith' en el nombre"
"Muéstrame contactos actualizados desde ayer"
"Busca contactos por teléfono '555-1234'"
"Encuentra contactos de la región 'California'"
"Muéstrame contactos ordenados por nombre"
"Busca contactos con tags específicos"
"Encuentra contactos con balance negativo"
"Muéstrame contactos creados en el último mes"
```

## Desarrollo

### Estructura del Proyecto

```
trackhs-mcp-server/
├── src/
│   ├── index.ts                # Entry point
│   ├── server.ts               # Configuración del servidor MCP
│   ├── core/                   # Componentes base
│   │   ├── api-client.ts       # Cliente HTTP para Track HS
│   │   ├── base-tool.ts        # Clase base para herramientas
│   │   └── types.ts            # Tipos compartidos
│   ├── tools/                  # Herramientas MCP
│   │   ├── get-reviews.ts      # Herramienta de reseñas
│   │   ├── get-reservation.ts  # Herramienta de reservaciones
│   │   ├── search-reservations.ts # Búsqueda de reservaciones
│   │   ├── get-units.ts        # Herramienta de unidades
│   │   ├── get-folios-collection.ts # Herramienta de folios
│   │   └── get-contacts.ts     # Herramienta de contactos
│   └── types/                  # Tipos específicos de Track HS
│       ├── reviews.ts          # Tipos de API de reseñas
│       ├── reservations.ts     # Tipos de API de reservaciones
│       ├── units.ts            # Tipos de API de unidades
│       ├── folios.ts           # Tipos de API de folios
│       └── contacts.ts         # Tipos de API de contactos
└── dist/                       # Archivos compilados
```

### Scripts Disponibles

```bash
npm run build      # Compilar TypeScript
npm run start      # Ejecutar servidor compilado
npm run dev        # Desarrollo con recarga automática
```

### Agregar Nuevos Endpoints

Para agregar un nuevo endpoint de Track HS:

1. **Crear nueva herramienta** en `src/tools/`:
```typescript
// src/tools/get-properties.ts
export class GetPropertiesTool extends BaseTrackHSTool {
  name = 'get_properties';
  description = 'Get property information';
  // ... implementación
}
```

2. **Registrar en el servidor** (`src/server.ts`):
```typescript
this.tools = [
  new GetReviewsTool(apiClient),
  new GetReservationTool(apiClient),
  new GetPropertiesTool(apiClient) // Nueva herramienta
];
```

## Seguridad

- Las credenciales se manejan exclusivamente via variables de entorno
- Comunicación HTTPS con la API de Track HS
- Validación de parámetros de entrada
- Manejo seguro de errores sin exposición de datos sensibles

## Solución de Problemas

### Error de Autenticación
```
Track HS API Error: 401 Unauthorized
```
**Solución:** Verificar que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` sean correctos.

### Error de Conexión
```
Track HS API Error: 500 Internal Server Error
```
**Solución:** Verificar que `TRACKHS_API_URL` sea correcto y que el servicio esté disponible.

### Herramienta No Encontrada
```
Unknown tool: tool_name
```
**Solución:** Verificar que la herramienta esté registrada en `server.ts`.

## Roadmap

### Próximas Funcionalidades
- [x] Gestión de Propiedades (Units/Properties)
- [x] Gestión de Folios (Bills/Receipts)
- [x] Gestión de Huéspedes (Contacts)
- [ ] Autenticación HMAC
- [ ] Cache inteligente
- [ ] Rate limiting
- [ ] Webhooks support

### Mejoras Técnicas
- [ ] Tests automatizados
- [ ] Documentación de API completa
- [ ] Logging estructurado
- [ ] Métricas de performance
- [ ] Docker support

## Contribuir

1. Fork el repositorio
2. Crear branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

MIT

## Soporte

Para soporte técnico:
- Crear issue en GitHub
- Contactar: support@trackhs.com
- Documentación API: https://support.trackhs.com

---

**Nota:** Este servidor MCP está en desarrollo activo. Las funcionalidades pueden cambiar entre versiones.