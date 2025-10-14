# Solución para el Problema del Endpoint de Units Collection

## 🔍 Análisis del Problema

### Problema Identificado
El endpoint `search_units` devuelve **400 Bad Request** en todas las consultas, mientras que los endpoints de reservaciones (V1 y V2) funcionan correctamente.

### Causa Raíz
El problema está en la **diferencia entre las APIs de TrackHS**:

1. **PMS API** (funcionando): `/pms/reservations`, `/pms/folios`
2. **Channel API** (problemático): `/pms/units`

## 🏗️ Arquitectura de APIs de TrackHS

### PMS API (Property Management System)
- **Propósito**: Gestión interna de reservaciones y folios
- **Autenticación**: Basic Auth
- **Endpoints**:
  - `/pms/reservations` ✅
  - `/pms/folios` ✅
  - `/v2/pms/reservations` ✅

### Channel API (Channel Management)
- **Propósito**: Integración con canales (OTAs, websites)
- **Autenticación**: HMAC o Basic Auth (dependiendo de configuración)
- **Endpoints**:
  - `/pms/units` ❌ (problema actual)

## 🔧 Soluciones Propuestas

### Solución 1: Configuración de Autenticación HMAC

El Channel API puede requerir autenticación HMAC en lugar de Basic Auth.

**Implementación necesaria:**

```python
# src/trackhs_mcp/infrastructure/utils/auth.py
class TrackHSAuth:
    def get_hmac_headers(self) -> dict[str, str]:
        """Genera headers para autenticación HMAC"""
        import hmac
        import hashlib
        import time

        timestamp = str(int(time.time()))
        message = f"{self.config.username}{timestamp}"
        signature = hmac.new(
            self.config.password.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return {
            "Authorization": f"HMAC {self.config.username}:{signature}",
            "X-Timestamp": timestamp,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
```

### Solución 2: URL Base Diferente

El Channel API puede estar en un dominio diferente.

**Configuración necesaria:**

```python
# src/trackhs_mcp/infrastructure/adapters/config.py
class TrackHSConfig:
    # URL para PMS API
    PMS_API_URL = "https://ihmvacations.trackhs.com/api"

    # URL para Channel API (diferente)
    CHANNEL_API_URL = "https://api-integration-example.tracksandbox.io/api"

    def get_channel_api_url(self) -> str:
        """Obtiene URL para Channel API"""
        return os.getenv("TRACKHS_CHANNEL_API_URL", self.CHANNEL_API_URL)
```

### Solución 3: Credenciales Específicas

El Channel API puede requerir credenciales diferentes.

**Variables de entorno necesarias:**

```bash
# PMS API (funcionando)
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=usuario_pms
TRACKHS_PASSWORD=password_pms

# Channel API (nuevo)
TRACKHS_CHANNEL_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_CHANNEL_USERNAME=usuario_channel
TRACKHS_CHANNEL_PASSWORD=password_channel
```

## 🚀 Implementación Recomendada

### Paso 1: Modificar el Cliente API

```python
# src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py
class TrackHSApiClient:
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.auth = TrackHSAuth(config)

        # Cliente para PMS API
        self.pms_client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout or 30
        )

        # Cliente para Channel API (si está configurado)
        if hasattr(config, 'channel_api_url'):
            self.channel_client = httpx.AsyncClient(
                base_url=config.channel_api_url,
                timeout=config.timeout or 30
            )
        else:
            self.channel_client = None

    async def get_units(self, endpoint: str, params: Dict[str, Any] = None):
        """Método específico para Channel API"""
        if not self.channel_client:
            raise ValueError("Channel API no configurado")

        # Usar autenticación HMAC para Channel API
        headers = self.auth.get_hmac_headers()
        response = await self.channel_client.get(endpoint, headers=headers, params=params)
        return response
```

### Paso 2: Modificar el Caso de Uso

```python
# src/trackhs_mcp/application/use_cases/search_units.py
class SearchUnitsUseCase:
    async def execute(self, params: SearchUnitsParams) -> Dict[str, Any]:
        # Usar cliente específico para Channel API
        response = await self.api_client.get_units("/pms/units", request_params)
        return self._process_response(response)
```

## 🔄 Alternativa: Usar Datos Embebidos

### Solución Inmediata (Recomendada)

En lugar de usar el endpoint de units, aprovechar los datos embebidos en las reservaciones:

```python
# Ejemplo de uso con datos embebidos
async def get_units_from_reservations():
    """Obtiene información de unidades desde reservaciones"""
    reservations = await search_reservations_v1(size=1000)

    units = {}
    for reservation in reservations.get('_embedded', {}).get('reservations', []):
        unit_data = reservation.get('unit', {})
        unit_id = unit_data.get('id')

        if unit_id and unit_id not in units:
            units[unit_id] = {
                'id': unit_data.get('id'),
                'name': unit_data.get('name'),
                'unitCode': unit_data.get('unitCode'),
                'bedrooms': unit_data.get('bedrooms'),
                'bathrooms': unit_data.get('bathrooms'),
                'maxOccupancy': unit_data.get('maxOccupancy'),
                'petsFriendly': unit_data.get('petsFriendly'),
                'amenities': unit_data.get('amenities', []),
                'address': {
                    'streetAddress': unit_data.get('streetAddress'),
                    'locality': unit_data.get('locality'),
                    'region': unit_data.get('region'),
                    'postal': unit_data.get('postal'),
                    'country': unit_data.get('country')
                }
            }

    return list(units.values())
```

## 📊 Ventajas de la Alternativa

### ✅ Ventajas
1. **Funciona inmediatamente** - No requiere configuración adicional
2. **Datos completos** - Incluye toda la información necesaria
3. **Consistente** - Usa la misma autenticación que las reservaciones
4. **Actualizado** - Los datos están actualizados con las reservaciones

### ⚠️ Limitaciones
1. **Solo unidades con reservaciones** - No incluye unidades sin reservaciones
2. **Dependiente de reservaciones** - Requiere consultar reservaciones primero
3. **Paginación compleja** - Necesita manejar paginación de reservaciones

## 🎯 Recomendación Final

### Para Uso Inmediato
**Usar datos embebidos de reservaciones** - Esta es la solución más práctica y funcional.

### Para Desarrollo Futuro
**Implementar configuración dual** - Separar PMS API y Channel API con autenticaciones específicas.

## 📝 Próximos Pasos

1. **Implementar función de unidades desde reservaciones**
2. **Documentar la nueva funcionalidad**
3. **Crear tests para la nueva implementación**
4. **Actualizar la documentación del MCP**

## 🔗 Referencias

- [Documentación Channel API](docs/trackhsDoc/get%20unit%20collection.md)
- [Configuración actual](src/trackhs_mcp/infrastructure/adapters/config.py)
- [Cliente API](src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py)
- [Caso de uso Units](src/trackhs_mcp/application/use_cases/search_units.py)
