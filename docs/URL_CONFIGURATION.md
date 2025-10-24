# Configuración de URL Base - TrackHS MCP Connector

## Problema Común: Duplicación de `/api` en URLs

### Síntoma

En los logs del servidor, ves URLs con `/api` duplicado:

```
https://ihmvacations.trackhs.com/api/api/v2/pms/reservations/37166708
                                      ↑   ↑
                                      ERROR: /api aparece dos veces
```

Esto resulta en un error 404:

```
ApiError: Endpoint not found: /api/v2/pms/reservations/37166708
```

### Causa

El problema ocurre cuando la variable de entorno `TRACKHS_API_URL` se configura incorrectamente con `/api` al final.

### Solución

#### ✅ Configuración Correcta

```bash
# Variable de entorno
TRACKHS_API_URL=https://ihmvacations.trackhs.com
```

**Sin** `/api` al final.

#### ❌ Configuración Incorrecta

```bash
# NO hagas esto
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
```

Esto causa el doble `/api`.

## Cómo Funciona

Los endpoints en el código **ya incluyen** el prefijo `/api`:

```python
# En get_reservation.py
endpoint = f"/api/v2/pms/reservations/{params.reservation_id}"

# En search_units.py
endpoint = "/api/pms/units"

# En search_reservations.py
endpoint = "/api/v2/pms/reservations"
```

Cuando httpx (el cliente HTTP) hace una petición, concatena:

```
base_url + endpoint
```

Por lo tanto:

- **Correcto:** `https://ihmvacations.trackhs.com` + `/api/v2/pms/reservations/123` = ✅
- **Incorrecto:** `https://ihmvacations.trackhs.com/api` + `/api/v2/pms/reservations/123` = ❌ (doble `/api`)

## Configuración en FastMCP Cloud

Al desplegar en FastMCP Cloud, asegúrate de configurar las variables de entorno así:

```
TRACKHS_API_URL=https://ihmvacations.trackhs.com
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

## Auto-Corrección

Desde la versión actual, el código detecta automáticamente si `TRACKHS_API_URL` contiene `/api` al final y lo elimina, mostrando un warning:

```
WARNING - base_url contiene '/api' al final (https://ihmvacations.trackhs.com/api).
Eliminándolo para evitar duplicación.
Configure TRACKHS_API_URL sin /api (ej: https://ihmvacations.trackhs.com)
```

Sin embargo, es mejor configurar correctamente desde el inicio.

## Debugging

Para verificar que la URL se está construyendo correctamente, revisa los logs en nivel DEBUG:

```bash
# Activar logs de debug
DEBUG=true

# En los logs verás:
API Request: GET /api/v2/pms/reservations/123
Base URL: https://ihmvacations.trackhs.com
Full URL: https://ihmvacations.trackhs.com/api/v2/pms/reservations/123
```

Verifica que `Full URL` **no** tenga `/api` duplicado.

## Variables de Entorno Relacionadas

```bash
# Requeridas
TRACKHS_API_URL=https://ihmvacations.trackhs.com  # Sin /api al final
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña

# Opcionales
TRACKHS_TIMEOUT=60                                 # Timeout general (segundos)
TRACKHS_SEARCH_TIMEOUT=120                         # Timeout para búsquedas (segundos)
DEBUG=false                                        # Activar logs detallados
```

## Resumen

| Configuración | Resultado | Estado |
|---------------|-----------|--------|
| `https://ihmvacations.trackhs.com` | `https://ihmvacations.trackhs.com/api/v2/pms/...` | ✅ Correcto |
| `https://ihmvacations.trackhs.com/` | `https://ihmvacations.trackhs.com/api/v2/pms/...` | ✅ Correcto (se normaliza) |
| `https://ihmvacations.trackhs.com/api` | ~~`https://ihmvacations.trackhs.com/api/api/v2/pms/...`~~ → Auto-corregido a ✅ | ⚠️ Warning |
| `https://ihmvacations.trackhs.com/api/` | ~~`https://ihmvacations.trackhs.com/api/api/v2/pms/...`~~ → Auto-corregido a ✅ | ⚠️ Warning |

## Soporte

Si continúas experimentando problemas de URL después de verificar la configuración:

1. Revisa los logs del servidor buscando warnings sobre URL
2. Verifica que no tengas configuraciones conflictivas en `.env` o variables de sistema
3. Reinicia el servidor después de cambiar las variables de entorno
4. Abre un issue en GitHub con los logs completos

---

**Última actualización:** 2025-10-24

