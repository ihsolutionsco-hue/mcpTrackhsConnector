/**
 * Servidor MCP moderno para Track HS usando McpServer high-level API
 * Implementa Streamable HTTP transport para servidores remotos
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { z } from 'zod';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

import { TrackHSApiClient } from './core/api-client.js';
import { BaseTrackHSTool } from './core/base-tool.js';
import { GetReviewsTool } from './tools/get-reviews.js';
import { GetReservationTool } from './tools/get-reservation.js';
import { SearchReservationsTool } from './tools/search-reservations.js';
import { GetUnitsTool } from './tools/get-units.js';
import { GetUnitTool } from './tools/get-unit.js';
import { GetFoliosCollectionTool } from './tools/get-folios-collection.js';
import { GetContactsTool } from './tools/get-contacts.js';
import { GetLedgerAccountsTool } from './tools/get-ledger-accounts.js';
import { GetLedgerAccountTool } from './tools/get-ledger-account.js';
import { GetReservationNotesTool } from './tools/get-reservation-notes.js';
import { GetNodesTool } from './tools/get-nodes.js';
import { GetNodeTool } from './tools/get-node.js';
import { GetMaintenanceWorkOrdersTool } from './tools/get-maintenance-work-orders.js';

export class TrackHSMCPServer {
  private server: Server;
  private apiClient: TrackHSApiClient;
  public tools: BaseTrackHSTool[];

  constructor() {
    // Validar variables de entorno
    this.validateEnvironment();

    // Configuración desde variables de entorno
    this.apiClient = new TrackHSApiClient({
      baseUrl: process.env.TRACKHS_API_URL!,
      username: process.env.TRACKHS_USERNAME!,
      password: process.env.TRACKHS_PASSWORD!
    });

    // Registrar herramientas
    this.tools = [
      new GetReviewsTool(this.apiClient),
      new GetReservationTool(this.apiClient),
      new SearchReservationsTool(this.apiClient),
      new GetUnitsTool(this.apiClient),
      new GetUnitTool(this.apiClient),
      new GetFoliosCollectionTool(this.apiClient),
      new GetContactsTool(this.apiClient),
      new GetLedgerAccountsTool(this.apiClient),
      new GetLedgerAccountTool(this.apiClient),
      new GetReservationNotesTool(this.apiClient),
      new GetNodesTool(this.apiClient),
      new GetNodeTool(this.apiClient),
      new GetMaintenanceWorkOrdersTool(this.apiClient)
    ];

    // Configurar servidor MCP con low-level API
    this.server = new Server({
      name: 'trackhs-mcp-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {},
        resources: {},
        prompts: {}
      }
    });

    this.setupHandlers();
  }

  /**
   * Valida que las variables de entorno estén configuradas
   */
  private validateEnvironment(): void {
    const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    
    for (const envVar of requiredEnvVars) {
      if (!process.env[envVar]) {
        throw new Error(`Variable de entorno requerida no configurada: ${envVar}`);
      }
    }

    // Validar formato de URL
    try {
      new URL(process.env.TRACKHS_API_URL!);
    } catch {
      throw new Error('TRACKHS_API_URL debe ser una URL válida');
    }
  }

  /**
   * Configura todos los manejadores del servidor MCP
   */
  private setupHandlers(): void {
    // Listar herramientas disponibles
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: this.tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema
        }))
      };
    });

    // Ejecutar herramientas
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      const tool = this.tools.find(t => t.name === name);
      if (!tool) {
        throw new Error(`Herramienta desconocida: ${name}`);
      }

      try {
        const result = await tool.execute(args || {});
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
        throw new Error(`Error en ejecución de herramienta: ${errorMessage}`);
      }
    });

    // Listar resources disponibles
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: 'trackhs://schema/reservations',
            name: 'reservations-schema',
            title: 'Esquema de Reservas',
            description: 'Esquema de datos para reservas en TrackHS',
            mimeType: 'application/json'
          },
          {
            uri: 'trackhs://schema/units',
            name: 'units-schema',
            title: 'Esquema de Unidades',
            description: 'Esquema de datos para unidades en TrackHS',
            mimeType: 'application/json'
          },
          {
            uri: 'trackhs://status/system',
            name: 'system-status',
            title: 'Estado del Sistema',
            description: 'Estado actual del sistema TrackHS y configuración',
            mimeType: 'application/json'
          },
          {
            uri: 'trackhs://docs/api',
            name: 'api-docs',
            title: 'Documentación de la API',
            description: 'Documentación de la API de TrackHS',
            mimeType: 'text/markdown'
          }
        ]
      };
    });

    // Leer resources
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      switch (uri) {
        case 'trackhs://schema/reservations':
          return {
            contents: [
              {
                uri,
                text: JSON.stringify({
                  schema: {
                    id: 'string',
                    guestName: 'string',
                    checkIn: 'date',
                    checkOut: 'date',
                    status: 'enum[confirmed, pending, cancelled]',
                    totalAmount: 'number',
                    unitId: 'string',
                    nodeId: 'string'
                  },
                  description: 'Estructura de datos para reservas en TrackHS'
                }, null, 2)
              }
            ]
          };
        
        case 'trackhs://schema/units':
          return {
            contents: [
              {
                uri,
                text: JSON.stringify({
                  schema: {
                    id: 'string',
                    name: 'string',
                    type: 'enum[apartment, house, room]',
                    capacity: 'number',
                    status: 'enum[available, occupied, maintenance]',
                    nodeId: 'string',
                    amenities: 'array[string]'
                  },
                  description: 'Estructura de datos para unidades en TrackHS'
                }, null, 2)
              }
            ]
          };
        
        case 'trackhs://status/system':
          return {
            contents: [
              {
                uri,
                text: JSON.stringify({
                  status: 'operational',
                  timestamp: new Date().toISOString(),
                  version: '1.0.0',
                  apiUrl: process.env.TRACKHS_API_URL,
                  toolsCount: this.tools.length,
                  capabilities: ['tools', 'resources', 'prompts']
                }, null, 2)
              }
            ]
          };
        
        case 'trackhs://docs/api':
          return {
            contents: [
              {
                uri,
                text: `# TrackHS API Documentation

## Endpoints Disponibles

### Reservas
- \`GET /reservations\` - Listar reservas
- \`GET /reservations/{id}\` - Obtener reserva específica
- \`GET /reservations/search\` - Buscar reservas

### Unidades
- \`GET /units\` - Listar unidades
- \`GET /units/{id}\` - Obtener unidad específica

### Contactos
- \`GET /crm/contacts\` - Listar contactos

### Contabilidad
- \`GET /pms/accounting/accounts\` - Listar cuentas contables
- \`GET /pms/accounting/folios\` - Listar folios

### Mantenimiento
- \`GET /maintenance/work-orders\` - Listar órdenes de trabajo

## Autenticación
Todas las peticiones requieren autenticación Basic Auth con las credenciales configuradas.
`
              }
            ]
          };
        
        default:
          throw new Error(`Resource no encontrado: ${uri}`);
      }
    });

    // Listar prompts disponibles
    this.server.setRequestHandler(ListPromptsRequestSchema, async () => {
      return {
        prompts: [
          {
            name: 'check-today-reservations',
            title: 'Revisar Reservas de Hoy',
            description: 'Obtener todas las reservas que llegan o salen hoy',
            arguments: [
              {
                name: 'date',
                description: 'Fecha en formato YYYY-MM-DD (por defecto: hoy)',
                required: false
              }
            ]
          },
          {
            name: 'unit-availability',
            title: 'Consultar Disponibilidad de Unidades',
            description: 'Verificar disponibilidad de unidades para fechas específicas',
            arguments: [
              {
                name: 'checkIn',
                description: 'Fecha de entrada en formato YYYY-MM-DD',
                required: true
              },
              {
                name: 'checkOut',
                description: 'Fecha de salida en formato YYYY-MM-DD',
                required: true
              },
              {
                name: 'nodeId',
                description: 'ID del nodo específico (opcional)',
                required: false
              }
            ]
          },
          {
            name: 'guest-contact-info',
            title: 'Información de Contacto de Huéspedes',
            description: 'Obtener información de contacto de huéspedes para reservas específicas',
            arguments: [
              {
                name: 'reservationId',
                description: 'ID de reserva específica (opcional)',
                required: false
              },
              {
                name: 'searchTerm',
                description: 'Término de búsqueda para filtrar huéspedes',
                required: false
              }
            ]
          },
          {
            name: 'maintenance-summary',
            title: 'Resumen de Órdenes de Mantenimiento',
            description: 'Obtener un resumen de las órdenes de mantenimiento pendientes y completadas',
            arguments: [
              {
                name: 'status',
                description: 'Estado de las órdenes a filtrar',
                required: false
              },
              {
                name: 'days',
                description: 'Número de días hacia atrás para buscar órdenes',
                required: false
              }
            ]
          },
          {
            name: 'financial-analysis',
            title: 'Análisis Financiero Básico',
            description: 'Obtener un análisis financiero básico de reservas y cuentas',
            arguments: [
              {
                name: 'period',
                description: 'Período para el análisis',
                required: true
              },
              {
                name: 'includeForecast',
                description: 'Incluir proyecciones futuras (true/false)',
                required: false
              }
            ]
          }
        ]
      };
    });

    // Obtener prompt específico
    this.server.setRequestHandler(GetPromptRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      switch (name) {
        case 'check-today-reservations':
          const date = args?.date || new Date().toISOString().split('T')[0];
          return {
            description: 'Revisar reservas para la fecha especificada',
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Por favor, revisa todas las reservas para la fecha ${date}. Incluye:
1. Reservas que llegan hoy (check-in)
2. Reservas que salen hoy (check-out)
3. Reservas que están activas hoy
4. Un resumen de ocupación por nodo/unidad

Usa las herramientas disponibles para obtener esta información.`
                }
              }
            ]
          };
        
        case 'unit-availability':
          const { checkIn, checkOut, nodeId } = args || {};
          return {
            description: 'Verificar disponibilidad de unidades',
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Necesito verificar la disponibilidad de unidades para las fechas:
- Entrada: ${checkIn}
- Salida: ${checkOut}
${nodeId ? `- Nodo específico: ${nodeId}` : ''}

Por favor:
1. Lista todas las unidades disponibles
2. Verifica si hay reservas conflictivas en esas fechas
3. Proporciona un resumen de disponibilidad por tipo de unidad
4. Incluye información de capacidad y amenidades`
                }
              }
            ]
          };
        
        case 'guest-contact-info':
          const { reservationId, searchTerm } = args || {};
          return {
            description: 'Obtener información de contacto de huéspedes',
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Necesito obtener información de contacto de huéspedes:
${reservationId ? `- Para la reserva ID: ${reservationId}` : ''}
${searchTerm ? `- Filtrando por: ${searchTerm}` : ''}

Por favor:
1. Obtén la información de contacto completa
2. Incluye nombre, email, teléfono y dirección
3. Verifica si hay notas especiales o preferencias
4. Proporciona un resumen organizado por reserva`
                }
              }
            ]
          };
        
        case 'maintenance-summary':
          const { status = 'all', days = 30 } = args || {};
          return {
            description: 'Obtener resumen de órdenes de mantenimiento',
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Necesito un resumen de las órdenes de mantenimiento:
- Estado: ${status === 'all' ? 'Todas' : status}
- Período: Últimos ${days} días

Por favor:
1. Lista todas las órdenes que coincidan con los criterios
2. Agrupa por estado (pendiente, en progreso, completada)
3. Incluye información de prioridad y fecha de vencimiento
4. Proporciona estadísticas de completitud
5. Identifica órdenes urgentes o vencidas`
                }
              }
            ]
          };
        
        case 'financial-analysis':
          const { period, includeForecast = false } = args || {};
          return {
            description: 'Obtener análisis financiero básico',
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Necesito un análisis financiero para el período: ${period}
${includeForecast ? '- Incluir proyecciones futuras' : ''}

Por favor:
1. Obtén datos de reservas para el período
2. Calcula ingresos totales y promedio por reserva
3. Analiza ocupación y tarifas
4. Incluye información de cuentas contables relevantes
5. Proporciona métricas clave de rendimiento
${includeForecast ? '6. Incluye proyecciones basadas en tendencias' : ''}`
                }
              }
            ]
          };
        
        default:
          throw new Error(`Prompt no encontrado: ${name}`);
      }
    });
  }

  /**
   * Obtiene la instancia del servidor MCP
   */
  getServer(): Server {
    return this.server;
  }

  /**
   * Obtiene información del servidor
   */
  getServerInfo() {
    return {
      name: 'trackhs-mcp-server',
      version: '1.0.0',
      toolsCount: this.tools.length,
      capabilities: ['tools', 'resources', 'prompts'],
      apiUrl: process.env.TRACKHS_API_URL
    };
  }
}
