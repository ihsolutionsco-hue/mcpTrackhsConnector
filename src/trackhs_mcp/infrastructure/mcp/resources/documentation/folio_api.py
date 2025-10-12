"""
Documentation resources para Folio API
Información concisa de la documentación de Folio API
"""

from typing import Any, Dict

from ....application.ports.api_client_port import ApiClientPort


def register_folio_api_documentation(mcp, api_client: ApiClientPort):
    """Registra la documentación de Folio API"""

    @mcp.resource(
        "trackhs://docs/folio-api",
        name="Folio API Documentation",
        description="Essential documentation for Folio API",
        mime_type="text/plain",
    )
    async def folio_api_docs() -> str:
        """Documentación concisa de Folio API"""
        return """# TrackHS Folio API - Get Folio

## Endpoint
- **URL**: `GET /pms/folios/{folioId}`
- **Versión**: 1.0

## Parámetros
- `folioId`: ID del folio (integer, required)

## Respuesta

### Campos Principales
- `id`: ID del folio
- `type`: guest|master
- `status`: open|closed
- `currentBalance`: Balance actual
- `realizedBalance`: Balance realizado
- `startDate/endDate`: Fechas de inicio y fin
- `contactId`: ID del contacto
- `reservationId`: ID de la reserva

### Información Financiera
- `agentCommission`: Comisión del agente
- `ownerCommission`: Comisión del propietario
- `ownerRevenue`: Ingresos del propietario
- `checkInDate/checkOutDate`: Fechas de check-in/out

### Objetos Embebidos
- `contact`: Información del contacto
- `travelAgent`: Información del agente de viajes
- `company`: Información de la empresa
- `masterFolioRule`: Regla del folio maestro
- `masterFolio`: Folio maestro

### Manejo de Excepciones
- `hasException`: Si tiene excepción
- `exceptionMessage`: Mensaje de excepción

## Códigos de Error
- **401**: No autorizado - Credenciales inválidas
- **403**: Prohibido - Permisos insuficientes
- **404**: No encontrado - Folio no existe
- **500**: Error interno del servidor

## Ejemplos de Uso

### Obtener Folio
```
GET /pms/folios/12345
```

### Respuesta Exitosa
```json
{
  "id": 12345,
  "type": "guest",
  "status": "open",
  "currentBalance": 1500.00,
  "contactId": 67890,
  "reservationId": 11111
}
```
"""
