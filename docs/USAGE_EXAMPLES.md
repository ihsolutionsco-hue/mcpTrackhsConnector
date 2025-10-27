# 📖 Ejemplos de Uso - TrackHS MCP Server

## 🎯 Descripción General

Esta guía proporciona ejemplos prácticos de cómo usar el TrackHS MCP Server en diferentes escenarios. Incluye casos de uso comunes, patrones de integración y mejores prácticas.

## 📋 Tabla de Contenidos

1. [Configuración Inicial](#configuración-inicial)
2. [Casos de Uso Comunes](#casos-de-uso-comunes)
3. [Patrones de Integración](#patrones-de-integración)
4. [Ejemplos Avanzados](#ejemplos-avanzados)
5. [Mejores Prácticas](#mejores-prácticas)
6. [Troubleshooting](#troubleshooting)

## 🚀 Configuración Inicial

### Instalación y Configuración Básica

```python
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_contraseña"
export TRACKHS_API_URL="https://api.trackhs.com"

# 3. Verificar configuración
python -c "from src.trackhs_mcp.server import mcp; print('✅ Servidor configurado correctamente')"
```

### Configuración con Archivo .env

```bash
# .env
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
TRACKHS_API_URL=https://api.trackhs.com
CACHE_TTL=300
RATE_LIMIT_RPM=60
LOG_LEVEL=INFO
```

```python
# Cargar configuración desde .env
from dotenv import load_dotenv
load_dotenv()

from src.trackhs_mcp.server import mcp
```

## 🏠 Casos de Uso Comunes

### 1. Gestión de Reservas

#### Buscar Reservas por Fecha

```python
import asyncio
from src.trackhs_mcp.server import mcp

async def buscar_reservas_fecha():
    """Buscar reservas para una fecha específica"""
    try:
        # Buscar reservas del 15 de enero de 2024
        reservas = await mcp.call_tool(
            "search_reservations",
            {
                "arrival_start": "2024-01-15",
                "arrival_end": "2024-01-15",
                "status": "confirmed",
                "size": 50
            }
        )
        
        print(f"Encontradas {reservas['total_items']} reservas")
        for reserva in reservas['_embedded']['reservations']:
            print(f"- {reserva['confirmation_number']}: {reserva['guest']['name']}")
            
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(buscar_reservas_fecha())
```

#### Obtener Detalles de Reserva

```python
async def obtener_detalles_reserva(reservation_id):
    """Obtener detalles completos de una reserva"""
    try:
        reserva = await mcp.call_tool(
            "get_reservation",
            {"reservation_id": reservation_id}
        )
        
        print(f"Reserva: {reserva['confirmation_number']}")
        print(f"Huésped: {reserva['guest']['name']}")
        print(f"Email: {reserva['guest']['email']}")
        print(f"Teléfono: {reserva['guest']['phone']}")
        print(f"Llegada: {reserva['arrival_date']}")
        print(f"Salida: {reserva['departure_date']}")
        print(f"Estado: {reserva['status']}")
        print(f"Unidad: {reserva['unit']['name']}")
        print(f"Balance: ${reserva['balance']}")
        
        return reserva
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejecutar
asyncio.run(obtener_detalles_reserva(12345))
```

#### Buscar Reservas por Huésped

```python
async def buscar_reservas_huesped(email):
    """Buscar reservas por email del huésped"""
    try:
        reservas = await mcp.call_tool(
            "search_reservations",
            {
                "search": email,
                "size": 100
            }
        )
        
        print(f"Reservas para {email}:")
        for reserva in reservas['_embedded']['reservations']:
            print(f"- {reserva['confirmation_number']}: {reserva['arrival_date']} a {reserva['departure_date']}")
            
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(buscar_reservas_huesped("john@example.com"))
```

### 2. Gestión de Unidades

#### Buscar Unidades por Capacidad

```python
async def buscar_unidades_capacidad(bedrooms, bathrooms):
    """Buscar unidades por número de dormitorios y baños"""
    try:
        unidades = await mcp.call_tool(
            "search_units",
            {
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "is_active": 1,
                "is_bookable": 1,
                "size": 25
            }
        )
        
        print(f"Unidades con {bedrooms} dormitorios y {bathrooms} baños:")
        for unidad in unidades['_embedded']['units']:
            print(f"- {unidad['name']} ({unidad['code']})")
            print(f"  Capacidad: {unidad['max_occupancy']} personas")
            print(f"  Área: {unidad['area']} m²")
            print(f"  Dirección: {unidad['address']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(buscar_unidades_capacidad(2, 1))
```

#### Buscar Amenidades

```python
async def buscar_amenidades():
    """Buscar todas las amenidades disponibles"""
    try:
        amenidades = await mcp.call_tool(
            "search_amenities",
            {
                "size": 100
            }
        )
        
        print("Amenidades disponibles:")
        for amenidad in amenidades['_embedded']['amenities']:
            print(f"- {amenidad['name']} ({amenidad['group']})")
            if amenidad['description']:
                print(f"  {amenidad['description']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(buscar_amenidades())
```

### 3. Gestión Financiera

#### Obtener Folio de Reserva

```python
async def obtener_folio_reserva(reservation_id):
    """Obtener folio financiero de una reserva"""
    try:
        folio = await mcp.call_tool(
            "get_folio",
            {"reservation_id": reservation_id}
        )
        
        print(f"Folio para reserva {reservation_id}:")
        print(f"Balance: ${folio['balance']}")
        print(f"Cargos: {len(folio['charges'])}")
        print(f"Pagos: {len(folio['payments'])}")
        print(f"Impuestos: {len(folio['taxes'])}")
        
        # Mostrar cargos
        if folio['charges']:
            print("\nCargos:")
            for cargo in folio['charges']:
                print(f"- {cargo['description']}: ${cargo['amount']}")
        
        # Mostrar pagos
        if folio['payments']:
            print("\nPagos:")
            for pago in folio['payments']:
                print(f"- {pago['type']}: ${pago['amount']} ({pago['status']})")
                
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(obtener_folio_reserva(12345))
```

### 4. Gestión de Mantenimiento

#### Crear Orden de Mantenimiento

```python
async def crear_orden_mantenimiento(unit_id, problema, descripcion, prioridad=3):
    """Crear orden de trabajo de mantenimiento"""
    try:
        orden = await mcp.call_tool(
            "create_maintenance_work_order",
            {
                "unit_id": unit_id,
                "summary": problema,
                "description": descripcion,
                "priority": prioridad,
                "estimated_cost": 100.0,
                "estimated_time": 120
            }
        )
        
        print(f"Orden de mantenimiento creada:")
        print(f"ID: {orden['id']}")
        print(f"Unidad: {unit_id}")
        print(f"Problema: {problema}")
        print(f"Prioridad: {prioridad}")
        print(f"Estado: {orden['status']}")
        
        return orden
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejecutar
asyncio.run(crear_orden_mantenimiento(
    unit_id=100,
    problema="Fuga en grifo",
    descripcion="Grifo del baño principal gotea constantemente",
    prioridad=5
))
```

#### Crear Orden de Housekeeping

```python
async def crear_orden_housekeeping(unit_id, fecha, tipo_limpieza=1):
    """Crear orden de trabajo de housekeeping"""
    try:
        orden = await mcp.call_tool(
            "create_housekeeping_work_order",
            {
                "unit_id": unit_id,
                "scheduled_at": fecha,
                "is_inspection": False,
                "clean_type_id": tipo_limpieza,
                "comments": "Limpieza post-reserva",
                "cost": 50.0
            }
        )
        
        print(f"Orden de housekeeping creada:")
        print(f"ID: {orden['id']}")
        print(f"Unidad: {unit_id}")
        print(f"Fecha: {fecha}")
        print(f"Estado: {orden['status']}")
        
        return orden
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejecutar
asyncio.run(crear_orden_housekeeping(
    unit_id=100,
    fecha="2024-01-15",
    tipo_limpieza=1
))
```

## 🔗 Patrones de Integración

### 1. Integración con Claude Desktop

#### Configuración en Claude Desktop

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "trackhs_mcp"],
      "env": {
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

#### Uso en Claude Desktop

```
Claude, por favor busca las reservas confirmadas para mañana y crea órdenes de housekeeping para las unidades que tienen checkout.
```

### 2. Integración con ElevenLabs

#### Configuración en ElevenLabs

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "trackhs_mcp"],
      "env": {
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña",
        "CACHE_TTL": "600"
      }
    }
  }
}
```

### 3. Integración con Aplicaciones Personalizadas

#### Cliente MCP Personalizado

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def cliente_personalizado():
    """Cliente MCP personalizado para TrackHS"""
    async with stdio_client(StdioServerParameters(
        command="python",
        args=["-m", "trackhs_mcp"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar
            await session.initialize()
            
            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("Herramientas disponibles:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Usar herramienta
            result = await session.call_tool(
                "search_reservations",
                {
                    "arrival_start": "2024-01-15",
                    "arrival_end": "2024-01-15",
                    "status": "confirmed"
                }
            )
            
            print(f"Resultado: {result.content}")
            
            # Cerrar sesión
            await session.close()

# Ejecutar
asyncio.run(cliente_personalizado())
```

## 🚀 Ejemplos Avanzados

### 1. Dashboard de Reservas

```python
import asyncio
from datetime import datetime, timedelta
from src.trackhs_mcp.server import mcp

async def dashboard_reservas():
    """Dashboard completo de reservas"""
    try:
        # Obtener fecha de hoy
        hoy = datetime.now().strftime("%Y-%m-%d")
        ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Buscar reservas de ayer, hoy y mañana
        reservas_ayer = await mcp.call_tool("search_reservations", {
            "arrival_start": ayer,
            "arrival_end": ayer,
            "size": 100
        })
        
        reservas_hoy = await mcp.call_tool("search_reservations", {
            "arrival_start": hoy,
            "arrival_end": hoy,
            "size": 100
        })
        
        reservas_mañana = await mcp.call_tool("search_reservations", {
            "arrival_start": mañana,
            "arrival_end": mañana,
            "size": 100
        })
        
        # Mostrar dashboard
        print("📊 DASHBOARD DE RESERVAS")
        print("=" * 50)
        print(f"📅 Ayer ({ayer}): {reservas_ayer['total_items']} reservas")
        print(f"📅 Hoy ({hoy}): {reservas_hoy['total_items']} reservas")
        print(f"📅 Mañana ({mañana}): {reservas_mañana['total_items']} reservas")
        
        # Mostrar reservas de hoy
        if reservas_hoy['total_items'] > 0:
            print(f"\n🏠 RESERVAS DE HOY ({hoy}):")
            for reserva in reservas_hoy['_embedded']['reservations']:
                print(f"- {reserva['confirmation_number']}: {reserva['guest']['name']}")
                print(f"  Unidad: {reserva['unit']['name']}")
                print(f"  Estado: {reserva['status']}")
                print()
        
        # Mostrar reservas de mañana
        if reservas_mañana['total_items'] > 0:
            print(f"\n🏠 RESERVAS DE MAÑANA ({mañana}):")
            for reserva in reservas_mañana['_embedded']['reservations']:
                print(f"- {reserva['confirmation_number']}: {reserva['guest']['name']}")
                print(f"  Unidad: {reserva['unit']['name']}")
                print(f"  Estado: {reserva['status']}")
                print()
                
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(dashboard_reservas())
```

### 2. Automatización de Checkout

```python
async def automatizar_checkout():
    """Automatizar proceso de checkout"""
    try:
        # Buscar reservas que hacen checkout hoy
        hoy = datetime.now().strftime("%Y-%m-%d")
        reservas_checkout = await mcp.call_tool("search_reservations", {
            "departure_start": hoy,
            "departure_end": hoy,
            "status": "confirmed",
            "size": 100
        })
        
        print(f"🔄 AUTOMATIZACIÓN DE CHECKOUT - {hoy}")
        print(f"Reservas con checkout: {reservas_checkout['total_items']}")
        
        for reserva in reservas_checkout['_embedded']['reservations']:
            unit_id = reserva['unit']['id']
            confirmation_number = reserva['confirmation_number']
            
            print(f"\n📋 Procesando checkout: {confirmation_number}")
            
            # Crear orden de housekeeping
            orden_limpieza = await mcp.call_tool("create_housekeeping_work_order", {
                "unit_id": unit_id,
                "scheduled_at": hoy,
                "is_inspection": False,
                "clean_type_id": 1,
                "comments": f"Limpieza post-checkout - {confirmation_number}"
            })
            
            print(f"✅ Orden de limpieza creada: {orden_limpieza['id']}")
            
            # Crear orden de inspección
            orden_inspeccion = await mcp.call_tool("create_housekeeping_work_order", {
                "unit_id": unit_id,
                "scheduled_at": hoy,
                "is_inspection": True,
                "comments": f"Inspección post-checkout - {confirmation_number}"
            })
            
            print(f"✅ Orden de inspección creada: {orden_inspeccion['id']}")
            
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(automatizar_checkout())
```

### 3. Reporte de Ingresos

```python
async def reporte_ingresos(fecha_inicio, fecha_fin):
    """Generar reporte de ingresos para un período"""
    try:
        # Buscar reservas en el período
        reservas = await mcp.call_tool("search_reservations", {
            "arrival_start": fecha_inicio,
            "arrival_end": fecha_fin,
            "status": "confirmed",
            "size": 1000
        })
        
        print(f"💰 REPORTE DE INGRESOS")
        print(f"Período: {fecha_inicio} a {fecha_fin}")
        print("=" * 50)
        
        total_ingresos = 0
        reservas_procesadas = 0
        
        for reserva in reservas['_embedded']['reservations']:
            try:
                # Obtener folio de cada reserva
                folio = await mcp.call_tool("get_folio", {
                    "reservation_id": reserva['id']
                })
                
                balance = folio.get('balance', 0)
                total_ingresos += balance
                reservas_procesadas += 1
                
                print(f"Reserva {reserva['confirmation_number']}: ${balance}")
                
            except Exception as e:
                print(f"Error procesando reserva {reserva['id']}: {e}")
        
        print(f"\n📊 RESUMEN:")
        print(f"Reservas procesadas: {reservas_procesadas}")
        print(f"Total de ingresos: ${total_ingresos:,.2f}")
        print(f"Ingreso promedio por reserva: ${total_ingresos/reservas_procesadas:,.2f}")
        
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(reporte_ingresos("2024-01-01", "2024-01-31"))
```

## 🏆 Mejores Prácticas

### 1. Manejo de Errores

```python
async def manejo_errores_ejemplo():
    """Ejemplo de manejo robusto de errores"""
    try:
        # Intentar operación
        resultado = await mcp.call_tool("search_reservations", {
            "arrival_start": "2024-01-15",
            "size": 10
        })
        
        return resultado
        
    except AuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        # Reintentar con nuevas credenciales
        return None
        
    except RateLimitError as e:
        print(f"⏳ Rate limit excedido: {e}")
        # Esperar y reintentar
        await asyncio.sleep(60)
        return await manejo_errores_ejemplo()
        
    except APIError as e:
        print(f"🔌 Error de API: {e}")
        # Loggear y continuar
        return None
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        # Loggear y re-lanzar
        raise
```

### 2. Cache Inteligente

```python
from src.trackhs_mcp.cache import get_cache

async def uso_cache_inteligente():
    """Ejemplo de uso de cache inteligente"""
    cache = get_cache()
    
    # Verificar cache primero
    cache_key = "reservations:2024-01-15:confirmed"
    cached_result = cache.get(cache_key)
    
    if cached_result:
        print("📦 Datos obtenidos del cache")
        return cached_result
    
    # Si no está en cache, obtener de API
    print("🌐 Obteniendo datos de API")
    resultado = await mcp.call_tool("search_reservations", {
        "arrival_start": "2024-01-15",
        "status": "confirmed",
        "size": 50
    })
    
    # Guardar en cache
    cache.set(cache_key, resultado, ttl=300)  # 5 minutos
    print("💾 Datos guardados en cache")
    
    return resultado
```

### 3. Paginación Eficiente

```python
async def paginacion_eficiente():
    """Ejemplo de paginación eficiente"""
    todas_reservas = []
    page = 1
    size = 50
    
    while True:
        try:
            # Obtener página
            resultado = await mcp.call_tool("search_reservations", {
                "page": page,
                "size": size,
                "status": "confirmed"
            })
            
            reservas = resultado['_embedded']['reservations']
            todas_reservas.extend(reservas)
            
            print(f"📄 Página {page}: {len(reservas)} reservas")
            
            # Verificar si hay más páginas
            if len(reservas) < size:
                break
                
            page += 1
            
            # Pequeña pausa para no sobrecargar la API
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"Error en página {page}: {e}")
            break
    
    print(f"📊 Total de reservas obtenidas: {len(todas_reservas)}")
    return todas_reservas
```

### 4. Monitoreo y Métricas

```python
from src.trackhs_mcp.metrics import get_metrics

async def monitoreo_ejemplo():
    """Ejemplo de monitoreo y métricas"""
    metrics = get_metrics()
    
    # Registrar métricas de request
    start_time = time.time()
    
    try:
        resultado = await mcp.call_tool("search_reservations", {
            "arrival_start": "2024-01-15",
            "size": 10
        })
        
        # Registrar éxito
        duration = time.time() - start_time
        metrics.record_request("GET", duration, 200)
        metrics.record_mcp_tool_call("search_reservations", duration, True)
        
        print(f"✅ Request exitoso en {duration:.2f}s")
        
    except Exception as e:
        # Registrar error
        duration = time.time() - start_time
        metrics.record_request("GET", duration, 500)
        metrics.record_mcp_tool_call("search_reservations", duration, False)
        
        print(f"❌ Request falló en {duration:.2f}s: {e}")
    
    # Mostrar métricas actuales
    print(f"📊 Métricas actuales:")
    print(f"Total requests: {metrics.metrics['requests_total']['value']}")
    print(f"Requests exitosos: {metrics.metrics['successful_requests']['value']}")
    print(f"Requests fallidos: {metrics.metrics['failed_requests']['value']}")
```

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión

```python
async def verificar_conectividad():
    """Verificar conectividad con TrackHS API"""
    try:
        # Probar con endpoint simple
        resultado = await mcp.call_tool("search_amenities", {
            "size": 1
        })
        
        print("✅ Conectividad OK")
        return True
        
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False
```

#### 2. Verificar Configuración

```python
def verificar_configuracion():
    """Verificar configuración del servidor"""
    import os
    
    print("🔍 Verificando configuración...")
    
    # Verificar variables de entorno
    required_vars = ['TRACKHS_USERNAME', 'TRACKHS_PASSWORD']
    for var in required_vars:
        if not os.getenv(var):
            print(f"❌ Variable {var} no configurada")
        else:
            print(f"✅ Variable {var} configurada")
    
    # Verificar archivo de configuración
    config_file = "fastmcp.json"
    if os.path.exists(config_file):
        print(f"✅ Archivo {config_file} encontrado")
    else:
        print(f"❌ Archivo {config_file} no encontrado")
```

#### 3. Limpiar Cache

```python
def limpiar_cache():
    """Limpiar cache del servidor"""
    from src.trackhs_mcp.cache import get_cache
    
    cache = get_cache()
    cache.clear()
    print("🧹 Cache limpiado")
```

## 📚 Referencias Adicionales

- [Documentación FastMCP](https://gofastmcp.com/)
- [Protocolo MCP](https://modelcontextprotocol.io/)
- [Documentación TrackHS API](https://docs.trackhs.com/)
- [Ejemplos de Integración](examples/)

---

*Última actualización: 2024-01-15*
