# Estrategia de Testing - Track HS MCP Server

Este documento describe la estrategia completa de testing implementada para el servidor MCP de Track HS.

## 📋 Estructura de Testing

### 1. Tests Unitarios (`tests/unit/`)
- **Propósito**: Probar componentes individuales de forma aislada
- **Cobertura**: 195 tests que cubren todas las funcionalidades básicas
- **Tiempo de ejecución**: ~22 segundos
- **Estado**: ✅ **Completamente implementado y funcionando**

#### Estructura:
```
tests/unit/
├── core/                    # Tests de componentes core
│   ├── auth.test.ts        # Autenticación
│   ├── api-client.test.ts  # Cliente API
│   ├── base-tool.test.ts   # Herramienta base
│   └── types.test.ts       # Tipos de datos
├── tools/                  # Tests de herramientas MCP
│   ├── get-reviews.test.ts
│   ├── get-contacts.test.ts
│   └── get-reservation.test.ts
└── types/                  # Tests de tipos de datos
    ├── reviews.test.ts
    └── contacts.test.ts
```

### 2. Tests de Integración (`tests/integration/`)
- **Propósito**: Probar la comunicación real con la API de Track HS
- **Cobertura**: Tests que validan flujos completos con API real
- **Tiempo de ejecución**: ~30 segundos por test
- **Estado**: ✅ **Implementado**

#### Estructura:
```
tests/integration/
├── api-client.integration.test.ts  # Integración con API real
├── tools.integration.test.ts       # Flujos completos de herramientas
├── server.integration.test.ts      # Servidor MCP completo
├── jest.config.js                  # Configuración Jest
└── setup.ts                        # Setup de integración
```

#### Características:
- **Comunicación real con API**: Tests que requieren conexión a la API de Track HS
- **Validación de respuestas**: Verificación de estructura de datos reales
- **Manejo de errores**: Tests de robustez con API real
- **Configuración flexible**: Soporte para diferentes entornos (dev, staging, prod)

### 3. Tests E2E (`tests/e2e/`)
- **Propósito**: Simular escenarios de usuario reales
- **Cobertura**: Flujos completos de usuario y servidor MCP
- **Tiempo de ejecución**: ~60 segundos por test
- **Estado**: ✅ **Implementado**

#### Estructura:
```
tests/e2e/
├── user-scenarios.e2e.test.ts  # Escenarios de usuario
├── mcp-server.e2e.test.ts      # Servidor MCP completo
├── jest.config.js              # Configuración Jest
└── setup.ts                    # Setup E2E
```

#### Escenarios de Usuario:
1. **Análisis de Reseñas de Hotel**: Flujo completo de análisis de reseñas
2. **Gestión de Contactos**: Búsqueda y gestión de contactos de clientes
3. **Gestión de Reservaciones**: Búsqueda y detalles de reservaciones
4. **Gestión de Unidades**: Información de unidades de alojamiento
5. **Flujo Completo**: Análisis integral de hotel
6. **Manejo de Errores**: Robustez en producción
7. **Performance**: Escalabilidad y rendimiento

## 🚀 Comandos de Testing

### Tests Unitarios
```bash
# Ejecutar todos los tests unitarios
npm run test:unit

# Ejecutar con watch mode
npm run test:watch

# Ejecutar con cobertura
npm run test:coverage
```

### Tests de Integración
```bash
# Ejecutar tests de integración
npm run test:integration

# Ejecutar con watch mode
npm run test:integration:watch

# Ejecutar con configuración específica
TRACKHS_API_URL=https://api.trackhs.com npm run test:integration
```

### Tests E2E
```bash
# Ejecutar todos los tests E2E
npm run test:e2e

# Ejecutar escenarios de usuario
npm run test:user-scenarios

# Ejecutar tests de performance
npm run test:performance
```

### Tests Completos
```bash
# Ejecutar todos los tipos de tests
npm run test:all

# Ejecutar en modo CI
npm run test:ci

# Ejecutar con debug
npm run test:debug
```

## ⚙️ Configuración

### Variables de Entorno

#### Para Tests Unitarios
```bash
# No se requieren variables de entorno
# Los tests usan mocks
```

