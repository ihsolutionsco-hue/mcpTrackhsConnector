# OAuth y Autenticación para Servidores MCP Remotos

## Introducción

La autenticación es fundamental para servidores MCP remotos que manejan datos sensibles o requieren control de acceso. OAuth 2.0 + PKCE es el estándar recomendado para implementar autenticación segura.

## Arquitectura OAuth para MCP

### Patrón Recomendado: Servidor Separado

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│             │  OAuth  │                  │ Token   │                 │
│  MCP Client │────────>│  Auth Server     │<────────│  MCP Server     │
│             │         │  (puerto 3001)   │validate │  (puerto 3232)  │
│             │<────────│                  │         │                 │
│             │  token  │  Emite tokens    │         │  Sirve recursos │
│             │         └──────────────────┘         │  MCP            │
│             │────────────────────────────────────> │                 │
│             │         Solicitudes MCP con token    │                 │
└─────────────┘                                      └─────────────────┘
```

### Componentes

1. **Servidor de Autorización**
   - Maneja flujo OAuth 2.0
   - Emite y gestiona tokens
   - Proporciona endpoint de introspección (RFC 7662)

2. **Servidor de Recursos MCP**
   - Sirve recursos del protocolo MCP
   - Valida tokens vía introspección
   - Enfocado puramente en funcionalidad MCP

## Flujo OAuth 2.0 + PKCE Completo

### 1. Registro del Cliente

**Propósito**: Registrar la aplicación con el servidor OAuth (una vez durante la configuración).

```http
POST /register
Content-Type: application/json

{
  "client_name": "Mi Aplicación MCP",
  "redirect_uris": ["http://localhost:3000/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"]
}
```

**Respuesta**:
```json
{
  "client_id": "xyz123",
  "client_secret": "abc456",
  "client_name": "Mi Aplicación MCP"
}
```

### 2. Solicitud de Autorización

**Propósito**: El usuario inicia la conexión al servidor MCP.

```http
GET /authorize?
  client_id=xyz123&
  redirect_uri=http://localhost:3000/callback&
  code_challenge=<SHA256_del_verifier>&
  code_challenge_method=S256&
  state=<token_CSRF>
```

### 3. Autenticación y Autorización del Usuario

**Flujo**:
1. Servidor muestra página de autorización
2. Usuario hace clic en "Continuar a Autenticación"
3. Redirección a proveedor de identidad upstream
4. Usuario selecciona/crea ID de usuario
5. Proveedor redirige de vuelta con userId
6. Servidor valida usuario y emite código de autorización

### 4. Intercambio de Código de Autorización

```http
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
client_id=xyz123&
client_secret=abc456&
code=<código_autorización>&
redirect_uri=http://localhost:3000/callback&
code_verifier=<string_aleatorio_original>
```

**Respuesta**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "def789",
  "expires_in": 604800,
  "token_type": "Bearer"
}
```

### 5. Uso de Tokens de Acceso

```http
POST /mcp
Authorization: Bearer <access_token>
Mcp-Session-Id: <session_id>
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Proceso de Validación**:
1. Servidor MCP recibe solicitud con token Bearer
2. Llama al endpoint `/introspect` del Servidor Auth
3. Servidor Auth valida token y devuelve metadatos
4. Servidor MCP valida audience y procede con la solicitud

### 6. Renovación de Token

```http
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=def789&
client_id=xyz123&
client_secret=abc456
```

## Implementación con Proveedores Comerciales

### Auth0

```typescript
// Configuración del servidor MCP
const authServerUrl = 'https://your-tenant.auth0.com';
const audience = 'https://your-mcp-server.com';

