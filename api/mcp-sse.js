/**
 * Servidor MCP con SSE para Track HS
 * Implementación del protocolo MCP con Server-Sent Events para Claude
 */

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

// Manejar CORS
function handleCORS(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

// Parse body de la request
async function parseBody(req) {
  return new Promise((resolve, reject) => {
    if (req.method !== 'POST') {
      resolve({});
      return;
    }

    if (req.body) {
      resolve(req.body);
      return;
    }

    let data = '';
    req.on('data', chunk => {
      data += chunk.toString();
    });

    req.on('end', () => {
      try {
        const body = data ? JSON.parse(data) : {};
        resolve(body);
      } catch (error) {
        reject(new Error('Invalid JSON in request body'));
      }
    });

    req.on('error', error => {
      reject(error);
    });
  });
}

// Health Check
async function handleHealth(req, res) {
  try {
    const tools = MCP_TOOLS.map(tool => tool.name);
    
    res.status(200).json({
      status: 'healthy',
      service: 'Track HS MCP SSE Server',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      tools: {
        count: tools.length,
        available: tools
      },
      environment: {
        nodeEnv: process.env.NODE_ENV || 'development',
        vercelUrl: process.env.VERCEL_URL || 'local',
        trackhsConfigured: !!(TRACKHS_CONFIG.username && TRACKHS_CONFIG.password)
      }
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
}

// Listar herramientas MCP
async function handleListTools(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ 
      error: 'Método no permitido',
      allowed: ['GET']
    });
    return;
  }

  try {
    res.status(200).json({
      success: true,
      tools: MCP_TOOLS,
      count: MCP_TOOLS.length,
      service: 'Track HS MCP SSE Server',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Error al obtener herramientas',
      message: error.message
    });
  }
}

// Ejecutar herramienta MCP
async function handleExecuteTool(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({
      error: 'Método no permitido',
      allowed: ['POST']
    });
    return;
  }

  try {
    const body = await parseBody(req);
    const { name, arguments: args } = body;

    if (!name) {
      res.status(400).json({
        success: false,
        error: 'Nombre de herramienta requerido',
        required: ['name'],
        example: {
          name: 'get_contacts',
          arguments: { page: 1, size: 10 }
        }
      });
      return;
    }

    const tool = MCP_TOOLS.find(t => t.name === name);
    if (!tool) {
      res.status(404).json({
        success: false,
        error: `Herramienta '${name}' no encontrada`,
        available: MCP_TOOLS.map(t => t.name)
      });
      return;
    }

    console.log(`Ejecutando herramienta MCP: ${name}`, args);

    const startTime = Date.now();
    const result = await executeMCPTool(name, args || {});
    const executionTime = Date.now() - startTime;

    res.status(200).json({
      success: true,
      result,
      tool: name,
      timestamp: new Date().toISOString(),
      executionTime: `${executionTime}ms`
    });
  } catch (error) {
    const errorMessage = error.message;
    console.error(`Error ejecutando herramienta MCP:`, error);

    res.status(500).json({
      success: false,
      error: `Error en ejecución de herramienta: ${errorMessage}`,
      timestamp: new Date().toISOString()
    });
  }
}

// Endpoint por defecto
async function handleDefault(req, res) {
  res.status(200).json({
    service: 'Track HS MCP SSE Server',
    version: '1.0.0',
    description: 'Servidor MCP con SSE para Track HS API - Compatible con Claude MCP Connector',
    endpoints: {
      health: {
        method: 'GET',
        path: '/api/mcp-sse/health',
        description: 'Health check del servicio MCP SSE'
      },
      tools: {
        method: 'GET',
        path: '/api/mcp-sse/tools',
        description: 'Listar herramientas MCP disponibles'
      },
      execute: {
        method: 'POST',
        path: '/api/mcp-sse/tools/{name}/execute',
        description: 'Ejecutar herramienta MCP específica',
        body: {
          name: 'string (required)',
          arguments: 'object (optional)'
        }
      }
    },
    claudeConnector: {
      url: 'https://trackhs-mcp-connector.vercel.app/api/mcp-sse/sse',
      description: 'URL para configurar en Claude MCP Connector (con SSE)'
    },
    timestamp: new Date().toISOString()
  });
}

// Handler principal
export default async function handler(req, res) {
  // Manejar CORS
  handleCORS(res);

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const { method, url } = req;
    const path = url?.split('?')[0] || '';

    console.log(`[${method}] ${path}`);

    // Routing basado en la URL
    if (path === '/api/mcp-sse/health' || path === '/mcp-sse/health' || path === '/api/mcp-sse') {
      return handleHealth(req, res);
    }

    if (path === '/api/mcp-sse/tools' || path === '/mcp-sse/tools') {
      return handleListTools(req, res);
    }

    if (path.startsWith('/api/mcp-sse/tools/') || (path.startsWith('/mcp-sse/tools/') && path.includes('/execute'))) {
      return handleExecuteTool(req, res);
    }

    // Endpoint por defecto
    return handleDefault(req, res);

  } catch (error) {
    console.error('Error en servidor MCP SSE:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
}
