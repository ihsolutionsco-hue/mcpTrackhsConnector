# Diagnóstico Completo - TrackHS API

Este documento describe el proceso completo de diagnóstico para resolver problemas con el servidor MCP de TrackHS en FastMCP Cloud.

## 🎯 Problema Identificado

**Error:** `Error calling tool 'search_units': Recurso no encontrado: <!DOCTYPE html>...`

**Causa:** La API está devolviendo una página HTML en lugar de una respuesta JSON, lo que indica un problema de configuración.

## 🚀 Solución Completa

### Paso 1: Diagnóstico Local (Recomendado)

```bash
python scripts/run_complete_local_diagnosis.py
```

**¿Qué hace?**
- Ejecuta todos los diagnósticos locales en secuencia
- Prueba la API real de TrackHS
- Identifica la configuración correcta
- Genera un reporte completo

**Ventajas:**
- Prueba la API real antes de desplegar
- Identifica problemas de configuración
- Ahorra tiempo en FastMCP Cloud
- Proporciona diagnóstico detallado

### Paso 2: Diagnóstico en FastMCP Cloud

```bash
python scripts/complete_diagnosis.py
```

**¿Qué hace?**
- Ejecuta diagnósticos en el entorno de FastMCP Cloud
- Prueba diferentes configuraciones
- Identifica problemas específicos del entorno
- Genera reporte para soporte técnico

## 🔍 Scripts de Diagnóstico Disponibles

### Scripts Locales (Recomendados)

#### 1. Diagnóstico Completo Local
```bash
python scripts/run_complete_local_diagnosis.py
```

#### 2. Tests Locales Básicos
```bash
python scripts/run_local_tests.py
```

#### 3. Tests Individuales
```bash
python scripts/test_basic_connectivity.py
python scripts/test_current_config_local.py
python scripts/test_local_api_real.py
python scripts/test_auth_methods_local.py
```

### Scripts de FastMCP Cloud

#### 1. Diagnóstico Completo
```bash
python scripts/complete_diagnosis.py
```

#### 2. Tests Específicos
```bash
python scripts/test_specific_issue.py
python scripts/test_current_config.py
python scripts/test_url_variations_simple.py
python scripts/test_auth_methods.py
python scripts/test_endpoints.py
```

## 📋 Configuración Requerida

### Variables de Entorno
```bash
export TRACKHS_USERNAME='tu_usuario'
export TRACKHS_PASSWORD='tu_password'
export TRACKHS_API_URL='https://ihmvacations.trackhs.com/api'  # Opcional
```

### Archivo .env (Alternativa)
```bash
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
```

## 🔍 Flujo de Diagnóstico Recomendado

### 1. Diagnóstico Local (Primero)
```bash
# Ejecutar diagnóstico completo local
python scripts/run_complete_local_diagnosis.py

# Si hay problemas específicos
python scripts/test_current_config_local.py
python scripts/test_local_api_real.py
python scripts/test_auth_methods_local.py
```

### 2. Configurar FastMCP Cloud
```bash
# Usar la configuración que funcionó en local
# Configurar variables de entorno en FastMCP Cloud
# Desplegar el servidor
```

### 3. Diagnóstico en FastMCP Cloud (Si es necesario)
```bash
# Si el problema persiste en FastMCP Cloud
python scripts/complete_diagnosis.py
python scripts/test_specific_issue.py
```

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

## 📄 Archivos de Reporte

Los scripts generan archivos de reporte con timestamp:

- `complete_local_diagnosis_report_YYYYMMDD_HHMMSS.json`
- `complete_diagnosis_report_YYYYMMDD_HHMMSS.json`
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

Si los diagnósticos no resuelven el problema, contacta soporte técnico con:

1. **Archivo de reporte** (generado por los scripts)
2. **Logs del servidor** (de FastMCP Cloud)
3. **Configuración de variables** (sin credenciales)
4. **Descripción del problema** (error específico)

## 🎯 Resultado Esperado

Después de ejecutar los diagnósticos, deberías tener:

1. **Configuración funcional** identificada
2. **Variables de entorno** correctas
3. **URL base** correcta
4. **Endpoint** correcto
5. **Método de autenticación** correcto

Con esta información, puedes configurar FastMCP Cloud correctamente y resolver el problema.

## 🚀 Próximos Pasos

### 1. Ejecutar Diagnóstico Local
```bash
python scripts/run_complete_local_diagnosis.py
```

### 2. Identificar Configuración Correcta
- Revisar los resultados del diagnóstico
- Identificar la configuración que funcionó
- Anotar las variables de entorno correctas

### 3. Configurar FastMCP Cloud
- Configurar variables de entorno en FastMCP Cloud
- Usar la configuración que funcionó en local
- Desplegar el servidor

### 4. Probar en FastMCP Cloud
- Probar la herramienta `search_units`
- Verificar que funcione correctamente
- Monitorear el funcionamiento

### 5. Si hay Problemas en FastMCP Cloud
- Ejecutar diagnósticos específicos de FastMCP Cloud
- Revisar variables de entorno
- Contactar soporte técnico si es necesario

## 🔍 Ventajas del Diagnóstico Local

### ✅ Ventajas
- Prueba la API real de TrackHS
- Identifica problemas antes de desplegar
- Ahorra tiempo en FastMCP Cloud
- Proporciona diagnóstico detallado
- Permite probar múltiples configuraciones

### ⚠️ Consideraciones
- Requiere credenciales reales
- Requiere conexión a internet
- No replica exactamente el entorno de FastMCP Cloud
- Puede fallar si la API no está disponible

## 📞 Soporte Técnico

Si necesitas ayuda adicional:

1. **Revisa la documentación** en `docs/`
2. **Ejecuta los diagnósticos** y revisa los reportes
3. **Contacta soporte técnico** con los reportes generados
4. **Incluye información detallada** sobre el problema

## 🎉 Conclusión

El diagnóstico completo te ayudará a:

1. **Identificar la configuración correcta** que funciona con la API real
2. **Configurar FastMCP Cloud** con la configuración correcta
3. **Resolver el problema** de "Recurso no encontrado"
4. **Tener un servidor MCP funcional** en FastMCP Cloud

Sigue el flujo de diagnóstico recomendado y deberías poder resolver el problema exitosamente.
