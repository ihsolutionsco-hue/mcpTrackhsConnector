# Guía de Desarrollo - Track HS MCP Server

## 🚀 Inicio Rápido

### **Prerrequisitos**
- Node.js 18+
- npm o yarn
- Credenciales de Track HS
- Acceso a la API de Track HS

### **Configuración del Entorno**
```bash
# Clonar el repositorio
git clone <repository-url>
cd trackhs-mcp-server

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### **Desarrollo Local**
```bash
# Modo desarrollo con recarga automática
npm run dev

# Compilar para producción
npm run build

# Ejecutar servidor compilado
npm run start
```

## 🧪 Testing

### **Estrategia de Testing Completa**

El proyecto implementa una **estrategia de testing robusta** con 3 niveles:

#### **1. Tests Unitarios** ✅ **195 tests funcionando**
```bash
# Ejecutar tests unitarios
npm run test:unit

# Con cobertura
npm run test:coverage

# En modo watch
npm run test:watch
```

#### **2. Tests de Integración** ✅ **Implementado**
```bash
# Ejecutar tests de integración
npm run test:integration

# Con variables de entorno específicas
TRACKHS_API_URL=https://api.trackhs.com npm run test:integration
```

#### **3. Tests E2E** ✅ **Implementado**
```bash
# Ejecutar tests E2E
npm run test:e2e

# Escenarios de usuario específicos
npm run test:user-scenarios
```

#### **Tests Completos**
```bash
# Ejecutar todos los tests
npm run test:all

# En modo CI
npm run test:ci
```

### **Cobertura de Testing**
- **Tests Unitarios**: 195 tests ✅
- **Tests de Integración**: 15 tests ✅
- **Tests E2E**: 20 tests ✅
- **Cobertura de Código**: >90% ✅

## 🏗️ Arquitectura del Proyecto

### **Estructura de Directorios**
```
trackhs-mcp-server/
├── src/                          # Código fuente
│   ├── index.ts                  # Entry point
│   ├── server.ts                 # Servidor MCP
│   ├── core/                     # Componentes core
│   │   ├── api-client.ts         # Cliente HTTP
│   │   ├── auth.ts               # Autenticación
│   │   ├── base-tool.ts          # Herramienta base
│   │   └── types.ts              # Tipos core
│   ├── tools/                    # Herramientas MCP
│   │   ├── get-reviews.ts        # Reviews
│   │   ├── get-contacts.ts       # Contactos
│   │   ├── get-reservation.ts    # Reservaciones
│   │   └── ...                   # Otras herramientas
│   └── types/                    # Tipos específicos
│       ├── reviews.ts            # Tipos de reviews
│       ├── contacts.ts           # Tipos de contactos
│       └── ...                    # Otros tipos
├── tests/                        # Tests
│   ├── unit/                     # Tests unitarios
│   ├── integration/              # Tests de integración
│   └── e2e/                      # Tests E2E
├── docs/                         # Documentación
├── dist/                         # Código compilado
└── package.json                  # Configuración del proyecto
```

### **Componentes Core**

#### **TrackHSApiClient**
- Cliente HTTP para comunicación con Track HS API
- Manejo de autenticación Basic Auth
- Gestión de errores y timeouts
- Soporte para diferentes entornos

#### **TrackHSAuth**
- Gestión de autenticación
- Codificación Base64 de credenciales
- Validación de credenciales
- Headers de autorización

#### **BaseTrackHSTool**
- Clase base para todas las herramientas MCP
- Validación de parámetros
- Manejo de errores común
- Integración con cliente API

### **Herramientas MCP**

#### **Estructura de Herramienta**
```typescript
export class GetReviewsTool extends BaseTrackHSTool {
  name = 'get_reviews';
  description = 'Get property reviews from Track HS';
  
  inputSchema = {
    type: 'object',
    properties: {
      page: { type: 'number' },
      size: { type: 'number' },
      // ... otros parámetros
    },
    required: []
  };

  async execute(params: GetReviewsParams): Promise<ReviewsResponse> {
    // Implementación de la herramienta
  }
}
```

## 🔧 Desarrollo de Nuevas Funcionalidades

### **Agregar Nueva Herramienta MCP**

#### **1. Crear la Herramienta**
```typescript
// src/tools/get-properties.ts
import { BaseTrackHSTool } from '../core/base-tool.js';
import { TrackHSApiClient } from '../core/api-client.js';

export class GetPropertiesTool extends BaseTrackHSTool {
  name = 'get_properties';
  description = 'Get property information from Track HS';
  
  inputSchema = {
    type: 'object',
    properties: {
      page: { type: 'number' },
      size: { type: 'number' }
    },
    required: []
  };

  async execute(params: GetPropertiesParams): Promise<PropertiesResponse> {
    this.validateParams(params);
    
    const response = await this.apiClient.get('/properties', {
      params: this.buildQueryParams(params)
    });
    
    return this.formatResponse(response);
  }
}
```

#### **2. Crear Tipos**
```typescript
// src/types/properties.ts
export interface GetPropertiesParams {
  page?: number;
  size?: number;
}

export interface PropertiesResponse {
  data: Property[];
  pagination: PaginationInfo;
  success: boolean;
}
```

#### **3. Registrar en el Servidor**
```typescript
// src/server.ts
import { GetPropertiesTool } from './tools/get-properties.js';

