# Despliegue en Producción para Servidores MCP Remotos

## Introducción

El despliegue en producción de servidores MCP remotos requiere consideraciones especiales de seguridad, escalabilidad, monitoreo y mantenimiento. Esta guía cubre las mejores prácticas para desplegar servidores MCP en entornos de producción.

## Arquitectura de Producción

### Arquitectura Recomendada

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Auth Server   │    │   MCP Servers   │
│   (Nginx/HAProxy)│    │   (Auth0/Okta)  │    │   (Node.js)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Redis Cluster │
                    │   (Sessions)    │
                    └─────────────────┘
```

### Componentes Principales

1. **Load Balancer**: Distribución de carga y terminación SSL
2. **Auth Server**: Autenticación OAuth 2.0 (Auth0, Okta, etc.)
3. **MCP Servers**: Múltiples instancias del servidor MCP
4. **Redis Cluster**: Almacenamiento de sesiones y caché
5. **Monitoring**: Métricas, logs y alertas

## Configuración de Infraestructura

### 1. Load Balancer (Nginx)

**nginx.conf**
```nginx
upstream mcp_backend {
    least_conn;
    server mcp-1.internal:3232 max_fails=3 fail_timeout=30s;
    server mcp-2.internal:3232 max_fails=3 fail_timeout=30s;
    server mcp-3.internal:3232 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.yourcompany.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=mcp:10m rate=10r/s;
    limit_req zone=mcp burst=20 nodelay;

    # MCP Endpoint
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
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Health Check
    location /health {
        access_log off;
        proxy_pass http://mcp_backend;
    }

    # Metrics
    location /metrics {
        allow 10.0.0.0/8;
        deny all;
        proxy_pass http://mcp_backend;
    }
}
```

### 2. Configuración de Redis

**redis.conf**
```conf
# Redis Cluster Configuration
port 6379
bind 0.0.0.0
protected-mode yes
requirepass your-redis-password

# Memory Management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log

# Network
tcp-keepalive 300
timeout 0

# Security
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
```

### 3. Configuración de Aplicación

**config/production.js**
```javascript
module.exports = {
  // Servidor
  server: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '3232'),
    transport: 'streamable-http',
    path: '/mcp'
  },

  // Autenticación
  auth: {
    serverUrl: process.env.AUTH_SERVER_URL,
    clientId: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRET,
    audience: process.env.AUDIENCE
  },

  // Base de datos
  redis: {
    url: process.env.REDIS_URL,
    retryDelayOnFailover: 100,
    maxRetriesPerRequest: 3,
    lazyConnect: true
  },

  // CORS
  cors: {
    origin: process.env.CORS_ORIGINS?.split(',') || [],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Mcp-Session-Id']
  },

  // Rate Limiting
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000'),
    max: parseInt(process.env.RATE_LIMIT_MAX || '100'),
    userMax: parseInt(process.env.RATE_LIMIT_USER_MAX || '50')
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: process.env.LOG_FORMAT || 'json',
    transports: ['console', 'file']
  },

  // Monitoreo
  monitoring: {
    enabled: true,
    metrics: {
      enabled: true,
      port: 9090,
      path: '/metrics'
    },
    health: {
      enabled: true,
      path: '/health'
    }
  }
};
```

## Docker y Contenedores

### Dockerfile Optimizado

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder

WORKDIR /app

# Instalar dependencias de build
RUN apk add --no-cache python3 make g++

# Copiar archivos de dependencias
COPY package*.json ./
COPY tsconfig.json ./

# Instalar dependencias
RUN npm ci --only=production && npm cache clean --force

# Copiar código fuente
COPY src/ ./src/

# Compilar TypeScript
RUN npm run build

# Imagen de producción
FROM node:18-alpine AS production

# Crear usuario no-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Instalar dependencias de runtime
RUN apk add --no-cache dumb-init

# Copiar archivos compilados
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./

# Configurar usuario
USER nodejs

# Exponer puerto
EXPOSE 3232

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3232/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"

# Comando de inicio
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

### Docker Compose para Producción

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "3232:3232"
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
      - AUTH_SERVER_URL=${AUTH_SERVER_URL}
      - CLIENT_ID=${CLIENT_ID}
      - CLIENT_SECRET=${CLIENT_SECRET}
    depends_on:
      - redis
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3232/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl:ro
    depends_on:
      - mcp-server
    restart: unless-stopped

volumes:
  redis_data:
```

## Kubernetes

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  labels:
    app: mcp-server
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
        - name: AUTH_SERVER_URL
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: auth-server-url
        - name: CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: client-id
        - name: CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: client-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3232
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 3232
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mcp-server-service
spec:
  selector:
    app: mcp-server
  ports:
  - port: 3232
    targetPort: 3232
    protocol: TCP
  type: ClusterIP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mcp-server-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - api.yourcompany.com
    secretName: mcp-tls-secret
  rules:
  - host: api.yourcompany.com
    http:
      paths:
      - path: /mcp
        pathType: Prefix
        backend:
          service:
            name: mcp-server-service
            port:
              number: 3232
```

## Monitoreo y Observabilidad

### Prometheus Metrics

```typescript
import prometheus from 'prom-client';

