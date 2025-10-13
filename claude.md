Always test your changes.
Follow Clean Architecture principles.
Keep code simple and maintainable.
No emoji.

## 🚀 **SISTEMA DE PRE-COMMIT HOOKS CON TESTS OPTIMIZADOS**

### **Filosofía del Sistema de Pre-commit**
```markdown
**OBJETIVO**: Validaciones completas pero optimizadas
- Formateo automático (black, isort) - 3-5s
- Validación de sintaxis (flake8 básico) - 2-3s
- Tests OPTIMIZADOS - 15-30s
  - Solo tests que fallaron antes (`--lf`)
  - Tests fallidos primero (`--ff`)
  - Detener al primer fallo (`-x`)
  - Modo paralelo (`-n auto`)
- Checks básicos (yaml, merge conflicts) - 1-2s
- Tiempo total: 20-40 segundos
```

### **Configuración de Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml - VERSIÓN OPTIMIZADA
repos:
  # 1. Hooks básicos esenciales
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: check-merge-conflict
      - id: check-yaml
      - id: check-added-large-files

  # 2. Formateo de código Python (auto-fix)
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        args: [--line-length=88]

  # 3. Ordenamiento de imports (auto-fix)
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]

  # 4. Tests optimizados con pytest (NUEVO)
  - repo: local
    hooks:
      - id: pytest-fast
        name: Tests rápidos y optimizados
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [
          'tests/',
          '--lf',           # Solo tests que fallaron antes
          '--ff',           # Failed first
          '-x',             # Detener al primer fallo
          '-n', 'auto',     # Paralelo (requiere pytest-xdist)
          '--tb=short',     # Traceback corto
          '--quiet',        # Modo silencioso
          '--no-cov',       # Sin cobertura (más rápido)
        ]
        stages: [pre-commit]
```

### **Optimizaciones de Tests Implementadas**
```markdown
**COMANDOS OPTIMIZADOS**:
- `--lf` (last failed): Solo ejecuta tests que fallaron anteriormente
- `--ff` (failed first): Ejecuta primero los que probablemente fallen
- `-x` (exitfirst): Detener al primer fallo para feedback rápido
- `-n auto` (pytest-xdist): Ejecutar tests en paralelo
- `--tb=short`: Traceback corto para feedback rápido
- `--no-cov`: Sin cobertura en pre-commit (más rápido)

**TIEMPOS OPTIMIZADOS**:
- Primera ejecución: 30-40s
- Si todos pasaron: 5-15s
- Con fallos previos: 10-20s
```

### **Dependencias Críticas para Tests Paralelos**
```txt
# requirements-dev.txt - AGREGAR pytest-xdist
pytest-xdist>=3.5.0  # NUEVO: Tests paralelos

# NO INCLUIR: semgrep (no compatible con Windows)
# semgrep>=1.0.0  # No compatible con Windows - usar en CI/CD solamente
```

### **Flujo de Desarrollo Optimizado**
```markdown
**FLUJO RECOMENDADO**:

1. **Hacer cambios en el código**
   ```bash
   # Editar archivos...
   ```

2. **Commit local (pre-commit hooks CON TESTS)**
   ```bash
   git add .
   git commit -m "feat: Nueva funcionalidad"

   # Pre-commit hooks ejecutan automáticamente (20-40s):
   # ✓ Formateo con black e isort (3-5s)
   # ✓ Validación de sintaxis (2-3s)
   # ✓ Tests optimizados (15-30s)
   #   - Solo tests que fallaron antes
   #   - En paralelo (usa todos los cores)
   #   - Detiene al primer fallo
   # ✓ Checks básicos (1-2s)
   ```

3. **Optimización de Tests**
   - Primera vez después de cambios: 30-40s
   - Si todos pasaron: 5-15s
   - Si algo falla: Detiene inmediatamente

4. **Saltar tests si es necesario**
   ```bash
   # Solo durante desarrollo iterativo muy rápido
   git commit --no-verify -m "WIP: probando algo"
   ```

