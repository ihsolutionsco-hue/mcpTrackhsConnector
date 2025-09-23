# Guía de Despliegue - Track HS MCP Server

## Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd trackhs-mcp-server

# 2. Ejecutar setup automático
npm run setup

# 3. Configurar credenciales
# Editar archivo .env con tus credenciales de Track HS

# 4. Iniciar servidor
npm start
```

## Configuración Manual

### 1. Instalar Dependencias

```bash
npm install
```

### 2. Compilar TypeScript

```bash
npm run build
```

### 3. Configurar Variables de Entorno

Crear archivo `.env`:

```bash
TRACKHS_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

### 4. Configurar Claude Desktop

Agregar a tu archivo de configuración de Claude Desktop:

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "node",
      "args": ["ruta/completa/a/trackhs-mcp-server/dist/index.js"],
      "env": {
        "TRACKHS_API_URL": "https://api-integration-example.tracksandbox.io/api",
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

## Desarrollo

### Modo Desarrollo

```bash
npm run dev
```

### Limpiar Build

```bash
npm run clean
```

### Recompilar

```bash
npm run build
```

## Verificación

### Probar Conexión

```bash
# Verificar que el servidor inicia correctamente
npm start
```

### Verificar Herramientas

El servidor MCP expone las siguientes herramientas:

- `get_reviews`: Obtener reseñas de propiedades
- `get_reservation`: Obtener detalles de reservación

## Solución de Problemas

### Error de Credenciales

```
Variable de entorno requerida no configurada: TRACKHS_USERNAME
```

**Solución:** Verificar que todas las variables de entorno estén configuradas en el archivo `.env`.

### Error de Compilación

```
Error en compilación: TypeScript
```

**Solución:** 
1. Verificar que TypeScript esté instalado: `npm install -g typescript`
2. Limpiar y recompilar: `npm run clean && npm run build`

### Error de Conexión API

```
Track HS API Error: 401 Unauthorized
```

**Solución:** Verificar credenciales en el archivo `.env`.

## Estructura del Proyecto

```
trackhs-mcp-server/
├── src/
│   ├── index.ts              # Punto de entrada
│   ├── server.ts              # Servidor MCP
│   ├── core/                  # Componentes base
│   │   ├── api-client.ts      # Cliente HTTP
│   │   ├── auth.ts            # Autenticación
│   │   ├── base-tool.ts       # Clase base
│   │   └── types.ts           # Tipos compartidos
│   ├── tools/                 # Herramientas MCP
│   │   ├── get-reviews.ts     # Reseñas
│   │   └── get-reservation.ts # Reservaciones
│   └── types/                 # Tipos específicos
│       ├── reviews.ts         # Tipos de reseñas
│       └── reservations.ts    # Tipos de reservaciones
├── dist/                      # Archivos compilados
├── scripts/                   # Scripts de utilidad
└── package.json
```

## Próximos Pasos

1. **Configurar credenciales** en el archivo `.env`
2. **Probar conexión** con `npm start`
3. **Configurar Claude Desktop** con este servidor
4. **Probar herramientas** desde Claude Desktop
