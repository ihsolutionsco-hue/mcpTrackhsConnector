# 🚀 Guía de Despliegue en Producción - TrackHS MCP Connector

## 📋 Problema Identificado

El servidor MCP funciona localmente pero **no encuentra los endpoints en producción**. Esto se debe a que las variables de entorno no están configuradas correctamente en el servidor de producción.

## 🔧 Solución

### 1. Configurar Variables de Entorno

En tu servidor de producción, configura las siguientes variables de entorno:

```bash
# Variables REQUERIDAS
export TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
export TRACKHS_USERNAME=tu_usuario_real
export TRACKHS_PASSWORD=tu_password_real
export TRACKHS_TIMEOUT=30

# Variables opcionales
export PRODUCTION=true
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO
```

### 2. Crear Archivo .env en Producción

Crea un archivo `.env` en el directorio del servidor con:

```env
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=tu_usuario_real
TRACKHS_PASSWORD=tu_password_real
TRACKHS_TIMEOUT=30
PRODUCTION=true
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Verificar Credenciales

**IMPORTANTE**: Las credenciales deben ser **reales y válidas**:

- ❌ **NO usar**: `your_username_here`, `your_password_here`
- ✅ **SÍ usar**: Credenciales reales de tu cuenta TrackHS

### 4. Verificar Conectividad

Ejecuta el script de verificación:

```bash
python verify_production_connectivity.py
```

## 🔍 Diagnóstico de Problemas

### Error: "Endpoint not found"

**Causa**: Variables de entorno no configuradas o credenciales incorrectas.

**Solución**:
1. Verificar que `TRACKHS_API_URL` esté configurada
2. Verificar que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` sean reales
3. Ejecutar script de diagnóstico

### Error: "Invalid credentials"

**Causa**: Credenciales expiradas o incorrectas.

**Solución**:
1. Contactar al administrador de TrackHS
2. Verificar que la cuenta esté activa
3. Confirmar permisos de API

### Error: "Connection timeout"

**Causa**: Problemas de conectividad de red.

**Solución**:
1. Verificar firewall del servidor
2. Probar conectividad a `https://ihmvacations.trackhs.com`
3. Verificar proxy si aplica

## 📊 Verificación de Estado

### Scripts de Diagnóstico

1. **Configuración**: `python diagnose_production_config.py`
2. **Conectividad**: `python verify_production_connectivity.py`

### Endpoints a Verificar

- ✅ **API V2**: `https://ihmvacations.trackhs.com/api/v2/pms/reservations`
- ✅ **API V1**: `https://ihmvacations.trackhs.com/api/pms/reservations`

## 🛠️ Configuración por Plataforma

### Docker

```dockerfile
ENV TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
ENV TRACKHS_USERNAME=tu_usuario_real
ENV TRACKHS_PASSWORD=tu_password_real
ENV TRACKHS_TIMEOUT=30
```

### Kubernetes

```yaml
env:
- name: TRACKHS_API_URL
  value: "https://ihmvacations.trackhs.com/api"
- name: TRACKHS_USERNAME
  value: "tu_usuario_real"
- name: TRACKHS_PASSWORD
  value: "tu_password_real"
```

### Heroku

```bash
heroku config:set TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
heroku config:set TRACKHS_USERNAME=tu_usuario_real
heroku config:set TRACKHS_PASSWORD=tu_password_real
```

## ✅ Checklist de Despliegue

- [ ] Variables de entorno configuradas
- [ ] Credenciales reales (no de ejemplo)
- [ ] Conectividad de red verificada
- [ ] Script de diagnóstico ejecutado
- [ ] Endpoints V1 y V2 funcionando
- [ ] Logs de error revisados

## 🆘 Soporte

Si sigues teniendo problemas:

1. Ejecuta `python diagnose_production_config.py`
2. Revisa los logs del servidor
3. Verifica la conectividad de red
4. Contacta al administrador de TrackHS

---

**Nota**: Este problema es común en despliegues donde las variables de entorno no se configuran correctamente en el entorno de producción.
