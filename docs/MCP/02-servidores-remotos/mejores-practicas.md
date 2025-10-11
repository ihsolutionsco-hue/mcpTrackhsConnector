# Mejores Prácticas para Servidores MCP Remotos

## Arquitectura y Diseño

### 1. Separación de Responsabilidades

**✅ Recomendado: Servidor Separado**
```
Cliente → Servidor Auth → Servidor MCP
```

**Ventajas**:
- Separación clara de responsabilidades
- Escalabilidad independiente
- Reutilización del servidor de auth
- Mantenimiento simplificado

**❌ Evitar: Servidor Integrado (excepto casos específicos)**
```
Cliente → Servidor MCP (con auth integrada)
```

**Cuándo usar servidor integrado**:
- Prototipos y demos
- Sistemas aislados (air-gapped)
- Requisitos de autenticación muy específicos

### 2. Gestión de Estado

**Redis para Sesiones**
```typescript
// Configuración recomendada
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  password: process.env.REDIS_PASSWORD,
  db: 0
});

// Estructura de datos recomendada
const sessionKey = `mcp:session:${sessionId}`;
const userKey = `mcp:user:${userId}`;
const tokenKey = `mcp:token:${accessToken}`;
```

**Jerarquía de Expiración**:
1. **Estado OAuth** (10 minutos) - `auth:pending`, `auth:exch`
2. **Sesiones de usuario** (7 días) - `auth:installation`, `auth:refresh`
3. **Credenciales de cliente** (30 días) - `auth:client`

### 3. Manejo de Errores

**Estructura de Respuesta Estándar**
```typescript
interface MCPError {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
  requestId: string;
}

// Códigos de error recomendados
const ERROR_CODES = {
  AUTHENTICATION_REQUIRED: 'AUTH_REQUIRED',
  INVALID_TOKEN: 'INVALID_TOKEN',
  INSUFFICIENT_PERMISSIONS: 'INSUFFICIENT_PERMISSIONS',
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
  INTERNAL_ERROR: 'INTERNAL_ERROR'
};
```

## Seguridad

### 1. Autenticación y Autorización

**OAuth 2.0 + PKCE (Obligatorio)**
```typescript
// Configuración PKCE
const codeVerifier = generateRandomString(128);
const codeChallenge = sha256(codeVerifier);

// Validación PKCE
const isValidPKCE = (verifier: string, challenge: string) => {
  return sha256(verifier) === challenge;
};
```

**Validación de Tokens**
```typescript
async function validateToken(token: string): Promise<TokenInfo> {
  const response = await fetch(`${AUTH_SERVER_URL}/introspect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Basic ${Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')}`
    },
    body: `token=${token}`
  });

  const introspection = await response.json();

  if (!introspection.active) {
    throw new Error('Token inválido o expirado');
  }

  // Validar audience
  if (introspection.aud !== EXPECTED_AUDIENCE) {
    throw new Error('Token no válido para este servidor');
  }

  return introspection;
}
```

### 2. Configuración de Seguridad

**HTTPS Obligatorio**
```typescript
// Configuración de servidor seguro
const server = https.createServer({
  key: fs.readFileSync('path/to/private-key.pem'),
  cert: fs.readFileSync('path/to/certificate.pem'),
  // Configuraciones adicionales de seguridad
  secureProtocol: 'TLSv1_2_method',
  ciphers: 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256'
}, app);
```

**CORS Configurado Correctamente**
```typescript
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://claude.ai'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Mcp-Session-Id']
}));
```

**Rate Limiting**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo 100 requests por ventana
  message: {
    error: 'Demasiadas solicitudes, intenta más tarde',
    retryAfter: '15 minutos'
  },
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/mcp', limiter);
```

### 3. Logging y Auditoría

**Estructura de Logs**
```typescript
interface SecurityLog {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR';
  event: string;
  userId?: string;
  sessionId?: string;
  ipAddress: string;
  userAgent: string;
  details: any;
}

// Eventos importantes a registrar
const SECURITY_EVENTS = {
  AUTH_SUCCESS: 'auth_success',
  AUTH_FAILURE: 'auth_failure',
  TOKEN_REFRESH: 'token_refresh',
  PERMISSION_DENIED: 'permission_denied',
  RATE_LIMIT_HIT: 'rate_limit_hit'
};
```

