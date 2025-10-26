# Tests Locales - API Real de TrackHS

Este documento describe cómo probar la API real de TrackHS en local antes de desplegar en FastMCP Cloud.

## 🎯 Objetivo

Probar la conexión real con la API de TrackHS en local para verificar que:
- Las credenciales son correctas
- La URL base es correcta
- El endpoint funciona
- El método de autenticación es correcto

## 🚀 Script Principal (Recomendado)

### Tests Locales Completos
```bash
python scripts/run_local_tests.py
```

**¿Qué hace?**
- Ejecuta todos los tests locales en secuencia
- Prueba la configuración actual
- Prueba múltiples configuraciones
- Prueba diferentes métodos de autenticación
- Genera un reporte completo

**Cuándo usarlo:**
- Primera vez que pruebas la API
- Quieres verificar que todo funciona antes de desplegar
- Necesitas un diagnóstico completo

## 🔍 Scripts de Test Individuales

### 1. Test de Configuración Actual
```bash
python scripts/test_current_config_local.py
```

**¿Qué hace?**
- Prueba la configuración actual con la API real
- Verifica que las credenciales funcionen
- Confirma que el endpoint responda correctamente

**Cuándo usarlo:**
- Verificar si la configuración actual funciona
- Diagnóstico rápido
- Validación después de cambios

### 2. Test de Múltiples Configuraciones
```bash
python scripts/test_local_api_real.py
```

**¿Qué hace?**
- Prueba diferentes URLs base
- Prueba diferentes endpoints
- Encuentra la combinación correcta
- Proporciona recomendaciones específicas

**Cuándo usarlo:**
- La configuración actual no funciona
- Quieres probar diferentes configuraciones
- Necesitas encontrar la URL correcta

### 3. Test de Métodos de Autenticación
```bash
python scripts/test_auth_methods_local.py
```

**¿Qué hace?**
- Prueba Basic Auth
- Prueba Bearer Token
- Prueba headers personalizados
- Prueba API Key
- Identifica el método correcto

**Cuándo usarlo:**
- Problemas de autenticación
- Credenciales correctas pero no funcionan
- Quieres probar diferentes métodos de auth

## 📋 Configuración Requerida

### Variables de Entorno
```bash
export TRACKHS_USERNAME='tu_usuario'
export TRACKHS_PASSWORD='tu_password'
export TRACKHS_API_URL='https://ihmvacations.trackhs.com/api'  # Opcional
```

### Archivo .env (Alternativa)
```bash
# Crear archivo .env en el directorio raíz
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
```

## 🔍 Interpretación de Resultados

### ✅ Test Exitoso
```
✅ Respuesta JSON válida recibida
✅ Autenticación básica exitosa
✅ Configuración actual funciona
```

**Significado:** La configuración funciona correctamente con la API real.

**Acción:** Usar esta configuración en FastMCP Cloud.

### ❌ Test Fallido
```
❌ HTTP Error 401
❌ Respuesta HTML recibida
❌ Credenciales inválidas
```

**Significado:** Hay un problema con la configuración.

**Acción:** Revisar el error específico y probar soluciones.

### ⚠️ Test Parcial
```
⚠️ Algunos tests fallaron
⚠️ Configuración parcialmente funcional
```

**Significado:** Algunas configuraciones funcionan, otras no.

**Acción:** Usar la configuración que funcionó.

## 🛠️ Soluciones Comunes

### Problema: Credenciales Incorrectas
```bash
# Verificar con TrackHS
# Obtener credenciales correctas
# Actualizar variables de entorno
```

### Problema: URL Base Incorrecta
```bash
# Probar diferentes URLs
https://ihmvacations.trackhs.com/api
https://ihmvacations.trackhs.com
https://api.trackhs.com/api
https://api.trackhs.com
```

### Problema: Endpoint Incorrecto
```bash
# Probar diferentes endpoints
pms/units
units
api/pms/units
```

### Problema: Método de Autenticación Incorrecto
```bash
# Probar diferentes métodos
Basic Auth (usuario/contraseña)
Bearer Token
Headers personalizados
API Key
```

## 📋 Flujo de Testing Recomendado

### 1. Test Inicial
```bash
python scripts/run_local_tests.py
```

### 2. Si hay problemas específicos
```bash
python scripts/test_current_config_local.py
```

### 3. Si la configuración no funciona
```bash
python scripts/test_local_api_real.py
python scripts/test_auth_methods_local.py
```

### 4. Si necesitas diagnóstico exhaustivo
```bash
python scripts/complete_diagnosis.py
```

## 📄 Archivos de Reporte

Los scripts generan archivos de reporte con timestamp:

- `local_tests_report_YYYYMMDD_HHMMSS.json`
- `local_api_test_results.json`
- `auth_methods_test_results.json`

**Incluye estos archivos cuando contactes soporte técnico.**

## 🔧 Configuración para FastMCP Cloud

### Variables de Entorno Requeridas
```bash
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
```

### Variables de Entorno Opcionales
```bash
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
```

### Estructura de Archivos Requerida
```
src/trackhs_mcp/__main__.py
src/trackhs_mcp/server.py
fastmcp.json
requirements.txt
```

## 📞 Soporte Técnico

Si los tests locales no resuelven el problema, contacta soporte técnico con:

1. **Archivo de reporte** (generado por los scripts)
2. **Logs del servidor** (de FastMCP Cloud)
3. **Configuración de variables** (sin credenciales)
4. **Descripción del problema** (error específico)

## 🎯 Resultado Esperado

Después de ejecutar los tests locales, deberías tener:

1. **Configuración funcional** identificada
2. **Variables de entorno** correctas
3. **URL base** correcta
4. **Endpoint** correcto
5. **Método de autenticación** correcto

Con esta información, puedes configurar FastMCP Cloud correctamente y resolver el problema.

## 🔍 Ventajas de Testing Local

### ✅ Ventajas
- Prueba la API real de TrackHS
- Verifica credenciales antes de desplegar
- Identifica problemas de configuración
- Proporciona diagnóstico detallado
- Ahorra tiempo en FastMCP Cloud

### ⚠️ Consideraciones
- Requiere credenciales reales
- Requiere conexión a internet
- Puede fallar si la API no está disponible
- No replica exactamente el entorno de FastMCP Cloud

## 🚀 Próximos Pasos

1. **Ejecutar tests locales** para verificar la configuración
2. **Identificar la configuración correcta** que funciona
3. **Configurar FastMCP Cloud** con la configuración correcta
4. **Desplegar el servidor** en FastMCP Cloud
5. **Probar la herramienta** `search_units` en FastMCP Cloud

Si los tests locales son exitosos, la configuración debería funcionar en FastMCP Cloud.
