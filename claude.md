Always test your changes.
Follow Clean Architecture principles.
Keep code simple and maintainable.
No emoji.




## 📚 **Guía de Conocimiento Crítico para Desarrolladores**

### 🔍 **1. Problemas de Integración API Identificados**

#### **A. Parsing JSON Inconsistente**
```markdown
**PROBLEMA**: La API de TrackHS puede devolver datos como:
- String JSON: `'{"id": 123, "name": "test"}'`
- Objeto JSON: `{"id": 123, "name": "test"}`

**SOLUCIÓN IMPLEMENTADA**:
- Cliente API con fallback manual en `trackhs_api_client.py`
- Validación de string JSON en use cases
- Logging de debug para diagnóstico

**CÓDIGO DE REFERENCIA**:
```python
# En trackhs_api_client.py líneas 141-164
if "application/json" in content_type:
    try:
        json_data = response.json()
        return json_data
    except Exception as json_error:
        # Fallback manual con json.loads()
```

#### **B. Nomenclatura de Campos Inconsistente**
```markdown
**PROBLEMA**: API TrackHS usa camelCase, modelos Pydantic usan snake_case
- API: `arrivalDate`, `departureDate`, `unitId`
- Modelo: `arrival_date`, `departure_date`, `unit_id`

**SOLUCIÓN IMPLEMENTADA**:
- Alias en todos los campos Pydantic
- Configuración `populate_by_name=True`
- Mapeo bidireccional completo

**CÓDIGO DE REFERENCIA**:
```python
# En reservations.py
class Reservation(BaseModel):
    model_config = {"populate_by_name": True}

    arrival_date: str = Field(..., alias="arrivalDate", description="...")
    unit_id: int = Field(..., alias="unitId", description="...")
```

### 🏗️ **2. Arquitectura y Patrones Críticos**

#### **A. Clean Architecture - Separación de Responsabilidades**
```markdown
**ESTRUCTURA OBLIGATORIA**:
- Domain: Entidades, excepciones, objetos de valor
- Application: Casos de uso, puertos (interfaces)
- Infrastructure: Adaptadores externos, MCP, utilidades

**REGLA DE ORO**: La capa de dominio NUNCA debe depender de infraestructura
```

#### **B. Manejo de Errores - Patrón @error_handler**
```markdown
**PROBLEMA COMÚN**: Errores no envueltos correctamente
**SOLUCIÓN**: Usar decorador @error_handler en todos los use cases

**CÓDIGO DE REFERENCIA**:
```python
@error_handler("get_reservation")
async def execute(self, params: GetReservationParams) -> Reservation:
    # Lógica del caso de uso
```

### 🧪 **3. Testing - Lecciones Aprendidas**

#### **A. Fixtures de Datos Completos**
```markdown
**PROBLEMA**: Tests fallan por datos mock incompletos
**SOLUCIÓN**: Usar fixture `sample_reservation_data` con TODOS los campos requeridos

**CAMPOS CRÍTICOS QUE SIEMPRE DEBEN INCLUIRSE**:
- security_deposit, updated_at, created_at, booked_at
- guest_breakdown (con todos los subcampos)
- contact_id, channel_id, folio_id, user_id, type_id, rate_type_id
- is_taxable, is_channel_locked, agreement_status
- automate_payment, revenue_realized_method
- updated_by, created_by, payment_plan, travel_insurance_products
```

#### **B. Tipos de Datos en Tests**
```markdown
**PROBLEMA**: Tests pasan enteros cuando el API espera strings
**SOLUCIÓN**: Siempre usar strings para reservation_id en tests

**EJEMPLO CORRECTO**:
```python
# ✅ CORRECTO
reservation_id = "12345"
params = GetReservationParams(reservation_id=reservation_id)

# ❌ INCORRECTO
reservation_id = 12345  # Causa errores de parsing
```

### 🔧 **4. Configuración y Deployment**

