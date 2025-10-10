#  Documentación - Track HS MCP Connector

##  Resumen Ejecutivo

**Track HS MCP Connector** es un servidor MCP (Model Context Protocol) remoto que conecta Claude con la API de Track HS, proporcionando 13 herramientas especializadas para gestión de propiedades, reservaciones, contactos, contabilidad y mantenimiento.

### ** Estado del Proyecto: COMPLETADO**
- **Versión**: 1.0.0
- **Servidor MCP**: 100% funcional
- **Herramientas**: 13 herramientas implementadas
- **Deploy**: Activo en Vercel
- **Testing**: Estrategia completa implementada

---

##  Tabla de Contenidos

1. [Configuración Rápida](#-configuración-rápida)
2. [Herramientas Disponibles](#-herramientas-disponibles)
3. [Configuración en Claude](#-configuración-en-claude)
4. [Desarrollo](#-desarrollo)
5. [Testing](#-testing)
6. [Troubleshooting](#-troubleshooting)

---

##  Configuración Rápida

### **Variables de Entorno Requeridas**
```bash
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

### **URLs de Despliegue**
- **Claude Web (Recomendado)**: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web`
- **Claude Web (Alternativo)**: `https://trackhs-mcp-connector.vercel.app/api/mcp-real`
- **Claude Desktop**: `node dist/index.js`

---

##  Herramientas Disponibles

| Herramienta | Descripción |
|-------------|-------------|
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

##  Configuración en Claude

### **Claude Desktop**
1. Configura `claude_desktop_config.json`:
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

2. Compila: `npm run build`
3. Reinicia Claude Desktop

### **Claude Web**
1. Ve a Settings > Connectors
2. Agrega custom connector con URL: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web`

---

##  Desarrollo

### **Comandos Principales**
```bash
# Desarrollo
npm run dev

# Testing
npm run test:all

# Build
npm run build

# Deploy
npm run deploy
```

### **Estructura del Proyecto**
```
src/
 core/           # Core del servidor MCP
 tools/          # Herramientas MCP
 types/          # Tipos TypeScript
 index.ts        # Punto de entrada
 server.ts       # Servidor principal
```

---

##  Testing

### **Estrategia de Testing**
- **Unit Tests**: `npm run test:unit`
- **Integration Tests**: `npm run test:integration`
- **E2E Tests**: `npm run test:e2e`
- **All Tests**: `npm run test:all`

### **Cobertura**
```bash
npm run test:coverage
```

---

##  Troubleshooting

### **Problemas Comunes**

**Claude no se conecta:**
- Verifica la URL del servidor
- Comprueba que el servidor esté funcionando
- Revisa los logs de Claude

**Error de autenticación:**
- Verifica las credenciales de Track HS
- Comprueba las variables de entorno
- Revisa la configuración de autenticación

**Herramientas no funcionan:**
- Verifica la conexión con Track HS API
- Comprueba los parámetros de entrada
- Revisa los logs del servidor

---

##  Soporte

- **GitHub Issues**: Para reportar problemas
- **Documentación**: Guías completas en `/docs`
- **Email**: Soporte técnico

---

**¡Listo para usar!** 

*Última actualización: 2025-01-27*