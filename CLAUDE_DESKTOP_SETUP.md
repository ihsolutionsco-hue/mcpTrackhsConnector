# 🤖 Configuración de Claude Desktop para Track HS MCP

## 📋 **Guía Paso a Paso**

### **Paso 1: Localizar el archivo de configuración**

#### **Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### **macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### **Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### **Paso 2: Crear/Editar el archivo de configuración**

Crea el archivo `claude_desktop_config.json` con el siguiente contenido:

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario_aqui",
        "TRACKHS_PASSWORD": "tu_contraseña_aqui"
      }
    }
  }
}
```

### **Paso 3: Compilar el servidor MCP**

En la terminal, desde la carpeta del proyecto:

```bash
# Instalar dependencias (si no lo has hecho)
npm install

# Compilar el servidor TypeScript
npm run build
```

### **Paso 4: Verificar la compilación**

Asegúrate de que existe el archivo `dist/index.js`:

```bash
ls dist/index.js
```

### **Paso 5: Reiniciar Claude Desktop**

1. **Cierra completamente Claude Desktop**
2. **Vuelve a abrir Claude Desktop**
3. **Verifica que aparezca el servidor MCP conectado**

### **Paso 6: Probar la conexión**

En Claude Desktop, deberías poder:
- Ver las herramientas MCP disponibles
- Ejecutar comandos como "Obtener contactos de Track HS"
- Acceder a datos de reservas, propiedades, etc.

## 🔧 **Troubleshooting**

### **Problema: Claude no detecta el servidor**
**Solución:**
1. Verifica que el archivo `claude_desktop_config.json` esté en la ubicación correcta
2. Verifica que el archivo `dist/index.js` existe
3. Verifica que las variables de entorno están configuradas correctamente
4. Reinicia Claude Desktop

### **Problema: Error de autenticación**
**Solución:**
1. Verifica que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` son correctos
2. Verifica que `TRACKHS_API_URL` apunta a la URL correcta
3. Prueba las credenciales en la API de Track HS directamente

### **Problema: Herramientas no aparecen**
**Solución:**
1. Verifica que la compilación fue exitosa
2. Revisa los logs de Claude Desktop
3. Verifica que el servidor MCP se inicia correctamente

## 📊 **Verificación de Configuración**

### **1. Verificar archivo de configuración**
```bash
# Windows
type "%APPDATA%\Claude\claude_desktop_config.json"

# macOS/Linux
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### **2. Verificar compilación**
```bash
node dist/index.js --help
```

### **3. Probar servidor localmente**
```bash
# En una terminal
node dist/index.js

# Debería mostrar: "Track HS MCP Server iniciado correctamente"
```

## 🎯 **URLs de Configuración**

### **Para Claude Web (Custom Connectors):**
- **URL**: `https://trackhs-mcp-connector.vercel.app/api/mcp-sse-claude`
- **Nombre**: `Track HS MCP Connector`

### **Para Claude Desktop (Local):**
- **Comando**: `node dist/index.js`
- **Variables de entorno**: Configuradas en `claude_desktop_config.json`

## ✅ **Checklist de Configuración**

- [ ] Archivo `claude_desktop_config.json` creado
- [ ] Variables de entorno configuradas correctamente
- [ ] Servidor compilado (`npm run build`)
- [ ] Archivo `dist/index.js` existe
- [ ] Claude Desktop reiniciado
- [ ] Servidor MCP aparece en Claude Desktop
- [ ] Herramientas MCP funcionan correctamente

## 🆘 **Soporte**

Si tienes problemas:
1. Revisa los logs de Claude Desktop
2. Verifica la configuración paso a paso
3. Prueba el servidor localmente
4. Contacta soporte técnico

---

**¡Configuración completada!** 🎉
