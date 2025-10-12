# 🔧 Guía de Solución de Problemas - Credenciales TrackHS

## Problema Identificado

El error `Invalid credentials` en FastMCP Cloud indica que las credenciales configuradas no son válidas para la API de TrackHS.

## 🔍 Diagnóstico

### Síntomas
- Error 401 Unauthorized en las peticiones a la API
- Logs muestran "Invalid credentials"
- Las herramientas MCP fallan al hacer peticiones

### Causas Posibles
1. **Credenciales encriptadas**: Las variables de entorno contienen valores encriptados en lugar de texto plano
2. **Credenciales incorrectas**: Los valores no corresponden a credenciales reales de TrackHS
3. **Formato incorrecto**: Las credenciales no están en el formato esperado por la API

## 🛠️ Soluciones

### Solución 1: Configurar Credenciales Reales (Recomendada)

1. **Obtén las credenciales reales de TrackHS**
   - Contacta al administrador de TrackHS
   - Obtén tu usuario y contraseña reales

2. **Actualiza las variables de entorno en FastMCP Cloud**
   ```
   TRACKHS_USERNAME=tu_usuario_real
   TRACKHS_PASSWORD=tu_password_real
   ```

3. **Verifica que las credenciales sean en texto plano**
   - No deben estar encriptadas
   - No deben ser hashes o valores codificados

### Solución 2: Verificar Configuración Actual

Ejecuta el script de diagnóstico:

```bash
python scripts/diagnose_credentials.py
```

Este script te ayudará a:
- Verificar que las variables de entorno estén configuradas
- Analizar el formato de las credenciales
- Probar la conexión a la API

### Solución 3: Implementar Decodificación (Si es necesario)

Si las credenciales están encriptadas por seguridad, puedes implementar decodificación en el código:

```python
# En src/trackhs_mcp/infrastructure/adapters/config.py
def decode_credentials(encrypted_value: str) -> str:
    """Decodifica credenciales encriptadas"""
    # Implementar tu lógica de decodificación aquí
    # Por ejemplo, si están en Base64:
    # return base64.b64decode(encrypted_value).decode('utf-8')
    return encrypted_value  # Por defecto, no decodificar
```

## 🧪 Pruebas

### Prueba Manual de Credenciales

```bash
# Usando curl para probar las credenciales
curl -u "tu_usuario:tu_password" \
     -H "Content-Type: application/json" \
     https://ihmvacations.trackhs.com/api/health
```

### Prueba con el Script de Diagnóstico

```bash
# Ejecutar diagnóstico completo
python scripts/diagnose_credentials.py
```

## 📋 Checklist de Verificación

- [ ] Variables de entorno configuradas en FastMCP Cloud
- [ ] Credenciales en texto plano (no encriptadas)
- [ ] Credenciales válidas de TrackHS
- [ ] URL de API correcta
- [ ] Script de diagnóstico ejecutado
- [ ] Prueba de conexión exitosa

## 🚨 Errores Comunes

### Error: "Credenciales no configuradas"
**Solución**: Configura `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` en FastMCP Cloud

### Error: "Invalid credentials"
**Solución**: Verifica que las credenciales sean las reales de TrackHS en texto plano

### Error: "Connection timeout"
**Solución**: Verifica que la URL `TRACKHS_API_URL` sea correcta y accesible

## 📞 Soporte Adicional

Si el problema persiste:

1. **Verifica con TrackHS**: Confirma que las credenciales sean válidas
2. **Revisa los logs**: Examina los logs detallados en FastMCP Cloud
3. **Prueba localmente**: Ejecuta el conector localmente para aislar el problema
4. **Contacta soporte**: Si todo lo demás falla, contacta al equipo de soporte

## 🔄 Proceso de Actualización

1. **Actualiza credenciales** en FastMCP Cloud
2. **Reinicia el servidor** para aplicar cambios
3. **Ejecuta diagnóstico** para verificar
4. **Prueba las herramientas** MCP
5. **Monitorea los logs** para errores

---

**Nota**: Esta guía asume que tienes acceso a las credenciales reales de TrackHS. Si no las tienes, contacta al administrador de TrackHS.