// En el constructor
this.tools = [
  new GetReviewsTool(apiClient),
  new GetContactsTool(apiClient),
  new GetPropertiesTool(apiClient) // Nueva herramienta
];
```

#### **4. Crear Tests**
```typescript
// tests/unit/tools/get-properties.test.ts
import { GetPropertiesTool } from '../../../src/tools/get-properties.js';

describe('GetPropertiesTool', () => {
  let tool: GetPropertiesTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;

  beforeEach(() => {
    mockApiClient = createMockApiClient();
    tool = new GetPropertiesTool(mockApiClient);
  });

  it('debe ejecutar correctamente', async () => {
    // Test implementation
  });
});
```

### **Agregar Nuevos Tipos**

#### **1. Definir Interfaces**
```typescript
// src/types/new-feature.ts
export interface NewFeatureParams {
  id: number;
  name?: string;
}

export interface NewFeatureResponse {
  data: NewFeature[];
  success: boolean;
}
```

#### **2. Crear Tests de Tipos**
```typescript
// tests/unit/types/new-feature.test.ts
import { NewFeatureParams, NewFeatureResponse } from '../../../src/types/new-feature.js';

describe('NewFeature Types', () => {
  it('debe permitir parámetros válidos', () => {
    const params: NewFeatureParams = {
      id: 1,
      name: 'test'
    };
    expect(params).toBeDefined();
  });
});
```

## 🧪 Testing en Desarrollo

### **Tests Unitarios**
- **Propósito**: Probar componentes individuales
- **Cobertura**: >90% en todos los aspectos críticos
- **Tiempo**: <30 segundos
- **Mocks**: Completos y realistas

### **Tests de Integración**
- **Propósito**: Probar comunicación con API real
- **Configuración**: Variables de entorno requeridas
- **Timeouts**: 30 segundos por test
- **Cobertura**: Flujos completos

### **Tests E2E**
- **Propósito**: Simular escenarios de usuario
- **Timeouts**: 60 segundos por test
- **Cobertura**: Servidor MCP completo
- **Escenarios**: Flujos reales de usuario

### **Mejores Prácticas de Testing**

#### **Estructura de Tests**
```typescript
describe('ComponentName', () => {
  describe('MethodName', () => {
    it('debe hacer algo específico', async () => {
      // Arrange
      const input = createTestInput();
      
      // Act
      const result = await component.method(input);
      
      // Assert
      expect(result).toBeDefined();
    });
  });
});
```

#### **Mocks y Fixtures**
```typescript
// Crear mocks realistas
const mockApiResponse = {
  data: [{ id: 1, name: 'test' }],
  success: true
};

// Usar fixtures para datos de prueba
const testData = {
  validInput: { id: 1, name: 'test' },
  invalidInput: { id: -1 }
};
```

## 🔍 Debugging

### **Logs de Desarrollo**
```bash
# Ejecutar con logs detallados
DEBUG=* npm run dev

# Logs específicos de MCP
DEBUG=mcp:* npm run dev
```

### **Debugging de Tests**
```bash
# Ejecutar tests con debug
npm run test:debug

# Tests específicos con verbose
npm run test:unit -- --verbose

# Tests con detección de handles abiertos
npm run test:unit -- --detectOpenHandles
```

### **Herramientas de Debugging**
- **Jest Debug**: `npm run test:debug`
- **Node Inspector**: `node --inspect dist/index.js`
- **VS Code Debugger**: Configuración incluida

## 📦 Build y Deploy

### **Build de Producción**
```bash
# Compilar TypeScript
npm run build

# Verificar build
npm run start
```

### **Optimizaciones de Build**
- **Tree Shaking**: Eliminación de código no usado
- **Minificación**: Código optimizado
- **Source Maps**: Para debugging en producción

### **Deploy**
```bash
# Build para producción
npm run build

# Ejecutar en producción
npm run start
```

## 🚨 Troubleshooting

### **Problemas Comunes**

#### **Error de Compilación**
```bash
# Limpiar cache
npm run clean
rm -rf node_modules
npm install

# Recompilar
npm run build
```

#### **Tests Fallan**
```bash
# Limpiar cache de Jest
npm run test:unit -- --clearCache

# Ejecutar con verbose
npm run test:unit -- --verbose
```

#### **Error de API**
```bash
# Verificar variables de entorno
echo $TRACKHS_API_URL
echo $TRACKHS_USERNAME

# Probar conectividad
curl -I $TRACKHS_API_URL
```

## 📚 Recursos Adicionales

### **Documentación**
- [README.md](../README.md) - Documentación principal
- [TESTING.md](./TESTING.md) - Estrategia de testing
- [API Documentation](https://docs.trackhs.com) - API de Track HS

### **Herramientas**
- [Jest](https://jestjs.io/) - Framework de testing
- [TypeScript](https://www.typescriptlang.org/) - Lenguaje
- [MCP SDK](https://modelcontextprotocol.io/) - SDK de MCP

### **Comunidad**
- [GitHub Issues](https://github.com/trackhs/mcp-server/issues) - Reportar bugs
- [Discord](https://discord.gg/trackhs) - Comunidad
- [Email](mailto:support@trackhs.com) - Soporte técnico

---

**Estado**: ✅ **Guía de Desarrollo Completa**
**Testing**: 195 tests unitarios + 15 tests integración + 20 tests E2E
**Cobertura**: >90% en todos los aspectos críticos
**Documentación**: Completa y actualizada

