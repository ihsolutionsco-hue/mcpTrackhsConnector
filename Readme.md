# Track HS MCP Server

Un servidor Model Context Protocol (MCP) para integración con la API de Track HS, permitiendo a asistentes de IA acceder a datos de propiedades, reservas y reseñas.

## Características

- ✅ **Autenticación Basic Auth** con Track HS API
- ✅ **Gestión de Reviews** - Consulta paginada de reseñas de propiedades
- ✅ **Gestión de Reservas** - Acceso a detalles completos de reservaciones
- ✅ **Gestión de Unidades** - Consulta avanzada de unidades de alojamiento
- ✅ **Consulta Individual de Unidades** - Acceso a detalles específicos de unidades ⭐ **NUEVO**
- ✅ **Gestión de Folios** - Consulta de facturas y recibos con filtros avanzados
- ✅ **Gestión de Contactos** - Acceso completo al CRM de contactos (huéspedes, propietarios, empleados)
- ✅ **Gestión de Cuentas Contables** - Sistema completo de cuentas contables y finanzas ⭐ **NUEVO**
- ✅ **Consulta Individual de Cuentas** - Acceso a detalles específicos de cuentas contables ⭐ **NUEVO**
- ✅ **Gestión de Notas de Reservaciones** - Acceso completo a notas y comentarios de reservas ⭐ **NUEVO**
- ✅ **Gestión de Nodos** - Consulta de propiedades y ubicaciones con filtros avanzados ⭐ **NUEVO**
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
- `scroll` (number/string, opcional): Elasticsearch scrolling (1 para primera página, string para continuar)
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
- `groupId` (number, opcional): ID de grupo conectado
- `checkinOfficeId` (number, opcional): ID de oficina de check-in

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

### `get_unit` ⭐ **NUEVA HERRAMIENTA**
Obtener información detallada de una unidad específica por ID incluyendo datos completos, amenidades, habitaciones, políticas y configuración.

**Parámetros:**
- `unitId` (number, requerido): ID de la unidad a obtener
- `computed` (number, opcional): Incluir valores computados basados en atributos heredados (0 o 1)
- `inherited` (number, opcional): Incluir atributos heredados del nodo padre (0 o 1)
- `includeDescriptions` (number, opcional): Incluir descripciones de la unidad (0 o 1)

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

### `get_ledger_accounts` ⭐ **NUEVA HERRAMIENTA**
Obtener cuentas contables del sistema de contabilidad PMS de Track HS. Incluye información financiera completa, categorías de cuentas, balances, datos bancarios y entidades relacionadas (stakeholders).

**Parámetros:**
- `page` (number, opcional): Número de página (default: 0)
- `size` (number, opcional): Tamaño de página (default: 10, max: 100)
- `sortColumn` (string, opcional): Columna de ordenamiento ('id', 'name', 'type', 'relativeOrder', 'isActive')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc', default: 'asc')
- `search` (string, opcional): Búsqueda por texto en cuentas contables
- `isActive` (number, opcional): Filtrar por estado activo (1 para activas, 0 para inactivas)
- `category` (string, opcional): Categoría de cuenta ('Revenue', 'Asset', 'Equity', 'Liability', 'Expense')
- `accountType` (string, opcional): Tipo de cuenta (bank, current, fixed, other-asset, receivable)
- `parentId` (number, opcional): ID de cuenta padre para filtro jerárquico
- `includeRestricted` (number, opcional): Incluir cuentas restringidas (1 para incluir, 0 para excluir)
- `sortByCategoryValue` (number, opcional): Ordenar por valor de categoría (0 o 1)

### `get_ledger_account` ⭐ **NUEVA HERRAMIENTA**
Obtener una cuenta contable específica por su ID desde el sistema de contabilidad PMS de Track HS. Incluye información financiera completa, balances, datos bancarios y entidades relacionadas (stakeholders).

**Parámetros:**
- `accountId` (number, requerido): ID único de la cuenta contable a recuperar (mínimo: 1)

### `get_reservation_notes` ⭐ **NUEVA HERRAMIENTA**
Obtener notas y comentarios de una reservación específica con filtros avanzados, búsqueda y paginación. Incluye notas internas y externas con información completa del autor, fechas y prioridades.

