# Testing Local - TrackHS MCP Connector

##  Guía de Testing Local

Esta guía te ayudará a probar el TrackHS MCP Connector localmente antes del deployment.

##  Prerrequisitos

### 1. Instalar Dependencias

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# O usar uv (recomendado)
uv pip install -r requirements.txt

# Instalar FastMCP
pip install fastmcp
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

##  Testing Automático

### Ejecutar Script de Testing

```bash
# Ejecutar tests automáticos
python test_local.py
```

Este script probará:
-  Conexión con Track HS API
-  Registro de herramientas MCP
-  Registro de resources MCP
-  Registro de prompts MCP

### Salida Esperada

```
 TrackHS MCP Connector - Testing Local
==================================================
 Probando conexión con Track HS API...
 Probando endpoint de salud...
 Conexión exitosa: {"status": "ok"}
 Probando endpoint de reservas...
 Reservas accesibles: 5 encontradas

 Probando herramientas MCP...
 Herramientas registradas exitosamente

 Probando resources MCP...
 Resources registrados exitosamente

 Probando prompts MCP...
 Prompts registrados exitosamente

==================================================
 RESUMEN DE TESTS
==================================================
 PASS Conexión API
 PASS Herramientas MCP
 PASS Resources MCP
 PASS Prompts MCP

 Resultado: 4/4 tests pasaron
 ¡Todos los tests pasaron! El servidor está listo.
```

##  Testing Manual

### 1. Ejecutar Servidor

```bash
# Modo desarrollo
fastmcp dev

# O ejecutar directamente
python -m src.trackhs_mcp.server
```

### 2. Usar MCP Inspector

```bash
# Instalar MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Ejecutar inspector
npx @modelcontextprotocol/inspector

# Conectar a: http://localhost:3000/mcp
```

### 3. Probar Herramientas

En MCP Inspector:

1. **Listar herramientas**:
   ```json
   {
     "method": "tools/list"
   }
   ```

2. **Ejecutar herramienta**:
   ```json
   {
     "method": "tools/call",
     "params": {
       "name": "get_reservation",
       "arguments": {
         "reservation_id": 12345
       }
     }
   }
   ```

3. **Listar resources**:
   ```json
   {
     "method": "resources/list"
   }
   ```

4. **Obtener resource**:
   ```json
   {
     "method": "resources/read",
     "params": {
       "uri": "trackhs://schema/reservations"
     }
   }
   ```

5. **Listar prompts**:
   ```json
   {
     "method": "prompts/list"
   }
   ```

6. **Obtener prompt**:
   ```json
   {
     "method": "prompts/get",
     "params": {
       "name": "check-today-reservations"
     }
   }
   ```

##  Troubleshooting

### Error: "Module not found"

```bash
# Verificar que estés en el directorio correcto
pwd
# Debe mostrar: /path/to/MCPtrackhsConnector

# Verificar que src/ existe
ls src/
```

### Error: "TRACKHS_USERNAME not set"

```bash
# Verificar archivo .env
cat .env

# Debe contener:
# TRACKHS_USERNAME=tu_usuario
# TRACKHS_PASSWORD=tu_contraseña
```

### Error: "Connection failed"

```bash
# Probar conectividad manual
curl -u $TRACKHS_USERNAME:$TRACKHS_PASSWORD $TRACKHS_API_URL/health
```

### Error: "FastMCP not found"

```bash
# Instalar FastMCP
pip install fastmcp

# Verificar instalación
fastmcp --version
```

##  Verificación de Funcionalidades

### 1. Herramientas (13 total)

- [ ] `get_reviews` - Obtener reseñas
- [ ] `get_reservation` - Obtener reserva
- [ ] `search_reservations` - Buscar reservas
- [ ] `get_units` - Listar unidades
- [ ] `get_unit` - Obtener unidad
- [ ] `get_folios_collection` - Obtener folios
- [ ] `get_contacts` - Listar contactos
- [ ] `get_ledger_accounts` - Listar cuentas
- [ ] `get_ledger_account` - Obtener cuenta
- [ ] `get_reservation_notes` - Obtener notas
- [ ] `get_nodes` - Listar nodos
- [ ] `get_node` - Obtener nodo
- [ ] `get_maintenance_work_orders` - Órdenes de trabajo

### 2. Resources (4 total)

- [ ] `trackhs://schema/reservations` - Esquema reservas
- [ ] `trackhs://schema/units` - Esquema unidades
- [ ] `trackhs://status/system` - Estado sistema
- [ ] `trackhs://docs/api` - Documentación API

### 3. Prompts (5 total)

- [ ] `check-today-reservations` - Revisar reservas hoy
- [ ] `unit-availability` - Disponibilidad unidades
- [ ] `guest-contact-info` - Info contacto huéspedes
- [ ] `maintenance-summary` - Resumen mantenimiento
- [ ] `financial-analysis` - Análisis financiero

##  Próximos Pasos

Una vez que todos los tests pasen:

1. **Commit y push** a GitHub
2. **Verificar deployment** automático
3. **Probar URL pública** generada
4. **Documentar** cualquier problema encontrado

##  Soporte

Si encuentras problemas:

1. **Revisar logs** del servidor
2. **Verificar configuración** de variables
3. **Probar conectividad** manual
4. **Crear issue** en GitHub

---

**Testing Local** - Asegurando calidad antes del deployment 
