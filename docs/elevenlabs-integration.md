# Integración con ElevenLabs

Esta guía explica cómo conectar el servidor MCP TrackHS con ElevenLabs para aprovechar las capacidades de audio IA.

## ¿Qué es ElevenLabs?

ElevenLabs es una plataforma de IA que proporciona servicios de conversión de texto a voz, clonación de voz y procesamiento de audio. Su servidor MCP permite que los agentes conversacionales accedan a estas capacidades.

## Configuración del Servidor MCP TrackHS

### 1. Desplegar en FastMCP Cloud

1. **Conectar repositorio** en FastMCP Cloud dashboard
2. **Configurar variables de entorno**:
   ```
   TRACKHS_API_URL=https://api.trackhs.com/api
   TRACKHS_USERNAME=tu_usuario
   TRACKHS_PASSWORD=tu_contraseña
   ```
3. **Hacer deploy**:
   ```bash
   git add .
   git commit -m "feat: HTTP transport for ElevenLabs"
   git push origin main
   ```
4. **Obtener URL del servidor**: `https://tu-servidor.fastmcp.cloud/mcp`

### 2. Verificar Funcionamiento

```bash
# Health check
curl https://tu-servidor.fastmcp.cloud/health

# Listar tools disponibles
curl -X POST https://tu-servidor.fastmcp.cloud/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**Nota**: FastMCP Cloud maneja automáticamente el transporte HTTP. No necesitas configurar transporte, host, puerto o CORS en el código Python.

## Configuración en ElevenLabs

### 1. Acceder a ElevenLabs

1. Ve a [ElevenLabs](https://elevenlabs.io)
2. Inicia sesión en tu cuenta
3. Navega a la sección de **Agents** o **MCP Servers**

### 2. Agregar Servidor MCP Personalizado

1. **Crear nuevo servidor MCP**:
   - Nombre: `TrackHS MCP Server`
   - Descripción: `Conector MCP para TrackHS API - Gestión de reservas y unidades`

2. **Configurar conexión**:
   - **URL**: `https://tu-servidor.fastmcp.cloud/mcp`
   - **Transport**: `Streamable HTTP`
   - **Headers**: (dejar vacío si no usas autenticación)

3. **Configurar permisos**:
   - **Aprobación de herramientas**: `Siempre Preguntar` (recomendado)
   - **Acceso a datos**: `Solo datos necesarios`

### 3. Probar Conexión

1. **Verificar conexión**: ElevenLabs debería mostrar "Conectado"
2. **Listar herramientas**: Deberías ver las 6 tools disponibles:
   - `search_reservations_v2`
   - `get_reservation_v2`
   - `get_folio`
   - `search_units`
   - `search_amenities`
   - `create_maintenance_work_order`

## Uso de las Herramientas

### Búsqueda de Reservas

```
Busca reservas para el huésped "John Smith" que lleguen entre el 1 y 15 de enero de 2024
```

El agente usará `search_reservations_v2` con los parámetros apropiados.

### Búsqueda de Unidades

```
Encuentra unidades con 2 habitaciones, 2 baños, que permitan mascotas y estén disponibles del 10 al 17 de febrero
```

El agente usará `search_units` con filtros de características.

### Gestión de Órdenes de Trabajo

```
Crea una orden de trabajo de mantenimiento para la unidad 123 por un problema de plomería
```

El agente usará `create_maintenance_work_order` con los detalles del problema.

## Configuración Avanzada

### Variables de Entorno Adicionales

```bash
# Configuración CORS para ElevenLabs
CORS_ORIGINS=https://elevenlabs.io,https://app.elevenlabs.io

# Configuración del servidor
HOST=0.0.0.0
PORT=8080
```

### Headers de Seguridad

Si necesitas autenticación adicional:

```bash
# En ElevenLabs, agregar headers:
Authorization: Bearer tu-token
X-API-Key: tu-api-key
```

## Troubleshooting

### "Cannot connect to MCP server"

**Causas comunes**:
- URL incorrecta (debe incluir `/mcp`)
- Servidor no desplegado
- CORS mal configurado

**Soluciones**:
1. Verificar que el servidor esté corriendo: `curl https://tu-servidor.fastmcp.cloud/health`
2. Verificar URL completa: `https://tu-servidor.fastmcp.cloud/mcp`
3. Revisar logs en FastMCP Cloud dashboard

### "Tools not available"

**Causas comunes**:
- Servidor no inicializado correctamente
- Variables de entorno faltantes
- Error en la API de TrackHS

**Soluciones**:
1. Verificar variables de entorno en FastMCP Cloud
2. Revisar logs del servidor
3. Probar conexión a TrackHS API

### "CORS error"

**Causas comunes**:
- Orígenes CORS no configurados
- Headers faltantes

**Soluciones**:
1. Agregar `https://elevenlabs.io` a `CORS_ORIGINS`
2. Verificar configuración en `fastmcp.yaml`
3. Reiniciar el servidor

## Mejores Prácticas

### Seguridad

1. **Usar HTTPS**: Siempre usar URLs HTTPS en producción
2. **Configurar CORS**: Limitar orígenes permitidos
3. **Monitorear acceso**: Revisar logs regularmente
4. **Rotar credenciales**: Cambiar contraseñas periódicamente

### Rendimiento

1. **Caché**: Usar caché para consultas frecuentes
2. **Rate limiting**: Configurar límites de requests
3. **Monitoreo**: Usar métricas de FastMCP Cloud
4. **Escalabilidad**: Configurar auto-scaling si es necesario

### Mantenimiento

1. **Actualizaciones**: Mantener dependencias actualizadas
2. **Backups**: Hacer backup de configuraciones
3. **Testing**: Probar integración regularmente
4. **Documentación**: Mantener documentación actualizada

## Recursos Adicionales

- [Documentación ElevenLabs MCP](https://elevenlabs.io/docs/conversational-ai/customization/mcp)
- [FastMCP Cloud Documentation](https://fastmcp.cloud/docs)
- [TrackHS API Documentation](https://api.trackhs.com/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io/specification)

## Soporte

Si tienes problemas con la integración:

1. **Revisar logs** en FastMCP Cloud dashboard
2. **Verificar configuración** de variables de entorno
3. **Probar conectividad** con curl
4. **Contactar soporte** de FastMCP Cloud o TrackHS