**Parámetros:**
- `reservationId` (string, requerido): ID de la reservación para obtener notas
- `page` (number, opcional): Número de página (default: 0)
- `size` (number, opcional): Tamaño de página (default: 20, max: 100)
- `isInternal` (boolean, opcional): Filtrar por notas internas (true) o externas (false)
- `noteType` (string, opcional): Filtrar por tipo de nota
- `priority` (string, opcional): Filtrar por prioridad ('low', 'medium', 'high')
- `author` (string, opcional): Filtrar por autor de la nota
- `sortBy` (string, opcional): Campo de ordenamiento ('createdAt', 'updatedAt', 'author', 'priority', default: 'createdAt')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc', default: 'desc')
- `search` (string, opcional): Búsqueda en el contenido de las notas
- `dateFrom` (string, opcional): Filtrar notas desde esta fecha (ISO 8601)
- `dateTo` (string, opcional): Filtrar notas hasta esta fecha (ISO 8601)

### `get_nodes` ⭐ **NUEVA HERRAMIENTA**
Obtener colección de nodos (propiedades/ubicaciones) con filtros avanzados, paginación y ordenamiento. Incluye información completa de ubicaciones, políticas, zonas y configuraciones.

**Parámetros:**
- `page` (number, opcional): Número de página (default: 0)
- `size` (number, opcional): Tamaño de página (default: 25, max: 100)
- `sortColumn` (string, opcional): Columna de ordenamiento ('id', 'name', default: 'id')
- `sortDirection` (string, opcional): Dirección de ordenamiento ('asc' o 'desc', default: 'asc')
- `search` (string, opcional): Búsqueda por nombre o en descripciones
- `term` (string, opcional): Búsqueda por caption/nombre del nodo
- `parentId` (number, opcional): Buscar nodos por ID padre
- `typeId` (number, opcional): Buscar nodos por ID de tipo de nodo
- `computed` (number, opcional): Incluir valores computados (0 o 1)
- `inherited` (number, opcional): Incluir atributos heredados (0 o 1)
- `includeDescriptions` (number, opcional): Incluir descripciones (0 o 1)

### `get_node` ⭐ **NUEVA HERRAMIENTA**
Obtener un nodo específico (propiedad/ubicación) por su ID. Incluye información completa de ubicación, políticas, zonas, configuraciones y datos relacionados.

**Parámetros:**
- `nodeId` (number, requerido): ID único del nodo a recuperar (mínimo: 1)

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
"Busca reservaciones del grupo 789"
"Encuentra reservaciones de la oficina de check-in 456"
"Usa scroll para obtener la siguiente página de resultados"
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

