# Guía de Despliegue en FastMCP Cloud

Esta guía te ayudará a desplegar correctamente el TrackHS MCP Connector en FastMCP Cloud.

## ✅ Correcciones Implementadas

### 1. Archivo `__main__.py` Creado
- ✅ Creado `src/trackhs_mcp/__main__.py` que FastMCP Cloud requiere
- ✅ Incluye manejo de errores y logging mejorado
- ✅ Validación de variables de entorno críticas

### 2. Configuración de Credenciales
- ✅ Eliminadas credenciales hardcodeadas
- ✅ Configuración segura desde variables de entorno
- ✅ Validación de credenciales requeridas

### 3. Pre-tests Automatizados
- ✅ Script `scripts/pretest.py` para validación pre-commit
- ✅ Scripts de pre-commit para Windows (PowerShell) y Linux (Bash)
- ✅ Validación de archivos, imports, dependencias y tests

### 4. Optimización de Build
- ✅ Archivo `.dockerignore` para optimizar el build
- ✅ Archivo `fastmcp.yaml` para configuración del servidor
- ✅ Dependencias optimizadas en `requirements.txt`

## 🚀 Pasos para Desplegar

### 1. Configurar Variables de Entorno en FastMCP Cloud

En el panel de FastMCP Cloud, configura estas variables de entorno:

```bash
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=tu_usuario_aqui
TRACKHS_PASSWORD=tu_password_aqui
TRACKHS_TIMEOUT=30
```

### 2. Ejecutar Pre-tests Antes del Commit

```bash
# Windows (PowerShell)
.\scripts\pre-commit.ps1

# Linux/Mac (Bash)
./scripts/pre-commit.sh

# O ejecutar directamente
python scripts/pretest.py
```

### 3. Hacer Commit y Push

```bash
git add .
git commit -m "fix: Preparar para despliegue en FastMCP Cloud"
git push origin main
```

### 4. Verificar Despliegue

1. Ve al panel de FastMCP Cloud
2. Verifica que el build sea exitoso
3. Revisa los logs del servidor
4. Prueba las herramientas MCP

## 🔧 Archivos Clave para FastMCP Cloud

### `src/trackhs_mcp/__main__.py`
- Punto de entrada principal requerido por FastMCP Cloud
- Manejo de errores y logging
- Validación de configuración

### `fastmcp.yaml`
- Configuración del servidor para FastMCP Cloud
- Variables de entorno requeridas
- Configuración de recursos

### `.dockerignore`
- Optimiza el build excluyendo archivos innecesarios
- Reduce el tamaño de la imagen Docker

### `scripts/pretest.py`
- Valida que todo esté listo para el despliegue
- Verifica archivos, imports, dependencias y tests

## 🐛 Solución de Problemas

### Error: "File not found: /app/src/trackhs_mcp/__main__.py"
- ✅ **Solucionado**: Se creó el archivo `__main__.py` en la ubicación correcta

### Error: "Invalid credentials"
- ✅ **Solucionado**: Se eliminaron las credenciales hardcodeadas
- ⚠️ **Acción requerida**: Configurar `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` en FastMCP Cloud

### Error: "Pre-flight check failed"
- ✅ **Solucionado**: Se mejoró el manejo de errores en `__main__.py`
- ✅ **Solucionado**: Se agregó validación de variables de entorno

## 📋 Checklist Pre-Despliegue

- [ ] Variables de entorno configuradas en FastMCP Cloud
- [ ] Pre-tests ejecutados y pasando
- [ ] Archivo `__main__.py` presente
- [ ] Credenciales no hardcodeadas
- [ ] Dependencias actualizadas en `requirements.txt`
- [ ] Tests con al menos 80% de éxito

## 🎯 Resultados Esperados

Después de implementar estas correcciones:

1. **Build exitoso** en FastMCP Cloud
2. **Servidor iniciando** correctamente
3. **Herramientas MCP** funcionando
4. **Logs limpios** sin errores de credenciales
5. **Pre-flight check** pasando

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs del servidor en FastMCP Cloud
2. Ejecuta `python scripts/pretest.py` localmente
3. Verifica que las variables de entorno estén configuradas
4. Asegúrate de que las credenciales de TrackHS sean válidas

---

**Nota**: Este despliegue está optimizado para FastMCP Cloud y sigue las mejores prácticas de desarrollo de software.