## Rendimiento y Escalabilidad

### 1. Caché de Tokens

**Implementación de Caché**
```typescript
class TokenCache {
  private cache = new Map<string, { data: any; expires: number }>();

  async get(token: string): Promise<any> {
    const cached = this.cache.get(token);

    if (cached && cached.expires > Date.now()) {
      return cached.data;
    }

    // Token expirado o no encontrado
    this.cache.delete(token);
    return null;
  }

  async set(token: string, data: any, ttl: number = 300000): Promise<void> {
    this.cache.set(token, {
      data,
      expires: Date.now() + ttl
    });
  }
}
```

### 2. Pool de Conexiones

**Configuración de Base de Datos**
```typescript
const dbConfig = {
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // máximo 20 conexiones
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
};
```

### 3. Monitoreo y Métricas

**Métricas Clave**
```typescript
// Métricas recomendadas
const metrics = {
  // Rendimiento
  requestDuration: new Histogram('mcp_request_duration_seconds'),
  activeConnections: new Gauge('mcp_active_connections'),

  // Errores
  errorRate: new Counter('mcp_errors_total'),
  authFailures: new Counter('mcp_auth_failures_total'),

  // Negocio
  toolsExecuted: new Counter('mcp_tools_executed_total'),
  resourcesAccessed: new Counter('mcp_resources_accessed_total')
};
```

## Configuración de Producción

### 1. Variables de Entorno

**Archivo .env.production**
```bash
# Servidor
NODE_ENV=production
PORT=3232
HOST=0.0.0.0

# Autenticación
AUTH_SERVER_URL=https://auth.yourcompany.com
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
JWT_SECRET=your_jwt_secret

# Base de datos
REDIS_URL=redis://your-redis-instance:6379
DB_URL=postgresql://user:pass@host:5432/db

# Seguridad
CORS_ORIGINS=https://claude.ai,https://your-app.com
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

### 2. Health Checks

**Endpoint de Salud**
```typescript
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: process.env.npm_package_version,
    checks: {
      database: await checkDatabase(),
      redis: await checkRedis(),
      authServer: await checkAuthServer()
    }
  };

  const isHealthy = Object.values(health.checks).every(check => check.status === 'ok');

  res.status(isHealthy ? 200 : 503).json(health);
});
```

### 3. Configuración de Logs

**Winston Logger**
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});
```

## Testing

### 1. Tests Unitarios

**Estructura de Tests**
```typescript
describe('MCP Server Authentication', () => {
  beforeEach(() => {
    // Setup de test
  });

  it('should validate valid token', async () => {
    const token = await generateTestToken();
    const result = await validateToken(token);
    expect(result.active).toBe(true);
  });

  it('should reject invalid token', async () => {
    await expect(validateToken('invalid-token')).rejects.toThrow();
  });
});
```

### 2. Tests de Integración

**Test de Flujo Completo**
```typescript
describe('OAuth Flow Integration', () => {
  it('should complete full OAuth flow', async () => {
    // 1. Iniciar flujo OAuth
    const authUrl = await initiateOAuthFlow();

    // 2. Simular autorización de usuario
    const authCode = await simulateUserAuthorization(authUrl);

    // 3. Intercambiar código por token
    const tokens = await exchangeCodeForToken(authCode);

    // 4. Usar token para solicitud MCP
    const response = await makeMCPRequest(tokens.access_token);

    expect(response.status).toBe(200);
  });
});
```

### 3. Tests de Carga

**Artillery.js**
```yaml
# load-test.yml
config:
  target: 'https://your-mcp-server.com'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "MCP Tool Execution"
    weight: 70
    flow:
      - post:
          url: "/mcp"
          headers:
            Authorization: "Bearer {{ token }}"
          json:
            jsonrpc: "2.0"
            id: 1
            method: "tools/call"
            params:
              name: "test_tool"
              arguments: {}
```

## Despliegue

### 1. Docker

**Dockerfile**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3232

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3232/health || exit 1

CMD ["node", "dist/server.js"]
```

### 2. Kubernetes

**Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: your-registry/mcp-server:latest
        ports:
        - containerPort: 3232
        env:
        - name: NODE_ENV
          value: "production"
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: redis-url
        livenessProbe:
          httpGet:
            path: /health
            port: 3232
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3232
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Referencias

- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [RFC 6749: OAuth 2.0 Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
