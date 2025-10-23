# 🎨 DIAGRAMA DEL PROYECTO
## TrackHS MCP Connector

```
                                    CLIENTES MCP
                          ┌──────────────────────────────┐
                          │  Claude.ai   │  ElevenLabs   │
                          └──────────────┬───────────────┘
                                         │
                                    HTTP/MCP Protocol
                                         │
                                         ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                    FASTMCP SERVER                             ║
        ║                   (Entry Point: __main__.py)                  ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║  Middleware:  [Logging] → [Error Handling] → [Schema Hook]   ║
        ╚═══════════════════════════════════════════════════════════════╝
                                         │
                ┌────────────────────────┼────────────────────────┐
                │                        │                        │
                ▼                        ▼                        ▼
        ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
        │   MCP TOOLS   │       │  MCP RESOURCES│       │  MCP PROMPTS  │
        │   (6 tools)   │       │  (16 resources)│       │  (3 prompts)  │
        └───────┬───────┘       └───────────────┘       └───────────────┘
                │
                │ Tool Invocation
                │
                ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                    CAPA DE APLICACIÓN                         ║
        ║                      (Use Cases)                              ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║                                                               ║
        ║  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ ║
        ║  │ SearchReservs   │  │ SearchUnits     │  │ CreateWork   │ ║
        ║  │                 │  │                 │  │ Order        │ ║
        ║  └─────────────────┘  └─────────────────┘  └──────────────┘ ║
        ║                                                               ║
        ║  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ ║
        ║  │ GetReservation  │  │ SearchAmenities │  │ GetFolio     │ ║
        ║  │                 │  │                 │  │              │ ║
        ║  └─────────────────┘  └─────────────────┘  └──────────────┘ ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
                                         │
                                         │ Uses Port Interface
                                         │
                                         ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                  CAPA DE INFRAESTRUCTURA                      ║
        ║                     (Adapters & Utils)                        ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║                                                               ║
        ║  ┌──────────────────────────────────────────────────────┐    ║
        ║  │         TrackHSApiClient (HTTP Client)               │    ║
        ║  │  • Authentication  • Request Building                │    ║
        ║  │  • Error Handling  • Response Processing             │    ║
        ║  └──────────────────────────────────────────────────────┘    ║
        ║                                                               ║
        ║  ┌──────────────────────────────────────────────────────┐    ║
        ║  │                   Utilities                          │    ║
        ║  │  • Validation      • Type Normalization              │    ║
        ║  │  • Date Parsing    • Pagination                      │    ║
        ║  │  • Error Transform • User Messages                   │    ║
        ║  └──────────────────────────────────────────────────────┘    ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
                                         │
                                         │ HTTP Requests
                                         │
                                         ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                     TRACK HS API                              ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║  • V2 API (Reservations, Folios)                             ║
        ║  • Channel API (Units, Amenities)                            ║
        ║  • Work Orders API (Maintenance, Housekeeping)               ║
        ╚═══════════════════════════════════════════════════════════════╝
                                         │
                                         │
                                         ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                      CAPA DE DOMINIO                          ║
        ║                  (Business Logic & Entities)                  ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║                                                               ║
        ║  Entities:                                                    ║
        ║  ┌─────────────┐ ┌──────┐ ┌──────┐ ┌─────────┐ ┌─────────┐  ║
        ║  │ Reservation │ │ Unit │ │Folio │ │Amenity  │ │WorkOrder│  ║
        ║  └─────────────┘ └──────┘ └──────┘ └─────────┘ └─────────┘  ║
        ║                                                               ║
        ║  Value Objects:                   Exceptions:                ║
        ║  ┌────────┐ ┌─────────┐          ┌──────────────────┐       ║
        ║  │ Config │ │ Request │          │ ApiException     │       ║
        ║  └────────┘ └─────────┘          │ ValidationError  │       ║
        ║                                   │ AuthError        │       ║
        ║                                   └──────────────────┘       ║
        ╚═══════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════

                         ESTRUCTURA DE CARPETAS

MCPtrackhsConnector/
│
├── src/trackhs_mcp/              ◄── 85 archivos Python
│   ├── domain/                   ◄── Entidades y lógica de negocio
│   │   ├── entities/             (7 archivos)
│   │   ├── value_objects/        (2 archivos)
│   │   └── exceptions/           (1 archivo)
│   │
│   ├── application/              ◄── Casos de uso
│   │   ├── ports/                (1 interface)
│   │   └── use_cases/            (7 casos de uso)
│   │
│   └── infrastructure/           ◄── Adaptadores e implementación
│       ├── adapters/             (2 archivos: config, api_client)
│       ├── mcp/                  (11 archivos: tools + server)
│       │   └── resources/        (16 recursos MCP)
│       ├── middleware/           (2 archivos: logging, errors)
│       ├── utils/                (10 utilidades)
│       └── validation/           (3 validadores)
│
├── tests/                        ◄── 29 archivos de tests
│   ├── critical/                 (9 tests críticos)
│   └── smoke/                    (4 tests rápidos)
│
├── docs/                         ◄── 1219 archivos de documentación
├── scripts/                      ◄── 62 scripts de desarrollo
├── examples/                     ◄── Ejemplos de uso
└── Configuration Files           ◄── pyproject.toml, requirements.txt


═══════════════════════════════════════════════════════════════════════

                         FLUJO DE UNA PETICIÓN

    1. Cliente envía petición MCP
              ↓
    2. FastMCP Server recibe
              ↓
    3. Middleware procesa (logging, validación)
              ↓
    4. MCP Tool identifica caso de uso
              ↓
    5. Use Case ejecuta lógica de negocio
              ↓
    6. ApiClient hace HTTP request a Track HS API
              ↓
    7. Track HS API responde
              ↓
    8. Response procesada y transformada
              ↓
    9. Entidades de dominio creadas
              ↓
   10. Resultado enviado al cliente


═══════════════════════════════════════════════════════════════════════

                      COMPONENTES PRINCIPALES

┌─────────────────────────────────────────────────────────────────────┐
│  6 MCP TOOLS                                                        │
├─────────────────────────────────────────────────────────────────────┤
│  1. search_reservations      →  Búsqueda avanzada (35+ filtros)    │
│  2. get_reservation           →  Detalles de reserva               │
│  3. get_folio                 →  Detalles de folio                 │
│  4. search_units              →  Búsqueda de unidades (35+ filtros)│
│  5. search_amenities          →  Búsqueda de amenidades            │
│  6. create_maintenance_work_order → Crear orden de trabajo         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  16 MCP RESOURCES                                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Schemas (6):        Esquemas de datos completos                   │
│  Documentation (4):  Docs esenciales de APIs                       │
│  Examples (4):       Ejemplos de uso                               │
│  References (2):     Valores válidos y formatos                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  3 MCP PROMPTS                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  1. search-reservations-by-dates     → Búsqueda por fechas        │
│  2. search-reservations-by-guest     → Búsqueda por huésped       │
│  3. search-reservations-advanced     → Búsqueda avanzada          │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════

                         TESTING & QUALITY

    Tests Críticos: 27/27 ✅
    Tests Totales:  299+ tests
    Cobertura:      95%+
    
    ┌─────────────────────┐
    │  Pre-commit Hooks   │
    ├─────────────────────┤
    │  • Black            │
    │  • Isort            │
    │  • Flake8           │
    │  • Pytest           │
    │  • YAML validation  │
    └─────────────────────┘
    
    Tiempo: 20-40s


═══════════════════════════════════════════════════════════════════════

                    DEPENDENCIAS PRINCIPALES

    Runtime:
    ├── fastmcp >= 2.8.0         (Framework MCP)
    ├── httpx >= 0.24.0          (HTTP Client)
    ├── pydantic >= 2.0.0        (Validation)
    └── python-dotenv >= 1.0.0   (Environment)

    Development:
    ├── pytest                    (Testing)
    ├── black                     (Formatting)
    ├── flake8                    (Linting)
    └── mypy                      (Type Checking)


═══════════════════════════════════════════════════════════════════════

                         DEPLOYMENT

    Local Dev → Git Commit → GitHub Push → FastMCP Cloud → Production
        ↓           ↓             ↓              ↓            ↓
    Hot Reload  Pre-commit   GitHub Actions  Auto Deploy   HTTP Server
                  Hooks         (CI/CD)


═══════════════════════════════════════════════════════════════════════

                    MÉTRICAS DEL PROYECTO

    📊 Código:           85 archivos Python | ~15,000 LOC
    🧪 Tests:            299+ tests | 27/27 críticos ✅
    📚 Documentación:    1,200+ archivos
    🎯 Cobertura:        95%+
    ⚡ Performance:      < 2s startup | < 500ms API response
    ✅ Estado:           Producción Ready


═══════════════════════════════════════════════════════════════════════
```