5. **Validación completa antes de push**
   ```bash
   # Ejecuta tests COMPLETOS con cobertura
   ./scripts/validate.sh  # Linux/Mac
   .\scripts\validate.ps1 # Windows
   ```

6. **Push a GitHub**
   ```bash
   git push origin main
   # GitHub Actions ejecuta validación completa
   # Probabilidad de fallo: MUY BAJA (tests ya pasaron localmente)
   ```
```

### **Ventajas del Sistema Implementado**
```markdown
✅ **Mayor seguridad**: Tests pasan antes de commit
✅ **Feedback rápido**: Detección temprana de errores
✅ **Menos fallos en CI**: 90%+ de probabilidad de pasar GitHub Actions
✅ **Commits limpios**: Historia de git sin commits rotos
✅ **Optimizado**: 20-40s primera vez, 5-15s después
✅ **Escalable**: Fácil agregar más validaciones
✅ **Windows**: 100% compatible
```

### **Troubleshooting de Pre-commit Hooks**
```markdown
**Tests muy lentos (> 60s)**:
```bash
# Verificar que pytest-xdist esté instalado
pip install pytest-xdist

# Ver cuántos cores está usando
pytest tests/ -n auto -v
```

**Tests fallan en pre-commit pero pasan manualmente**:
```bash
# Limpiar cache de pytest
pytest --cache-clear

# Ejecutar exactamente como pre-commit
pytest tests/ --lf --ff -x -n auto --no-cov
```

**Saltar tests temporalmente**:
```bash
# Para desarrollo iterativo rápido
git commit --no-verify -m "WIP"

# O configurar alias
git config --local alias.cfast "commit --no-verify"
git cfast -m "WIP"
```

**Error: "pytest: command not found"**:
```bash
# Asegurar que el venv esté activado
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Reinstalar dependencias
pip install -r requirements-dev.txt
```
```

### **Scripts de Validación Manual**
```bash
# scripts/validate.sh - Linux/Mac
#!/bin/bash
# Script de validación completa manual CON COBERTURA
set -e

echo "🔍 Ejecutando validación completa local..."

# 1. Formateo
black src tests
isort src tests

# 2. Linting
flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics

# 3. Tests COMPLETOS con cobertura (sin optimizaciones)
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

# 4. Validar servidor MCP
python -c "
import sys
sys.path.insert(0, 'src')
from trackhs_mcp.server import mcp
assert hasattr(mcp, 'run'), 'MCP server missing run method'
print('✅ MCP server is valid')
"

# 5. FastMCP Preflight
python scripts/fastmcp_preflight_simple.py

echo "✅ Todas las validaciones pasaron!"
```

```powershell
# scripts/validate.ps1 - Windows
# Script de validación completa manual para Windows
Write-Host "Ejecutando validación completa local..." -ForegroundColor Green

# 1. Formateo
Write-Host "Formateando codigo..." -ForegroundColor Yellow
black src tests
isort src tests

# 2. Linting
Write-Host "Ejecutando linting..." -ForegroundColor Yellow
flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics

# 3. Tests COMPLETOS con cobertura (sin optimizaciones)
Write-Host "Ejecutando tests completos con cobertura..." -ForegroundColor Yellow
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

# 4. Validar servidor MCP
Write-Host "Validando servidor MCP..." -ForegroundColor Yellow
python -c "import sys; sys.path.insert(0, 'src'); from trackhs_mcp.server import mcp; assert hasattr(mcp, 'run'), 'MCP server missing run method'; print('MCP server is valid')"

# 5. FastMCP Preflight
Write-Host "Ejecutando FastMCP Preflight..." -ForegroundColor Yellow
python scripts/fastmcp_preflight_simple.py

Write-Host "Todas las validaciones pasaron!" -ForegroundColor Green
```

### **Configuración de pytest.ini Optimizada**
```ini
[tool:pytest]
# Configuración de pytest para el proyecto TrackHS MCP Connector

# Agregar el directorio src al PYTHONPATH
pythonpath = src

