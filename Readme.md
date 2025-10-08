# 🚀 Track HS MCP Connector

[![Deploy Status](https://img.shields.io/badge/Deploy-Vercel-00C7B7?style=flat-square&logo=vercel)](https://trackhs-mcp-connector.vercel.app)
[![Node Version](https://img.shields.io/badge/Node.js-20+-green?style=flat-square&logo=node.js)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**Conector MCP remoto** que conecta Claude con la API de Track HS. Permite acceder a datos de propiedades, reservas, contactos, contabilidad y más.

## ✨ **¿Qué hace?**

- 🎯 **13 herramientas** para gestionar propiedades y reservas
- 🤖 **Conecta Claude** con Track HS API
- 🌐 **Funciona en la nube** (Vercel)
- 🔐 **Seguro** con autenticación

## 🚀 **Estado: ✅ FUNCIONANDO**

- **URL**: `https://trackhs-mcp-connector.vercel.app`
- **13 herramientas** activas
- **Conexión real** con Track HS
- **Tiempo de respuesta**: ~200ms

---

## 🛠️ **Herramientas Disponibles**

| Herramienta | ¿Qué hace? |
|-------------|------------|
| `get_contacts` | Lista contactos del CRM |
| `get_reservation` | Detalles de una reserva |
| `search_reservations` | Buscar reservas |
| `get_units` | Lista de unidades |
| `get_unit` | Detalle de unidad |
| `get_reviews` | Reseñas de propiedades |
| `get_folios_collection` | Facturas contables |
| `get_ledger_accounts` | Cuentas contables |
| `get_ledger_account` | Cuenta específica |
| `get_reservation_notes` | Notas de reservas |
| `get_nodes` | Propiedades/nodos |
| `get_node` | Propiedad específica |
| `get_maintenance_work_orders` | Órdenes de trabajo |

---

## 🤖 **Configurar en Claude**

### **Opción 1: Claude Desktop (Recomendado)**

1. **Configura tu archivo `claude_desktop_config.json`**:
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

2. **Compila tu servidor**:
```bash
npm run build
```

3. **Reinicia Claude Desktop**

### **Opción 2: Claude Web (Custom Connectors)**

1. **Ve a Settings > Connectors**
2. **Haz clic en "Add custom connector"**
3. **Completa los campos**:
   - **Nombre**: `Track HS MCP Connector`
   - **URL del servidor MCP remoto**: `https://trackhs-mcp-connector.vercel.app/api/mcp-real` ⭐ **RECOMENDADO**
4. **Haz clic en "Add"**

---

## 🔧 **Configuración Requerida**

### **Variables de Entorno**
```bash
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

### **URLs Disponibles**

#### **🎯 URLs Recomendadas para Claude**
- **Claude Web (MCP Real)**: `https://trackhs-mcp-connector.vercel.app/api/mcp-real` ⭐ **RECOMENDADO**
- **Claude Web (SSE)**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude`
- **Claude Web (HTTP)**: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude`

#### **📊 URLs de Diagnóstico**
- **Principal**: `https://trackhs-mcp-connector.vercel.app/api`
- **MCP SSE Final**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-final/sse`
- **MCP SSE Real**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-real/sse`
- **MCP Remoto**: `https://trackhs-mcp-connector.vercel.app/api/remote-mcp`

---

## 🧪 **Probar el Conector**

### **1. Health Check**
```bash
curl https://trackhs-mcp-connector.vercel.app/api
```

### **2. Listar Herramientas (Servidor MCP Real)**
```bash
curl https://trackhs-mcp-connector.vercel.app/api/mcp-real/tools
```

### **3. Probar Protocolo MCP (JSON-RPC 2.0)**
```bash
# Inicializar conexión MCP
curl -X POST https://trackhs-mcp-connector.vercel.app/api/mcp-real \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"elicitation":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'

# Listar herramientas MCP
curl -X POST https://trackhs-mcp-connector.vercel.app/api/mcp-real \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

### **4. Health Check (Servidor MCP Real)**
```bash
curl https://trackhs-mcp-connector.vercel.app/api/mcp-real/health
```

---

## 🚀 **Desarrollo Local**

### **Instalación**
```bash
# Clonar repositorio
git clone https://github.com/ihsolutionsco-hue/mcpTrackhsConnector.git
cd mcpTrackhsConnector

# Instalar dependencias
npm install

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales
```

### **Comandos**
```bash
# Desarrollo
npm run dev

# Testing
npm run test:all

# Deploy
npm run deploy
```

---

## 📊 **Ejemplos de Uso**

### **Obtener Contactos**
```json
{
  "name": "get_contacts",
  "arguments": {
    "page": 1,
    "size": 10,
    "search": "john"
  }
}
```

### **Buscar Reservas**
```json
{
  "name": "search_reservations",
  "arguments": {
    "page": 1,
    "size": 5,
    "status": "confirmed"
  }
}
```

### **Obtener Unidades**
```json
{
  "name": "get_units",
  "arguments": {
    "page": 1,
    "size": 10,
    "nodeId": 123
  }
}
```

---

## 🔍 **Troubleshooting**

### **Problema: Claude no se conecta**
**Solución**: 
- Verifica que la URL sea correcta
- Comprueba que el servidor esté funcionando
- Revisa los logs de Claude

### **Problema: Error de autenticación**
**Solución**:
- Verifica las credenciales de Track HS
- Comprueba las variables de entorno
- Revisa la configuración de autenticación

### **Problema: Herramientas no funcionan**
**Solución**:
- Verifica la conexión con Track HS API
- Comprueba los parámetros de entrada
- Revisa los logs del servidor

---

## 📚 **Documentación Completa**

Para documentación detallada, consulta:
- **[DOCUMENTACION_COMPLETA.md](./DOCUMENTACION_COMPLETA.md)** - Documentación exhaustiva
- **[docs/README.md](./docs/README.md)** - Guía de desarrollo
- **[docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Guía de desarrollo
- **[docs/TESTING.md](./docs/TESTING.md)** - Estrategia de testing

---

## 🎯 **Estado del Proyecto**

### ✅ **COMPLETADO AL 100%**
- **Versión**: 1.0.0
- **13 Herramientas MCP**: Funcionando
- **6 Servidores MCP**: Desplegados
- **230+ Tests**: Funcionando
- **Documentación**: Completa
- **Deploy**: Activo en Vercel

### **URLs para Claude**

#### **🎯 URLs Recomendadas**
```
# Claude Web (MCP Real) - RECOMENDADO ⭐
https://trackhs-mcp-connector.vercel.app/api/mcp-real

# Claude Web (SSE) - Alternativo
https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude

# Claude Web (HTTP) - Alternativo
https://trackhs-mcp-connector.vercel.app/api/mcp-claude

# Claude Desktop (Local)
node dist/index.js
```

---

## 📞 **Soporte**

- **GitHub Issues**: Para reportar problemas
- **Documentación**: Guías completas
- **Email**: Soporte técnico

---

**¡Listo para usar!** 🎉

*Última actualización: 2025-10-07*