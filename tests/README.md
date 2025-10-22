# Testing Strategy - MVP

## 🎯 Filosofía de Testing Simplificada

Esta estrategia de testing está diseñada para un **MVP** (Minimum Viable Product) con enfoque en:

- ✅ **Comportamiento, no implementación**
- ✅ **Un test por funcionalidad crítica**
- ✅ **Feedback rápido para iteración ágil**
- ✅ **Cobertura suficiente (70-80%) para MVP**

## 🚀 Quick Start

```bash
# Verificación rápida (<5 segundos)
pytest tests/smoke/ -v

# Tests completos (<30 segundos)
pytest tests/critical/ -v

# Todo junto (<30 segundos)
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src/trackhs_mcp --cov-report=term-missing
```

## 📁 Estructura Simplificada

```
tests/
├── critical/          # ~40 tests de funcionalidad crítica
│   ├── test_api_client.py           # Auth, conexión, errores HTTP
│   ├── test_search_reservations.py  # Tool completa + validaciones
│   ├── test_get_reservation.py      # Tool completa + validaciones
│   ├── test_get_folio.py           # Tool completa + validaciones
│   ├── test_search_units.py        # Tool completa + validaciones
│   ├── test_search_amenities.py    # Tool completa + validaciones
│   └── test_create_work_order.py   # Tool completa + validaciones
├── smoke/            # ~25 tests de humo
│   ├── test_mcp_server.py          # Servidor levanta y responde
│   ├── test_all_tools_registered.py # Todas las tools están registradas
│   └── test_resources_prompts.py   # Resources y prompts cargan
└── conftest.py       # Fixtures compartidas (simplificadas)
```

## 🧪 Tipos de Tests

### Tests Críticos (`critical/`)

Verifican **comportamiento esencial** de cada herramienta MCP:

- ✅ **Autenticación funciona** - API client maneja credenciales
- ✅ **Herramientas ejecutan** - Cada tool MCP funciona con parámetros válidos
- ✅ **Validación de parámetros** - Rechaza valores inválidos correctamente
- ✅ **Manejo de errores HTTP** - 401, 404, 500, timeout
- ✅ **Paginación funciona** - Navegación entre páginas
- ✅ **Transformación de datos** - API → MCP es correcta

### Tests de Humo (`smoke/`)

Verifican **integración básica** del sistema:

- ✅ **Servidor MCP levanta** - Sin errores de configuración
- ✅ **6 tools registradas** - Todas las herramientas están disponibles
- ✅ **16 resources disponibles** - Schemas, docs, examples, references
- ✅ **3 prompts disponibles** - Prompts de búsqueda funcionan
- ✅ **Schema hook activo** - Corrección automática de esquemas

## 📊 Métricas de Éxito

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Tests Totales** | 755 | ~65 | -91% |
| **Tiempo Ejecución** | ~2 min | <30s | -75% |
| **Archivos Test** | 51 | 12 | -76% |
| **Cobertura** | 89-95% | 70-80% | Suficiente para MVP |
| **Mantenibilidad** | Baja | Alta | Cambios simples |

## 🔧 Comandos Útiles

```bash
# Solo tests críticos
pytest tests/critical/ -v

# Solo smoke tests (muy rápido)
pytest tests/smoke/ -v

# Tests con marcadores
pytest -m critical -v
pytest -m smoke -v

# Con cobertura específica
pytest tests/critical/ --cov=src/trackhs_mcp --cov-report=html

# Tests en paralelo (si está disponible)
pytest tests/ -n auto
```

## 🎯 Qué NO Testeamos (Simplificación)

❌ **Tests de implementación interna**:
- Funciones `_parse_id_string`, `_validate_date`
- Value objects triviales (Pydantic ya los valida)
- Utilidades simples (logging, formateo)

❌ **Tests duplicados**:
- Mismo comportamiento en unit + integration + e2e
- Validación de Pydantic (ya está testeado)
- Tests de tipos (MyPy hace esto)

❌ **Tests de Clean Architecture**:
- Tests de cada capa por separado
- Tests de ports/adapters como concepto
- Tests de inyección de dependencias

❌ **Tests de detalles**:
- Mensajes de error exactos
- Call counts específicos
- Orden de llamadas
- Formato de logs

## 🚀 Flujo de Desarrollo

### Desarrollo Rápido
```bash
# 1. Hacer cambios
# 2. Verificación rápida
pytest tests/smoke/ -v

# 3. Si todo OK, commit
git add .
git commit -m "feat: nueva funcionalidad"
```

### Antes de Push
```bash
# Tests completos
pytest tests/ -v --cov=src/trackhs_mcp

# Si todo OK, push
git push origin main
```

### Desarrollo Iterativo
```bash
# Para cambios frecuentes, saltar tests temporalmente
git commit --no-verify -m "WIP: desarrollo iterativo"

# Cuando esté listo, validación completa
pytest tests/ -v
git commit -m "feat: funcionalidad completa"
```

## 🐛 Troubleshooting

### Tests Muy Lentos
```bash
# Verificar que pytest-xdist esté instalado
pip install pytest-xdist

# Ejecutar en paralelo
pytest tests/ -n auto
```

### Tests Fallan
```bash
# Ver detalles del error
pytest tests/ -v --tb=long

# Solo el test que falla
pytest tests/critical/test_search_reservations.py::TestSearchReservationsCritical::test_search_reservations_basic_success -v
```

### Cobertura Baja
```bash
# Ver qué no está cubierto
pytest tests/ --cov=src/trackhs_mcp --cov-report=term-missing

# Generar reporte HTML
pytest tests/ --cov=src/trackhs_mcp --cov-report=html
# Abrir htmlcov/index.html
```

## 📈 Beneficios de Esta Estrategia

✅ **Velocidad**: 4x más rápido (2min → 30s)
✅ **Simplicidad**: 10x menos código (755 → 65 tests)
✅ **Mantenibilidad**: Cambios requieren actualizar 1-2 tests, no 10-20
✅ **Claridad**: Tests expresan "qué" hace el sistema, no "cómo"
✅ **Iteración rápida**: Ciclo de feedback inmediato
✅ **Suficiente para MVP**: 70-80% cobertura es excelente para validar producto

## 🔄 Migración desde Tests Antiguos

Si necesitas volver a los tests antiguos:

```bash
# Los tests antiguos están en la rama backup
git checkout backup-old-tests

# Para volver a la nueva estrategia
git checkout main
```

## 📚 Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [MCP Protocol](https://modelcontextprotocol.io)
- [TrackHS API Documentation](https://api.trackhs.com/docs)
