Always test your changes.
Follow Clean Architecture principles.
Keep code simple and maintainable.
No emoji.



Excelente pregunta. Basándome en todo el trabajo que hemos realizado, aquí está la información fundamental que debe documentarse para futuros desarrolladores:

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

Esta documentación debe mantenerse actualizada y ser la primera referencia para cualquier desarrollador que trabaje en el proyecto.
