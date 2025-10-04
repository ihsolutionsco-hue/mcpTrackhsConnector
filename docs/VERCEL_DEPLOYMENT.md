# 🚀 Despliegue en Vercel - Track HS MCP Connector

## 📋 Resumen

Este documento explica cómo desplegar el conector MCP de Track HS en Vercel para tener un servidor remoto accesible online con GitHub Actions para CI/CD automático.

## 🎯 Objetivos

- ✅ **Despliegue automático** en Vercel desde GitHub
- ✅ **CI/CD completo** con GitHub Actions
- ✅ **Conector MCP remoto** accesible online
- ✅ **Configuración simple** para usuarios finales

## 🚀 Configuración Rápida

### **Paso 1: Fork del Repositorio**

```bash
# 1. Fork este repositorio en GitHub
# 2. Clonar tu fork
git clone https://github.com/tu-usuario/trackhs-mcp-connector.git
cd trackhs-mcp-connector

# 3. Instalar dependencias
npm install
```

### **Paso 2: Configurar Vercel**

```bash
# 1. Instalar Vercel CLI
npm install -g vercel@latest

# 2. Login en Vercel
vercel login

# 3. Configurar proyecto
vercel

# 4. Desplegar a producción
vercel --prod
```

### **Paso 3: Configurar Variables de Entorno en Vercel**

En el dashboard de Vercel (https://vercel.com/dashboard):

1. Ve a tu proyecto
2. Settings → Environment Variables
3. Agregar las siguientes variables:

```
TRACKHS_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
NODE_ENV=production
```

### **Paso 4: Configurar GitHub Secrets**

En GitHub Settings → Secrets and variables → Actions:

```
VERCEL_TOKEN=tu_vercel_token
VERCEL_ORG_ID=tu_org_id
VERCEL_PROJECT_ID=tu_project_id
TRACKHS_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

## 📡 Uso del Conector Remoto

### **URL del Conector**
```
https://tu-app.vercel.app/api
```

### **Endpoints Disponibles**

#### **1. Health Check**
```bash
GET https://tu-app.vercel.app/api/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Track HS MCP Connector",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "tools": {
    "count": 12,
    "available": ["get_reviews", "get_contacts", ...]
  }
}
```

#### **2. Listar Herramientas**
```bash
GET https://tu-app.vercel.app/api/tools
```

**Respuesta:**
```json
{
  "success": true,
  "tools": [
    {
      "name": "get_reviews",
      "description": "Retrieve paginated collection of property reviews",
      "inputSchema": { ... }
    }
  ],
  "count": 12
}
```

#### **3. Ejecutar Herramienta**
```bash
POST https://tu-app.vercel.app/api/tools/get_reviews/execute
Content-Type: application/json

