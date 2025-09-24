# Track HS MCP Remote Connector

Un conector MCP remoto para integración con la API de Track HS, permitiendo a asistentes de IA acceder a datos de propiedades, reservas y reseñas a través de internet. Desplegado en Cloudflare Workers para máxima escalabilidad y disponibilidad.

## Características

- ✅ **Autenticación Basic Auth** con Track HS API
- ✅ **Gestión de Reviews** - Consulta paginada de reseñas de propiedades
- ✅ **Gestión de Reservas** - Acceso a detalles completos de reservaciones
- ✅ **Gestión de Unidades** - Consulta avanzada de unidades de alojamiento
- ✅ **Gestión de Folios** - Consulta de facturas y recibos con filtros avanzados
- ✅ **Gestión de Contactos** - Acceso completo al CRM de contactos
- ✅ **Hosting en Cloudflare Workers** - Escalable y gratuito
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

## Instalación y Configuración

### Prerrequisitos

- Node.js 18+ 
- Cuenta de Cloudflare (gratuita)
- Credenciales de Track HS (usuario y contraseña)
- Acceso a la API de Track HS

### Configuración Rápida

1. **Clonar e instalar dependencias:**
```bash
git clone <repository-url>
cd trackhs-mcp-remote
npm install
```

2. **Configurar Cloudflare:**
```bash
# Instalar Wrangler CLI
npm install -g wrangler

# Autenticar con Cloudflare (usar token predefinido "Edit Cloudflare Workers")
wrangler login

# Configurar variables secretas
wrangler secret put TRACKHS_API_URL --name trackhs-mcp-remote
wrangler secret put TRACKHS_USERNAME --name trackhs-mcp-remote  
wrangler secret put TRACKHS_PASSWORD --name trackhs-mcp-remote
```

3. **Compilar y desplegar:**
```bash
# Compilar el código
npm run build

# Desplegar a Cloudflare Workers
wrangler deploy --name trackhs-mcp-remote
```

### Configuración de Variables Secretas

**Importante:** Necesitas configurar estas variables secretas en Cloudflare:

- `TRACKHS_API_URL`: URL base de tu API de Track HS (ej: `https://api.trackhs.com/api`)
- `TRACKHS_USERNAME`: Tu usuario de Track HS
- `TRACKHS_PASSWORD`: Tu contraseña de Track HS

**Comando para configurar cada variable:**
```bash
wrangler secret put TRACKHS_API_URL --name trackhs-mcp-remote
# Luego pegar la URL cuando te lo pida

wrangler secret put TRACKHS_USERNAME --name trackhs-mcp-remote  
# Luego pegar tu usuario cuando te lo pida

wrangler secret put TRACKHS_PASSWORD --name trackhs-mcp-remote
# Luego pegar tu contraseña cuando te lo pida
```

## Uso con Claude

### Obtener URL del Conector

Una vez desplegado, tu conector estará disponible en:
```
https://trackhs-mcp-remote.tu-subdomain.workers.dev
```

**Endpoints disponibles:**
- `https://trackhs-mcp-remote.tu-subdomain.workers.dev/health` - Health check
- `https://trackhs-mcp-remote.tu-subdomain.workers.dev/mcp/tools` - Listar herramientas
- `https://trackhs-mcp-remote.tu-subdomain.workers.dev/mcp/call` - Ejecutar herramientas

### Configuración en Claude Desktop

1. Ir a **Settings > Connectors**
2. Hacer clic en **"Add custom connector"**
3. Pegar la URL del conector: `https://trackhs-mcp-remote.tu-subdomain.workers.dev`
4. Hacer clic en **"Add"**

### Configuración en Claude Web

1. Ir a **Settings > Connectors**
2. Hacer clic en **"Add custom connector"**
3. Pegar la URL del conector: `https://trackhs-mcp-remote.tu-subdomain.workers.dev`
4. Hacer clic en **"Add"**

### Verificar Funcionamiento

Puedes verificar que el conector funciona visitando:
```
https://trackhs-mcp-remote.tu-subdomain.workers.dev/health
```