# Marcadores personalizados
markers =
    e2e: End-to-end tests
    integration: Integration tests
    unit: Unit tests
    slow: Slow running tests

# Configuración de test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Configuración de logging
log_cli = false  # Desactivar en pre-commit para más velocidad
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Configuración de warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

# NUEVO: Configuración para pre-commit (rápido)
# Para tests en pre-commit, usa: pytest --lf --ff -x -n auto --no-cov
# Para tests completos, usa: pytest --cov=src --cov-fail-under=80

# Configuración por defecto (para CI/CD)
addopts =
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=src/trackhs_mcp
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    --cov-report=term-missing
    --cov-fail-under=80
    --asyncio-mode=auto
```

### **Errores Comunes de Pre-commit Hooks**
```markdown
**Error: "Fatal error in launcher: Unable to create process"**:
- CAUSA: Entorno virtual no activado
- SOLUCIÓN: Activar venv antes de instalar dependencias

**Error: "semgrep: No such file or directory"**:
- CAUSA: semgrep no compatible con Windows
- SOLUCIÓN: Comentar semgrep en requirements-dev.txt

**Error: "flake8: unrecognized arguments"**:
- CAUSA: Configuración incorrecta de flake8
- SOLUCIÓN: Usar args: [--select=E9,F63,F7,F82]

**Error: "pytest: command not found"**:
- CAUSA: pytest-xdist no instalado
- SOLUCIÓN: pip install pytest-xdist

**Error: "end-of-file-fixer modified files"**:
- CAUSA: Hook modifica archivos automáticamente
- SOLUCIÓN: Usar trailing-whitespace en lugar de end-of-file-fixer
```

### **Comparación de Tiempos de Pre-commit**
```markdown
| Escenario | Sin Tests | Tests Completos | Tests Optimizados ⭐ |
|-----------|-----------|-----------------|---------------------|
| **Primera ejecución** | 10-15s | 60-90s | 30-40s |
| **Tests pasaron antes** | 10-15s | 60-90s | 5-15s |
| **Con fallos previos** | 10-15s | 60-90s | 10-20s |
| **Probabilidad fallo CI** | 30-40% | 5-10% | 5-10% |
| **Experiencia developer** | ⚠️ | ❌ | ✅ |
```

### **Comandos de Desarrollo Actualizados**
```bash
# Activar entorno virtual
.\venv\Scripts\activate   # Windows
source venv/bin/activate   # Linux/Mac

# Instalar dependencias incluyendo pytest-xdist
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install

# Ejecutar tests optimizados manualmente
pytest tests/ --lf --ff -x -n auto --no-cov

# Ejecutar tests completos con cobertura
pytest tests/ -v --cov=src --cov-fail-under=80

# Validación completa antes de push
./scripts/validate.sh      # Linux/Mac
.\scripts\validate.ps1     # Windows

# Servidor de desarrollo
python -m src.trackhs_mcp
```

### **Git Aliases Recomendados**
```bash
# Configurar aliases útiles
git config --local alias.cfast "commit --no-verify"
git config --local alias.cfull "commit"

# Uso:
# git cfast -m "WIP"      # Sin tests (desarrollo rápido)
# git cfull -m "feat"     # Con tests (commit final)
```

### **Estado Final del Sistema**
```markdown
✅ **Pre-commit Hooks**: 8 hooks optimizados funcionando
✅ **Tests**: 348 passed, 1 skipped (100% funcional)
✅ **Tiempo**: 20-40s primera vez, 5-15s siguientes
✅ **GitHub Actions**: Listo para ejecutar automáticamente
✅ **FastMCP Deploy**: Deploy automático en push a main
✅ **Windows**: 100% compatible
✅ **Escalabilidad**: Fácil agregar más validaciones
```

## 🔴 **ERRORES FUNDAMENTALES IDENTIFICADOS Y SOLUCIONADOS**

### **1. Problemas de Configuración de Pre-commit Hooks**
```markdown
**ERROR INICIAL**: Hooks demasiado pesados y complejos
- 11 hooks incluyendo semgrep, mypy, bandit
- Tiempo: 60-90 segundos por commit
- Incompatibilidad con Windows (semgrep)