// Validación de token
const response = await fetch(`${authServerUrl}/oauth/introspect`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': `Basic ${Buffer.from('client_id:client_secret').toString('base64')}`
  },
  body: `token=${token}`
});
```

### Okta

```typescript
const authServerUrl = 'https://your-domain.okta.com';
const response = await fetch(`${authServerUrl}/oauth2/v1/introspect`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': `Basic ${Buffer.from('client_id:client_secret').toString('base64')}`
  },
  body: `token=${token}`
});
```

### Azure AD / Microsoft Entra

```typescript
const authServerUrl = 'https://login.microsoftonline.com/your-tenant';
const response = await fetch(`${authServerUrl}/oauth2/v2.0/introspect`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: `token=${token}&client_id=${clientId}&client_secret=${clientSecret}`
});
```

## Seguridad: PKCE (Proof Key for Code Exchange)

PKCE previene ataques de interceptación de código de autorización:

### 1. Generación del Code Verifier
```typescript
const codeVerifier = generateRandomString(128);
const codeChallenge = sha256(codeVerifier);
```

### 2. Solicitud de Autorización
```http
GET /authorize?
  client_id=xyz123&
  code_challenge=<code_challenge>&
  code_challenge_method=S256
```

### 3. Intercambio de Token
```http
POST /token
code_verifier=<code_verifier_original>
```

### 4. Validación del Servidor
```typescript
const isValid = sha256(codeVerifier) === storedCodeChallenge;
```

## Mejores Prácticas de Seguridad

### 1. Configuración de Tokens
- **Expiración**: 7 días para access tokens, 30 días para refresh tokens
- **Scopes**: Control granular de permisos
- **Audience**: Validación de destinatario del token

### 2. Gestión de Sesiones
- **Redis**: Para almacenamiento de sesiones
- **Limpieza**: Eliminación automática de tokens expirados
- **Aislamiento**: Sesiones separadas por usuario

### 3. Monitoreo y Auditoría
- **Logs**: Registro de eventos de autenticación
- **Métricas**: Monitoreo de intentos de acceso
- **Alertas**: Notificaciones de actividad sospechosa

### 4. Configuración de Producción
- **HTTPS**: Obligatorio para todos los endpoints
- **CORS**: Configuración apropiada para dominios permitidos
- **Rate Limiting**: Protección contra ataques de fuerza bruta

## Ejemplo de Implementación

### Servidor de Autorización (Node.js + Express)

```typescript
import express from 'express';
import { OAuth2Server } from 'oauth2-server';

const app = express();

// Configuración OAuth
const oauth = new OAuth2Server({
  model: {
    // Implementar métodos del modelo OAuth
    getClient: async (clientId) => { /* ... */ },
    saveToken: async (token) => { /* ... */ },
    getAccessToken: async (accessToken) => { /* ... */ },
    // ... otros métodos
  }
});

// Endpoint de autorización
app.get('/authorize', async (req, res) => {
  try {
    const authRequest = await oauth.authorize({
      headers: req.headers,
      method: req.method,
      query: req.query,
      body: req.body
    });
    
    // Mostrar página de autorización
    res.render('authorize', { authRequest });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Endpoint de token
app.post('/token', async (req, res) => {
  try {
    const token = await oauth.token({
      headers: req.headers,
      method: req.method,
      query: req.query,
      body: req.body
    });
    
    res.json(token);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Endpoint de introspección
app.post('/introspect', async (req, res) => {
  const { token } = req.body;
  
  try {
    const introspection = await oauth.introspect(token);
    res.json(introspection);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

### Servidor MCP con Autenticación

```typescript
import { FastMCP } from 'mcp/server/fastmcp';
import { AuthSettings } from 'mcp/server/auth/settings';

// Configuración de autenticación
const authSettings = new AuthSettings({
  issuer_url: 'https://your-auth-server.com',
  resource_server_url: 'https://your-mcp-server.com',
  required_scopes: ['mcp:read', 'mcp:write']
});

// Crear servidor MCP con autenticación
const mcp = new FastMCP('Mi Servidor Remoto', {
  auth: authSettings
});

// Middleware de autenticación
mcp.use(async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Token requerido' });
  }
  
  try {
    // Validar token con servidor de autorización
    const response = await fetch(`${authSettings.issuer_url}/introspect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `token=${token}`
    });
    
    const introspection = await response.json();
    
    if (!introspection.active) {
      return res.status(401).json({ error: 'Token inválido' });
    }
    
    req.user = introspection;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Error de autenticación' });
  }
});

// Herramienta protegida
mcp.tool('getUserData', async (req) => {
  const userId = req.user.sub;
  // Lógica de la herramienta
  return { userId, data: '...' };
});
```

## Referencias

- [RFC 6749: OAuth 2.0 Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7662: Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
- [RFC 7636: PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- [Especificación de Autorización MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
