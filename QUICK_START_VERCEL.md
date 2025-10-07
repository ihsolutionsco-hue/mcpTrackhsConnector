# 🚀 Guía Rápida de Despliegue en Vercel

## ✅ Pre-requisitos
- ✅ Cuenta en [Vercel](https://vercel.com)
- ✅ Cuenta en GitHub
- ✅ Credenciales de Track HS API

---

## 📦 Paso 1: Preparar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/MCPtrackhsConnector.git
cd MCPtrackhsConnector

# Instalar dependencias
npm install

# Verificar que el build funciona
npm run build
```

---

## 🌐 Paso 2: Crear Proyecto en Vercel

### Opción A: Desde el Dashboard de Vercel (Recomendado)

1. Ve a [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Click en **"Add New Project"**
3. Click en **"Import Git Repository"**
4. Selecciona tu repositorio **MCPtrackhsConnector**
5. Click en **"Import"**

### Configuración del Proyecto:

```
Framework Preset: Other
Root Directory: ./
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Node Version: 18.x
```

6. **NO hagas clic en Deploy todavía** - primero configura las variables de entorno

---

## 🔐 Paso 3: Configurar Variables de Entorno

1. En la página de configuración del proyecto, ve a **"Environment Variables"**
2. Agrega las siguientes variables:

### Variables Obligatorias:

| Variable | Valor | Entorno |
|----------|-------|---------|
| `TRACKHS_API_URL` | `https://ihmvacations.trackhs.com/api` | Production, Preview, Development |
| `TRACKHS_USERNAME` | `aba99777416466b6bdc1a25223192ccb` | Production, Preview, Development |
| `TRACKHS_PASSWORD` | `18c874610113f355cc11000a24215cbda` | Production, Preview, Development |
| `NODE_ENV` | `production` | Production |

**⚠️ IMPORTANTE:** Asegúrate de seleccionar **todos los entornos** (Production, Preview, Development) para cada variable.

---

## 🚀 Paso 4: Desplegar

1. Click en **"Deploy"**
2. Espera 2-3 minutos mientras Vercel construye y despliega tu proyecto
3. Una vez completado, verás una URL como: `https://tu-proyecto.vercel.app`

---

## ✅ Paso 5: Verificar el Despliegue

### Verificar Configuración:

```bash
# Ejecutar script de verificación
npm run verify:vercel
```

Este script verificará:
- ✅ Variables de entorno configuradas
- ✅ URL de API válida
- ✅ Conectividad con Track HS
- ✅ Configuración de Vercel
- ✅ Archivo API implementado

### Probar el Health Check:

```bash
curl https://tu-proyecto.vercel.app/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "Track HS MCP Connector",
  "version": "1.0.0",
  "tools": {
    "count": 13,
    "available": ["get_reviews", "get_contacts", ...]
  },
  "environment": {
    "trackhsConfigured": true
  }
}
```

### Listar Herramientas:

```bash
curl https://tu-proyecto.vercel.app/api/tools
```

### Ejecutar una Herramienta:

```bash
curl -X POST https://tu-proyecto.vercel.app/api/tools/get_reviews/execute \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_reviews",
    "arguments": {
      "page": 1,
      "size": 5
    }
  }'
```

---

## 🔧 Uso del Conector

### A. En Claude Desktop

Agrega esta configuración a tu archivo de Claude Desktop:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trackhs": {
      "url": "https://tu-proyecto.vercel.app/api"
    }
  }
}
```

### B. En Make.com

1. Crea un nuevo escenario
2. Agrega módulo **HTTP** → **Make a Request**
3. Configura:

```
URL: https://tu-proyecto.vercel.app/api/tools/get_reviews/execute
Method: POST
Headers:
  Content-Type: application/json
