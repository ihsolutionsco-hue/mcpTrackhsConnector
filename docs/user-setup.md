# Guía de Configuración para Usuarios - Track HS MCP Remote

## Configuración del Conector

### URL del Conector
```
https://trackhs-mcp-remote.tu-subdomain.workers.dev/mcp
```

## Configuración en Claude

### Claude Web (claude.ai)

1. **Ir a Configuración:**
   - Hacer clic en tu avatar en la esquina superior derecha
   - Seleccionar "Settings"

2. **Acceder a Conectores:**
   - En el menú lateral, hacer clic en "Connectors"

3. **Agregar Conector Personalizado:**
   - Hacer clic en "Add custom connector" en la parte inferior de la sección
   - Pegar la URL del conector: `https://trackhs-mcp-remote.tu-subdomain.workers.dev/mcp`
   - Hacer clic en "Add"

4. **Habilitar el Conector:**
   - El conector aparecerá en la lista
   - Hacer clic en el botón "Search and tools" en la parte inferior izquierda del chat
   - Seleccionar el conector Track HS para habilitarlo

### Claude Desktop

1. **Ir a Configuración:**
   - Abrir Claude Desktop
   - Hacer clic en el ícono de configuración (⚙️)

2. **Acceder a Conectores:**
   - Seleccionar "Connectors" en el menú lateral

3. **Agregar Conector Personalizado:**
   - Hacer clic en "Add custom connector"
   - Pegar la URL del conector: `https://trackhs-mcp-remote.tu-subdomain.workers.dev/mcp`
   - Hacer clic en "Add"

4. **Habilitar el Conector:**
   - El conector aparecerá en la lista
   - Hacer clic en el botón "Search and tools" en la parte inferior izquierda del chat
   - Seleccionar el conector Track HS para habilitarlo

## Uso del Conector

### Herramientas Disponibles

Una vez habilitado, Claude tendrá acceso a las siguientes herramientas:

#### 🔍 **get_reviews**
- Consultar reseñas de propiedades
- Filtrar por fecha, contenido, rating
- Paginación y ordenamiento

#### 🏨 **get_reservation**
- Obtener detalles completos de una reservación específica
- Información de huéspedes, pagos, políticas

#### 🔎 **search_reservations**
- Búsqueda avanzada de reservaciones
- Filtros por fechas, estados, nodos, unidades
- Búsqueda por texto y tags

#### 🏠 **get_units**
- Consultar unidades de alojamiento
- Filtros por características físicas (dormitorios, baños)
- Filtros por políticas (mascotas, eventos, fumadores)
- Filtros de disponibilidad

#### 📄 **get_folios_collection**
- Consultar folios y facturas
- Filtros por tipo, estado, contacto
- Información de balances y pagos

#### 👥 **get_contacts**
- Acceso al CRM de contactos
- Búsqueda por nombre, email, teléfono
- Información de huéspedes, propietarios, empleados

### Ejemplos de Consultas

#### Consultas de Reseñas
```
"Muéstrame las últimas 10 reseñas de propiedades"
"Busca reseñas que contengan 'excelente' en los comentarios"
"Obtén reseñas actualizadas desde el 2024-01-01"
```

#### Consultas de Reservaciones
```
"Muestra los detalles de la reservación #12345"
"Busca todas las reservaciones confirmadas"
"Encuentra reservaciones de llegada entre el 1 y 15 de enero de 2024"
"Muéstrame reservaciones del nodo 123 con estado 'Checked In'"
```

#### Consultas de Unidades
```
"Muéstrame todas las unidades disponibles"
"Busca unidades con 3 dormitorios o más"
"Encuentra unidades que permitan mascotas"
"Busca unidades disponibles entre el 1 y 15 de marzo de 2024"
```

#### Consultas de Folios
```
"Muéstrame todos los folios abiertos"
"Busca folios del huésped con ID 12345"
"Encuentra folios de tipo 'guest' ordenados por balance actual"
```

#### Consultas de Contactos
```
"Muéstrame todos los contactos VIP"
"Busca contactos por email 'john@example.com'"
"Encuentra contactos que contengan 'Smith' en el nombre"
```

## Solución de Problemas

### El Conector No Aparece
- Verificar que la URL del conector sea correcta
- Asegurarse de que el servidor esté desplegado y funcionando
- Verificar la conexión a internet

### Error de Conexión
- Verificar que el servidor esté en línea
- Comprobar que la URL no tenga errores de tipeo
- Intentar nuevamente en unos minutos

### Herramientas No Disponibles
- Asegurarse de que el conector esté habilitado
- Verificar que se esté usando el botón "Search and tools"
- Comprobar que Claude tenga permisos para usar las herramientas

### Datos No Encontrados
- Verificar que los parámetros de búsqueda sean correctos
- Comprobar que los IDs existan en el sistema
- Revisar que los filtros de fecha sean válidos

## Seguridad y Privacidad

### Datos Sensibles
- El conector accede a datos de Track HS a través de credenciales seguras
- Las credenciales se almacenan de forma encriptada en Cloudflare
- No se almacenan datos localmente en tu dispositivo

### Permisos
- El conector solo puede leer datos, no modificarlos
- No se pueden realizar cambios en el sistema Track HS
- Todas las operaciones son de solo lectura

### Privacidad
- Las consultas se procesan de forma segura
- No se almacenan logs de las consultas
- Los datos se transmiten de forma encriptada

## Soporte

Si tienes problemas con el conector:

1. **Verificar la URL:** Asegúrate de que la URL del conector sea correcta
2. **Revisar la conexión:** Verifica que tengas conexión a internet
3. **Contactar soporte:** Si el problema persiste, contacta al administrador del sistema

## Actualizaciones

El conector se actualiza automáticamente. No necesitas hacer nada para recibir las últimas funcionalidades.

---

**Nota:** Este conector está diseñado para uso profesional. Asegúrate de tener los permisos necesarios para acceder a los datos de Track HS.
