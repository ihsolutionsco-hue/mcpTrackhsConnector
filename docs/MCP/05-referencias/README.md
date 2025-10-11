# Referencias MCP

Esta sección contiene documentación técnica de referencia para desarrolladores MCP.

## Especificación MCP

**Ubicación**: [especificacion/](./especificacion/)

Documentación oficial de la especificación MCP por versión:

- **2024-11-05**: Primera versión estable
- **2025-03-26**: Versión con mejoras de transporte
- **2025-06-18**: Versión actual con autorización OAuth
- **draft**: Versión en desarrollo

### Estructura de la Especificación

```
especificacion/
├── 2024-11-05/          # Primera versión
├── 2025-03-26/          # Versión con transporte HTTP
├── 2025-06-18/          # Versión actual (recomendada)
└── draft/               # Versión en desarrollo
    ├── architecture/    # Arquitectura del protocolo
    ├── basic/          # Conceptos básicos
    ├── client/         # Funcionalidades del cliente
    └── server/         # Funcionalidades del servidor
```

## Schemas

**Ubicación**: [schemas/](./schemas/)

Esquemas de validación para implementaciones MCP:

- **schema.json**: Esquema JSON Schema para validación
- **schema.ts**: Definiciones TypeScript para desarrollo

### Uso de los Schemas

**JSON Schema** (para validación):
```typescript
import Ajv from 'ajv';
import schema from './schemas/schema.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);

// Validar mensaje MCP
const isValid = validate(mcpMessage);
```

**TypeScript** (para desarrollo):
```typescript
import { MCPRequest, MCPResponse } from './schemas/schema';

function handleMCPRequest(request: MCPRequest): MCPResponse {
  // Implementación tipada
}
```

## APIs de Referencia

### Python SDK
**Ubicación**: [07-repositorios-originales/python-sdk/](../07-repositorios-originales/python-sdk/)

Documentación completa del SDK Python:
- [API Reference](https://modelcontextprotocol.github.io/python-sdk/api/)
- [Guías de desarrollo](../03-guias-desarrollo/)
- [Ejemplos prácticos](../04-ejemplos/)

### TypeScript SDK
**Ubicación**: [07-repositorios-originales/modelcontextprotocol/](../07-repositorios-originales/modelcontextprotocol/)

Documentación del SDK TypeScript:
- [Especificación TypeScript](./especificacion/)
- [Definiciones de tipos](./schemas/schema.ts)

## Herramientas de Desarrollo

### MCP Inspector
**Ubicación**: [06-herramientas/guia-inspector.md](../06-herramientas/guia-inspector.md)

Herramienta interactiva para testing y debugging:
- Testing de servidores MCP
- Debugging de conexiones
- Validación de protocolo

## Recursos Adicionales

### Repositorios Oficiales
- **MCP Specification**: [07-repositorios-originales/modelcontextprotocol/](../07-repositorios-originales/modelcontextprotocol/)
- **Python SDK**: [07-repositorios-originales/python-sdk/](../07-repositorios-originales/python-sdk/)
- **MCP Inspector**: [07-repositorios-originales/inspector/](../07-repositorios-originales/inspector/)

### Enlaces Externos
- [Sitio web oficial MCP](https://modelcontextprotocol.io)
- [Especificación en línea](https://spec.modelcontextprotocol.io)
- [GitHub oficial](https://github.com/modelcontextprotocol)

## Versiones y Compatibilidad

### Matriz de Compatibilidad

| Cliente | Servidor | Transporte | Compatibilidad |
|---------|----------|------------|----------------|
| Claude Desktop | Local | stdio | ✅ Completa |
| Claude Web | Remoto | HTTP | ✅ Completa |
| Custom Client | Local/Remoto | stdio/HTTP | ✅ Completa |

### Migración entre Versiones

**De 2024-11-05 a 2025-03-26**:
- Nuevos transportes HTTP
- Mejoras en manejo de errores
- Compatibilidad hacia atrás mantenida

**De 2025-03-26 a 2025-06-18**:
- Autenticación OAuth 2.0
- Nuevas capacidades de cliente
- Mejoras en seguridad