#### **A. Variables de Entorno Críticas**
```markdown
**REQUERIDAS**:
- TRACKHS_API_URL: URL base de la API
- TRACKHS_USERNAME: Usuario de autenticación
- TRACKHS_PASSWORD: Contraseña de autenticación
- DEBUG: "true" para logging detallado (solo desarrollo)

**IMPORTANTE**: Nunca commitear credenciales al repositorio
```

#### **B. Logging y Debugging**
```markdown
**CONFIGURACIÓN**:
- Logging detallado solo con DEBUG=true
- Usar logger.debug() en lugar de logger.info() para información técnica
- Incluir contexto en todos los logs de error
```

### 📋 **5. Checklist de Desarrollo**

#### **Antes de Implementar Nueva Funcionalidad:**
```markdown
□ Verificar que la API devuelve datos en el formato esperado
□ Agregar alias camelCase si la API usa camelCase
□ Configurar populate_by_name=True en modelos Pydantic
□ Crear fixture completo con todos los campos requeridos
□ Escribir tests que usen strings para IDs
□ Usar @error_handler en todos los use cases
□ Verificar que los tests pasan localmente
```

#### **Antes de Hacer Commit:**
```markdown
□ Ejecutar pytest tests/ -v (todos los 299 tests)
□ Verificar cobertura: pytest tests/ --cov=src/trackhs_mcp
□ Ejecutar linting: flake8 src/
□ Formatear código: black src/
□ Verificar que no hay credenciales en el código
□ Actualizar documentación si es necesario
```

### 🚨 **6. Errores Comunes y Soluciones**

#### **A. "Field required [type=missing]"**
```markdown
**CAUSA**: Datos mock incompletos en tests
**SOLUCIÓN**: Usar fixture sample_reservation_data completo
```

#### **B. "'int' object has no attribute 'strip'"**
```markdown
**CAUSA**: Pasando enteros cuando se esperan strings
**SOLUCIÓN**: Convertir todos los IDs a strings en tests
```

#### **C. "Input should be a valid dictionary"**
```markdown
**CAUSA**: API devuelve string JSON en lugar de objeto
**SOLUCIÓN**: Implementar parsing robusto con fallback manual
```

#### **D. "35 validation errors for Reservation"**
```markdown
**CAUSA**: Falta de alias camelCase en modelos Pydantic
**SOLUCIÓN**: Agregar alias y configurar populate_by_name=True
```

### 📖 **7. Documentación de Referencia**

#### **Archivos Críticos para Revisar:**
```markdown
- src/trackhs_mcp/domain/entities/reservations.py (modelos con alias)
- src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py (parsing robusto)
- src/trackhs_mcp/application/use_cases/get_reservation.py (manejo de errores)
- tests/conftest.py (fixture sample_reservation_data)
- tests/unit/mcp/test_get_reservation_v2_tool.py (ejemplos de tests correctos)
```

#### **Comandos de Desarrollo:**
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar tests completos
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=src/trackhs_mcp

# Linting y formateo
flake8 src/
black src/
isort src/

# Servidor de desarrollo
python -m src.trackhs_mcp
```

### 🎯 **8. Principios de Desarrollo**

#### **A. Siempre Validar Datos de API**
```markdown
- Nunca asumir formato de respuesta
- Implementar fallbacks para parsing
- Loggear errores de parsing para debugging
```

#### **B. Mantener Compatibilidad**
```markdown
- Usar alias para soportar múltiples formatos
- Configurar populate_by_name=True
- Documentar cambios en nomenclatura
```

#### **C. Testing Exhaustivo**
```markdown
- Tests para casos exitosos y de error
- Datos mock completos y realistas
- Verificar tipos de datos correctos
- Cobertura de código >95%
```

### 🔧 **9. Lecciones de Validación de Modelos Pydantic (Nuevo)**

#### **A. Validación de Tipos Flexibles con Union**
```markdown
**PROBLEMA CRÍTICO**: API devuelve diferentes tipos para el mismo campo
- Campo `alternates` puede ser: `["string"]` o `[{"type": "airbnb", "id": "123"}]`
- Modelo esperaba solo `List[str]` pero API devuelve `List[dict]`

