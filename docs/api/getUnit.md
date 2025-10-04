# Get Unit API

## Descripción
Obtiene información detallada de una unidad específica por su ID desde Track HS. Esta herramienta complementa la funcionalidad de `get_units` permitiendo acceder a todos los detalles de una unidad específica.

## Parámetros

### Requeridos
- **`unitId`** (number): ID de la unidad a obtener

### Opcionales
- **`computed`** (number): Incluir valores computados basados en atributos heredados
  - `0` = false (por defecto)
  - `1` = true
- **`inherited`** (number): Incluir atributos heredados del nodo padre
  - `0` = false (por defecto) 
  - `1` = true
- **`includeDescriptions`** (number): Incluir descripciones de la unidad
  - `0` = false (por defecto)
  - `1` = true

## Ejemplos de Uso

### Obtener unidad básica
```json
{
  "unitId": 7
}
```

### Obtener unidad con datos heredados y computados
```json
{
  "unitId": 7,
  "inherited": 1,
  "computed": 1
}
```

### Obtener unidad con descripciones
```json
{
  "unitId": 7,
  "includeDescriptions": 1
}
```

### Obtener unidad con todos los datos disponibles
```json
{
  "unitId": 7,
  "computed": 1,
  "inherited": 1,
  "includeDescriptions": 1
}
```

## Respuesta

La respuesta incluye un objeto `Unit` completo con la siguiente información:

### Información Básica
- `id`: ID de la unidad
- `name`: Nombre de la unidad
- `shortName`: Nombre corto
- `unitCode`: Código de la unidad
- `headline`: Título promocional
- `shortDescription`: Descripción corta
- `longDescription`: Descripción larga
- `houseRules`: Reglas de la casa

### Ubicación y Contacto
- `nodeId`: ID del nodo asociado
- `streetAddress`: Dirección
- `locality`: Ciudad
- `region`: Estado/Región
- `postal`: Código postal
- `country`: País
- `latitude`/`longitude`: Coordenadas GPS
- `phone`: Teléfono
- `website`: Sitio web

### Configuración de Check-in/Check-out
- `timezone`: Zona horaria
- `checkinTime`: Hora de check-in
- `checkoutTime`: Hora de check-out
- `hasEarlyCheckin`: Permite check-in temprano
- `hasLateCheckout`: Permite check-out tardío
- `earlyCheckinTime`: Hora de check-in temprano
- `lateCheckoutTime`: Hora de check-out tardío

### Características Físicas
- `bedrooms`: Número de habitaciones
- `fullBathrooms`: Baños completos
- `halfBathrooms`: Medios baños
- `threeQuarterBathrooms`: Baños de 3/4
- `maxOccupancy`: Ocupación máxima
- `area`: Área en metros cuadrados
- `floors`: Número de pisos

### Políticas
- `petsFriendly`: Permite mascotas
- `maxPets`: Máximo número de mascotas
- `eventsAllowed`: Permite eventos
- `smokingAllowed`: Permite fumar
- `childrenAllowed`: Permite niños
- `minimumAgeLimit`: Edad mínima requerida
- `isAccessible`: Accesible para discapacitados

### Amenidades y Habitaciones
- `bedTypes`: Tipos de camas disponibles
- `rooms`: Configuración de habitaciones
- `amenities`: Lista de amenidades
- `amenityDescription`: Descripción de amenidades

### Información Adicional
- `unitType`: Tipo de unidad
- `lodgingType`: Tipo de alojamiento
- `directions`: Instrucciones de llegada
- `checkinDetails`: Detalles de check-in
- `custom`: Datos personalizados
- `localOffice`: Información de oficina local
- `updatedAt`: Fecha de última actualización

## Casos de Uso Comunes

### 1. Consulta Rápida de Unidad
```json
{
  "unitId": 123
}
```
**Uso**: Obtener información básica de una unidad específica.

### 2. Análisis Detallado
```json
{
  "unitId": 123,
  "computed": 1,
  "inherited": 1,
  "includeDescriptions": 1
}
```
**Uso**: Obtener toda la información disponible para análisis completo.

### 3. Verificación de Políticas
```json
{
  "unitId": 123,
  "inherited": 1
}
```
**Uso**: Verificar políticas específicas de la unidad incluyendo las heredadas.

## Integración con Otras Herramientas

Esta herramienta se complementa perfectamente con:

- **`get_units`**: Buscar unidades y luego obtener detalles específicos
- **`get_nodes`**: Obtener información del nodo padre de la unidad
- **`get_reservation`**: Verificar detalles de unidades en reservaciones

## Notas Técnicas

- La herramienta utiliza el endpoint `/pms/units/{unitId}` de Track HS
- Los parámetros opcionales se pasan como query parameters
- La respuesta sigue el esquema de la API Channel de Track HS
- Compatible con autenticación Basic Auth y HMAC

## Manejo de Errores

- **404**: Unidad no encontrada
- **401**: Error de autenticación
- **403**: Sin permisos para acceder a la unidad
- **500**: Error interno del servidor

## Limitaciones

- Requiere el ID exacto de la unidad
- No soporta búsqueda por nombre o código
- Para búsquedas, usar `get_units` primero