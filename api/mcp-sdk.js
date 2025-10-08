/**
 * Servidor MCP usando SDK oficial - Track HS
 * Implementación correcta usando @modelcontextprotocol/sdk
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { HttpServerTransport } from '@modelcontextprotocol/sdk/server/http.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

import https from 'https';
import http from 'http';

// Configuración de Track HS
const TRACKHS_CONFIG = {
  baseUrl: process.env.TRACKHS_API_URL || 'https://api.trackhs.com/api',
  username: process.env.TRACKHS_USERNAME,
  password: process.env.TRACKHS_PASSWORD
};

// Verificar configuración
function validateConfig() {
  if (!TRACKHS_CONFIG.username || !TRACKHS_CONFIG.password) {
    throw new Error('Variables de entorno TRACKHS_USERNAME y TRACKHS_PASSWORD requeridas');
  }
  return true;
}

// Crear header de autenticación
function getAuthHeader() {
  const credentials = Buffer.from(`${TRACKHS_CONFIG.username}:${TRACKHS_CONFIG.password}`).toString('base64');
  return `Basic ${credentials}`;
}

// Realizar petición a Track HS API
async function makeTrackHSRequest(endpoint, options = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(`${TRACKHS_CONFIG.baseUrl}${endpoint}`);
    
    const requestOptions = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: options.method || 'GET',
      headers: {
        'Authorization': getAuthHeader(),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
      }
    };

    const protocol = url.protocol === 'https:' ? https : http;
    
    const req = protocol.request(requestOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch (error) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    
    req.end();
  });
}

// Definir herramientas MCP
const MCP_TOOLS = [
  {
    name: "get_contacts",
    description: "Obtener lista de contactos de Track HS",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_reservation",
    description: "Obtener información de una reserva específica",
    inputSchema: {
      type: "object",
      properties: {
        reservationId: { type: "string", description: "ID de la reserva" }
      },
      required: ["reservationId"]
    }
  },
  {
    name: "search_reservations",
    description: "Buscar reservas con filtros",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 },
        status: { type: "string", description: "Estado de la reserva" }
      }
    }
  },
  {
    name: "get_nodes",
    description: "Obtener lista de propiedades/nodos",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_node",
    description: "Obtener información de una propiedad específica",
    inputSchema: {
      type: "object",
      properties: {
        nodeId: { type: "string", description: "ID de la propiedad" }
      },
      required: ["nodeId"]
    }
  },
  {
    name: "get_units",
    description: "Obtener lista de unidades disponibles",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_unit",
    description: "Obtener información de una unidad específica",
    inputSchema: {
      type: "object",
      properties: {
        unitId: { type: "string", description: "ID de la unidad" }
      },
      required: ["unitId"]
    }
  },
  {
    name: "get_ledger_accounts",
    description: "Obtener cuentas contables",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_ledger_account",
    description: "Obtener información de una cuenta contable específica",
    inputSchema: {
      type: "object",
      properties: {
        accountId: { type: "string", description: "ID de la cuenta contable" }
      },
      required: ["accountId"]
    }
  },
  {
    name: "get_folios_collection",
    description: "Obtener folios/facturas",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_maintenance_work_orders",
    description: "Obtener órdenes de trabajo de mantenimiento",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_reviews",
    description: "Obtener reseñas de propiedades",
    inputSchema: {
      type: "object",
      properties: {
        page: { type: "number", default: 1 },
        size: { type: "number", default: 10 }
      }
    }
  },
  {
    name: "get_reservation_notes",
    description: "Obtener notas de reservas",
    inputSchema: {
      type: "object",
      properties: {
        reservationId: { type: "string", description: "ID de la reserva" }
      },
      required: ["reservationId"]
    }
  }
];

// Ejecutar herramienta MCP
async function executeMCPTool(toolName, args) {
  try {
    validateConfig();
    
    switch (toolName) {
      case 'get_contacts':
        return await makeTrackHSRequest('/contacts', { 
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_reservation':
        return await makeTrackHSRequest(`/reservations/${args.reservationId}`);
      
      case 'search_reservations':
        return await makeTrackHSRequest('/reservations/search', {
          method: 'POST',
          body: { page: args.page || 1, size: args.size || 10, status: args.status }
        });
      
      case 'get_nodes':
        return await makeTrackHSRequest('/nodes', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_node':
        return await makeTrackHSRequest(`/nodes/${args.nodeId}`);
      
      case 'get_units':
        return await makeTrackHSRequest('/units', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_unit':
        return await makeTrackHSRequest(`/units/${args.unitId}`);
      
      case 'get_ledger_accounts':
        return await makeTrackHSRequest('/ledger-accounts', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_ledger_account':
        return await makeTrackHSRequest(`/ledger-accounts/${args.accountId}`);
      
      case 'get_folios_collection':
        return await makeTrackHSRequest('/folios', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_maintenance_work_orders':
        return await makeTrackHSRequest('/maintenance/work-orders', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_reviews':
        return await makeTrackHSRequest('/reviews', {
          method: 'GET',
          body: { page: args.page || 1, size: args.size || 10 }
        });
      
      case 'get_reservation_notes':
        return await makeTrackHSRequest(`/reservations/${args.reservationId}/notes`);
      
      default:
        throw new Error(`Herramienta desconocida: ${toolName}`);
    }
  } catch (error) {
    throw new Error(`Error ejecutando herramienta ${toolName}: ${error.message}`);
  }
}

// Main handler para Vercel
export default async function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    // Health check
    if (req.url === '/health' || req.url.endsWith('/health')) {
      res.status(200).json({
        status: 'healthy',
        service: 'Track HS MCP SDK Server',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        tools: {
          count: MCP_TOOLS.length,
          available: MCP_TOOLS.map(t => t.name)
        }
      });
      return;
    }

    // Tools list endpoint
    if (req.url === '/tools' || req.url.endsWith('/tools')) {
      res.status(200).json({
        success: true,
        tools: MCP_TOOLS
      });
      return;
    }

    // MCP Server usando SDK
    const mcpServer = new Server({
      name: 'trackhs-mcp-sdk-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {}
      }
    });

    // Register tool listing handler
    mcpServer.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: MCP_TOOLS
      };
    });

    // Register tool execution handler
    mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      try {
        const result = await executeMCPTool(name, args || {});
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        throw new Error(`Tool execution error: ${errorMessage}`);
      }
    });

    // Use Http Server Transport for Vercel's req/res
    const transport = new HttpServerTransport(req, res);
    await mcpServer.connect(transport);

  } catch (error) {
    console.error('Error en servidor MCP SDK:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: error.message
    });
  }
}