Body:
{
  "name": "get_reviews",
  "arguments": {
    "page": 1,
    "size": 10
  }
}
```

### C. Desde Cualquier Aplicación

Usa los siguientes endpoints:

```
GET  /api/health              - Health check
GET  /api/tools               - Listar herramientas disponibles
POST /api/tools/{name}/execute - Ejecutar herramienta
```

---

## 📊 Herramientas Disponibles

| Herramienta | Descripción |
|-------------|-------------|
| `get_reviews` | Obtener reseñas de propiedades |
| `get_reservation` | Obtener detalles de una reservación |
| `search_reservations` | Buscar reservaciones con filtros |
| `get_units` | Obtener unidades de alojamiento |
| `get_unit` | Obtener detalles de una unidad |
| `get_folios_collection` | Obtener folios/facturas |
| `get_contacts` | Obtener contactos del CRM |
| `get_ledger_accounts` | Obtener cuentas contables |
| `get_ledger_account` | Obtener detalles de una cuenta |
| `get_reservation_notes` | Obtener notas de reservaciones |
| `get_nodes` | Obtener nodos/propiedades |
| `get_node` | Obtener detalles de un nodo |
| `get_maintenance_work_orders` | Obtener órdenes de trabajo |

---

## 🔄 Actualizar el Despliegue

Cada vez que hagas push a GitHub, Vercel desplegará automáticamente:

```bash
git add .
git commit -m "Actualización del conector"
git push origin main
```

Vercel detectará el cambio y desplegará automáticamente en ~2 minutos.

---

## 🐛 Solución de Problemas

### Error: "Variables de entorno no configuradas"

**Diagnóstico:**
```bash
npm run verify:vercel
```

**Solución:**
1. Ve a Vercel Dashboard → Tu Proyecto → Settings → Environment Variables
2. Verifica que todas las variables estén configuradas:
   - `TRACKHS_API_URL`
   - `TRACKHS_USERNAME`
   - `TRACKHS_PASSWORD`
   - `NODE_ENV=production`
3. Re-despliega el proyecto (Deployments → ... → Redeploy)

### Error: "Build failed"

**Diagnóstico:**
```bash
# Verificar build local
npm run build

# Verificar configuración
npm run verify:vercel
```

**Solución:**
1. Verifica que `npm run build` funcione localmente
2. Revisa los logs en Vercel Dashboard → Deployments → View Function Logs
3. Asegúrate de que Node.js versión sea 18.x
4. Verifica que `api/index.js` esté implementado correctamente

### Error: "FUNCTION_INVOCATION_FAILED"

**Diagnóstico:**
```bash
# Verificar implementación
npm run verify:vercel

# Ver logs de Vercel
vercel logs --follow
```

**Solución:**
1. Verifica que `api/index.js` no esté en modo demostración
2. Confirma que las variables de entorno estén configuradas
3. Verifica que la URL de Track HS sea accesible
4. Re-despliega el proyecto

### Error: "Tool not found"

**Solución:**
1. Verifica que el endpoint sea correcto: `/api/tools/{nombre}/execute`
2. Lista las herramientas disponibles: `GET /api/tools`
3. Usa el nombre exacto de la herramienta (ej: `get_reviews`, no `getReviews`)

### Error de Conectividad con Track HS

**Diagnóstico:**
```bash
# Probar conectividad
curl -I $TRACKHS_API_URL

# Verificar credenciales
npm run verify:vercel
```

**Solución:**
1. Verifica que la URL de Track HS sea correcta
2. Confirma que las credenciales sean válidas
3. Verifica que el servicio de Track HS esté disponible
4. Revisa los logs de Vercel para errores específicos

---

## 📚 Documentación Adicional

- [Documentación completa](./docs/VERCEL_DEPLOYMENT.md)
- [Uso de herramientas](./Readme.md)
- [Tests](./docs/TESTING.md)

---

## ✅ Checklist de Despliegue

- [ ] Repositorio clonado
- [ ] Dependencias instaladas
- [ ] Build exitoso localmente (`npm run build`)
- [ ] Verificación de configuración (`npm run verify:vercel`)
- [ ] Proyecto creado en Vercel
- [ ] Variables de entorno configuradas:
  - [ ] `TRACKHS_API_URL`
  - [ ] `TRACKHS_USERNAME`
  - [ ] `TRACKHS_PASSWORD`
  - [ ] `NODE_ENV=production`
- [ ] Despliegue completado
- [ ] Health check funciona (`/api/health`)
- [ ] Lista de herramientas funciona (`/api/tools`)
- [ ] Al menos una herramienta probada (`/api/tools/{name}/execute`)
- [ ] Configurado en Claude Desktop o Make.com

---

**🎉 ¡Listo! Tu conector MCP está funcionando online.**

**URL de tu API:** `https://tu-proyecto.vercel.app/api`
