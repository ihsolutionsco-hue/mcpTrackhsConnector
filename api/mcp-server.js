/**
 * Servidor MCP Real para Track HS - Vercel
 * Implementación del protocolo MCP para Claude
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

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

    const protocol = url.protocol === 'https:' ? require('https') : require('http');
    
    const req = protocol.request(requestOptions, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`Track HS API Error: ${res.statusCode} ${res.statusMessage}`));
          }
        } catch (error) {
          reject(new Error(`Error parsing response: ${error.message}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(new Error(`Request failed: ${error.message}`));
    });

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }

    req.end();
  });
}

// Herramientas MCP disponibles
const MCP_TOOLS = [
  {
    name: 'get_reviews',
    description: 'Obtener reseñas de propiedades de Track HS',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        updatedSince: { type: 'string' }
      }
    }
  },
  {
    name: 'get_contacts',
    description: 'Obtener lista de contactos del CRM',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        email: { type: 'string' }
      }
    }
  },
  {
    name: 'get_reservation',
    description: 'Obtener detalles de una reserva específica',
    inputSchema: {
      type: 'object',
      properties: {
        reservationId: { type: 'string' }
      },
      required: ['reservationId']
    }
  },
  {
    name: 'search_reservations',
    description: 'Buscar reservas con filtros',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        nodeId: { type: 'number' },
        unitId: { type: 'number' },
        status: { type: 'string' }
      }
    }
  },
  {
    name: 'get_units',
    description: 'Obtener lista de unidades disponibles',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        nodeId: { type: 'number' }
      }
    }
  },
  {
    name: 'get_unit',
    description: 'Obtener detalles de una unidad específica',
    inputSchema: {
      type: 'object',
      properties: {
        unitId: { type: 'number' }
      },
      required: ['unitId']
    }
  },
  {
    name: 'get_folios_collection',
    description: 'Obtener folios/facturas contables',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        type: { type: 'string' },
        status: { type: 'string' }
      }
    }
  },
  {
    name: 'get_ledger_accounts',
    description: 'Obtener cuentas contables',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        category: { type: 'string' },
        isActive: { type: 'number' }
      }
    }
  },
  {
    name: 'get_ledger_account',
    description: 'Obtener detalles de una cuenta contable',
    inputSchema: {
      type: 'object',
      properties: {
        accountId: { type: 'number' }
      },
      required: ['accountId']
    }
  },
  {
    name: 'get_reservation_notes',
    description: 'Obtener notas de reservaciones',
    inputSchema: {
      type: 'object',
      properties: {
        reservationId: { type: 'string' },
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 }
      },
      required: ['reservationId']
    }
  },
  {
    name: 'get_nodes',
    description: 'Obtener nodos/propiedades',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' }
      }
    }
  },
  {
    name: 'get_node',
    description: 'Obtener detalles de un nodo específico',
    inputSchema: {
      type: 'object',
      properties: {
        nodeId: { type: 'number' }
      },
      required: ['nodeId']
    }
  },
  {
    name: 'get_maintenance_work_orders',
    description: 'Obtener órdenes de trabajo de mantenimiento',
    inputSchema: {
      type: 'object',
      properties: {
        page: { type: 'number', default: 1 },
        size: { type: 'number', default: 10 },
        search: { type: 'string' },
        status: { type: 'string' }
      }
    }
  }
];

// Ejecutar herramienta MCP
async function executeMCPTool(toolName, args) {
  try {
    validateConfig();
    
    switch (toolName) {
      case 'get_reviews':
        const reviewsParams = new URLSearchParams();
        if (args.page) reviewsParams.append('page', args.page);
        if (args.size) reviewsParams.append('size', args.size);
        if (args.search) reviewsParams.append('search', args.search);
        if (args.updatedSince) reviewsParams.append('updatedSince', args.updatedSince);
        
        const reviewsEndpoint = `/channel-management/channel/reviews?${reviewsParams.toString()}`;
        const reviewsData = await makeTrackHSRequest(reviewsEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: reviewsData,
          timestamp: new Date().toISOString()
        };

      case 'get_contacts':
        const contactsParams = new URLSearchParams();
        if (args.page) contactsParams.append('page', args.page);
        if (args.size) contactsParams.append('size', args.size);
        if (args.search) contactsParams.append('search', args.search);
        if (args.email) contactsParams.append('email', args.email);
        
        const contactsEndpoint = `/crm/contacts?${contactsParams.toString()}`;
        const contactsData = await makeTrackHSRequest(contactsEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: contactsData,
          timestamp: new Date().toISOString()
        };

      case 'get_reservation':
        if (!args.reservationId) {
          throw new Error('reservationId es requerido');
        }
        
        const reservationData = await makeTrackHSRequest(`/reservations/${args.reservationId}`);
        
        return {
          tool: toolName,
          status: 'success',
          data: reservationData,
          timestamp: new Date().toISOString()
        };

      case 'search_reservations':
        const searchParams = new URLSearchParams();
        if (args.page) searchParams.append('page', args.page);
        if (args.size) searchParams.append('size', args.size);
        if (args.search) searchParams.append('search', args.search);
        if (args.nodeId) searchParams.append('nodeId', args.nodeId);
        if (args.unitId) searchParams.append('unitId', args.unitId);
        if (args.status) searchParams.append('status', args.status);
        
        const searchEndpoint = `/reservations/search?${searchParams.toString()}`;
        const searchData = await makeTrackHSRequest(searchEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: searchData,
          timestamp: new Date().toISOString()
        };

      case 'get_units':
        const unitsParams = new URLSearchParams();
        if (args.page) unitsParams.append('page', args.page);
        if (args.size) unitsParams.append('size', args.size);
        if (args.search) unitsParams.append('search', args.search);
        if (args.nodeId) unitsParams.append('nodeId', args.nodeId);
        
        const unitsEndpoint = `/units?${unitsParams.toString()}`;
        const unitsData = await makeTrackHSRequest(unitsEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: unitsData,
          timestamp: new Date().toISOString()
        };

      case 'get_unit':
        if (!args.unitId) {
          throw new Error('unitId es requerido');
        }
        
        const unitData = await makeTrackHSRequest(`/units/${args.unitId}`);
        
        return {
          tool: toolName,
          status: 'success',
          data: unitData,
          timestamp: new Date().toISOString()
        };

      case 'get_folios_collection':
        const foliosParams = new URLSearchParams();
        if (args.page) foliosParams.append('page', args.page);
        if (args.size) foliosParams.append('size', args.size);
        if (args.search) foliosParams.append('search', args.search);
        if (args.type) foliosParams.append('type', args.type);
        if (args.status) foliosParams.append('status', args.status);
        
        const foliosEndpoint = `/pms/accounting/folios?${foliosParams.toString()}`;
        const foliosData = await makeTrackHSRequest(foliosEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: foliosData,
          timestamp: new Date().toISOString()
        };

      case 'get_ledger_accounts':
        const ledgerParams = new URLSearchParams();
        if (args.page) ledgerParams.append('page', args.page);
        if (args.size) ledgerParams.append('size', args.size);
        if (args.search) ledgerParams.append('search', args.search);
        if (args.category) ledgerParams.append('category', args.category);
        if (args.isActive !== undefined) ledgerParams.append('isActive', args.isActive);
        
        const ledgerEndpoint = `/pms/accounting/accounts?${ledgerParams.toString()}`;
        const ledgerData = await makeTrackHSRequest(ledgerEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: ledgerData,
          timestamp: new Date().toISOString()
        };

      case 'get_ledger_account':
        if (!args.accountId) {
          throw new Error('accountId es requerido');
        }
        
        const accountData = await makeTrackHSRequest(`/pms/accounting/accounts/${args.accountId}`);
        
        return {
          tool: toolName,
          status: 'success',
          data: accountData,
          timestamp: new Date().toISOString()
        };

      case 'get_reservation_notes':
        if (!args.reservationId) {
          throw new Error('reservationId es requerido');
        }
        
        const notesParams = new URLSearchParams();
        if (args.page) notesParams.append('page', args.page);
        if (args.size) notesParams.append('size', args.size);
        
        const notesEndpoint = `/reservations/${args.reservationId}/notes?${notesParams.toString()}`;
        const notesData = await makeTrackHSRequest(notesEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: notesData,
          timestamp: new Date().toISOString()
        };

      case 'get_nodes':
        const nodesParams = new URLSearchParams();
        if (args.page) nodesParams.append('page', args.page);
        if (args.size) nodesParams.append('size', args.size);
        if (args.search) nodesParams.append('search', args.search);
        
        const nodesEndpoint = `/nodes?${nodesParams.toString()}`;
        const nodesData = await makeTrackHSRequest(nodesEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: nodesData,
          timestamp: new Date().toISOString()
        };

      case 'get_node':
        if (!args.nodeId) {
          throw new Error('nodeId es requerido');
        }
        
        const nodeData = await makeTrackHSRequest(`/nodes/${args.nodeId}`);
        
        return {
          tool: toolName,
          status: 'success',
          data: nodeData,
          timestamp: new Date().toISOString()
        };

      case 'get_maintenance_work_orders':
        const maintenanceParams = new URLSearchParams();
        if (args.page) maintenanceParams.append('page', args.page);
        if (args.size) maintenanceParams.append('size', args.size);
        if (args.search) maintenanceParams.append('search', args.search);
        if (args.status) maintenanceParams.append('status', args.status);
        
        const maintenanceEndpoint = `/maintenance/work-orders?${maintenanceParams.toString()}`;
        const maintenanceData = await makeTrackHSRequest(maintenanceEndpoint);
        
        return {
          tool: toolName,
          status: 'success',
          data: maintenanceData,
          timestamp: new Date().toISOString()
        };

      default:
        throw new Error(`Herramienta '${toolName}' no implementada`);
    }
  } catch (error) {
    return {
      tool: toolName,
      status: 'error',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

// Crear servidor MCP
async function createMCPServer() {
  const server = new Server({
    name: 'trackhs-mcp-server',
    version: '1.0.0'
  }, {
    capabilities: {
      tools: {}
    }
  });

  // Listar herramientas disponibles
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: MCP_TOOLS
    };
  });

  // Ejecutar herramientas
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
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
      const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
      throw new Error(`Error en ejecución de herramienta: ${errorMessage}`);
    }
  });

  return server;
}

// Iniciar servidor MCP
async function startMCPServer() {
  try {
    const server = await createMCPServer();
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('Track HS MCP Server iniciado correctamente');
  } catch (error) {
    console.error('Error al iniciar Track HS MCP Server:', error);
    process.exit(1);
  }
}

// Ejecutar servidor
if (import.meta.url === `file://${process.argv[1]}`) {
  startMCPServer();
}

export default startMCPServer;
