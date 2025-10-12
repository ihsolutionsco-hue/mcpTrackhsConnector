# Guía de Configuración de Desarrollo

Esta guía te ayudará a configurar el entorno de desarrollo completo para el TrackHS MCP Connector, incluyendo pre-commit hooks, FastMCP preflight checks y GitHub Actions.

## 🚀 Configuración Inicial

### 1. Prerrequisitos

- Python 3.11+
- Git
- pip o uv

### 2. Clonar e Instalar Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/ihsolutionsco-hue/mcpTrackhsConnector.git
cd MCPtrackhsConnector

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Configurar Variables de Entorno

```bash
# Copiar plantilla de entorno
cp .env.example .env

# Editar con tus credenciales
# TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
# TRACKHS_USERNAME=tu_usuario
# TRACKHS_PASSWORD=tu_contraseña
# TRACKHS_TIMEOUT=30
```

## 🔧 Configuración de Pre-commit Hooks

### 1. Instalar Pre-commit

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks en el repositorio
pre-commit install
```

### 2. Ejecutar Hooks Manualmente

```bash
# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar en archivos específicos
pre-commit run --files src/trackhs_mcp/server.py
```

### 3. Hooks Configurados

El proyecto incluye los siguientes hooks:

- **Formateo**: Black, isort
- **Linting**: Flake8, mypy
- **Seguridad**: Bandit, safety
- **Validación**: YAML, JSON, TOML
- **Pre-tests**: Suite completa de tests
- **FastMCP Preflight**: Validaciones específicas de FastMCP

## 🛡️ FastMCP Preflight Checks

### 1. Ejecutar Preflight Manualmente

```bash
# Ejecutar preflight completo
python scripts/fastmcp_preflight.py

# Ejecutar pre-tests
python scripts/pretest.py
```

### 2. Validaciones Incluidas

- **Configuración FastMCP**: Valida `fastmcp.yaml`
- **Servidor MCP**: Verifica configuración del servidor
- **Archivo principal**: Valida `__main__.py`
- **Variables de entorno**: Verifica configuración
- **Dependencias**: Valida `requirements.txt`
- **Seguridad**: Detecta credenciales hardcodeadas

## 🧪 Testing

### 1. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/unit/ -v                    # Tests unitarios
pytest tests/integration/ -v            # Tests de integración
pytest tests/e2e/ -v                     # Tests end-to-end

# Con cobertura
pytest tests/ --cov=src --cov-report=html
```

### 2. Calidad de Código

```bash
# Formateo
black src tests
isort src tests

# Linting
flake8 src tests
mypy src

# Seguridad
bandit -r src
safety check
```

## 🔄 Flujo de Trabajo

### 1. Desarrollo Local

```bash
# 1. Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios
# ... editar archivos ...

# 3. Ejecutar preflight
python scripts/fastmcp_preflight.py

# 4. Hacer commit (pre-commit se ejecuta automáticamente)
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 5. Push a GitHub
git push origin feature/nueva-funcionalidad
```

### 2. GitHub Actions

Al hacer push, GitHub Actions ejecuta automáticamente:

1. **Pre-commit checks**: Formateo, linting, seguridad
2. **FastMCP preflight**: Validaciones específicas de FastMCP
3. **Quality checks**: Tests completos con cobertura
4. **Deploy**: Preparación para despliegue a FastMCP Cloud

### 3. Despliegue a FastMCP Cloud

#### Configuración de Secrets en GitHub

En GitHub Settings > Secrets and variables > Actions, configurar:

```
FASTMCP_API_KEY=tu_api_key_de_fastmcp
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

#### Despliegue Automático

- Push a `main` → GitHub Actions ejecuta validaciones
- Si todas pasan → Preparación para despliegue
- Despliegue manual requerido en FastMCP Cloud

## 📋 Configuración de GitHub Secrets

### 1. Acceder a Configuración

1. Ve a tu repositorio en GitHub
2. Settings > Secrets and variables > Actions
3. New repository secret

### 2. Secrets Requeridos

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `FASTMCP_API_KEY` | API key de FastMCP Cloud | `fmcp_1234567890abcdef` |
| `TRACKHS_API_URL` | URL de la API TrackHS | `https://ihmvacations.trackhs.com/api` |
| `TRACKHS_USERNAME` | Usuario de TrackHS | `tu_usuario` |
| `TRACKHS_PASSWORD` | Contraseña de TrackHS | `tu_contraseña` |