Deberías ver una respuesta JSON con `{"status": "ok"}`.

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
trackhs-mcp-remote/
├── src/
│   ├── index.ts                # Entry point
│   ├── server.ts               # Servidor MCP
│   ├── core/                   # Componentes base
│   │   ├── api-client.ts       # Cliente HTTP para Track HS
│   │   ├── auth.ts            # Autenticación
│   │   ├── base-tool.ts       # Clase base para herramientas
│   │   └── types.ts           # Tipos compartidos
│   ├── tools/                  # Herramientas MCP
│   │   ├── get-reviews.ts     # Herramienta de reseñas
│   │   ├── get-reservation.ts # Herramienta de reservaciones
│   │   ├── search-reservations.ts # Búsqueda de reservaciones
│   │   ├── get-units.ts       # Herramienta de unidades
│   │   ├── get-folios-collection.ts # Herramienta de folios
│   │   └── get-contacts.ts    # Herramienta de contactos
│   └── types/                  # Tipos específicos de Track HS
│       ├── reviews.ts         # Tipos de API de reseñas
│       ├── reservations.ts    # Tipos de API de reservaciones
│       ├── units.ts           # Tipos de API de unidades
│       ├── folios.ts          # Tipos de API de folios
│       └── contacts.ts        # Tipos de API de contactos
├── cloudflare/
│   ├── worker.ts              # Worker principal
│   └── wrangler.toml          # Configuración Cloudflare
└── scripts/
    └── setup.js               # Script de configuración
```

### Scripts Disponibles

```bash
npm run build      # Compilar TypeScript
npm run deploy     # Desplegar a Cloudflare
npm run dev        # Desarrollo local
npm run test       # Testing local
npm run setup      # Configuración inicial
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

- Las credenciales se manejan exclusivamente via variables de entorno de Cloudflare
- Comunicación HTTPS con la API de Track HS
- Validación de parámetros de entrada
- Manejo seguro de errores sin exposición de datos sensibles
- CORS configurado para Claude

## Solución de Problemas

### Error de Autenticación con Cloudflare
```
Authentication error [code: 10000]
```
**Solución:** 
1. Usar el token predefinido "Edit Cloudflare Workers" en lugar de token personalizado
2. Ir a: https://dash.cloudflare.com/profile/api-tokens
3. Buscar "Edit Cloudflare Workers" y hacer clic en "Use"
4. Configurar el nuevo token: `$env:CLOUDFLARE_API_TOKEN="nuevo_token"`

### Error de Variables Secretas
```
Variable de entorno requerida no configurada: TRACKHS_API_URL
```
**Solución:** Configurar las variables secretas:
```bash
wrangler secret put TRACKHS_API_URL --name trackhs-mcp-remote
wrangler secret put TRACKHS_USERNAME --name trackhs-mcp-remote  
wrangler secret put TRACKHS_PASSWORD --name trackhs-mcp-remote
```

### Error de Autenticación con Track HS
```
Track HS API Error: 401 Unauthorized
```
**Solución:** Verificar que las credenciales de Track HS sean correctas en las variables secretas.

### Error de Conexión
```
Track HS API Error: 500 Internal Server Error
```
**Solución:** Verificar que `TRACKHS_API_URL` sea correcto y que el servicio esté disponible.

### Error de Despliegue
```
Error: Failed to deploy
```
**Solución:** 
1. Verificar autenticación: `wrangler whoami`
2. Usar token predefinido "Edit Cloudflare Workers"
3. Verificar que el código esté compilado: `npm run build`

## Roadmap

### Próximas Funcionalidades
- [ ] Autenticación OAuth 2.0
- [ ] Cache inteligente
- [ ] Rate limiting
- [ ] Webhooks support
- [ ] Métricas de uso

### Mejoras Técnicas
- [ ] Tests automatizados
- [ ] Logging estructurado
- [ ] Docker support
- [ ] CI/CD pipeline

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

## Estado Actual del Proyecto

### ✅ Completado
- [x] Arquitectura del conector MCP remoto
- [x] Implementación de 6 herramientas Track HS
- [x] Configuración para Cloudflare Workers
- [x] Autenticación Basic Auth
- [x] Documentación completa
- [x] Manejo de errores robusto

### 🔄 En Progreso
- [ ] Despliegue exitoso en Cloudflare Workers
- [ ] Configuración de variables secretas
- [ ] Pruebas de funcionalidad

### 📋 Próximos Pasos
1. **Completar autenticación con Cloudflare** usando token predefinido
2. **Configurar variables secretas** de Track HS
3. **Desplegar el worker** y obtener URL
4. **Probar conectividad** con Claude
5. **Documentar URL final** del conector

---

**Nota:** Este conector MCP remoto está en desarrollo activo. Las funcionalidades pueden cambiar entre versiones.