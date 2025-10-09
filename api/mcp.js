/**
 * Endpoint MCP optimizado para Vercel
 * Implementa Streamable HTTP transport sin gestión de sesiones (stateless)
 * Configurado para funcionar con Claude y otros clientes MCP
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { TrackHSApiClient } from '../dist/core/api-client.js';
import { GetContactsTool } from '../dist/tools/get-contacts.js';
import { GetReservationTool } from '../dist/tools/get-reservation.js';
import { GetUnitsTool } from '../dist/tools/get-units.js';
import { GetReviewsTool } from '../dist/tools/get-reviews.js';
import { SearchReservationsTool } from '../dist/tools/search-reservations.js';
import { GetUnitTool } from '../dist/tools/get-unit.js';
import { GetFoliosCollectionTool } from '../dist/tools/get-folios-collection.js';
import { GetLedgerAccountsTool } from '../dist/tools/get-ledger-accounts.js';
import { GetLedgerAccountTool } from '../dist/tools/get-ledger-account.js';
import { GetReservationNotesTool } from '../dist/tools/get-reservation-notes.js';
import { GetNodesTool } from '../dist/tools/get-nodes.js';
import { GetNodeTool } from '../dist/tools/get-node.js';
import { GetMaintenanceWorkOrdersTool } from '../dist/tools/get-maintenance-work-orders.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

// Cache para el servidor MCP (reutilizable)
let mcpServer = null;
let apiClient = null;
let tools = null;

/**
 * Inicializa el servidor MCP con todas las herramientas
 */
function initializeMCPServer() {
  if (mcpServer) {
    return mcpServer;
  }

  try {
    // Validar variables de entorno
    const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    for (const envVar of requiredEnvVars) {
      if (!process.env[envVar]) {
        throw new Error(`Variable de entorno requerida no configurada: ${envVar}`);
      }
    }

    // Crear cliente API
    apiClient = new TrackHSApiClient({
      baseUrl: process.env.TRACKHS_API_URL,
      username: process.env.TRACKHS_USERNAME,
      password: process.env.TRACKHS_PASSWORD
    });

    // Crear herramientas
    tools = [
      new GetContactsTool(apiClient),
      new GetReservationTool(apiClient),
      new GetUnitsTool(apiClient),
      new GetReviewsTool(apiClient),
      new SearchReservationsTool(apiClient),
      new GetUnitTool(apiClient),
      new GetFoliosCollectionTool(apiClient),
      new GetLedgerAccountsTool(apiClient),
      new GetLedgerAccountTool(apiClient),
      new GetReservationNotesTool(apiClient),
      new GetNodesTool(apiClient),
      new GetNodeTool(apiClient),
      new GetMaintenanceWorkOrdersTool(apiClient)
    ];

    // Crear servidor MCP
    mcpServer = new Server({
      name: 'trackhs-mcp-server',
      version: '1.0.0'
    }, {
            capabilities: {
        tools: {},
              resources: {},
              prompts: {}
      }
    });

    // Configurar manejadores
    setupHandlers();

    return mcpServer;
  } catch (error) {
    console.error('Error inicializando servidor MCP:', error);
    throw error;
  }
}

/**
 * Configura todos los manejadores del servidor MCP
 */
function setupHandlers() {
  // Listar herramientas disponibles
  mcpServer.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: tools.map(tool => ({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.inputSchema
      }))
    };
  });

  // Ejecutar herramientas
  mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    const tool = tools.find(t => t.name === name);
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
  mcpServer.setRequestHandler(ListResourcesRequestSchema, async () => {
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
  mcpServer.setRequestHandler(ReadResourceRequestSchema, async (request) => {
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
                toolsCount: tools.length,
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
  mcpServer.setRequestHandler(ListPromptsRequestSchema, async () => {
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
  mcpServer.setRequestHandler(GetPromptRequestSchema, async (request) => {
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

// Main handler para Vercel
export default async function handler(req, res) {
  // Configurar CORS con headers necesarios para MCP
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Mcp-Session-Id');
  res.setHeader('Access-Control-Expose-Headers', 'Mcp-Session-Id');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
        return;
      }

  try {
    // Health check endpoint
    if (req.url === '/health' || req.url.endsWith('/health')) {
      const server = initializeMCPServer();
      
        res.status(200).json({
        status: 'healthy',
        service: 'Track HS MCP Server',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        capabilities: ['tools', 'resources', 'prompts'],
        toolsCount: tools.length,
        apiUrl: process.env.TRACKHS_API_URL
        });
        return;
      }

    // Tools list endpoint (para debugging)
    if (req.url === '/tools' || req.url.endsWith('/tools')) {
      const server = initializeMCPServer();
      
      res.status(200).json({
        success: true,
        tools: tools.map(tool => ({
          name: tool.name,
          title: tool.title,
          description: tool.description
        })),
        count: tools.length,
        serverInfo: {
          name: 'trackhs-mcp-server',
          version: '1.0.0',
          capabilities: ['tools', 'resources', 'prompts']
        }
      });
      return;
    }

    // MCP JSON-RPC 2.0 endpoint (principal)
    if (req.method === 'POST') {
      const server = initializeMCPServer();
      
      // Crear un transport simple para manejar la petición
      const transport = {
        async handleRequest(request, response, body) {
          try {
            // Parsear el body de la petición
            const requestData = typeof body === 'string' ? JSON.parse(body) : body;
            
            // Procesar la petición MCP
            const result = await server.request(requestData);
            
            response.status(200).json(result);
  } catch (error) {
            console.error('Error procesando petición MCP:', error);
            response.status(200).json({
      jsonrpc: '2.0',
              id: requestData?.id || null,
      error: {
        code: -32603,
                message: 'Internal Server Error',
                data: error.message
              }
            });
          }
        }
      };

      await transport.handleRequest(req, res, req.body);
      return;
    }

    // Default response para GET requests
    const server = initializeMCPServer();
    
    res.status(200).json({
      message: 'Track HS MCP Server',
      version: '1.0.0',
      endpoints: {
        health: '/health',
        tools: '/tools',
        mcp: 'POST / (JSON-RPC 2.0)'
      },
      capabilities: ['tools', 'resources', 'prompts'],
      toolsCount: tools.length,
      documentation: {
        connection: 'Use this endpoint as a Custom Connector in Claude',
        url: 'https://trackhs-mcp-connector.vercel.app/api/mcp',
        transport: 'Streamable HTTP'
      }
    });

  } catch (error) {
    console.error('Error en servidor MCP:', error);
    
    // Si es un error de JSON-RPC, devolver formato correcto
    if (req.method === 'POST') {
      res.status(200).json({
        jsonrpc: '2.0',
        id: null,
        error: {
          code: -32603,
          message: 'Internal Server Error',
          data: process.env.NODE_ENV === 'development' ? error.stack : undefined
        }
      });
    } else {
      res.status(500).json({
        error: 'Internal Server Error',
        message: error.message,
        timestamp: new Date().toISOString(),
        service: 'Track HS MCP Server'
      });
    }
  }
}