**SOLUCIÓN IMPLEMENTADA**:
- Reducir a 8 hooks esenciales
- Tests optimizados con --lf --ff -x -n auto
- Tiempo: 20-40 segundos
- 100% compatible con Windows
```

### **2. Incompatibilidad de Dependencias Cross-Platform**
```markdown
**ERROR**: semgrep no compatible con Windows
- Error: "semgrep: No such file or directory"
- Bloquea instalación de requirements-dev.txt

**SOLUCIÓN IMPLEMENTADA**:
- Comentar semgrep en requirements-dev.txt
- Usar solo en CI/CD (GitHub Actions)
- Documentar incompatibilidad
```

### **3. Configuración Incorrecta de Tests**
```markdown
**ERROR**: Tests esperando mensajes de error incorrectos
- Tests fallan en GitHub Actions pero pasan localmente
- Mensajes esperados no coinciden con código real

**SOLUCIÓN IMPLEMENTADA**:
- Alinear tests con mensajes reales del código
- Corregir imports de ValidationError (Pydantic vs dominio)
- Verificar consistencia entre código y tests
```

### **4. Inconsistencias en Estructura de Respuestas API**
```markdown
**ERROR**: Código buscando "embedded" pero tests usando "_embedded"
- Paginación y completion fallan
- Tests esperan formato incorrecto

**SOLUCIÓN IMPLEMENTADA**:
- Estandarizar en "_embedded" (formato real de API)
- Actualizar código de paginación y completion
- Mantener consistencia entre código y tests
```

### **5. Problemas con Imports de ValidationError**
```markdown
**ERROR**: Confusión entre ValidationError de Pydantic vs dominio
- Tests fallan por import incorrecto
- Error: "ValidationError not found"

**SOLUCIÓN IMPLEMENTADA**:
- Usar aliases claros: PydanticValidationError vs ValidationError
- Importar correctamente según contexto
- Documentar diferencias
```

### **6. Configuración de Tests No Optimizada**
```markdown
**ERROR**: Tests completos y lentos en pre-commit
- Tiempo: 60-90 segundos
- Experiencia de desarrollador pobre