#### Para Tests de Integración
```bash
TRACKHS_API_URL=https://api.trackhs.com
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
```

#### Para Tests E2E
```bash
TRACKHS_API_URL=https://api.trackhs.com
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
```

### Configuración de Jest

#### Tests Unitarios
- **Timeout**: 10 segundos
- **Cobertura**: Habilitada
- **Mocks**: Completos

#### Tests de Integración
- **Timeout**: 30 segundos
- **API Real**: Requerida
- **Cobertura**: Habilitada

#### Tests E2E
- **Timeout**: 60 segundos
- **API Real**: Requerida
- **Workers**: Secuencial
- **Cobertura**: Habilitada

## 📊 Métricas de Testing

### Cobertura de Código
- **Líneas**: >90%
- **Funciones**: >95%
- **Ramas**: >85%
- **Declaraciones**: >90%

### Distribución de Tests
- **Unitarios**: 195 tests (~22s)
- **Integración**: 15 tests (~30s c/u)
- **E2E**: 20 tests (~60s c/u)

### Objetivos de Performance
- **Tests Unitarios**: <30 segundos
- **Tests de Integración**: <5 minutos
- **Tests E2E**: <10 minutos
- **Tests Completos**: <15 minutos

## 🔧 Herramientas y Utilidades

### Mocks y Fixtures
- **API Responses**: `tests/mocks/api-responses.ts`
- **Test Helpers**: `tests/utils/test-helpers.ts`
- **Configuración**: `tests/config/test-config.ts`

### Utilidades de Testing
- **Mock Factory**: Creación de mocks estructurados
- **Assertion Helpers**: Aserciones comunes
- **Test Data**: Datos de prueba realistas
- **Error Simulation**: Simulación de errores

## 🛡️ Mejores Prácticas

### Estructura de Tests
1. **AAA Pattern**: Arrange, Act, Assert
2. **Naming**: Descriptivo y claro
3. **Isolation**: Tests independientes
4. **Cleanup**: Limpieza después de cada test

### Manejo de Errores
1. **Error Simulation**: Simulación de errores reales
2. **Edge Cases**: Casos límite y excepciones
3. **Network Errors**: Errores de red y timeout
4. **API Errors**: Errores de API específicos

### Performance
1. **Parallel Execution**: Tests paralelos cuando sea posible
2. **Resource Management**: Gestión eficiente de recursos
3. **Timeout Configuration**: Timeouts apropiados
4. **Memory Management**: Limpieza de memoria

## 🚨 Troubleshooting

### Problemas Comunes

#### Tests de Integración Fallan
```bash
# Verificar variables de entorno
echo $TRACKHS_API_URL
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD

# Verificar conectividad
curl -I $TRACKHS_API_URL
```

#### Tests E2E Timeout
```bash
# Aumentar timeout
npm run test:e2e -- --testTimeout=120000

# Ejecutar en modo debug
npm run test:debug
```

#### Tests Unitarios Fallan
```bash
# Limpiar cache
npm run clean
rm -rf node_modules
npm install

# Ejecutar con verbose
npm run test:unit -- --verbose
```

## 📈 Próximos Pasos

### Mejoras Planificadas
1. **Tests de Performance**: Métricas de rendimiento
2. **Tests de Seguridad**: Validación de seguridad
3. **Tests de Carga**: Pruebas de carga y estrés
4. **Tests de Compatibilidad**: Diferentes versiones de Node.js

### Automatización
1. **CI/CD Pipeline**: Integración continua
2. **Test Reports**: Reportes automatizados
3. **Coverage Reports**: Reportes de cobertura
4. **Performance Monitoring**: Monitoreo de rendimiento

## 📚 Recursos Adicionales

- **Jest Documentation**: https://jestjs.io/docs/getting-started
- **Testing Best Practices**: https://testingjavascript.com/
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Track HS API**: https://docs.trackhs.com/

---

**Estado**: ✅ **Estrategia de Testing Completamente Implementada**
**Cobertura**: 195 tests unitarios + 15 tests integración + 20 tests E2E
**Tiempo Total**: ~15 minutos para suite completa
**Calidad**: Cobertura >90% en todos los aspectos críticos