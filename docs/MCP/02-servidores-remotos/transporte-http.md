# Transporte HTTP para Servidores MCP Remotos

## Introducción

El transporte HTTP es fundamental para servidores MCP remotos, permitiendo la comunicación entre clientes y servidores a través de internet. MCP soporta dos tipos principales de transporte HTTP: **Streamable HTTP** (recomendado) y **Server-Sent Events (SSE)**.

## Streamable HTTP (Recomendado)

### Características

- **Escalabilidad**: Soporte para múltiples clientes concurrentes
- **Resumibilidad**: Capacidad de reanudar conexiones interrumpidas
- **Estándar Web**: Basado en HTTP estándar
- **Flexibilidad**: Soporte para JSON y SSE responses

### Configuración Básica

```typescript
import { FastMCP } from 'mcp/server/fastmcp';

const mcp = new FastMCP('Mi Servidor Remoto');

// Configuración Streamable HTTP
mcp.run({
  transport: 'streamable-http',
  host: '0.0.0.0',
  port: 3232,
  path: '/mcp'
});
```

### Configuración Avanzada

```typescript
// Configuración completa
const mcp = new FastMCP('Mi Servidor Remoto', {
  // Configuración de transporte
  streamableHttp: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '3232'),
    path: '/mcp',
    
    // Configuración de CORS
    cors: {
      origin: process.env.CORS_ORIGINS?.split(',') || ['https://claude.ai'],
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE'],
      allowedHeaders: ['Content-Type', 'Authorization', 'Mcp-Session-Id']
    },
    
    // Configuración de sesiones
    session: {
      store: 'redis', // o 'memory' para desarrollo
      redis: {
        url: process.env.REDIS_URL
      },
      ttl: 7 * 24 * 60 * 60 * 1000, // 7 días
      secret: process.env.SESSION_SECRET
    },
    
    // Configuración de eventos
    events: {
      enabled: true,
      store: 'redis',
      ttl: 24 * 60 * 60 * 1000 // 24 horas
    }
  }
});
```

### Endpoints HTTP

**Endpoint Principal**: `POST /mcp`
```http
POST /mcp
Content-Type: application/json
Authorization: Bearer <token>
Mcp-Session-Id: <session-id>

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Endpoint de Eventos**: `GET /mcp/events`
```http
GET /mcp/events
Authorization: Bearer <token>
Mcp-Session-Id: <session-id>
Accept: text/event-stream
```

### Manejo de Sesiones

```typescript
// Configuración de sesiones con Redis
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Almacenamiento de sesión
async function storeSession(sessionId: string, data: any) {
  await redis.setex(
    `mcp:session:${sessionId}`,
    7 * 24 * 60 * 60, // 7 días
    JSON.stringify(data)
  );
}

// Recuperación de sesión
async function getSession(sessionId: string) {
  const data = await redis.get(`mcp:session:${sessionId}`);
  return data ? JSON.parse(data) : null;
}
```

## Server-Sent Events (SSE)

### Características

- **Tiempo Real**: Comunicación bidireccional en tiempo real
- **Simplicidad**: Fácil implementación
- **Compatibilidad**: Soporte nativo en navegadores

### Configuración

```typescript
// Configuración SSE
const mcp = new FastMCP('Mi Servidor SSE', {
  transport: 'sse',
  host: '0.0.0.0',
  port: 3232,
  path: '/sse'
});
```

### Implementación Manual

```typescript
import express from 'express';
import { createServer } from 'http';

const app = express();
const server = createServer(app);

// Endpoint SSE
app.get('/sse', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Cache-Control'
  });

  // Enviar evento de conexión
  res.write('event: connected\n');
  res.write('data: {"status": "connected"}\n\n');

  // Manejar desconexión
  req.on('close', () => {
    console.log('Cliente desconectado');
  });
});

// Endpoint para enviar mensajes
app.post('/sse/message', (req, res) => {
  const { sessionId, message } = req.body;
  
  // Enviar mensaje a cliente específico
  sendToClient(sessionId, message);
  
  res.json({ success: true });
});
```

## Configuración de CORS

### Configuración Básica

```typescript
import cors from 'cors';

app.use(cors({
  origin: [
    'https://claude.ai',
    'https://app.claude.ai',
    'https://your-app.com'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'Mcp-Session-Id',
    'X-Requested-With'
  ],
  exposedHeaders: ['Mcp-Session-Id']
}));
```

### Configuración Dinámica

```typescript
// CORS dinámico basado en origen
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];
    
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('No permitido por CORS'));
    }
  },
  credentials: true
};

app.use(cors(corsOptions));
```

## Autenticación HTTP

### Middleware de Autenticación

```typescript
import jwt from 'jsonwebtoken';

// Middleware de autenticación
async function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Token de acceso requerido' });
  }

  try {
    // Validar token con servidor de autorización
    const response = await fetch(`${process.env.AUTH_SERVER_URL}/introspect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${Buffer.from(`${process.env.CLIENT_ID}:${process.env.CLIENT_SECRET}`).toString('base64')}`
      },
      body: `token=${token}`
    });

    const introspection = await response.json();

    if (!introspection.active) {
      return res.status(401).json({ error: 'Token inválido' });
    }

    req.user = introspection;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Error de autenticación' });
  }
}

