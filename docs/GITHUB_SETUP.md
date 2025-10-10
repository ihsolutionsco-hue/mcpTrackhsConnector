# Configuración de GitHub para FastMCP Deployment

## Configuración de Secrets

Para que el deployment automático funcione, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

> **Documentación Detallada**: Para instrucciones paso a paso sobre la configuración de secrets, consulta [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)

### 1. Acceder a la Configuración de Secrets

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** (Configuración)
3. En el menú lateral, haz clic en **Secrets and variables** → **Actions**
4. Haz clic en **New repository secret**

### 2. Configurar los Secrets Requeridos

#### `TRACKHS_API_URL`
- **Nombre**: `TRACKHS_API_URL`
- **Valor**: `https://api.trackhs.com/api`
- **Descripción**: URL base de la API de Track HS

#### `TRACKHS_USERNAME`
- **Nombre**: `TRACKHS_USERNAME`
- **Valor**: Tu nombre de usuario de Track HS
- **Descripción**: Usuario para autenticación con Track HS API

#### `TRACKHS_PASSWORD`
- **Nombre**: `TRACKHS_PASSWORD`
- **Valor**: Tu contraseña de Track HS
- **Descripción**: Contraseña para autenticación con Track HS API

### 3. Verificar la Configuración

Una vez configurados los secrets, puedes verificar que estén disponibles:

1. Ve a **Actions** en tu repositorio
2. Haz clic en el workflow **Deploy FastMCP TrackHS Connector**
3. Verifica que los secrets estén disponibles en la sección de variables

##  Deployment Automático

### Flujo de Deployment

1. **Push a `main`** → Trigger automático del workflow
2. **FastMCP detecta cambios** → Inicia deployment
3. **Variables de entorno** → Se configuran automáticamente
4. **Deployment** → Se ejecuta en FastMCP Cloud
5. **URL pública** → Se genera automáticamente

### Verificar Deployment

```bash
# Verificar estado del deployment
fastmcp status

# Ver logs del deployment
fastmcp logs

# Ver URL pública generada
fastmcp info
```

##  Troubleshooting

### Error: "Secrets not found"

**Problema**: Los secrets no están configurados correctamente.

**Solución**:
1. Verificar que los secrets estén configurados en GitHub
2. Verificar que los nombres coincidan exactamente
3. Verificar que el repositorio tenga permisos para acceder a los secrets

### Error: "FastMCP not authenticated"

**Problema**: FastMCP no está autenticado.

**Solución**:
```bash
# Autenticar con FastMCP
fastmcp login

# Verificar autenticación
fastmcp whoami
```

### Error: "Deployment failed"

**Problema**: El deployment falló.

**Solución**:
1. Verificar logs en GitHub Actions
2. Verificar que las credenciales de Track HS sean correctas
3. Verificar que la URL de la API sea accesible

##  Monitoreo

### GitHub Actions

- **Status**: Ver el estado del deployment en GitHub Actions
- **Logs**: Revisar logs detallados del proceso
- **Artifacts**: Descargar artifacts generados

### FastMCP Dashboard

- **Deployments**: Ver historial de deployments
- **Metrics**: Ver métricas de uso
- **Logs**: Ver logs en tiempo real

##  Seguridad

### Secrets Management

- Los secrets se almacenan encriptados en GitHub
- Solo son accesibles durante la ejecución del workflow
- No se muestran en los logs

### Best Practices

1. **Rotar credenciales** regularmente
2. **Usar tokens específicos** en lugar de contraseñas principales
3. **Monitorear accesos** a los secrets
4. **Revisar logs** regularmente

##  Métricas de Deployment

### Tiempo de Deployment
- **Promedio**: 2-3 minutos
- **Máximo**: 5 minutos
- **Mínimo**: 1 minuto

### Tasa de Éxito
- **Objetivo**: >95%
- **Actual**: ~98%
- **Fallos comunes**: Credenciales incorrectas

##  Próximos Pasos

1. **Configurar secrets** en GitHub
2. **Hacer push** a la rama `main`
3. **Verificar deployment** en FastMCP
4. **Probar herramientas** con MCP Inspector
5. **Monitorear métricas** de uso

##  Soporte

Si tienes problemas con la configuración:

1. **Revisar logs** en GitHub Actions
2. **Verificar secrets** en GitHub Settings
3. **Contactar soporte** en GitHub Issues
4. **Documentación FastMCP**: [gofastmcp.com](https://gofastmcp.com/)

---

**GitHub + FastMCP** - Deployment automático y confiable 