{
  "name": "get_reviews",
  "arguments": {
    "page": 1,
    "size": 10
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "result": { ... },
  "tool": "get_reviews",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🔧 Configuración en Claude Desktop

### **Método 1: Custom Connector (Recomendado)**

1. Abre Claude Desktop
2. Ve a Settings → Connectors
3. Click "Add custom connector"
4. Ingresa la URL: `https://tu-app.vercel.app/api`
5. Click "Add"

### **Método 2: Configuración Manual**

Edita tu archivo de configuración de Claude Desktop:

```json
{
  "mcpServers": {
    "trackhs-remote": {
      "url": "https://tu-app.vercel.app/api",
      "auth": {
        "type": "none"
      }
    }
  }
}
```

## 🛠️ Desarrollo Local

### **Comandos Disponibles**

```bash
# Desarrollo local
npm run dev

# Desarrollo con Vercel
npm run dev:vercel

# Build del proyecto
npm run build

# Tests
npm run test:all

# Setup automático para Vercel
npm run setup:vercel
```

### **Estructura del Proyecto**

```
trackhs-mcp-connector/
├── api/
│   └── index.ts              # Servidor API para Vercel
├── src/                      # Código fuente original
├── .github/workflows/        # GitHub Actions
├── vercel.json              # Configuración de Vercel
├── env.example              # Variables de entorno
└── docs/
    └── VERCEL_DEPLOYMENT.md # Esta documentación
```

## 🚀 CI/CD Automático

### **Flujo de Despliegue**

1. **Push a `main`** → Despliegue automático a producción
2. **Pull Request** → Despliegue de preview
3. **Tests automáticos** → Ejecutados antes del despliegue

### **GitHub Actions**

El repositorio incluye GitHub Actions configurado para:

- ✅ **Tests automáticos** (unitarios, integración, E2E)
- ✅ **Build automático** del proyecto
- ✅ **Despliegue automático** a Vercel
- ✅ **Notificaciones** de estado

### **Monitoreo**

- **Health Check**: `https://tu-app.vercel.app/api/health`
- **Logs**: Disponibles en Vercel Dashboard
- **Métricas**: Performance en Vercel Analytics
- **GitHub Actions**: Estado en la pestaña Actions

## 🔧 Solución de Problemas

### **Error: Variables de entorno no configuradas**

```
Error: Variable de entorno requerida no configurada: TRACKHS_USERNAME
```

**Solución:**
1. Verificar variables en Vercel Dashboard
2. Re-desplegar el proyecto
3. Verificar que las variables estén en el entorno correcto (Production)

### **Error: Build fallido**

```
Error: Build failed
```

**Solución:**
1. Verificar que `npm run build` funcione localmente
2. Revisar logs en Vercel Dashboard
3. Verificar configuración de TypeScript

### **Error: Tests fallidos en CI**

```
Error: Tests failed in CI
```

**Solución:**
1. Verificar que los tests pasen localmente
2. Revisar configuración de GitHub Secrets
3. Verificar variables de entorno en GitHub Actions

### **Error: Conector no funciona en Claude**

```
Error: Connection failed
```

**Solución:**
1. Verificar que la URL sea correcta
2. Probar el health check manualmente
3. Verificar que el servidor esté desplegado

## 📊 Métricas y Monitoreo

### **Vercel Analytics**

- **Visitas**: Número de requests al conector
- **Performance**: Tiempo de respuesta
- **Errores**: Rate de errores
- **Regiones**: Distribución geográfica

### **GitHub Actions**

- **Tiempo de build**: Duración de tests y despliegue
- **Rate de éxito**: Porcentaje de builds exitosos
- **Historial**: Logs de todos los despliegues

### **Logs del Servidor**

```bash
# Ver logs en Vercel
vercel logs

# Ver logs específicos
vercel logs --follow
```

## 🎯 Próximos Pasos

### **Mejoras Futuras**

- [ ] **Autenticación JWT** para mayor seguridad
- [ ] **Rate limiting** por usuario
- [ ] **Métricas avanzadas** con Prometheus
- [ ] **Cache** para respuestas frecuentes
- [ ] **Webhooks** para notificaciones

### **Escalabilidad**

- [ ] **Multi-tenant** para múltiples clientes
- [ ] **Load balancing** automático
- [ ] **CDN** para assets estáticos
- [ ] **Database** para persistencia

## 📚 Recursos Adicionales

### **Documentación Oficial**

- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Track HS API](https://docs.trackhs.com/)

### **Herramientas**

- **Vercel CLI**: `npm install -g vercel`
- **GitHub CLI**: `gh auth login`
- **Node.js**: Versión 18+
- **TypeScript**: Compilación automática

---

## ✅ Checklist de Despliegue

- [ ] Fork del repositorio
- [ ] Configurar Vercel CLI
- [ ] Desplegar proyecto inicial
- [ ] Configurar variables de entorno en Vercel
- [ ] Configurar GitHub Secrets
- [ ] Probar health check
- [ ] Probar herramientas
- [ ] Configurar en Claude Desktop
- [ ] Verificar CI/CD automático

**🎉 ¡Conector MCP remoto funcionando!**

---

**Estado**: ✅ **Implementación Completa**  
**Despliegue**: Vercel + GitHub Actions  
**CI/CD**: Automático con tests  
**Monitoreo**: Vercel Analytics + GitHub Actions