**SOLUCIÓN IMPLEMENTADA**:
```python
# ANTES (RÍGIDO - FALLA)
alternates: Optional[List[str]] = Field(...)

# DESPUÉS (FLEXIBLE - FUNCIONA)
alternates: Optional[List[Union[str, dict]]] = Field(
    default=None,
    description="IDs alternativos (strings o objetos con type e id)"
)
```

**BENEFICIOS**:
- ✅ Acepta formato real de la API
- ✅ Mantiene retrocompatibilidad
- ✅ Permite acceso directo a propiedades: `alt['type']`, `alt['id']`
```

#### **B. Campos Opcionales vs Requeridos - Alineación con OpenAPI**
```markdown
**PROBLEMA CRÍTICO**: Modelo marca campos como requeridos cuando API no los incluye
- Campo `payment_plan` marcado como requerido
- API no siempre incluye este campo en la respuesta
- Especificación OpenAPI no lo marca como `required`

**SOLUCIÓN IMPLEMENTADA**:
```python
# ANTES (RÍGIDO - FALLA)
payment_plan: List[PaymentPlan] = Field(..., alias="paymentPlan")

# DESPUÉS (FLEXIBLE - FUNCIONA)
payment_plan: Optional[List[PaymentPlan]] = Field(
    default=None,
    alias="paymentPlan",
    description="Plan de pagos (opcional)"
)
```

**REGLAS DE ORO**:
- ✅ Verificar especificación OpenAPI antes de marcar campos como requeridos
- ✅ Usar `Optional[]` para campos que pueden estar ausentes
- ✅ Usar `default=None` para campos opcionales
```

#### **C. Validación de Datos Reales vs Datos Mock**
```markdown
**PROBLEMA**: Tests pasan con datos mock pero fallan con datos reales
- Datos mock: `"alternates": ["ALT123"]`
- Datos reales: `"alternates": [{"type": "airbnb", "id": "HMCNNSE3SJ"}]`

**SOLUCIÓN IMPLEMENTADA**:
- Crear fixture `sample_reservation_data_v2` con formato real de API
- Mantener fixture original para retrocompatibilidad
- Validar con reservas reales del sistema

**CÓDIGO DE REFERENCIA**:
```python
# tests/conftest.py - Fixture con datos reales
@pytest.fixture
def sample_reservation_data_v2():
    return {
        "id": 37165851,
        "alternates": [{"type": "airbnb", "id": "HMCNNSE3SJ"}],
        # ... resto de campos
    }
```

#### **D. Impacto de Errores de Validación en Producción**
```markdown
**PROBLEMA CRÍTICO**: Errores de validación bloquean 100% de reservas
- Error en `alternates`: Bloquea todas las reservas de canales OTA
- Error en `payment_plan`: Bloquea reservas sin plan de pagos
- Resultado: 0% de reservas funcionan

**LECCIÓN APRENDIDA**:
- ✅ Errores de validación son BLOQUEANTES para producción
- ✅ Siempre validar con datos reales de la API
- ✅ Implementar tipos flexibles con `Union[]`
- ✅ Verificar especificación OpenAPI oficial
```

### 🧪 **10. Testing de Validación de Modelos (Nuevo)**

#### **A. Tests de Validación Específicos**
```markdown
**PROBLEMA**: Tests generales no detectan errores de validación específicos
**SOLUCIÓN**: Crear tests específicos para validación de modelos

**EJEMPLO DE TEST DE VALIDACIÓN**:
```python
def test_alternates_as_objects():
    """Test que alternates acepta objetos con type e id"""
    data = {
        "id": 37165851,
        "alternates": [{"type": "airbnb", "id": "HMCNNSE3SJ"}],
        # ... resto de campos requeridos
    }

    reservation = Reservation(**data)
    assert reservation.alternates[0]['type'] == 'airbnb'
    assert reservation.alternates[0]['id'] == 'HMCNNSE3SJ'
