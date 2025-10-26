# Scripts de Diagnóstico para FastMCP Cloud - TrackHS API

Este documento describe todos los scripts de diagnóstico disponibles para resolver problemas con el servidor MCP de TrackHS en FastMCP Cloud.

## 🚀 Script Principal (Recomendado)

### Diagnóstico Completo
```bash
python scripts/complete_diagnosis.py
```

**¿Qué hace?**
- Ejecuta todos los diagnósticos en secuencia
- Genera un reporte completo con timestamp
- Proporciona recomendaciones específicas
- Guarda resultados en archivo JSON

**Cuándo usarlo:**
- Primera vez que experimentas el problema
- Quieres un diagnóstico completo
- Necesitas un reporte para soporte técnico

## 🔍 Scripts de Diagnóstico Específicos

### 1. Verificación de Configuración
```bash
python scripts/check_fastmcp_cloud_config.py
```

**¿Qué hace?**
- Verifica variables de entorno
- Valida configuración de fastmcp.json
- Comprueba estructura de archivos
- Verifica dependencias

**Cuándo usarlo:**
- Problemas de configuración inicial
- Variables de entorno no configuradas
- Errores de dependencias

### 2. Diagnóstico del Problema Específico
```bash
python scripts/test_specific_issue.py
```

**¿Qué hace?**
- Reproduce exactamente el error reportado
- Analiza la respuesta HTML recibida
- Identifica la causa raíz del problema
- Proporciona diagnóstico específico

**Cuándo usarlo:**
- Tienes el error específico: "Recurso no encontrado: <!DOCTYPE html>..."
- Quieres entender exactamente qué está pasando
- Necesitas un análisis detallado del problema

### 3. Prueba de Configuración Actual
```bash
python scripts/test_current_config.py
```

**¿Qué hace?**
- Prueba la configuración actual
- Verifica conectividad
- Valida credenciales
- Confirma que el endpoint funciona

**Cuándo usarlo:**
- Verificar si la configuración actual funciona
- Diagnóstico rápido
- Validación después de cambios

### 4. Prueba de Variaciones de URL
```bash
python scripts/test_url_variations_simple.py
```

**¿Qué hace?**
- Prueba diferentes URLs base
- Prueba diferentes endpoints
- Encuentra la combinación correcta
- Proporciona recomendaciones específicas

**Cuándo usarlo:**
- La URL base podría ser incorrecta
- Quieres probar diferentes configuraciones
- Necesitas encontrar la URL correcta

### 5. Prueba de Métodos de Autenticación
```bash
python scripts/test_auth_methods.py
```

**¿Qué hace?**
- Prueba Basic Auth
- Prueba Bearer Token
- Prueba headers personalizados
- Identifica el método correcto

**Cuándo usarlo:**
- Problemas de autenticación
- Credenciales correctas pero no funcionan
- Quieres probar diferentes métodos de auth

### 6. Prueba de Endpoints Disponibles
```bash
python scripts/test_endpoints.py
```

**¿Qué hace?**
- Prueba diferentes endpoints
- Identifica endpoints disponibles
- Encuentra el endpoint correcto
- Proporciona lista de endpoints funcionales

**Cuándo usarlo:**
- El endpoint podría ser incorrecto
- Quieres ver qué endpoints están disponibles
- Necesitas encontrar el endpoint correcto

### 7. Diagnóstico Avanzado
```bash
python scripts/diagnose_fastmcp_cloud.py
```

**¿Qué hace?**
- Prueba múltiples configuraciones
- Genera reporte detallado
- Proporciona análisis completo
- Guarda resultados en JSON

**Cuándo usarlo:**
- Diagnóstico exhaustivo
- Necesitas probar muchas configuraciones
- Quieres un análisis completo

## 📊 Interpretación de Resultados

### ✅ Resultado Exitoso
```
✅ Configuración exitosa
✅ Endpoint funciona
✅ Autenticación exitosa
```

**Significado:** La configuración funciona correctamente.

**Acción:** Usar esta configuración en FastMCP Cloud.

### ❌ Resultado Fallido
```
❌ Error HTTP 404
❌ Respuesta HTML recibida
❌ Credenciales inválidas
```

**Significado:** Hay un problema con la configuración.

**Acción:** Revisar el error específico y probar soluciones.

### ⚠️ Resultado Parcial
```
⚠️ Algunos tests fallaron
⚠️ Configuración parcialmente funcional
```

**Significado:** Algunas configuraciones funcionan, otras no.

**Acción:** Usar la configuración que funcionó.

## 🛠️ Soluciones Comunes

### Problema: Variables de Entorno No Configuradas
```bash
# Configurar en FastMCP Cloud
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
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
```

## 📋 Flujo de Diagnóstico Recomendado

### 1. Diagnóstico Inicial
```bash
python scripts/complete_diagnosis.py
```

### 2. Si hay problemas específicos
```bash
python scripts/test_specific_issue.py
```

### 3. Si la configuración no funciona
```bash
python scripts/test_url_variations_simple.py
python scripts/test_auth_methods.py
python scripts/test_endpoints.py
```

### 4. Si necesitas diagnóstico exhaustivo
```bash
python scripts/diagnose_fastmcp_cloud.py
```

## 📄 Archivos de Reporte

Los scripts generan archivos de reporte con timestamp:

- `complete_diagnosis_report_YYYYMMDD_HHMMSS.json`
- `fastmcp_cloud_diagnosis.json`
- `full_diagnosis_results.json`

**Incluye estos archivos cuando contactes soporte técnico.**

## 🔧 Configuración en FastMCP Cloud

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

Si los scripts no resuelven el problema, contacta soporte técnico con:

1. **Archivo de reporte** (generado por los scripts)
2. **Logs del servidor** (de FastMCP Cloud)
3. **Configuración de variables** (sin credenciales)
4. **Descripción del problema** (error específico)

## 🎯 Resultado Esperado

Después de ejecutar los scripts de diagnóstico, deberías tener:

1. **Configuración funcional** identificada
2. **Variables de entorno** correctas
3. **URL base** correcta
4. **Endpoint** correcto
5. **Método de autenticación** correcto

Con esta información, puedes configurar FastMCP Cloud correctamente y resolver el problema.
