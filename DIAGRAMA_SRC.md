# 📊 Diagrama de Arquitectura - TrackHS MCP Connector

## 🏗️ Arquitectura Hexagonal (Clean Architecture)

Este proyecto sigue los principios de **Clean Architecture** y está organizado en 3 capas principales:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         🌐 MUNDO EXTERIOR                            │
│                   (MCP Client / Claude Desktop)                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     📦 INFRASTRUCTURE LAYER                          │
│                    (Detalles de Implementación)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🔧 server.py ──► Punto de entrada FastMCP                          │
│                                                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐                │
│  │   📱 TOOLS           │  │   🔌 ADAPTERS        │                │
│  │                      │  │                      │                │
│  │  ├─ get_reservation  │  │  ├─ trackhs_api     │                │
│  │  ├─ search_units     │  │  │    _client.py    │                │
│  │  ├─ search_amenities │  │  │                  │                │
│  │  ├─ get_folio        │  │  └─ config.py      │                │
│  │  ├─ create_*_wo      │  │                      │                │
│  │  └─ registry.py      │  └──────────────────────┘                │
│  └──────────────────────┘                                            │
│                                                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐                │
│  │   📚 RESOURCES       │  │   🛠️ UTILS           │                │
│  │                      │  │                      │                │
│  │  ├─ documentation/   │  │  ├─ auth.py         │                │
│  │  ├─ examples/        │  │  ├─ validation_*    │                │
│  │  ├─ schemas/         │  │  ├─ error_handling  │                │
│  │  ├─ prompts/         │  │  ├─ logging.py      │                │
│  │  └─ references/      │  │  └─ pagination.py   │                │
│  └──────────────────────┘  └──────────────────────┘                │
│                                                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐                │
│  │   🚦 MIDDLEWARE      │  │   ✅ VALIDATION      │                │
│  │                      │  │                      │                │
│  │  ├─ error_handling   │  │  ├─ api_parameters  │                │
│  │  └─ logging          │  │  ├─ date_validators │                │
│  └──────────────────────┘  │  └─ enhanced_valid. │                │
│                             └──────────────────────┘                │
└─────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ Implementa Ports
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│                      💼 APPLICATION LAYER                            │
│                      (Casos de Uso / Lógica de Negocio)            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🔌 PORTS (Interfaces)                                               │
│  └─ api_client_port.py  ──► Interface para clientes API            │
│                                                                       │
│  🎯 USE CASES (Casos de Uso)                                        │
│  ├─ get_reservation.py          ──► Obtener reservación            │
│  ├─ search_reservations.py      ──► Buscar reservaciones           │
│  ├─ search_units.py              ──► Buscar unidades               │
│  ├─ search_amenities.py          ──► Buscar amenidades             │
│  ├─ get_folio.py                 ──► Obtener folio                 │
│  ├─ create_work_order.py         ──► Crear orden de mantenimiento  │
│  └─ create_housekeeping_wo.py    ──► Crear orden de limpieza       │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ Usa Entidades
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│                        🎯 DOMAIN LAYER                               │
│                    (Núcleo del Negocio - Sin Dependencias)          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📦 ENTITIES (Entidades de Dominio)                                 │
│  ├─ base.py                     ──► Clase base para entidades      │
│  ├─ reservations.py             ──► Modelo de Reservación          │
│  ├─ units.py                    ──► Modelo de Unidad               │
│  ├─ amenities.py                ──► Modelo de Amenidades           │
│  ├─ folios.py                   ──► Modelo de Folio                │
│  ├─ work_orders.py              ──► Modelo de Orden de Mant.       │
│  └─ housekeeping_work_orders.py ──► Modelo de Orden de Limpieza    │
│                                                                       │
│  💎 VALUE OBJECTS (Objetos de Valor)                                │
│  ├─ config.py                   ──► Configuración del sistema      │
│  └─ request.py                  ──► Objetos de petición            │
│                                                                       │
│  ⚠️ EXCEPTIONS (Excepciones de Dominio)                            │
│  └─ api_exceptions.py           ──► Excepciones personalizadas     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

```
1️⃣  MCP Client (Claude) envía petición
              ↓
2️⃣  server.py (FastMCP) recibe la solicitud
              ↓
3️⃣  Tool correspondiente procesa la petición
              ↓
4️⃣  Tool llama al Use Case de Application
              ↓
5️⃣  Use Case usa el Port (interface)
              ↓
6️⃣  Adapter (trackhs_api_client) implementa el Port
              ↓
7️⃣  Adapter realiza HTTP request a TrackHS API
              ↓
8️⃣  Respuesta se convierte en Entity (Domain)
              ↓
9️⃣  Entity se valida y procesa
              ↓
🔟  Respuesta vuelve al MCP Client
```