// Métricas personalizadas
const mcpRequestDuration = new prometheus.Histogram({
  name: 'mcp_request_duration_seconds',
  help: 'Duración de solicitudes MCP',
  labelNames: ['method', 'status_code', 'user_id'],
  buckets: [0.1, 0.5, 1, 2, 5, 10]
});

const mcpActiveConnections = new prometheus.Gauge({
  name: 'mcp_active_connections',
  help: 'Conexiones MCP activas'
});

const mcpToolsExecuted = new prometheus.Counter({
  name: 'mcp_tools_executed_total',
  help: 'Total de herramientas MCP ejecutadas',
  labelNames: ['tool_name', 'user_id']
});

const mcpErrors = new prometheus.Counter({
  name: 'mcp_errors_total',
  help: 'Total de errores MCP',
  labelNames: ['error_type', 'user_id']
});

// Endpoint de métricas
app.get('/metrics', (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(prometheus.register.metrics());
});
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "MCP Server Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mcp_request_duration_seconds_count[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(mcp_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "singlestat",
        "targets": [
          {
            "expr": "mcp_active_connections",
            "legendFormat": "Active"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mcp_errors_total[5m])",
            "legendFormat": "Errors/sec"
          }
        ]
      }
    ]
  }
}
```

### Alertas

```yaml
# Prometheus Alert Rules
groups:
- name: mcp-server
  rules:
  - alert: MCPHighErrorRate
    expr: rate(mcp_errors_total[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate in MCP server"
      description: "MCP server error rate is {{ $value }} errors/sec"

  - alert: MCPHighResponseTime
    expr: histogram_quantile(0.95, rate(mcp_request_duration_seconds_bucket[5m])) > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High response time in MCP server"
      description: "95th percentile response time is {{ $value }}s"

  - alert: MCPDown
    expr: up{job="mcp-server"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "MCP server is down"
      description: "MCP server has been down for more than 1 minute"
```

## Logging y Auditoría

### Configuración de Logs

```typescript
import winston from 'winston';
import { createLogger, format, transports } from 'winston';

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.json()
  ),
  defaultMeta: { service: 'mcp-server' },
  transports: [
    new transports.Console({
      format: format.combine(
        format.colorize(),
        format.simple()
      )
    }),
    new transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5
    }),
    new transports.File({
      filename: 'logs/combined.log',
      maxsize: 5242880, // 5MB
      maxFiles: 5
    })
  ]
});

// Logging de auditoría
const auditLogger = createLogger({
  level: 'info',
  format: format.combine(
    format.timestamp(),
    format.json()
  ),
  transports: [
    new transports.File({
      filename: 'logs/audit.log',
      maxsize: 10485760, // 10MB
      maxFiles: 10
    })
  ]
});

// Middleware de auditoría
app.use('/mcp', (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    auditLogger.info('MCP Request', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - start,
      user: req.user?.sub,
      sessionId: req.sessionId,
      ip: req.ip,
      userAgent: req.get('User-Agent')
    });
  });

  next();
});
```

## Backup y Recuperación

### Backup de Redis

```bash
#!/bin/bash
# backup-redis.sh

REDIS_HOST="your-redis-host"
REDIS_PORT="6379"
BACKUP_DIR="/backups/redis"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de Redis
redis-cli -h $REDIS_HOST -p $REDIS_PORT --rdb $BACKUP_DIR/redis_backup_$DATE.rdb

# Comprimir backup
gzip $BACKUP_DIR/redis_backup_$DATE.rdb

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "redis_backup_*.rdb.gz" -mtime +7 -delete

echo "Backup completado: redis_backup_$DATE.rdb.gz"
```

### Restauración de Redis

```bash
#!/bin/bash
# restore-redis.sh

REDIS_HOST="your-redis-host"
REDIS_PORT="6379"
BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "Uso: $0 <archivo_backup>"
  exit 1
fi

# Descomprimir backup
gunzip -c $BACKUP_FILE > /tmp/redis_restore.rdb

# Restaurar Redis
redis-cli -h $REDIS_HOST -p $REDIS_PORT --rdb /tmp/redis_restore.rdb

# Limpiar archivo temporal
rm /tmp/redis_restore.rdb

echo "Restauración completada"
```

## Seguridad en Producción

### Configuración de Seguridad

```typescript
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

// Configuración de seguridad
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://claude.ai"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

// Rate limiting por IP
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo 100 requests por IP
  message: {
    error: 'Demasiadas solicitudes desde esta IP',
    retryAfter: '15 minutos'
  },
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/mcp', limiter);
```

### Validación de Entrada

```typescript
import Joi from 'joi';

// Esquema de validación para solicitudes MCP
const mcpRequestSchema = Joi.object({
  jsonrpc: Joi.string().valid('2.0').required(),
  id: Joi.alternatives().try(Joi.string(), Joi.number()).required(),
  method: Joi.string().required(),
  params: Joi.object().optional()
});

// Middleware de validación
app.use('/mcp', (req, res, next) => {
  const { error } = mcpRequestSchema.validate(req.body);

  if (error) {
    return res.status(400).json({
      error: 'Solicitud MCP inválida',
      details: error.details[0].message
    });
  }

  next();
});
```

## Referencias

- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Kubernetes Production Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [Redis Production Guide](https://redis.io/docs/management/security/)
- [Prometheus Monitoring](https://prometheus.io/docs/guides/go-application/)