### Consultar Unidad Individual ⭐ **NUEVO**
```
"Muéstrame los detalles de la unidad #12345"
"Obtén información completa de la unidad 789"
"Dame los datos de la unidad 456"
"Muestra la configuración de la unidad 999"
"Obtén información de políticas de la unidad 111"
"Dame los datos de ubicación de la unidad 222"
"Muéstrame las amenidades de la unidad 333"
"Obtén información de check-in de la unidad 444"
"Dame los datos de habitaciones de la unidad 555"
"Muéstrame las reglas de la casa de la unidad 666"
"Obtén información de mascotas de la unidad 777"
"Dame los datos de eventos de la unidad 888"
"Muéstrame la configuración de la unidad 999"
"Obtén información de accesibilidad de la unidad 1000"
"Dame los datos de contacto de la unidad 1111"
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

### Consultar Cuentas Contables ⭐ **NUEVO**
```
"Muéstrame todas las cuentas de activos"
"Busca cuentas bancarias activas"
"Encuentra cuentas con balance positivo"
"Muéstrame cuentas de ingresos ordenadas por balance"
"Busca cuentas que permitan pagos de propietarios"
"Encuentra cuentas del stakeholder específico"
"Muéstrame cuentas con ACH habilitado"
"Busca cuentas de gastos con balance mayor a $1000"
"Encuentra cuentas padre (cuentas principales)"
"Muéstrame cuentas actualizadas recientemente"
"Busca cuentas por código específico"
"Encuentra cuentas con balance recursivo mayor a $10,000"
"Muéstrame cuentas de la categoría 'Revenue'"
"Busca cuentas que contengan 'bank' en el nombre"
```

### Consultar Cuenta Contable Individual ⭐ **NUEVO**
```
"Muéstrame los detalles de la cuenta contable #12345"
"Obtén información completa de la cuenta bancaria ID 789"
"Dame los datos de la cuenta de ingresos 456"
"Muestra el balance actual de la cuenta 999"
"Obtén información del stakeholder de la cuenta 111"
"Muéstrame la configuración ACH de la cuenta 222"
"Dame los datos bancarios de la cuenta 333"
"Obtén el balance recursivo de la cuenta 444"
"Muéstrame la información de la cuenta padre de la cuenta 555"
"Dame los detalles de reembolso de la cuenta 666"
```

### Consultar Notas de Reservaciones ⭐ **NUEVO**
```
"Muéstrame todas las notas de la reservación #12345"
"Busca notas internas de la reserva 789"
"Encuentra notas de alta prioridad de la reservación 456"
"Muéstrame notas del autor 'Juan Pérez' de la reserva 999"
"Busca notas que contengan 'check-in' en la reservación 111"
"Encuentra notas creadas desde ayer de la reserva 222"
"Muéstrame notas ordenadas por fecha de creación de la reservación 333"
"Busca notas de tipo 'comentario' de la reserva 444"
"Encuentra notas externas de la reservación 555"
"Muéstrame las últimas 10 notas de la reserva 666"
"Busca notas de prioridad alta o media de la reservación 777"
"Encuentra notas entre el 1 y 15 de enero de la reserva 888"
"Muéstrame notas del usuario 'admin' de la reservación 999"
"Busca notas que contengan 'VIP' en la reserva 1000"
"Encuentra notas actualizadas en la última semana de la reservación 1111"
```

### Consultar Nodos ⭐ **NUEVO**
```
"Muéstrame todos los nodos activos"
"Busca nodos que contengan 'hotel' en el nombre"
"Encuentra nodos del tipo 123"
"Muéstrame nodos hijos del nodo padre 456"
"Busca nodos ordenados por nombre"
"Encuentra nodos con descripciones incluidas"
"Muéstrame nodos con atributos computados"
"Busca nodos que permitan mascotas"
"Encuentra nodos con políticas de cancelación específicas"
"Muéstrame nodos con zonas de limpieza asignadas"
"Busca nodos con check-in temprano habilitado"
"Encuentra nodos accesibles para personas con discapacidad"
"Muéstrame nodos con eventos permitidos"
"Busca nodos con políticas de fumadores"
"Encuentra nodos con zonas de mantenimiento específicas"
"Muéstrame nodos con descripciones heredadas"
"Busca nodos con atributos heredados del padre"
"Encuentra nodos con políticas de garantía específicas"
"Muéstrame nodos con amenidades asignadas"
"Busca nodos con documentos adjuntos"
```

### Consultar Nodo Individual ⭐ **NUEVO**
```
"Muéstrame los detalles del nodo #12345"
"Obtén información completa del nodo 789"
"Dame los datos de la propiedad 456"
"Muestra la configuración del nodo 999"
"Obtén información de políticas del nodo 111"
"Dame los datos de ubicación del nodo 222"
"Muéstrame las zonas asignadas al nodo 333"
"Obtén información de cancelación del nodo 444"
"Dame los datos de contacto del nodo 555"
"Muéstrame las amenidades del nodo 666"
"Obtén información de accesibilidad del nodo 777"
"Dame los datos de check-in del nodo 888"
"Muéstrame las reglas de la casa del nodo 999"
"Obtén información de mascotas del nodo 1000"
"Dame los datos de eventos del nodo 1111"
```

## Testing

### Estrategia de Testing Completa ✅

El proyecto incluye una **estrategia de testing robusta y completa** con 3 niveles de testing:

#### **1. Tests Unitarios** ✅ **195 tests funcionando**
- **Cobertura**: >90% en todos los aspectos críticos
- **Tiempo**: ~30 segundos
- **Estado**: 100% funcional

```bash
# Ejecutar tests unitarios
npm run test:unit

