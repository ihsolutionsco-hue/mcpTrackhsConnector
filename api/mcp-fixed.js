/**
 * Endpoint MCP optimizado para Vercel - Versión corregida
 * Implementa Streamable HTTP transport usando Express + McpServer
 * Configurado para funcionar con Claude y otros clientes MCP
 */

const express = require('express');
const { z } = require('zod');

// Crear instancia de Express
const app = express();
app.use(express.json());

// Configuración CORS básica según teoría MCP
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

// Validar variables de entorno
function validateEnvironment() {
  const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
  
  for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
      throw new Error(`Variable de entorno requerida no configurada: ${envVar}`);
    }
  }

  // Validar formato de URL
  try {
    const url = new URL(process.env.TRACKHS_API_URL);
    console.log('URL validada correctamente:', url.href);
  } catch (error) {
    console.error('Error validando URL:', process.env.TRACKHS_API_URL);
    throw new Error(`TRACKHS_API_URL debe ser una URL válida: ${process.env.TRACKHS_API_URL}`);
  }
}

// Helper function para formatear respuestas según protocolo MCP
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

// Cliente API simplificado para Vercel
class TrackHSApiClient {
  constructor(config) {
    this.baseUrl = config.baseUrl;
    this.auth = Buffer.from(`${config.username}:${config.password}`).toString('base64');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    console.log(`[TrackHS API] Realizando petición a: ${url}`);
    
    try {
      const fetchOptions = {
        method: options.method || 'GET',
        headers: {
          'Authorization': `Basic ${this.auth}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers
        }
      };
      
      if (options.body) {
        fetchOptions.body = options.body;
      }
      
      const response = await fetch(url, fetchOptions);
      
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
      console.error(`[TrackHS API] Error en petición:`, error);
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
  validateEnvironment();
  console.log('[MCP Server] Variables de entorno validadas correctamente');
  
  apiClient = new TrackHSApiClient({
    baseUrl: process.env.TRACKHS_API_URL,
    username: process.env.TRACKHS_USERNAME,
    password: process.env.TRACKHS_PASSWORD
  });
  
  console.log('[MCP Server] Cliente API inicializado correctamente');
} catch (error) {
  console.error('[MCP Server] Error de configuración:', error.message);
}

// Endpoint principal MCP
app.post('/', async (req, res) => {
  console.log('POST request received:', {
    method: req.method,
    url: req.url,
    body: req.body
  });
  
  try {
    // Manejar peticiones JSON-RPC 2.0
    const { jsonrpc, method, params, id } = req.body;
    
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
        if (!apiClient) {
          throw new Error('API Client no inicializado');
        }

        const { name, arguments: args } = params;
        
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
        break;

      case 'resources/list':
        result = {
          resources: [
            {
              uri: 'trackhs://schema/reservations',
              name: 'reservations-schema',
              title: 'Esquema de Reservas',
              description: 'Esquema de datos para reservas en TrackHS',
              mimeType: 'application/json'
            },
            {
              uri: 'trackhs://status/system',
              name: 'system-status',
              title: 'Estado del Sistema',
              description: 'Estado actual del sistema TrackHS y configuración',
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
              description: 'Obtener todas las reservas que llegan o salen hoy',
              arguments: [
                {
                  name: 'date',
                  description: 'Fecha en formato YYYY-MM-DD (por defecto: hoy)',
                  required: false
                }
              ]
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

    res.json({
      jsonrpc: '2.0',
      result,
      id
    });

  } catch (error) {
    console.error('Error handling MCP request:', error);
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

// Health check endpoint
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

// Default GET response
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

// Exportar handler compatible con Vercel serverless
module.exports = app;