## 🐛 Solución de Problemas

### Pre-commit Hooks con Tests

#### Configuración Inicial

```bash
# 1. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 2. Instalar dependencias incluyendo pytest-xdist
pip install -r requirements-dev.txt

# 3. Instalar pre-commit hooks
pre-commit install
```

#### Qué Hacen los Hooks

Los pre-commit hooks ejecutan validaciones completas:

1. **Formateo automático** (3-5s)
   - Black: Formatea código Python
   - isort: Ordena imports

2. **Validación de sintaxis** (2-3s)
   - flake8: Solo errores críticos

3. **Tests optimizados** (15-30s)
   - `--lf`: Solo tests que fallaron antes
   - `--ff`: Tests fallidos primero
   - `-x`: Detener al primer fallo
   - `-n auto`: Paralelo (usa todos los cores)
   - Sin cobertura (más rápido)

4. **Checks básicos** (1-2s)
   - Espacios, merge conflicts, YAML

**Tiempo total**:
- Primera vez: 30-40s
- Siguientes (sin fallos): 5-15s
- Con fallos previos: 10-20s

#### Optimización de Tests

**Comportamiento inteligente:**

```bash
# Escenario 1: Primera vez
git commit  # Ejecuta todos los tests: 30-40s

# Escenario 2: Todos pasaron
git commit  # Solo verifica: 5-15s

# Escenario 3: Algo falló antes
git commit  # Solo ejecuta tests que fallaron: 10-20s

# Escenario 4: Desarrollo rápido
git commit --no-verify  # Sin tests: < 5s
```

#### Troubleshooting

**Tests muy lentos (> 60s)**
```bash
# Verificar que pytest-xdist esté instalado
pip install pytest-xdist

# Ver cuántos cores está usando
pytest tests/ -n auto -v
```

**Tests fallan en pre-commit pero pasan manualmente**
```bash
# Limpiar cache de pytest
pytest --cache-clear

# Ejecutar exactamente como pre-commit
pytest tests/ --lf --ff -x -n auto --no-cov
```

**Saltar tests temporalmente**
```bash
# Para desarrollo iterativo rápido
git commit --no-verify -m "WIP"

# O configurar alias
git config --local alias.cfast "commit --no-verify"
git cfast -m "WIP"
```

**Error: "pytest: command not found"**
```bash
# Asegurar que el venv esté activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements-dev.txt
```

**Pre-commit Hooks Fallan**

```bash
# Ver logs detallados
pre-commit run --all-files --verbose

# Saltar hooks específicos
SKIP=mypy pre-commit run --all-files

# Actualizar hooks
pre-commit autoupdate
```

### FastMCP Preflight Fallan

```bash
# Ejecutar con debug
python scripts/fastmcp_preflight.py

# Verificar configuración
python -c "import yaml; print(yaml.safe_load(open('fastmcp.yaml')))"
```

### Tests Fallan

```bash
# Ejecutar tests específicos
pytest tests/unit/test_config.py -v

# Con debug
pytest tests/ -v -s --tb=long
```

### GitHub Actions Fallan

1. Revisar logs en GitHub Actions
2. Verificar que los secrets estén configurados
3. Ejecutar validaciones localmente

## 📚 Recursos Adicionales

- [Documentación Pre-commit](https://pre-commit.com/)
- [Documentación FastMCP](https://gofastmcp.com)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Pytest](https://docs.pytest.org/)

## 🤝 Contribuir

### 1. Fork del Repositorio

### 2. Configurar Entorno Local

```bash
git clone tu-fork
cd MCPtrackhsConnector
pip install -r requirements-dev.txt
pre-commit install
```

### 3. Crear Feature Branch

```bash
git checkout -b feature/tu-funcionalidad
```

### 4. Desarrollo

- Hacer cambios
- Ejecutar `python scripts/fastmcp_preflight.py`
- Hacer commit (pre-commit se ejecuta automáticamente)

### 5. Push y Pull Request

```bash
git push origin feature/tu-funcionalidad
# Crear Pull Request en GitHub
```

## 📞 Soporte

Si encuentras problemas:

1. Revisa esta documentación
2. Ejecuta `python scripts/fastmcp_preflight.py` localmente
3. Revisa los logs de GitHub Actions
4. Abre un issue en GitHub
