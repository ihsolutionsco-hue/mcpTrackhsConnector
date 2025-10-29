# Guía de Debugging - TrackHS MCP Connector

## Resumen

Esta guía proporciona herramientas y técnicas para diagnosticar problemas con la API de TrackHS, especialmente cuando se obtienen respuestas exitosas pero sin datos.

## Herramientas de Debugging Disponibles

### 1. Herramienta de Diagnóstico (`diagnose_api`)

Nueva herramienta que ejecuta una serie de tests para identificar problemas:

```python
# Ejecutar diagnóstico completo
diagnose_api(test_type="full")

# Tests específicos
diagnose_api(test_type="connectivity")  # Test de conectividad
diagnose_api(test_type="auth")          # Test de autenticación
diagnose_api(test_type="endpoints")     # Test de endpoints
diagnose_api(test_type="data_structure") # Test de estructura de datos
```

### 2. Logging Mejorado

El sistema ahora incluye logging detallado en múltiples niveles:

#### Logs de Búsqueda de Unidades
- **Parámetros de entrada**: Valores originales y convertidos
- **Respuesta de API**: Estructura y contenido de la respuesta
- **Procesamiento**: Detalles del procesamiento de datos
- **Resultado final**: Métricas de la búsqueda completada

#### Logs de Cliente API
- **Conversión de parámetros**: Cambios booleanos aplicados
- **Estructura de respuesta**: Análisis de la estructura recibida
- **Extracción de datos**: Detalles de extracción de paginación

## Problemas Comunes y Soluciones

### 1. Respuesta Exitosa Sin Datos

**Síntoma**: API devuelve 200 OK pero `total_items = 0`

**Posibles Causas**:
- Base de datos vacía en ambiente de testing
- Permisos insuficientes en la API key
- Filtros por defecto que ocultan todas las unidades
- Configuración de tenant/cuenta incorrecta

**Diagnóstico**:
```python
# 1. Verificar conectividad básica
diagnose_api(test_type="connectivity")

# 2. Verificar autenticación
diagnose_api(test_type="auth")

# 3. Probar diferentes endpoints
diagnose_api(test_type="endpoints")

# 4. Analizar estructura de datos
diagnose_api(test_type="data_structure")
```

### 2. Errores de Estructura de Respuesta

**Síntoma**: Errores al procesar la respuesta de la API

**Solución**: El sistema ahora detecta automáticamente diferentes estructuras:
- `_embedded.units` (HAL)
- `embedded.units` (sin guión bajo)
- `data.units` (estructura personalizada)
- `units` (estructura directa)

### 3. Problemas de Conversión de Parámetros

**Síntoma**: Parámetros booleanos no se convierten correctamente

**Solución**: El sistema ahora loggea todas las conversiones:
```python
# Logs incluyen:
{
    "conversion_changes": {
        "is_active": {"original": true, "converted": 1},
        "is_bookable": {"original": false, "converted": 0}
    }
}
```

## Métricas de Debugging

### Contadores de Filtros
- `has_filters`: Indica si hay filtros significativos aplicados
- `filter_count`: Número total de filtros activos
- `boolean_conversions`: Conversiones booleanas aplicadas

### Análisis de Respuesta
- `response_structure`: Tipo de estructura detectada
- `units_count`: Número de unidades en la respuesta
- `total_items`: Total de elementos disponibles
- `pagination_info`: Información de paginación calculada

## Configuración de Logging

### Niveles de Log
- **INFO**: Operaciones normales y métricas
- **WARNING**: Problemas no críticos (ej: unidad individual con error)
- **ERROR**: Errores que impiden la operación
- **DEBUG**: Detalles técnicos de procesamiento

### Estructura de Logs
Todos los logs incluyen contexto estructurado:
```json
{
    "message": "Descripción del evento",
    "extra": {
        "param_count": 5,
        "has_filters": true,
        "units_count": 0,
        "response_structure": "direct"
    }
}
```

## Próximos Pasos para Resolución

### 1. Verificar Datos en TrackHS
- Confirmar que existen unidades en la base de datos
- Verificar que las unidades tienen `is_active=true`
- Validar estado de `is_bookable` en las unidades

### 2. Validar Permisos
- Revisar scope de la API key
- Confirmar acceso de lectura a la tabla de unidades
- Validar filtros de tenant/organización

### 3. Testing Adicional
- Probar con datos reales en ambiente de staging
- Validar búsqueda por `unit_ids` específicos
- Probar endpoint `get_unit` (si existe) con ID conocido

### 4. Monitoreo Continuo
- Implementar alertas cuando `total_items = 0` de forma recurrente
- Métricas de uso por tipo de filtro
- Logging de queries vacías para análisis

## Herramientas de Análisis

### Análisis de Respuesta de API
```python
def analyze_api_response(response):
    """Analiza la estructura de una respuesta de API"""
    return {
        "type": type(response).__name__,
        "keys": list(response.keys()) if isinstance(response, dict) else "not_dict",
        "has_units": "units" in response if isinstance(response, dict) else False,
        "units_count": len(response.get("units", [])) if isinstance(response, dict) else 0,
        "total_items": response.get("total_items", "not_found") if isinstance(response, dict) else "not_found"
    }
```

### Validación de Filtros
```python
def validate_filters(params):
    """Valida que los filtros sean significativos"""
    meaningful_fields = [
        'search', 'bedrooms', 'is_active', 'is_bookable',
        'pets_friendly', 'arrival', 'departure'
    ]
    return any(params.get(field) is not None for field in meaningful_fields)
```

## Contacto y Soporte

Para problemas adicionales o preguntas sobre debugging:
- Revisar logs estructurados en el sistema de logging
- Usar la herramienta `diagnose_api` para análisis automático
- Consultar la documentación de la API de TrackHS
- Contactar al equipo de desarrollo con logs detallados
