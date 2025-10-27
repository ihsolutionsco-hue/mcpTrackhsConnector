# ⚙️ Guía de Configuración - TrackHS MCP Server

## 🎯 Descripción General

Esta guía detalla cómo configurar el TrackHS MCP Server para diferentes entornos y casos de uso. Incluye configuraciones para desarrollo, testing, staging y producción.

## 📋 Tabla de Contenidos

1. [Configuración Básica](#configuración-básica)
2. [Variables de Entorno](#variables-de-entorno)
3. [Configuración FastMCP](#configuración-fastmcp)
4. [Configuración de Cache](#configuración-de-cache)
5. [Configuración de Métricas](#configuración-de-métricas)
6. [Configuración de Middleware](#configuración-de-middleware)
7. [Configuración por Entorno](#configuración-por-entorno)
8. [Troubleshooting](#troubleshooting)

## 🔧 Configuración Básica

### Requisitos del Sistema

- **Python**: 3.11+
- **Memoria**: Mínimo 512MB, recomendado 1GB+
- **CPU**: 1 core mínimo, 2+ cores recomendado
- **Red**: Acceso a internet para TrackHS API
- **Almacenamiento**: 100MB para aplicación + logs

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/ihsolutionsco-hue/mcpTrackhsConnector.git
cd mcpTrackhsConnector

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -m trackhs_mcp --version
```

## 🌍 Variables de Entorno

### Variables Requeridas

```bash
# Credenciales de TrackHS API
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_contraseña"
```

### Variables Opcionales

```bash
# URL de la API (default: https://api.trackhs.com)
export TRACKHS_API_URL="https://api.trackhs.com"

# Configuración de cache
export CACHE_TTL="300"                    # TTL en segundos
export CACHE_MAX_SIZE="1000"             # Tamaño máximo del cache
export CACHE_STRATEGY="adaptive"         # Estrategia de cache

# Configuración de rate limiting
export RATE_LIMIT_RPM="60"               # Requests por minuto
export RATE_LIMIT_BURST="10"             # Tamaño de burst

# Configuración de métricas
export METRICS_ENABLED="true"            # Habilitar métricas
export METRICS_PORT="9090"               # Puerto de métricas

# Configuración de logging
export LOG_LEVEL="INFO"                  # Nivel de logging
export LOG_FORMAT="json"                 # Formato de logs

# Configuración de retry
export MAX_RETRIES="3"                   # Máximo de reintentos
export RETRY_DELAY="1"                   # Delay entre reintentos (segundos)

# Configuración de timeout
export API_TIMEOUT="30"                  # Timeout de API (segundos)
export HEALTH_CHECK_TIMEOUT="10"         # Timeout de health check

# Configuración de testing
export TESTING="false"                   # Modo testing
export MOCK_API="false"                  # Usar API mock
```

### Archivo .env

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
TRACKHS_API_URL=https://api.trackhs.com

# Cache
CACHE_TTL=300
CACHE_MAX_SIZE=1000
CACHE_STRATEGY=adaptive

# Rate Limiting
RATE_LIMIT_RPM=60
RATE_LIMIT_BURST=10

# Métricas
METRICS_ENABLED=true
METRICS_PORT=9090

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Retry
MAX_RETRIES=3
RETRY_DELAY=1

# Timeout
API_TIMEOUT=30
HEALTH_CHECK_TIMEOUT=10

# Testing
TESTING=false
MOCK_API=false
```

## ⚙️ Configuración FastMCP

### Archivo fastmcp.json

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "src/trackhs_mcp/__main__.py:mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.11",
    "requirements": "requirements.txt",
    "fastmcp_version": "2.13.0"
  },
  "server": {
    "name": "TrackHS API",
    "description": "Servidor MCP para TrackHS API con validación Pydantic",
    "version": "2.0.0",
    "website_url": "https://github.com/ihsolutionsco-hue/mcpTrackhsConnector"
  },
  "logging": {
    "level": "INFO",
    "format": "json"
  },
  "cors": {
    "origins": [
      "https://elevenlabs.io",
      "https://api.elevenlabs.io",
      "https://app.elevenlabs.io",
      "https://claude.ai",
      "https://app.claude.ai"
    ],
    "credentials": true,
    "methods": ["GET", "POST", "DELETE", "OPTIONS"]
  },
  "health_check": {
    "enabled": true,
    "endpoint": "/health",
    "timeout": 30
  },
  "environment_variables": {
    "required": [
      "TRACKHS_USERNAME",
      "TRACKHS_PASSWORD"
    ],
    "optional": [
      "TRACKHS_API_URL",
      "CACHE_TTL",
      "RATE_LIMIT_RPM",
      "METRICS_ENABLED"
    ]
  }
}
```

### Configuración Avanzada

```json
{
  "server": {
    "name": "TrackHS API",
    "description": "Servidor MCP para TrackHS API",
    "version": "2.0.0",
    "website_url": "https://github.com/ihsolutionsco-hue/mcpTrackhsConnector",
    "max_concurrent_requests": 100,
    "request_timeout": 30,
    "response_timeout": 60
  },
  "middleware": {
    "error_handling": {
      "enabled": true,
      "include_traceback": true,
      "transform_errors": true
    },
    "retry": {
      "enabled": true,
      "max_retries": 3,
      "retry_exceptions": [
        "httpx.RequestError",
        "httpx.HTTPStatusError"
      ]
    },
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 60,
      "burst_size": 10
    },
    "caching": {
      "enabled": true,
      "default_ttl": 300,
      "max_size": 1000
    }
  }
}
```

## 💾 Configuración de Cache

### Cache Básico

```python
# src/trackhs_mcp/cache.py
from src.trackhs_mcp.cache import IntelligentCache, CacheStrategy

# Cache por defecto
cache = IntelligentCache(
    max_size=1000,
    default_ttl=300,  # 5 minutos
    strategy=CacheStrategy.ADAPTIVE
)
```

### Cache Especializado

```python
# Cache para reservas (TTL más largo)
reservation_cache = IntelligentCache(
    max_size=500,
    default_ttl=600,  # 10 minutos
    strategy=CacheStrategy.CACHE_ASIDE
)

# Cache para unidades (TTL más corto)
unit_cache = IntelligentCache(
    max_size=200,
    default_ttl=180,  # 3 minutos
    strategy=CacheStrategy.WRITE_THROUGH
)

# Cache para amenidades (TTL muy largo)
amenity_cache = IntelligentCache(
    max_size=100,
    default_ttl=3600,  # 1 hora
    strategy=CacheStrategy.WRITE_BEHIND
)
```

### Configuración por Tipo de Dato

```python
# Configuración de cache por tipo
CACHE_CONFIGS = {
    "reservations": {
        "max_size": 500,
        "ttl": 600,
        "strategy": CacheStrategy.CACHE_ASIDE
    },
    "units": {
        "max_size": 200,
        "ttl": 180,
        "strategy": CacheStrategy.WRITE_THROUGH
    },
    "amenities": {
        "max_size": 100,
        "ttl": 3600,
        "strategy": CacheStrategy.WRITE_BEHIND
    },
    "work_orders": {
        "max_size": 300,
        "ttl": 300,
        "strategy": CacheStrategy.ADAPTIVE
    }
}
```

## 📊 Configuración de Métricas

### Métricas Básicas

```python
# src/trackhs_mcp/metrics.py
from src.trackhs_mcp.metrics import PrometheusMetrics

# Configuración básica
metrics = PrometheusMetrics(
    namespace="trackhs_mcp",
    subsystem="server"
)
```

### Métricas Avanzadas

```python
# Configuración avanzada de métricas
metrics = PrometheusMetrics(
    namespace="trackhs_mcp",
    subsystem="server",
    labels={
        "environment": "production",
        "version": "2.0.0",
        "region": "us-east-1"
    }
)

# Configurar métricas personalizadas
metrics.add_custom_metric(
    name="business_metrics",
    type="gauge",
    description="Métricas de negocio personalizadas"
)
```

### Configuración de Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'trackhs-mcp'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 5s
    scrape_timeout: 3s
```

## 🔧 Configuración de Middleware

### Middleware Básico

```python
# src/trackhs_mcp/middleware_native.py
from src.trackhs_mcp.middleware_native import (
    TrackHSLoggingMiddleware,
    TrackHSAuthMiddleware,
    TrackHSMetricsMiddleware,
    TrackHSRateLimitMiddleware
)

# Configuración básica
middleware_chain = [
    TrackHSLoggingMiddleware(),
    TrackHSAuthMiddleware(api_client),
    TrackHSMetricsMiddleware(),
    TrackHSRateLimitMiddleware(requests_per_minute=60)
]
```

### Middleware Avanzado

```python
# Configuración avanzada de middleware
middleware_chain = [
    TrackHSLoggingMiddleware(
        log_level="INFO",
        include_request_body=False,
        include_response_body=False
    ),
    TrackHSAuthMiddleware(
        api_client=api_client,
        cache_ttl=300,
        retry_attempts=3
    ),
    TrackHSMetricsMiddleware(
        enable_histograms=True,
        enable_gauges=True,
        enable_counters=True
    ),
    TrackHSRateLimitMiddleware(
        requests_per_minute=60,
        burst_size=10,
        cleanup_interval=60
    )
]
```

## 🌍 Configuración por Entorno

### Desarrollo

```bash
# .env.development
TRACKHS_USERNAME=dev_user
TRACKHS_PASSWORD=dev_password
TRACKHS_API_URL=https://dev-api.trackhs.com

# Cache más pequeño para desarrollo
CACHE_TTL=60
CACHE_MAX_SIZE=100

# Rate limiting más permisivo
RATE_LIMIT_RPM=120
RATE_LIMIT_BURST=20

# Logging detallado
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Testing habilitado
TESTING=true
MOCK_API=false
```

### Testing

```bash
# .env.testing
TRACKHS_USERNAME=test_user
TRACKHS_PASSWORD=test_password
TRACKHS_API_URL=https://test-api.trackhs.com

# Cache deshabilitado para testing
CACHE_TTL=0
CACHE_MAX_SIZE=0

# Rate limiting deshabilitado
RATE_LIMIT_RPM=999999

# Logging mínimo
LOG_LEVEL=WARNING
LOG_FORMAT=json

# Testing habilitado
TESTING=true
MOCK_API=true
```

### Staging

```bash
# .env.staging
TRACKHS_USERNAME=staging_user
TRACKHS_PASSWORD=staging_password
TRACKHS_API_URL=https://staging-api.trackhs.com

# Cache moderado
CACHE_TTL=300
CACHE_MAX_SIZE=500

# Rate limiting moderado
RATE_LIMIT_RPM=60
RATE_LIMIT_BURST=10

# Logging estándar
LOG_LEVEL=INFO
LOG_FORMAT=json

# Testing deshabilitado
TESTING=false
MOCK_API=false
```

### Producción

```bash
# .env.production
TRACKHS_USERNAME=prod_user
TRACKHS_PASSWORD=prod_password
TRACKHS_API_URL=https://api.trackhs.com

# Cache optimizado
CACHE_TTL=600
CACHE_MAX_SIZE=2000

# Rate limiting estricto
RATE_LIMIT_RPM=30
RATE_LIMIT_BURST=5

# Logging mínimo
LOG_LEVEL=WARNING
LOG_FORMAT=json

# Testing deshabilitado
TESTING=false
MOCK_API=false

# Timeouts más largos
API_TIMEOUT=60
HEALTH_CHECK_TIMEOUT=30
```

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. Error de Autenticación

**Síntoma**: `AuthenticationError: Credenciales inválidas`

**Solución**:
```bash
# Verificar credenciales
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD

# Verificar URL de API
echo $TRACKHS_API_URL

# Probar conectividad
curl -u "$TRACKHS_USERNAME:$TRACKHS_PASSWORD" "$TRACKHS_API_URL/pms/units/amenities?page=1&size=1"
```

#### 2. Error de Rate Limit

**Síntoma**: `RateLimitError: Límite de requests excedido`

**Solución**:
```bash
# Aumentar rate limit
export RATE_LIMIT_RPM=120
export RATE_LIMIT_BURST=20

# O implementar backoff
export RETRY_DELAY=2
export MAX_RETRIES=5
```

#### 3. Error de Cache

**Síntoma**: `CacheError: Error en operación de cache`

**Solución**:
```bash
# Limpiar cache
python -c "from src.trackhs_mcp.cache import get_cache; get_cache().clear()"

# Reducir tamaño de cache
export CACHE_MAX_SIZE=100

# Deshabilitar cache temporalmente
export CACHE_TTL=0
```

#### 4. Error de Métricas

**Síntoma**: `MetricsError: Error en métricas`

**Solución**:
```bash
# Deshabilitar métricas temporalmente
export METRICS_ENABLED=false

# Verificar puerto de métricas
netstat -tlnp | grep 9090

# Cambiar puerto de métricas
export METRICS_PORT=9091
```

### Logs de Debugging

#### Habilitar Logs Detallados

```bash
# Logging de debug
export LOG_LEVEL=DEBUG
export LOG_FORMAT=text

# Logging de requests HTTP
export HTTPX_DEBUG=true

# Logging de cache
export CACHE_DEBUG=true
```

#### Verificar Logs

```bash
# Ver logs en tiempo real
tail -f logs/trackhs_mcp.log

# Buscar errores específicos
grep -i "error" logs/trackhs_mcp.log

# Buscar warnings
grep -i "warning" logs/trackhs_mcp.log
```

### Monitoreo de Salud

#### Health Check

```bash
# Verificar salud del servidor
curl http://localhost:8000/health

# Verificar métricas
curl http://localhost:9090/metrics
```

#### Métricas de Rendimiento

```bash
# Ver métricas de cache
curl http://localhost:9090/metrics | grep cache

# Ver métricas de requests
curl http://localhost:9090/metrics | grep requests

# Ver métricas de TrackHS API
curl http://localhost:9090/metrics | grep trackhs_api
```

### Configuración de Red

#### Firewall

```bash
# Abrir puertos necesarios
sudo ufw allow 8000  # Puerto del servidor MCP
sudo ufw allow 9090  # Puerto de métricas

# Verificar puertos abiertos
sudo ufw status
```

#### Proxy

```bash
# Configurar proxy si es necesario
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

## 📚 Referencias Adicionales

- [Documentación FastMCP](https://gofastmcp.com/)
- [Documentación TrackHS API](https://docs.trackhs.com/)
- [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [Python Environment Variables](https://docs.python.org/3/library/os.html#os.environ)

---

*Última actualización: 2024-01-15*
