# 🚀 Guía de Configuración - Track HS MCP Connector

## 📋 Configuración Rápida

### **1. Variables de Entorno**
```bash
# Copia el archivo de ejemplo
cp env.example .env

# Edita con tus credenciales
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

### **2. Instalación**
```bash
# Instalar dependencias
npm install

# Compilar proyecto
npm run build

# Probar conexión
npm run test:connector
```

---

## 🤖 Configuración en Claude

### **Claude Desktop (Recomendado)**

#### **Ubicación del archivo de configuración:**

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

#### **Configuración:**
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

#### **Pasos:**
1. **Compila el proyecto**: `npm run build`
2. **Configura el archivo** con la configuración anterior
3. **Reinicia Claude Desktop**

---

### **Claude Web (Custom Connectors)**

#### **Paso 1: Acceder a Claude Web**
1. Ve a [claude.ai](https://claude.ai)
2. Inicia sesión con tu cuenta

#### **Paso 2: Configurar Custom Connector**
1. Haz clic en tu avatar (esquina superior derecha)
2. Selecciona "Settings"
3. En el menú lateral, haz clic en "Connectors"
4. Haz clic en "Add custom connector"

#### **Paso 3: Configurar el Conector**
Completa los campos con la siguiente información:

**Configuración Recomendada:**
- **Nombre**: `Track HS MCP Connector`
- **URL del servidor MCP remoto**: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web`
- **Descripción**: `Conector MCP para Track HS API`

**Configuración Alternativa:**
- **URL del servidor MCP remoto**: `https://trackhs-mcp-connector.vercel.app/api/mcp-real`

#### **Paso 4: Activar el Conector**
1. Haz clic en "Add"
2. El conector aparecerá en tu lista
3. Asegúrate de que esté activado

---

## 🧪 Verificar Configuración

### **Health Check**
```bash
# Verificar servidor principal
curl https://trackhs-mcp-connector.vercel.app/api

# Verificar servidor MCP Claude Web
curl https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web/health
```

### **Probar Herramientas**
```bash
# Listar herramientas disponibles
curl https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web/tools
```

### **Probar Protocolo MCP**
```bash
# Inicializar conexión MCP
curl -X POST https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"elicitation":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'

# Listar herramientas MCP
curl -X POST https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

---

## 🔧 Desarrollo Local

### **Comandos de Desarrollo**
```bash
# Desarrollo con hot reload
npm run dev

# Testing completo
npm run test:all

# Testing específico
npm run test:unit
npm run test:integration
npm run test:e2e

# Build para producción
npm run build

# Verificar configuración
npm run verify:final
```

### **Estructura del Proyecto**
```
src/
├── core/                    # Core del servidor MCP
│   ├── api-client.ts        # Cliente API de Track HS
│   ├── auth.ts             # Autenticación
│   ├── base-tool.ts        # Clase base para herramientas
│   └── types.ts            # Tipos principales
├── tools/                   # Herramientas MCP
│   ├── get-contacts.ts     # Gestión de contactos
│   ├── get-reservation.ts  # Detalles de reservas
│   ├── search-reservations.ts # Búsqueda de reservas
│   └── ...                 # Otras herramientas
├── types/                   # Tipos específicos
│   ├── contacts.ts         # Tipos de contactos
│   ├── reservations.ts     # Tipos de reservas
│   └── ...                 # Otros tipos
├── index.ts                # Punto de entrada
└── server.ts               # Servidor principal
```

---

## 🚀 Despliegue

### **Despliegue en Vercel**
```bash
# Deploy a producción
npm run deploy

# Deploy preview
npm run deploy:preview

# Verificar despliegue
npm run check:deployment
```

### **Configuración de Vercel**
1. **Variables de Entorno en Vercel:**
   - `TRACKHS_API_URL`
   - `TRACKHS_USERNAME`
   - `TRACKHS_PASSWORD`

2. **URLs Disponibles:**
   - Principal: `https://trackhs-mcp-connector.vercel.app/api`
   - MCP Claude Web: `https://trackhs-mcp-connector.vercel.app/api/mcp-claude-web`
   - MCP Real: `https://trackhs-mcp-connector.vercel.app/api/mcp-real`

---

## 🔍 Troubleshooting

### **Problemas Comunes**

**1. Claude no se conecta al servidor**
- ✅ Verifica que la URL sea correcta
- ✅ Comprueba que el servidor esté funcionando
- ✅ Revisa los logs de Claude

**2. Error de autenticación con Track HS**
- ✅ Verifica las credenciales de Track HS
- ✅ Comprueba las variables de entorno
- ✅ Revisa la configuración de autenticación

**3. Herramientas no funcionan**
- ✅ Verifica la conexión con Track HS API
- ✅ Comprueba los parámetros de entrada
- ✅ Revisa los logs del servidor

**4. Error de compilación**
- ✅ Verifica que Node.js sea versión 20+
- ✅ Ejecuta `npm install` para instalar dependencias
- ✅ Revisa la configuración de TypeScript

### **Logs y Debugging**
```bash
# Ver logs del servidor
npm run dev

# Testing con debug
npm run test:debug

# Verificar configuración
npm run verify:final
```

---

## 📞 Soporte

- **GitHub Issues**: Para reportar problemas
- **Documentación**: Guías completas en `/docs`
- **Email**: Soporte técnico

---

**¡Configuración completada!** 🎉

*Última actualización: 2025-01-27*
