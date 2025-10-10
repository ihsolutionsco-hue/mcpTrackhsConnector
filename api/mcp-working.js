/**
 * Endpoint MCP funcional para Vercel
 * Versión optimizada que funciona correctamente
 */

const express = require('express');

// Crear app Express
const app = express();

// Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Mcp-Session-Id');
  res.header('Access-Control-Expose-Headers', 'Mcp-Session-Id');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  next();
});

// Cliente API para TrackHS
class TrackHSApiClient {
  constructor() {
    this.baseUrl = process.env.TRACKHS_API_URL;
    this.auth = Buffer.from(`${process.env.TRACKHS_USERNAME}:${process.env.TRACKHS_PASSWORD}`).toString('base64');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        method: options.method || 'GET',
        headers: {
          'Authorization': `Basic ${this.auth}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers
        },
        body: options.body ? JSON.stringify(options.body) : undefined
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Track HS API Error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return await response.text();
      }
    } catch (error) {
      throw new Error(`Error en petición a Track HS: ${error.message}`);
    }
  }

  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }
}

// Inicializar cliente API
let apiClient = null;
try {
  if (process.env.TRACKHS_API_URL && process.env.TRACKHS_USERNAME && process.env.TRACKHS_PASSWORD) {
    apiClient = new TrackHSApiClient();
    console.log('[MCP] Cliente API inicializado correctamente');
  } else {
    console.log('[MCP] Variables de entorno no configuradas, usando modo simulado');
  }
} catch (error) {
  console.error('[MCP] Error inicializando cliente API:', error.message);
}

// Helper para formatear respuestas MCP
function formatMCPResponse(data) {
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(data, null, 2)
      }
    ]
  };
}

// Endpoint principal MCP
app.post('/', async (req, res) => {
  console.log('[MCP] Request recibido:', {
    method: req.method,
    url: req.url,
    body: req.body,
    headers: req.headers
  });

  try {
    const { jsonrpc, method, params, id } = req.body;

    // Validar JSON-RPC 2.0
    if (jsonrpc !== '2.0') {
      return res.status(400).json({
        jsonrpc: '2.0',
        error: { code: -32600, message: 'Invalid Request' },
        id: null
      });
    }

    let result = null;

    switch (method) {
      case 'tools/list':
        result = {
          tools: [
            {
              name: 'get_contacts',
              description: 'Retrieve all contacts from Track HS CRM system',
              inputSchema: {
                type: 'object',
                properties: {
                  sortColumn: { type: 'string', enum: ['id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip'] },
                  sortDirection: { type: 'string', enum: ['asc', 'desc'], default: 'asc' },
                  search: { type: 'string' },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_reservation',
              description: 'Get detailed information for a specific reservation by ID',
              inputSchema: {
                type: 'object',
                properties: {
                  reservationId: { type: 'string', description: 'The ID of the reservation to retrieve' }
                },
                required: ['reservationId']
              }
            },
            {
              name: 'search_reservations',
              description: 'Search reservations with various filters',
              inputSchema: {
                type: 'object',
                properties: {
                  checkIn: { type: 'string' },
                  checkOut: { type: 'string' },
                  status: { type: 'string' },
                  guestName: { type: 'string' },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_units',
              description: 'Get list of units/properties',
              inputSchema: {
                type: 'object',
                properties: {
                  nodeId: { type: 'string' },
                  status: { type: 'string' },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_unit',
              description: 'Get specific unit details by ID',
              inputSchema: {
                type: 'object',
                properties: {
                  unitId: { type: 'string', description: 'The ID of the unit to retrieve' }
                },
                required: ['unitId']
              }
            },
            {
              name: 'get_reviews',
              description: 'Get property reviews',
              inputSchema: {
                type: 'object',
                properties: {
                  nodeId: { type: 'string' },
                  rating: { type: 'number', minimum: 1, maximum: 5 },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            }
          ]
        };
        break;

      case 'tools/call':
        const { name, arguments: args } = params;
        
        if (!apiClient) {
          // Modo simulado para testing
          result = formatMCPResponse({
            message: 'API Client no configurado - Modo simulado',
            tool: name,
            arguments: args,
            simulatedData: {
              data: [
                { id: 1, name: 'Datos simulados', type: 'test' }
              ],
              meta: { page: 1, total: 1, simulated: true }
            }
          });
        } else {
          // Modo real con API
          try {
            switch (name) {
              case 'get_contacts':
                const contactsQuery = new URLSearchParams();
                if (args.sortColumn) contactsQuery.append('sortColumn', args.sortColumn);
                if (args.sortDirection) contactsQuery.append('sortDirection', args.sortDirection);
                if (args.search) contactsQuery.append('search', args.search);
                if (args.page) contactsQuery.append('page', args.page.toString());
                if (args.size) contactsQuery.append('size', args.size.toString());
                
                const contactsEndpoint = `/crm/contacts?${contactsQuery.toString()}`;
                const contactsData = await apiClient.get(contactsEndpoint);
                result = formatMCPResponse(contactsData);
                break;

              case 'get_reservation':
                if (!args.reservationId) {
                  throw new Error('El ID de reservación es requerido');
                }
                const reservationEndpoint = `/v2/pms/reservations/${encodeURIComponent(args.reservationId)}`;
                const reservationData = await apiClient.get(reservationEndpoint);
                result = formatMCPResponse(reservationData);
                break;

              case 'search_reservations':
                const searchQuery = new URLSearchParams();
                if (args.checkIn) searchQuery.append('checkIn', args.checkIn);
                if (args.checkOut) searchQuery.append('checkOut', args.checkOut);
                if (args.status) searchQuery.append('status', args.status);
                if (args.guestName) searchQuery.append('guestName', args.guestName);
                if (args.page) searchQuery.append('page', args.page.toString());
                if (args.size) searchQuery.append('size', args.size.toString());
                
                const searchEndpoint = `/v2/pms/reservations/search?${searchQuery.toString()}`;
                const searchData = await apiClient.get(searchEndpoint);
                result = formatMCPResponse(searchData);
                break;

              case 'get_units':
                const unitsQuery = new URLSearchParams();
                if (args.nodeId) unitsQuery.append('nodeId', args.nodeId);
                if (args.status) unitsQuery.append('status', args.status);
                if (args.page) unitsQuery.append('page', args.page.toString());
                if (args.size) unitsQuery.append('size', args.size.toString());
                
                const unitsEndpoint = `/pms/units?${unitsQuery.toString()}`;
                const unitsData = await apiClient.get(unitsEndpoint);
                result = formatMCPResponse(unitsData);
                break;

              case 'get_unit':
                if (!args.unitId) {
                  throw new Error('El ID de unidad es requerido');
                }
                const unitEndpoint = `/pms/units/${encodeURIComponent(args.unitId)}`;
                const unitData = await apiClient.get(unitEndpoint);
                result = formatMCPResponse(unitData);
                break;

              case 'get_reviews':
                const reviewsQuery = new URLSearchParams();
                if (args.nodeId) reviewsQuery.append('nodeId', args.nodeId);
                if (args.rating) reviewsQuery.append('rating', args.rating.toString());
                if (args.page) reviewsQuery.append('page', args.page.toString());
                if (args.size) reviewsQuery.append('size', args.size.toString());
                
                const reviewsEndpoint = `/pms/reviews?${reviewsQuery.toString()}`;
                const reviewsData = await apiClient.get(reviewsEndpoint);
                result = formatMCPResponse(reviewsData);
                break;

              default:
                throw new Error(`Herramienta desconocida: ${name}`);
            }
          } catch (apiError) {
            result = formatMCPResponse({
              error: 'Error en API de TrackHS',
              message: apiError.message,
              tool: name,
              arguments: args
            });
          }
        }
        break;

      case 'resources/list':
        result = {
          resources: [
            {
              uri: 'trackhs://status/system',
              name: 'system-status',
              title: 'Estado del Sistema',
              description: 'Estado actual del sistema TrackHS',
              mimeType: 'application/json'
            }
          ]
        };
        break;

      case 'prompts/list':
        result = {
          prompts: [
            {
              name: 'check-today-reservations',
              title: 'Revisar Reservas de Hoy',
              description: 'Obtener todas las reservas que llegan o salen hoy'
            }
          ]
        };
        break;

      default:
        return res.status(400).json({
          jsonrpc: '2.0',
          error: { code: -32601, message: 'Method not found' },
          id
        });
    }

    console.log('[MCP] Respuesta enviada:', { method, result: result ? 'OK' : 'NULL' });
    
    res.json({
      jsonrpc: '2.0',
      result,
      id
    });

  } catch (error) {
    console.error('[MCP] Error:', error);
    res.status(500).json({
      jsonrpc: '2.0',
      error: {
        code: -32603,
        message: 'Internal server error',
        data: error.message
      },
      id: req.body.id || null
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Track HS MCP Server',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    environment: {
      trackhsConfigured: !!(process.env.TRACKHS_API_URL && process.env.TRACKHS_USERNAME && process.env.TRACKHS_PASSWORD),
      hasApiClient: !!apiClient
    }
  });
});

// Default GET
app.get('/', (req, res) => {
  res.json({
    message: 'Track HS MCP Server',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      mcp: 'POST / (JSON-RPC 2.0)'
    },
    capabilities: ['tools', 'resources', 'prompts']
  });
});

// Exportar para Vercel
module.exports = app;
