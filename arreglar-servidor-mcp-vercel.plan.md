<!-- 3a28c436-55e7-41a8-b593-4ec1c6582691 45411ada-9ec4-4a5e-af65-63ebd5836b4b -->
# Plan: Arreglar Servidor MCP en Vercel

## Problema Identificado

Vercel está sirviendo el código fuente compilado (`dist/index.js`) en la ruta raíz en lugar de ejecutar las funciones serverless en `api/mcp.js`. Las peticiones GET/POST a `/api/mcp` retornan "Cannot GET/POST" porque Express no está siendo ejecutado correctamente como función serverless de Vercel.

## Solución

### 1. Convertir Express app a handler de Vercel serverless

**Archivo**: `api/mcp.js` (línea 669-670)

Cambiar:

```javascript
// Exportar handler para Vercel
export default app;
```

Por:

```javascript
// Exportar handler compatible con Vercel serverless
export default (req, res) => {
  return app(req, res);
};
```

**Razón**: Vercel espera una función handler `(req, res) => {}`, no una instancia de Express directamente.

### 2. Agregar manejo de métodos OPTIONS para CORS

**Archivo**: `api/mcp.js` (después de línea 616)

Agregar antes de las rutas GET:

```javascript
// Handle OPTIONS for CORS preflight
app.options('*', (req, res) => {
  res.status(200).end();
});
```

**Razón**: Asegurar que las peticiones CORS preflight funcionen correctamente.

### 3. Verificar estructura de carpetas

Confirmar que existe:

- `api/mcp.js` (función serverless)
- `api/health.js` (función serverless)
- `api/index.js` (página de información)

### 4. Actualizar vercel.json para mejor compatibilidad

**Archivo**: `vercel.json`

Agregar antes de `rewrites`:

```json
"routes": [
  { "src": "/api/mcp", "dest": "/api/mcp.js" },
  { "src": "/api/health", "dest": "/api/health.js" },
  { "src": "/api/tools", "dest": "/api/mcp.js" }
],
```

**Razón**: Proporcionar rutas explícitas adicionales a los rewrites.

### 5. Agregar logging de debug temporal

**Archivo**: `api/mcp.js` (línea 589)

Agregar al inicio del handler POST:

```javascript
app.post('/', async (req, res) => {
  console.log('POST request received:', {
    method: req.method,
    url: req.url,
    body: req.body
  });
  
  try {
    // ... código existente
```

**Razón**: Diagnosticar si las peticiones están llegando correctamente al handler.

### 6. Redeploy y verificación

- Hacer deploy a Vercel
- Probar endpoints:
  - GET `/api/health` (debe retornar JSON con status)
  - GET `/api/mcp` (debe retornar info del servidor)
  - POST `/api/mcp` con JSON-RPC (debe procesar petición MCP)
- Verificar logs en Vercel dashboard

## Archivos a Modificar

1. `api/mcp.js` - Ajustar export y agregar logging
2. `vercel.json` - Agregar routes explícitas (opcional pero recomendado)

## Resultado Esperado

- `/api/mcp` responderá correctamente a GET (info) y POST (JSON-RPC)
- El servidor será un conector MCP funcional desde Claude
- No se servirá código fuente, solo respuestas JSON apropiadas

### To-dos

- [x] Convertir export de Express a handler compatible con Vercel serverless en api/mcp.js
- [x] Agregar manejo de OPTIONS para CORS preflight
- [x] Agregar logging de debug temporal para diagnosticar peticiones
- [x] Deploy a Vercel y probar todos los endpoints (health, mcp GET/POST)
- [x] Verificar funcionamiento como conector MCP desde cliente real

## ✅ RESULTADO FINAL - COMPLETADO

**Estado**: ✅ **FUNCIONANDO PERFECTAMENTE**

### Endpoints Verificados:
- ✅ `GET /api/health` - Health check funcionando
- ✅ `GET /api/mcp` - Información del servidor MCP funcionando
- ✅ `POST /api/mcp` - Endpoint principal MCP funcionando

### Conector MCP Listo:
- **URL**: `https://trackhs-mcp-connector.vercel.app/api/mcp`
- **Transport**: Streamable HTTP
- **Capabilities**: tools, resources, prompts
- **Herramientas**: 13 herramientas TrackHS disponibles
- **Recursos**: 4 recursos MCP (esquemas, status, docs)
- **Prompts**: 5 prompts predefinidos

### Configuración para Claude Desktop:
```json
{
  "mcpServers": {
    "trackhs-remote": {
      "url": "https://trackhs-mcp-connector.vercel.app/api/mcp"
    }
  }
}
```

**🎉 El servidor MCP TrackHS está completamente funcional y listo para producción.**
