# 🌐 Configuración de Claude Web para Track HS MCP

## 📋 **Guía Paso a Paso**

### **Paso 1: Acceder a Claude Web**

1. **Abre tu navegador**
2. **Ve a [claude.ai](https://claude.ai)**
3. **Inicia sesión con tu cuenta**

### **Paso 2: Configurar Custom Connector**

1. **Haz clic en tu avatar** (esquina superior derecha)
2. **Selecciona "Settings"**
3. **En el menú lateral, haz clic en "Connectors"**
4. **Haz clic en "Add custom connector"**

### **Paso 3: Configurar el Conector**

Completa los campos con la siguiente información:

#### **Información Básica:**
- **Nombre del conector**: `Track HS MCP Connector`
- **URL del servidor MCP remoto**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude`

#### **Configuración Avanzada (Opcional):**
- **OAuth Client ID**: (Dejar vacío)
- **OAuth Client Secret**: (Dejar vacío)
- **Headers personalizados**: (Dejar vacío)

### **Paso 4: Guardar y Conectar**

1. **Haz clic en "Add"**
2. **Espera a que se establezca la conexión**
3. **Verifica que aparezca como "Connected"**

### **Paso 5: Activar Herramientas**

1. **En la interfaz de chat, haz clic en el ícono de herramientas** (🔧)
2. **Selecciona "Search and tools"**
3. **Activa las herramientas de Track HS que necesites**
4. **Haz clic en "Connect"**

## 🧪 **Probar la Conexión**

### **Comandos de Prueba:**

```
# Obtener contactos
"Obtén los primeros 5 contactos de Track HS"

# Buscar reservas
"Busca reservas confirmadas en Track HS"

# Obtener propiedades
"Muéstrame las propiedades disponibles en Track HS"

# Obtener cuentas contables
"Lista las cuentas contables activas"
```

## 🔧 **Troubleshooting**

### **Problema: No se puede conectar**
**Solución:**
1. Verifica que la URL sea correcta: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude`
2. Verifica que el servidor esté funcionando
3. Revisa la consola del navegador para errores
4. Intenta con la URL alternativa: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude`

### **Problema: Herramientas no aparecen**
**Solución:**
1. Verifica que el conector esté conectado
2. Revisa que las herramientas estén activadas
3. Reinicia la página de Claude
4. Verifica los permisos del conector

### **Problema: Error de autenticación**
**Solución:**
1. Verifica que las variables de entorno estén configuradas en Vercel
2. Revisa los logs del servidor
3. Contacta al administrador del sistema

## 📊 **URLs Alternativas**

Si la URL principal no funciona, prueba estas alternativas:

### **URLs de Respaldo:**
- **SSE**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude`
- **HTTP**: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude`
- **SSE Final**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-final/sse`
- **SSE Real**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-real/sse`

## 🎯 **Herramientas Disponibles**

### **📞 CRM y Contactos:**
- `get_contacts` - Obtener lista de contactos
- `get_reservation_notes` - Obtener notas de reservas

### **🏠 Propiedades y Unidades:**
- `get_nodes` - Obtener propiedades/nodos
- `get_node` - Obtener propiedad específica
- `get_units` - Obtener unidades disponibles
- `get_unit` - Obtener unidad específica

### **📅 Reservas:**
- `get_reservation` - Obtener reserva específica
- `search_reservations` - Buscar reservas

### **💰 Contabilidad:**
- `get_ledger_accounts` - Obtener cuentas contables
- `get_ledger_account` - Obtener cuenta específica
- `get_folios_collection` - Obtener folios/facturas

### **🔧 Mantenimiento:**
- `get_maintenance_work_orders` - Obtener órdenes de trabajo

### **⭐ Reseñas:**
- `get_reviews` - Obtener reseñas de propiedades

## ✅ **Checklist de Configuración**

- [ ] Claude Web abierto y logueado
- [ ] Navegado a Settings > Connectors
- [ ] Custom connector creado
- [ ] URL configurada correctamente
- [ ] Conector conectado exitosamente
- [ ] Herramientas activadas
- [ ] Pruebas de comandos exitosas

## 🆘 **Soporte**

### **Verificación de Estado del Servidor:**
```bash
# Health check
curl https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude/health

# Listar herramientas
curl https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude/tools
```

### **Logs y Debugging:**
1. Abre las herramientas de desarrollador del navegador (F12)
2. Ve a la pestaña "Console"
3. Busca errores relacionados con MCP
4. Revisa la pestaña "Network" para ver las peticiones

---

**¡Configuración completada!** 🎉