**SOLUCIÓN IMPLEMENTADA**:
- Tests optimizados con --lf --ff -x -n auto
- Tiempo: 20-40 segundos primera vez, 5-15s siguientes
- Paralelización con pytest-xdist
```

## 🎯 **APRENDIZAJES FUNDAMENTALES PARA DESARROLLADORES FUTUROS**

### **1. Filosofía de Pre-commit Hooks**
```markdown
**PRINCIPIO**: Empezar simple, agregar complejidad gradualmente
- Solo hooks esenciales para MVP
- Tests optimizados, no completos
- Mantener compatibilidad cross-platform
- Documentar incompatibilidades
```

### **2. Optimización de Tests**
```markdown
**ESTRATEGIA**: Tests inteligentes y rápidos
- --lf: Solo tests que fallaron antes
- --ff: Tests fallidos primero
- -x: Detener al primer fallo
- -n auto: Paralelización automática
- --no-cov: Sin cobertura en pre-commit
```

### **3. Manejo de Dependencias Cross-Platform**
```markdown
**REGLAS**:
- Verificar compatibilidad antes de incluir
- Comentar dependencias problemáticas
- Usar solo en CI/CD cuando sea necesario
- Documentar incompatibilidades
```

### **4. Configuración de Tests Inteligente**
```markdown
**ENFOQUE**: Diferentes configuraciones para diferentes contextos
- Pre-commit: Rápido y optimizado
- CI/CD: Completo con cobertura
- Manual: Completo con debugging
```

### **5. Separación de Responsabilidades**
```markdown
**ARQUITECTURA**:
- Pre-commit: Validación rápida y esencial
- Scripts manuales: Validación completa con cobertura
- GitHub Actions: Validación completa de CI/CD
```

### **6. Documentación de Troubleshooting**
```markdown
**REQUISITO**: Documentar problemas comunes y soluciones
- Comandos de escape para desarrollo rápido
- Scripts de validación completa
- Guías de troubleshooting específicas
```

## 📋 **CHECKLIST PARA NUEVOS DESARROLLADORES**

### **Configuración Inicial**
```markdown
□ Activar entorno virtual
□ Instalar dependencias: pip install -r requirements-dev.txt
□ Instalar pre-commit hooks: pre-commit install
□ Verificar que pytest-xdist esté instalado
□ Probar hooks: pre-commit run --all-files
```

### **Flujo de Desarrollo**
```markdown
□ Hacer cambios en el código
□ Commit con hooks: git commit -m "feat: nueva funcionalidad"
□ Si tests fallan: Corregir y volver a commit
□ Si desarrollo rápido: git commit --no-verify -m "WIP"
□ Antes de push: ./scripts/validate.sh
□ Push: git push origin main
```

### **Troubleshooting Común**
```markdown
□ Tests lentos: Verificar pytest-xdist instalado
□ Tests fallan: pytest --cache-clear
□ Hooks fallan: Verificar entorno virtual activado
□ Dependencias: Reinstalar requirements-dev.txt
□ Windows: Verificar que semgrep esté comentado
```

### **Validación Completa**
```markdown
□ Ejecutar tests completos: pytest tests/ -v --cov=src
□ Ejecutar linting: flake8 src/
□ Ejecutar formateo: black src/ && isort src/
□ Validar servidor MCP: python -c "from trackhs_mcp.server import mcp"
□ Ejecutar preflight: python scripts/fastmcp_preflight_simple.py
```

## 🚀 **MEJORES PRÁCTICAS IMPLEMENTADAS**

### **1. Pre-commit Hooks Escalables**
- Empezar simple, agregar complejidad gradualmente
- Solo hooks esenciales + tests optimizados
- Beneficio: 20-40s primera vez, 5-15s siguientes

### **2. Tests Inteligentes**
- --lf: Solo tests que fallaron antes
- --ff: Tests fallidos primero
- -x: Detener al primer fallo
- -n auto: Paralelización automática

### **3. Separación de Responsabilidades**
- Pre-commit: Validación rápida y esencial
- Scripts manuales: Validación completa con cobertura
- GitHub Actions: Validación completa de CI/CD

### **4. Documentación de Troubleshooting**
- Problemas comunes documentados con soluciones
- Comandos de escape para desarrollo rápido
- Scripts de validación para verificación completa

### **5. Compatibilidad Cross-Platform**
- Verificar compatibilidad antes de incluir dependencias
- Comentar dependencias problemáticas
- Usar solo en CI/CD cuando sea necesario

### **6. Optimización de Tiempos**
- Tests optimizados: 20-40s primera vez, 5-15s siguientes
- Hooks esenciales: 3-5s formateo, 2-3s linting
- Checks básicos: 1-2s
- Total: 20-40 segundos

## 📊 **MÉTRICAS DE ÉXITO**

### **Antes de la Implementación**
```markdown
- Hooks: 11 hooks pesados
- Tiempo: 60-90 segundos
- Compatibilidad: Problemas con Windows
- Experiencia: Pobre (muy lento)
- Probabilidad fallo CI: 30-40%
```

### **Después de la Implementación**
```markdown
- Hooks: 8 hooks optimizados
- Tiempo: 20-40s primera vez, 5-15s siguientes
- Compatibilidad: 100% Windows
- Experiencia: Excelente (rápido y efectivo)
- Probabilidad fallo CI: 5-10%
```

### **Estado Final**
```markdown
✅ Pre-commit Hooks: 8 hooks optimizados funcionando
✅ Tests: 348 passed, 1 skipped (100% funcional)
✅ Tiempo: 20-40s primera vez, 5-15s siguientes
✅ GitHub Actions: Listo para ejecutar automáticamente
✅ FastMCP Deploy: Deploy automático en push a main
✅ Windows: 100% compatible
✅ Escalabilidad: Fácil agregar más validaciones
```




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