```

#### **B. Validación con Datos Reales**
```markdown
**REGLAS**:
- ✅ Siempre probar con IDs de reservas reales del sistema
- ✅ Validar con diferentes canales (Airbnb, Marriott, Booking.com)
- ✅ Probar casos con y sin campos opcionales
- ✅ Verificar que todos los campos se mapean correctamente
```

### 📋 **11. Checklist de Validación de Modelos (Nuevo)**

#### **Antes de Implementar Modelo Pydantic:**
```markdown
□ Verificar especificación OpenAPI oficial
□ Identificar campos que pueden estar ausentes
□ Usar `Optional[]` para campos no marcados como `required`
□ Implementar tipos flexibles con `Union[]` para campos con múltiples formatos
□ Agregar alias para campos con nomenclatura diferente
□ Configurar `populate_by_name=True`
```

#### **Antes de Deploy a Producción:**
```markdown
□ Probar con datos reales de la API (no solo mocks)
□ Validar con diferentes tipos de reservas (diferentes canales)
□ Verificar que campos opcionales manejan valores `None`
□ Confirmar que tipos flexibles aceptan todos los formatos
□ Ejecutar tests de validación específicos
□ Documentar cambios en tipos de datos
```

### 🚨 **12. Errores de Validación Críticos (Nuevo)**

#### **A. "Input should be a valid string [type=string_type, input_value={'type': 'airbnb'}]"**
```markdown
**CAUSA**: Modelo espera `List[str]` pero API devuelve `List[dict]`
**SOLUCIÓN**: Usar `List[Union[str, dict]]`
**IMPACTO**: Bloquea 100% de reservas con IDs alternativos
```

#### **B. "Field required [type=missing, input_value={...}]"**
```markdown
**CAUSA**: Campo marcado como requerido pero API no lo incluye
**SOLUCIÓN**: Usar `Optional[]` y `default=None`
**IMPACTO**: Bloquea reservas sin ese campo
```

#### **C. "35 validation errors for Reservation"**
```markdown
**CAUSA**: Múltiples errores de validación por tipos incorrectos
**SOLUCIÓN**: Revisar todos los campos y tipos de datos
**IMPACTO**: Bloquea completamente la funcionalidad
```

### 📖 **13. Archivos de Referencia Actualizados**

#### **Archivos Críticos para Validación:**
```markdown
- src/trackhs_mcp/domain/entities/reservations.py (modelos con tipos flexibles)
- tests/conftest.py (fixtures con datos reales)
- docs/api/v2-bugfixes-alternates-paymentplan.md (documentación de correcciones)
- CHANGELOG.md (historial de cambios de validación)
```

#### **Comandos de Validación:**
```bash
# Tests específicos de validación
pytest tests/unit/mcp/test_get_reservation_v2_tool.py -v

# Tests de integración
pytest tests/integration/test_get_reservation_v2_integration.py -v

# Tests E2E
pytest tests/e2e/test_get_reservation_v2_e2e.py -v

# Validación con datos reales
python scripts/test_reservation_validation.py
```

### 🎯 **14. Principios de Validación de Modelos**

#### **A. Flexibilidad vs Rigidez**
```markdown
- ✅ Usar `Union[]` para campos con múltiples formatos
- ✅ Usar `Optional[]` para campos que pueden estar ausentes
- ✅ Mantener retrocompatibilidad con formatos anteriores
- ❌ No asumir formato único de la API
```

#### **B. Validación Exhaustiva**
```markdown
- ✅ Probar con datos reales de la API
- ✅ Validar con diferentes tipos de reservas
- ✅ Verificar manejo de campos opcionales
- ✅ Confirmar que todos los campos se mapean correctamente
```

#### **C. Documentación de Cambios**
```markdown
- ✅ Documentar cambios en tipos de datos
- ✅ Crear documentación de correcciones
- ✅ Actualizar CHANGELOG con cambios críticos
- ✅ Mantener ejemplos actualizados
```

Esta documentación debe mantenerse actualizada y ser la primera referencia para cualquier desarrollador que trabaje en el proyecto.
