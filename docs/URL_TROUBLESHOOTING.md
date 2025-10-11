# Guía de Solución de Problemas - URLs y Endpoints

## 🔍 Problemas Comunes con URLs y Endpoints

### **1. Error 404 - Endpoint not found**

**Síntomas:**
```
Error — Endpoint not found: /v2/pms/reservations
```

**Causas posibles:**
- URL base incorrecta
- Endpoint no existe en esa URL base
- Problemas de red o DNS

**Soluciones:**

#### **Paso 1: Validar URL Base**
```bash
# Ejecutar validador de URLs
python validate_urls.py
```

#### **Paso 2: Verificar Configuración**
```bash
# Verificar variables de entorno
echo $TRACKHS_API_URL
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD
```

#### **Paso 3: Probar URLs Manualmente**
```bash
# Probar con curl
curl -I "https://api-integration-example.tracksandbox.io/api/v2/pms/reservations"
curl -I "https://ihvmvacations.trackhs.com/api/v2/pms/reservations"
```

### **2. Error 401 - Unauthorized**

**Síntomas:**
```
AuthenticationError: Invalid credentials
```

**Causas:**
- Credenciales incorrectas
- Usuario sin permisos
- Token expirado

**Soluciones:**
1. Verificar credenciales en `.env`
2. Contactar administrador para permisos
3. Regenerar credenciales si es necesario

### **3. Error 403 - Forbidden**

**Síntomas:**
```
AuthenticationError: Access forbidden
```

**Causas:**
- Usuario sin permisos para el endpoint
- Restricciones de IP
- Límites de API

**Soluciones:**
1. Verificar permisos de usuario
2. Contactar soporte técnico
3. Revisar límites de API

### **4. Error de Conexión**

**Síntomas:**
```
NetworkError: Connection error
```

**Causas:**
- Problemas de red
- Firewall bloqueando conexiones
- DNS no resuelve

**Soluciones:**
1. Verificar conectividad de red
2. Configurar proxy si es necesario
3. Verificar DNS

## 🛠️ Herramientas de Diagnóstico

### **1. Validador de URLs**
```bash
python validate_urls.py
```

### **2. Test Local**
```bash
python test_local.py
```

### **3. Tests Unitarios**
```bash
pytest tests/unit/
```

### **4. Tests de Integración**
```bash
pytest tests/integration/
```

## 📋 Checklist de Solución de Problemas

### **Antes de Reportar un Problema:**

- [ ] ¿Ejecutaste `python validate_urls.py`?
- [ ] ¿Verificaste las variables de entorno?
- [ ] ¿Probaste con credenciales reales?
- [ ] ¿Revisaste los logs de error?
- [ ] ¿Probaste diferentes URLs base?

### **Información para Reportar:**

1. **URL base utilizada:**
2. **Endpoint que falla:**
3. **Código de error exacto:**
4. **Variables de entorno (sin credenciales):**
5. **Logs completos del error:**
6. **Resultado de `validate_urls.py`:**

## 🔧 Configuraciones Recomendadas

### **Para Desarrollo:**
```bash
TRACKHS_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_USERNAME=test_user
TRACKHS_PASSWORD=test_password
```

### **Para Testing:**
```bash
TRACKHS_API_URL=https://api-test.trackhs.com/api
TRACKHS_USERNAME=test_user
TRACKHS_PASSWORD=test_password
```

### **Para Producción:**
```bash
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario_real
TRACKHS_PASSWORD=tu_password_real
```

### **Para IHVM:**
```bash
TRACKHS_API_URL=https://ihvmvacations.trackhs.com/api
TRACKHS_USERNAME=tu_usuario_ihvm
TRACKHS_PASSWORD=tu_password_ihvm
```

## 📞 Soporte

Si los problemas persisten:

1. **Revisar documentación:** `docs/`
2. **Ejecutar tests:** `pytest tests/`
3. **Contactar soporte técnico** con información completa
4. **Verificar estado de la API** en el dashboard de TrackHS

## 🔄 Actualizaciones

- **v1.0:** Configuración inicial
- **v1.1:** Agregado validador de URLs
- **v1.2:** Configuración centralizada
- **v1.3:** Documentación de troubleshooting