## 📋 Descripción Detallada de Capas

### 🎯 DOMAIN (Dominio)
**Propósito**: Contiene la lógica de negocio pura, sin dependencias externas.

- **Entities**: Modelos de datos del negocio
  - `Reservation`, `Unit`, `Amenity`, `Folio`, `WorkOrder`
- **Value Objects**: Objetos inmutables que representan conceptos
- **Exceptions**: Excepciones específicas del dominio

**Regla de oro**: Esta capa NO conoce nada sobre HTTP, bases de datos o frameworks.

### 💼 APPLICATION (Aplicación)
**Propósito**: Contiene los casos de uso y orquesta el flujo de la aplicación.

- **Use Cases**: Implementan la lógica de negocio específica
  - Cada use case representa una acción que un usuario puede realizar
- **Ports**: Interfaces que definen contratos para la infraestructura
  - Define QUÉ necesita, no CÓMO se implementa

**Regla de oro**: Depende solo del Domain, no de Infrastructure.

### 📦 INFRASTRUCTURE (Infraestructura)
**Propósito**: Implementa los detalles técnicos y se comunica con el mundo exterior.

#### Componentes principales:

1. **Tools**: Herramientas MCP expuestas a Claude
   - Cada tool mapea a un use case
   - Valida entrada y formatea salida

2. **Adapters**: Implementaciones concretas de los Ports
   - `trackhs_api_client.py`: Cliente HTTP para TrackHS API
   - `config.py`: Gestión de configuración

3. **Resources**: Recursos para documentación y validación
   - `documentation/`: Docs de API
   - `examples/`: Ejemplos de uso
   - `schemas/`: Esquemas de validación
   - `prompts/`: Prompts para el LLM
   - `references/`: Referencias de valores válidos

4. **Utils**: Utilidades transversales
   - Autenticación, validación, logging, manejo de errores

5. **Middleware**: Procesamiento intermedio de peticiones

6. **Validation**: Validadores específicos

## 🎨 Principios Aplicados

### ✅ SOLID Principles
- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Las implementaciones pueden sustituir interfaces
- **I**nterface Segregation: Interfaces pequeñas y específicas
- **D**ependency Inversion: Dependemos de abstracciones (ports), no de concretos

### 🏗️ Clean Architecture Benefits
1. **Independencia de Frameworks**: El negocio no depende de FastMCP
2. **Testeable**: Lógica de negocio fácil de testear sin HTTP
3. **Independencia de UI**: Puede funcionar con cualquier interfaz
4. **Independencia de Base de Datos**: No estamos acoplados a TrackHS
5. **Independencia de Agentes Externos**: La lógica de negocio es agnóstica

## 🔌 Ejemplo de Flujo: Buscar Unidades

```python
# 1. Cliente MCP llama a search_units tool
"search_units(bedrooms='2', pets_friendly='1')"
        ↓
# 2. Tool en infrastructure/tools/search_units.py
@mcp.tool()
def search_units(...):
    # Valida parámetros
    # Llama al use case
    result = search_units_use_case.execute(...)
        ↓
# 3. Use Case en application/use_cases/search_units.py
class SearchUnitsUseCase:
    def execute(self, params):
        # Usa el port
        response = self.api_client.search_units(params)
        # Convierte a Entity
        return [Unit(**data) for data in response]
        ↓
# 4. Adapter en infrastructure/adapters/trackhs_api_client.py
class TrackHSApiClient:
    def search_units(self, params):
        # Hace HTTP request
        response = requests.get(f"{base_url}/units", params=params)
        return response.json()
        ↓
# 5. Entity en domain/entities/units.py
@dataclass
class Unit:
    id: int
    name: str
    bedrooms: int
    # ... validación automática
```

## 📊 Estadísticas del Proyecto

```
Domain Layer:        14 archivos
Application Layer:   11 archivos  
Infrastructure:      59 archivos
─────────────────────────────────
Total:               84 archivos
```

## 🚀 Ventajas de Esta Arquitectura

1. **Mantenibilidad**: Cambios en la API no afectan el dominio
2. **Escalabilidad**: Fácil agregar nuevos use cases o adapters
3. **Testing**: Cada capa se puede testear independientemente
4. **Claridad**: La estructura refleja el negocio
5. **Flexibilidad**: Podemos cambiar FastMCP por otro framework sin afectar el core

---

**Nota**: Esta arquitectura permite que el proyecto sea robusto, testeable y fácil de mantener a largo plazo.