// Aplicar middleware a rutas MCP
app.use('/mcp', authenticateToken);
```

### Manejo de Sesiones

```typescript
// Middleware de sesión
function sessionMiddleware(req, res, next) {
  const sessionId = req.headers['mcp-session-id'];
  
  if (!sessionId) {
    return res.status(400).json({ error: 'Session ID requerido' });
  }

  req.sessionId = sessionId;
  next();
}

app.use('/mcp', sessionMiddleware);
```

## Rate Limiting

### Configuración Básica

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo 100 requests por ventana
  message: {
    error: 'Demasiadas solicitudes',
    retryAfter: '15 minutos'
  },
  standardHeaders: true,
  legacyHeaders: false,
  // Aplicar límite por IP
  keyGenerator: (req) => req.ip
});

app.use('/mcp', limiter);
```

### Rate Limiting por Usuario

```typescript
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

const userLimiter = rateLimit({
  store: new RedisStore({
    sendCommand: (...args) => redis.call(...args),
  }),
  windowMs: 15 * 60 * 1000,
  max: 50, // 50 requests por usuario
  keyGenerator: (req) => req.user?.sub || req.ip,
  message: {
    error: 'Límite de usuario excedido',
    retryAfter: '15 minutos'
  }
});

app.use('/mcp', userLimiter);
```

## Monitoreo y Logging

### Middleware de Logging

```typescript
import morgan from 'morgan';
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/access.log' })
  ]
});

// Middleware de logging HTTP
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Middleware de logging MCP
app.use('/mcp', (req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    logger.info('MCP Request', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration,
      user: req.user?.sub,
      sessionId: req.sessionId
    });
  });
  
  next();
});
```

### Métricas de Rendimiento

```typescript
import prometheus from 'prom-client';

// Métricas personalizadas
const mcpRequestDuration = new prometheus.Histogram({
  name: 'mcp_request_duration_seconds',
  help: 'Duración de solicitudes MCP',
  labelNames: ['method', 'status_code', 'user_id']
});

const mcpActiveConnections = new prometheus.Gauge({
  name: 'mcp_active_connections',
  help: 'Conexiones MCP activas'
});

// Middleware de métricas
app.use('/mcp', (req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    
    mcpRequestDuration
      .labels(req.method, res.statusCode, req.user?.sub || 'anonymous')
      .observe(duration);
  });
  
  next();
});

// Endpoint de métricas
app.get('/metrics', (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(prometheus.register.metrics());
});
```

## Configuración de Producción

### Variables de Entorno

```bash
# Servidor
NODE_ENV=production
HOST=0.0.0.0
PORT=3232

# Transporte
TRANSPORT_TYPE=streamable-http
HTTP_PATH=/mcp
SSE_PATH=/sse

# CORS
CORS_ORIGINS=https://claude.ai,https://app.claude.ai
CORS_CREDENTIALS=true

# Sesiones
SESSION_STORE=redis
REDIS_URL=redis://your-redis:6379
SESSION_SECRET=your-session-secret
SESSION_TTL=604800000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_USER_MAX=50

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

### Configuración de Nginx

```nginx
upstream mcp_backend {
    server 127.0.0.1:3232;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name your-mcp-server.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Configuración de seguridad
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=mcp:10m rate=10r/s;
    limit_req zone=mcp burst=20 nodelay;
    
    # Proxy a servidor MCP
    location /mcp {
        proxy_pass http://mcp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # SSE endpoint
    location /sse {
        proxy_pass http://mcp_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_set_header Cache-Control no-cache;
        proxy_buffering off;
    }
}
```

## Testing

### Tests de Transporte

```typescript
import request from 'supertest';
import { FastMCP } from 'mcp/server/fastmcp';

describe('HTTP Transport', () => {
  let app: Express;
  let mcp: FastMCP;

  beforeEach(async () => {
    mcp = new FastMCP('Test Server');
    
    // Configurar herramientas de prueba
    mcp.tool('test_tool', () => 'test result');
    
    app = mcp.createExpressApp();
  });

  it('should handle MCP requests via HTTP', async () => {
    const response = await request(app)
      .post('/mcp')
      .set('Authorization', 'Bearer valid-token')
      .set('Mcp-Session-Id', 'test-session')
      .send({
        jsonrpc: '2.0',
        id: 1,
        method: 'tools/list'
      });

    expect(response.status).toBe(200);
    expect(response.body.result.tools).toHaveLength(1);
  });

  it('should handle SSE connections', async () => {
    const response = await request(app)
      .get('/sse')
      .set('Authorization', 'Bearer valid-token')
      .set('Accept', 'text/event-stream');

    expect(response.status).toBe(200);
    expect(response.headers['content-type']).toBe('text/event-stream');
  });
});
```

## Referencias

- [Especificación MCP - Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [Express.js Documentation](https://expressjs.com/)
- [CORS Configuration Guide](https://expressjs.com/en/resources/middleware/cors.html)
- [Rate Limiting Best Practices](https://expressjs.com/en/advanced/best-practice-performance.html)
