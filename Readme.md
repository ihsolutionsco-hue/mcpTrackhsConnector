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

- **URL**: `https://trackhs-mcp-connector.vercel.app/api/mcp`
- **13 herramientas** activas
- **4 resources** disponibles
- **5 prompts** para workflows
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

## 🤖 **Configuración Rápida**

### **Claude Desktop (Recomendado)**
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

### **Claude Web**
- **URL**: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web`
- Ve a Settings > Connectors > Add custom connector

---

## 🚀 **Desarrollo Local**

```bash
# Instalación
npm install

# Desarrollo
npm run dev

# Testing
npm run test:all

# Deploy
npm run deploy
```

---

## 📚 **Documentación**

- **[docs/README.md](./docs/README.md)** - Documentación completa
- **[docs/setup.md](./docs/setup.md)** - Guía de configuración
- **[docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Guía de desarrollo
- **[docs/TESTING.md](./docs/TESTING.md)** - Estrategia de testing

---

## 🎯 **URLs para Claude**

```
# Claude Web (Recomendado) ⭐
https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web

# Claude Web (Alternativo)
https://trackhs-mcp-connector.vercel.app/api/mcp-real

# Claude Desktop (Local)
node dist/index.js
```

---

## 📞 **Soporte**

- **GitHub Issues**: Para reportar problemas
- **Documentación**: Guías completas en `/docs`
- **Email**: Soporte técnico

---

**¡Listo para usar!** 🎉

*Última actualización: 2025-01-27*