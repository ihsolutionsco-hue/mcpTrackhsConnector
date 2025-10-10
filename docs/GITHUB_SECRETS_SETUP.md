# Configuración de Secrets en GitHub

## Configuración de Secrets Requeridos

Para que el deployment automático funcione correctamente, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

### Secrets Requeridos

1. **`TRACKHS_API_URL`**
   - **Descripción**: URL base de la API de Track HS
   - **Valor**: `https://api.trackhs.com/api`
   - **Ejemplo**: `https://api.trackhs.com/api`

2. **`TRACKHS_USERNAME`**
   - **Descripción**: Nombre de usuario para autenticación con Track HS
   - **Valor**: Tu nombre de usuario de Track HS
   - **Ejemplo**: `tu_usuario_trackhs`

3. **`TRACKHS_PASSWORD`**
   - **Descripción**: Contraseña para autenticación con Track HS
   - **Valor**: Tu contraseña de Track HS
   - **Ejemplo**: `tu_contraseña_segura`

## Cómo Configurar los Secrets

### Paso 1: Acceder a la Configuración del Repositorio

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **"Settings"** (Configuración)
3. En el menú lateral izquierdo, haz clic en **"Secrets and variables"**
4. Selecciona **"Actions"**

### Paso 2: Agregar Cada Secret

Para cada secret:

1. Haz clic en **"New repository secret"**
2. En el campo **"Name"**, ingresa el nombre del secret (ej: `TRACKHS_API_URL`)
3. En el campo **"Secret"**, ingresa el valor correspondiente
4. Haz clic en **"Add secret"**

### Paso 3: Verificar la Configuración

Después de agregar todos los secrets, deberías ver:

- `TRACKHS_API_URL`
- `TRACKHS_USERNAME`
- `TRACKHS_PASSWORD`

## Validación de Secrets

El workflow de GitHub Actions incluye validación automática de secrets:

```yaml
- name: Validate secrets
  run: |
    echo "Validating required secrets..."
    if [ -z "${{ secrets.TRACKHS_API_URL }}" ]; then
      echo "Warning: TRACKHS_API_URL secret is not set"
      echo "Please configure this secret in GitHub repository settings"
    else
      echo "TRACKHS_API_URL is configured"
    fi
    # ... validación para otros secrets
```

## Troubleshooting

### Error: "Context access might be invalid"

Este error aparece en el linter local porque los secrets no están configurados en tu entorno local. Es normal y no afecta el funcionamiento en GitHub.

**Solución**: Los secrets solo están disponibles en el entorno de GitHub Actions, no en tu máquina local.

### Error: "Secret is not set"

Si ves este error en los logs de GitHub Actions:

1. Verifica que el secret esté configurado en GitHub
2. Asegúrate de que el nombre del secret sea exactamente el mismo (case-sensitive)
3. Verifica que el valor del secret no esté vacío

### Error: "Authentication failed"

Si el deployment falla por autenticación:

1. Verifica que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` sean correctos
2. Verifica que `TRACKHS_API_URL` sea la URL correcta de la API
3. Prueba las credenciales localmente primero

## Testing Local

Antes de hacer push, puedes probar localmente:

```bash
# Configurar variables de entorno localmente
export TRACKHS_API_URL="https://api.trackhs.com/api"
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_contraseña"

# Probar el servidor localmente
python test_local.py

# Probar con FastMCP
fastmcp dev
```

## Seguridad

### Mejores Prácticas

1. **Nunca** incluyas secrets en el código
2. **Nunca** hagas commit de archivos `.env` con credenciales reales
3. Usa **diferentes credenciales** para desarrollo y producción
4. **Rota las contraseñas** regularmente
5. Usa **tokens de API** en lugar de contraseñas cuando sea posible

### Archivos a Ignorar

Asegúrate de que estos archivos estén en `.gitignore`:

```
.env
.env.local
.env.production
*.key
*.pem
```

## Verificación Post-Configuración

Después de configurar los secrets:

1. Haz un commit y push a la rama `main`
2. Ve a la pestaña **"Actions"** en GitHub
3. Verifica que el workflow se ejecute sin errores
4. Revisa los logs para confirmar que los secrets se cargan correctamente

## Soporte

Si tienes problemas con la configuración:

1. Revisa los logs de GitHub Actions
2. Verifica que todos los secrets estén configurados
3. Prueba las credenciales localmente primero
4. Consulta la documentación de FastMCP

---

**Configuración Completada** - Secrets configurados correctamente para deployment automático
