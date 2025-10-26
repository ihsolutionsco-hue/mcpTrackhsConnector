# Diagnóstico de FastMCP Cloud - TrackHS API

Este documento describe cómo diagnosticar problemas con el servidor MCP de TrackHS cuando se ejecuta en FastMCP Cloud.

## Problema Identificado

El error que estás experimentando es:

```
Error calling tool 'search_units': Recurso no encontrado: <!DOCTYPE html><html lang="en">...
```

Este error indica que la API está devolviendo una página HTML de "Page not found" en lugar de una respuesta JSON, lo que sugiere:

1. **URL incorrecta**: El endpoint no existe o la URL base es incorrecta
2. **Problema de autenticación**: Las credenciales no son válidas
3. **Endpoint incorrecto**: El path del endpoint no es el correcto

## Scripts de Diagnóstico

### 1. Diagnóstico Completo

```bash
python scripts/run_full_diagnosis.py
```

Este script ejecuta todos los diagnósticos automáticamente y genera un reporte completo.

### 2. Diagnósticos Individuales

#### Probar Configuración Actual
```bash
python scripts/test_current_config.py
```

#### Probar Variaciones de URL
```bash
python scripts/test_url_variations_simple.py
```

#### Probar Métodos de Autenticación
```bash
python scripts/test_auth_methods.py
```

#### Probar Endpoints Disponibles
```bash
python scripts/test_endpoints.py
```

#### Diagnóstico Avanzado
```bash
python scripts/diagnose_fastmcp_cloud.py
```

## Configuración de Variables de Entorno

Asegúrate de que las siguientes variables estén configuradas en FastMCP Cloud:

```bash
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api  # Opcional
```

## Posibles Soluciones

### 1. Verificar URL Base

La URL base por defecto es `https://ihmvacations.trackhs.com/api`. Si esta no funciona, prueba:

- `https://ihmvacations.trackhs.com` (sin `/api`)
- `https://api.trackhs.com/api`
- `https://api.trackhs.com`

### 2. Verificar Endpoint

El endpoint por defecto es `pms/units`. Si este no funciona, prueba:

- `units`
- `api/pms/units`
- `pms/units/`

### 3. Verificar Credenciales

Asegúrate de que las credenciales sean correctas:

- Username: Tu nombre de usuario de TrackHS
- Password: Tu contraseña de TrackHS

### 4. Verificar Método de Autenticación

TrackHS puede usar diferentes métodos de autenticación:

- **Basic Auth** (usuario/contraseña)
- **Bearer Token** (token de API)
- **Headers personalizados** (X-API-Key, X-API-Secret)

## Mejoras Implementadas

### 1. Logging Mejorado

El servidor ahora incluye logging detallado que muestra:

- URL completa de la petición
- Headers de respuesta
- Preview del contenido de respuesta
- Detección automática de respuestas HTML

### 2. Manejo de Errores Mejorado

- Detección automática de respuestas HTML
- Mensajes de error más descriptivos
- Diagnóstico de problemas de autenticación

### 3. Scripts de Diagnóstico

- Scripts automatizados para probar diferentes configuraciones
- Reportes detallados de resultados
- Recomendaciones automáticas

## Uso de los Scripts

### Ejecutar Diagnóstico Completo

```bash
# Desde el directorio raíz del proyecto
python scripts/run_full_diagnosis.py
```

### Ejecutar Diagnóstico Específico

```bash
# Probar solo la configuración actual
python scripts/test_current_config.py

# Probar diferentes URLs
python scripts/test_url_variations_simple.py

# Probar métodos de autenticación
python scripts/test_auth_methods.py

# Probar endpoints
python scripts/test_endpoints.py
```

## Interpretación de Resultados

### ✅ Configuración Exitosa

Si un script muestra "✅", significa que esa configuración funciona correctamente.

### ❌ Configuración Fallida

Si un script muestra "❌", revisa:

1. **Credenciales**: Verifica que TRACKHS_USERNAME y TRACKHS_PASSWORD sean correctos
2. **URL Base**: Prueba diferentes variaciones de URL
3. **Endpoint**: Verifica que el endpoint sea correcto
4. **Red**: Verifica la conectividad de red

### 🔍 Respuesta HTML

Si recibes una respuesta HTML en lugar de JSON, significa:

- El endpoint no existe
- La URL base es incorrecta
- Hay un problema de autenticación

## Solución Recomendada

1. **Ejecuta el diagnóstico completo**:
   ```bash
   python scripts/run_full_diagnosis.py
   ```

2. **Revisa los resultados** y usa la configuración que funcionó

3. **Actualiza las variables de entorno** en FastMCP Cloud con la configuración exitosa

4. **Reinicia el servidor** en FastMCP Cloud

## Contacto

Si los scripts de diagnóstico no resuelven el problema, contacta al soporte técnico con:

1. Los resultados de los scripts de diagnóstico
2. Los logs del servidor
3. La configuración de variables de entorno (sin las credenciales)