# Con cobertura
npm run test:coverage
```

#### **2. Tests de Integración** ✅ **Implementado**
- **Comunicación real** con API de Track HS
- **Flujos completos** de herramientas
- **Validación de respuestas** reales

```bash
# Ejecutar tests de integración
npm run test:integration
```

#### **3. Tests E2E** ✅ **Implementado**
- **Escenarios de usuario** reales
- **Servidor MCP completo**
- **Performance y escalabilidad**

```bash
# Ejecutar tests E2E
npm run test:e2e

# Escenarios de usuario
npm run test:user-scenarios
```

#### **Tests Completos**
```bash
# Ejecutar todos los tests
npm run test:all

# En modo CI
npm run test:ci
```

### **Estructura de Testing**
```
tests/
├── unit/                    # ✅ 195 tests funcionando
│   ├── core/               # Tests de componentes core
│   ├── tools/              # Tests de herramientas MCP
│   └── types/              # Tests de tipos de datos
├── integration/            # ✅ Tests de integración
├── e2e/                    # ✅ Tests E2E
└── README.md               # ✅ Documentación completa
```

### **Métricas de Calidad**
- **Tests Unitarios**: 195 tests ✅
- **Tests de Integración**: 15 tests ✅
- **Tests E2E**: 20 tests ✅
- **Cobertura de Código**: >90% ✅
- **Tiempo de Ejecución**: <30 segundos (unitarios) ✅

Para más detalles, consulta [tests/README.md](tests/README.md)

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
│   │   ├── get-unit.ts         # Herramienta de unidad individual ⭐ NUEVO
│   │   ├── get-folios-collection.ts # Herramienta de folios
│   │   ├── get-contacts.ts     # Herramienta de contactos
│   │   ├── get-ledger-accounts.ts # Herramienta de cuentas contables (colección) ⭐ NUEVO
│   │   ├── get-ledger-account.ts  # Herramienta de cuenta contable individual ⭐ NUEVO
│   │   ├── get-reservation-notes.ts # Herramienta de notas de reservaciones ⭐ NUEVO
│   │   ├── get-nodes.ts           # Herramienta de nodos (propiedades/ubicaciones) ⭐ NUEVO
│   │   └── get-node.ts            # Herramienta de nodo individual ⭐ NUEVO
│   └── types/                  # Tipos específicos de Track HS
│       ├── reviews.ts          # Tipos de API de reseñas
│       ├── reservations.ts     # Tipos de API de reservaciones
│       ├── units.ts            # Tipos de API de unidades
│       ├── folios.ts           # Tipos de API de folios
│       ├── contacts.ts         # Tipos de API de contactos
│       ├── ledger-accounts.ts  # Tipos de API de cuentas contables ⭐ NUEVO
│       ├── reservation-notes.ts # Tipos de API de notas de reservaciones ⭐ NUEVO
│       └── nodes.ts            # Tipos de API de nodos (propiedades/ubicaciones) ⭐ NUEVO
└── dist/                       # Archivos compilados
```

### Scripts Disponibles

```bash
# Desarrollo
npm run build      # Compilar TypeScript
npm run start      # Ejecutar servidor compilado
npm run dev        # Desarrollo con recarga automática

# Testing
npm run test:unit          # Tests unitarios (195 tests)
npm run test:integration   # Tests de integración
npm run test:e2e          # Tests E2E
npm run test:all          # Todos los tests
npm run test:coverage     # Tests con cobertura
npm run test:ci           # Tests en modo CI
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
- [x] Consulta Individual de Unidades ⭐ **COMPLETADO**
- [x] Gestión de Folios (Bills/Receipts)
- [x] Gestión de Huéspedes (Contacts)
- [x] Gestión de Cuentas Contables (Ledger Accounts) ⭐ **COMPLETADO**
- [x] Consulta Individual de Cuentas Contables ⭐ **COMPLETADO**
- [x] Gestión de Notas de Reservaciones ⭐ **COMPLETADO**


### Mejoras Técnicas
- [x] Tests automatizados ⭐ **COMPLETADO**


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