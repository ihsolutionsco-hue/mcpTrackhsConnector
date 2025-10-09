# Guía de Uso del Servidor MCP TrackHS

## 🚀 Servidor MCP Funcionando

El servidor MCP para TrackHS está desplegado y funcionando en:
- **URL Principal**: `https://trackhs-mcp-connector.vercel.app/api/mcp`
- **Health Check**: `https://trackhs-mcp-connector.vercel.app/api/health`
- **Tools List**: `https://trackhs-mcp-connector.vercel.app/api/tools`

## 🔧 Configuración en Claude

### Paso 1: Abrir Claude Desktop
1. Abre Claude Desktop
2. Ve a **Settings** → **Connectors**
3. Haz clic en **Add connector**

### Paso 2: Configurar Custom Connector
1. **Name**: `TrackHS MCP Server`
2. **URL**: `https://trackhs-mcp-connector.vercel.app/api/mcp`
3. **Transport**: `Streamable HTTP`
4. Haz clic en **Add**

### Paso 3: Verificar Conexión
- Claude debería mostrar "Connected" junto al connector
- Si hay errores, verifica que las variables de entorno estén configuradas en Vercel

## 🛠️ Herramientas Disponibles

### Tools (13 herramientas)
- `get_contacts` - Obtener contactos del CRM
- `get_reservation` - Obtener detalles de reservación
- `get_units` - Listar unidades de alojamiento
- `get_reviews` - Obtener reseñas de propiedades
- `search_reservations` - Buscar reservaciones
- `get_unit` - Obtener detalles de unidad específica
- `get_folios_collection` - Listar folios contables
- `get_ledger_accounts` - Listar cuentas contables
- `get_ledger_account` - Obtener cuenta contable específica
- `get_reservation_notes` - Obtener notas de reservación
- `get_nodes` - Listar nodos/propiedades
- `get_node` - Obtener detalles de nodo específico
- `get_maintenance_work_orders` - Listar órdenes de mantenimiento

### Resources (4 recursos)
- `trackhs://schema/reservations` - Esquema de datos de reservas
- `trackhs://schema/units` - Esquema de datos de unidades
- `trackhs://status/system` - Estado del sistema
- `trackhs://docs/api` - Documentación de la API

### Prompts (5 prompts)
- `check-today-reservations` - Revisar reservas de hoy
- `unit-availability` - Consultar disponibilidad de unidades
- `guest-contact-info` - Información de contacto de huéspedes
- `maintenance-summary` - Resumen de órdenes de mantenimiento
- `financial-analysis` - Análisis financiero básico

## 📝 Ejemplos de Uso

### 1. Obtener Contactos
```
Pregunta a Claude: "Obtén todos los contactos del CRM de TrackHS"
```

### 2. Revisar Reservas de Hoy
```
Pregunta a Claude: "Revisa las reservas de hoy usando el prompt check-today-reservations"
```

### 3. Consultar Disponibilidad
```
Pregunta a Claude: "Verifica la disponibilidad de unidades del 15 al 20 de octubre"
```

### 4. Análisis Financiero
```
Pregunta a Claude: "Haz un análisis financiero del mes actual"
```

## 🔍 Verificación del Estado

### Health Check
```bash
curl https://trackhs-mcp-connector.vercel.app/api/health
```

### Lista de Herramientas
```bash
curl https://trackhs-mcp-connector.vercel.app/api/tools
```

## ⚠️ Variables de Entorno Requeridas

El servidor necesita estas variables configuradas en Vercel:
- `TRACKHS_API_URL` - URL de la API de TrackHS
- `TRACKHS_USERNAME` - Usuario de TrackHS
- `TRACKHS_PASSWORD` - Contraseña de TrackHS

## 🐛 Solución de Problemas

### Error: "Variable de entorno requerida no configurada"
- Verifica que las variables de entorno estén configuradas en Vercel
- Ve a Vercel Dashboard → Project Settings → Environment Variables

### Error: "Herramienta desconocida"
- Verifica que el nombre de la herramienta sea correcto
- Usa `/api/tools` para ver la lista completa

### Error de CORS
- El servidor ya tiene CORS configurado correctamente
- Si persiste, verifica que estés usando la URL correcta

## 📊 Estado del Servidor

- ✅ **Build**: Funcionando correctamente
- ✅ **Deployment**: Desplegado en Vercel
- ✅ **Health Check**: Respondiendo
- ✅ **Tools**: 13 herramientas disponibles
- ✅ **Resources**: 4 recursos disponibles
- ✅ **Prompts**: 5 prompts disponibles
- ✅ **CORS**: Configurado correctamente

## 🎯 Próximos Pasos

1. **Configurar variables de entorno** en Vercel
2. **Probar conexión** desde Claude
3. **Ejecutar herramientas** para verificar funcionamiento
4. **Usar prompts** para workflows automatizados

---

**¡El servidor MCP está listo para usar!** 🎉
