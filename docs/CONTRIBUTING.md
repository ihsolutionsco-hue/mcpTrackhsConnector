# Guía de Contribución - TrackHS MCP Connector

¡Gracias por tu interés en contribuir al TrackHS MCP Connector! Esta guía te ayudará a configurar tu entorno de desarrollo y seguir las mejores prácticas del proyecto.

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ihsolutionsco-hue/mcpTrackhsConnector.git
cd mcpTrackhsConnector
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### 4. Configurar Pre-commit Hooks

**¡IMPORTANTE!** Los pre-commit hooks son obligatorios para este proyecto. Previenen errores de formato y calidad antes de hacer commit.

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks
pre-commit install

# (Opcional) Instalar hooks para todos los commits
pre-commit install --hook-type pre-push
```

### 5. Verificar Configuración

```bash
# Ejecutar todos los checks localmente
pre-commit run --all-files

# Ejecutar tests
pytest

# Verificar formato
black --check src/ tests/
isort --check-only src/ tests/
```

## 🛠️ Herramientas de Desarrollo

### Formateo Automático

El proyecto usa **Black** e **isort** para formateo automático:

```bash
# Formatear todo el código
black src/ tests/
isort src/ tests/

# Verificar formato (sin cambiar archivos)
black --check src/ tests/
isort --check-only src/ tests/
```

### Linting

Usamos **Flake8** para linting:

```bash
# Ejecutar linting
flake8 src/ tests/

# Con configuración específica
flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
```

### Type Checking

**MyPy** para verificación de tipos:

```bash
# Verificar tipos
mypy src/

# Con configuración específica
mypy src/ --ignore-missing-imports --no-strict-optional
```

### Testing

```bash
# Ejecutar todos los tests
pytest

# Solo tests unitarios
pytest tests/unit/

# Solo tests de integración
pytest tests/integration/

# Con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/test_search_reservations_validation.py -v
```

## 📝 Flujo de Trabajo

### 1. Crear Branch

```bash
# Crear y cambiar a nueva branch
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/corregir-bug
```

### 2. Desarrollo

- Escribe código siguiendo las convenciones del proyecto
- Los pre-commit hooks se ejecutarán automáticamente
- Si hay errores, corrígelos antes de hacer commit

### 3. Testing

```bash
# Ejecutar tests relevantes
pytest tests/unit/test_tu_funcionalidad.py

# Ejecutar todos los tests
pytest
```

### 4. Commit

```bash
# Los pre-commit hooks se ejecutarán automáticamente
git add .
git commit -m "feat: agregar nueva funcionalidad de búsqueda"

# Si hay errores de formato, corrígelos y vuelve a hacer commit
```

### 5. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub.

## 🎯 Convenciones de Código

### Estructura de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: cambios de formato (sin lógica)
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

### Naming Conventions

- **Funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Variables**: `snake_case`

### Documentación

- Docstrings en todas las funciones públicas
- Type hints obligatorios
- Comentarios para lógica compleja

```python
def search_reservations(
    page: int = 1,
    size: int = 10,
    # ... más parámetros
) -> dict:
    """
    Search reservations in Track HS API V2 with comprehensive filtering options.

    Args:
        page: Page number (0-based, max 10k total results)
        size: Page size (max 10k total results)
        # ... más documentación

    Returns:
        Complete reservation data with embedded objects

    Raises:
        ValidationError: If parameters are invalid
    """
```

## 🧪 Testing

### Escribir Tests

```python
import pytest
from unittest.mock import AsyncMock, patch
from src.trackhs_mcp.core.error_handling import ValidationError

class TestMiFuncionalidad:
    """Tests para mi funcionalidad"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.mark.asyncio
    async def test_caso_exitoso(self, mock_api_client):
        """Test caso exitoso"""
        # Arrange
        mock_api_client.get.return_value = {"data": "test"}

        # Act
        result = await mi_funcion()

        # Assert
        assert result == {"data": "test"}
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_caso_error(self, mock_api_client):
        """Test manejo de errores"""
        # Arrange
        mock_api_client.get.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(ValidationError):
            await mi_funcion()
```

### Markers de Tests

```python
@pytest.mark.unit
def test_unitario():
    """Test unitario rápido"""
    pass

@pytest.mark.integration
def test_integracion():
    """Test de integración"""
    pass

@pytest.mark.e2e
def test_end_to_end():
    """Test end-to-end"""
    pass

@pytest.mark.slow
def test_lento():
    """Test que toma tiempo"""
    pass
```

## 🔧 Configuración de IDE

### VS Code

Crea `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm

1. Configurar Python interpreter: `venv/Scripts/python.exe`
2. Habilitar Black como formatter
3. Configurar Flake8 como linter
4. Configurar pytest como test runner

## 🚨 Troubleshooting

### Pre-commit Hooks Fallan

```bash
# Ver qué hooks están fallando
pre-commit run --all-files

# Saltar hooks temporalmente (solo en emergencias)
git commit --no-verify -m "fix: corrección urgente"

# Actualizar hooks
pre-commit autoupdate
```

### Tests Fallan

```bash
# Ejecutar tests con más detalle
pytest -v --tb=short

# Ejecutar solo tests que fallan
pytest --lf

# Ejecutar tests con coverage
pytest --cov=src --cov-report=html
```

### Formato Inconsistente

```bash
# Aplicar formato automáticamente
black src/ tests/
isort src/ tests/

# Verificar formato
black --check src/ tests/
isort --check-only src/ tests/
```

## 📚 Recursos Adicionales

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)

## 🤝 Proceso de Review

1. **Automático**: GitHub Actions ejecuta todos los checks
2. **Manual**: Review de código por maintainers
3. **Aprobación**: Al menos 1 aprobación requerida
4. **Merge**: Solo después de que todos los checks pasen

## ❓ Preguntas Frecuentes

**Q: ¿Puedo saltar los pre-commit hooks?**
A: Solo en emergencias con `--no-verify`, pero es mejor arreglar los problemas.

**Q: ¿Qué hago si los tests fallan en CI pero pasan localmente?**
A: Verifica que tu entorno local coincida con CI (Python 3.11, mismas dependencias).

**Q: ¿Cómo agrego nuevas dependencias?**
A: Actualiza `requirements.txt` y `requirements-dev.txt`, luego ejecuta `pip install -r requirements-dev.txt`.

---

¡Gracias por contribuir! 🎉
