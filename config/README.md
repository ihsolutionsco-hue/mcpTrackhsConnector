# 📁 Configuración del Proyecto

Este directorio contiene todas las configuraciones centralizadas del proyecto Track HS MCP Connector.

## 📋 Archivos de Configuración

### **Configuración Principal**
- `tsconfig.json` - Configuración de TypeScript
- `jest.config.mjs` - Configuración de Jest para testing
- `vercel.json` - Configuración de despliegue en Vercel

### **Configuración de Desarrollo**
- `development.json` - Configuración para desarrollo local
- `deployment.json` - Configuración de despliegue
- `project.json` - Metadatos del proyecto

## 🔧 Uso

### **TypeScript**
```bash
# Compilar proyecto
npm run build

# Desarrollo con hot reload
npm run dev
```

### **Testing**
```bash
# Ejecutar todos los tests
npm run test:all

# Tests unitarios
npm run test:unit

# Tests de integración
npm run test:integration

# Tests E2E
npm run test:e2e

# Cobertura
npm run test:coverage
```

### **Despliegue**
```bash
# Deploy a producción
npm run deploy

# Deploy preview
npm run deploy:preview
```

## 📊 Configuración de Cobertura

El proyecto tiene configurados umbrales de cobertura:

- **Global**: 80% (branches, functions, lines, statements)
- **Core**: 85% (módulos core del servidor MCP)
- **Tools**: 80% (herramientas MCP)
- **Types**: 70% (definiciones de tipos)

## 🚀 Configuración de Vercel

La configuración de Vercel incluye:

- **Funciones serverless** con timeout de 30s
- **Memoria**: 1024MB por función
- **Región**: iad1 (Virginia, US)
- **CORS** habilitado para integración
- **Rewrites** para múltiples endpoints

## 📝 Notas

- Todas las configuraciones están centralizadas en este directorio
- Los archivos principales (`tsconfig.json`, `jest.config.mjs`, `vercel.json`) extienden las configuraciones de este directorio
- Para modificar configuraciones, edita los archivos en este directorio
- Los cambios se aplicarán automáticamente al usar los comandos de npm
