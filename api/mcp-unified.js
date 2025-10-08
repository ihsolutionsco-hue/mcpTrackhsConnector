/**
 * Servidor MCP Unificado para Track HS
 * Implementación correcta del protocolo MCP con JSON-RPC 2.0
 * Siguiendo las mejores prácticas de MCP
 */

import https from 'https';
import http from 'http';

// Configuración de Track HS
const TRACKHS_CONFIG = {
  baseUrl: process.env.TRACKHS_API_URL || 'https://api.trackhs.com/api',
  username: process.env.TRACKHS_USERNAME,
  password: process.env.TRACKHS_PASSWORD
};

// Validar configuración
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
          if (res.statusCode >= 200 && res.statusCode < 300) {
            const parsed = JSON.parse(data);
            resolve(parsed);
          } else {
            reject(new Error(`Track HS API Error: ${res.statusCode} ${res.statusMessage}`));
          }
        } catch (error) {
          reject(new Error(`Error parsing response: ${error.message}`));
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

// Importar esquemas estandarizados
import { MCP_TOOLS_SCHEMAS, validateToolSchema } from './tools-schemas.js';

// Usar esquemas estandarizados
const MCP_TOOLS = MCP_TOOLS_SCHEMAS;

// Ejecutar herramienta MCP
async function executeMCPTool(toolName, args) {
  try {
    validateConfig();
    
    // Validar esquema de la herramienta
    validateToolSchema(toolName, args);
    
    switch (toolName) {
      case 'get_contacts':
        const contactsParams = new URLSearchParams();
        if (args.page) contactsParams.append('page', args.page);
        if (args.size) contactsParams.append('size', args.size);
        if (args.search) contactsParams.append('search', args.search);
        if (args.email) contactsParams.append('email', args.email);
        
        return await makeTrackHSRequest(`/crm/contacts?${contactsParams.toString()}`);
      
      case 'get_reservation':
        if (!args.reservationId) {
          throw new Error('reservationId es requerido');
        }
        return await makeTrackHSRequest(`/reservations/${args.reservationId}`);
      
      case 'search_reservations':
        const searchParams = new URLSearchParams();
        if (args.page) searchParams.append('page', args.page);
        if (args.size) searchParams.append('size', args.size);
        if (args.search) searchParams.append('search', args.search);
        if (args.nodeId) searchParams.append('nodeId', args.nodeId);
        if (args.unitId) searchParams.append('unitId', args.unitId);
        if (args.status) searchParams.append('status', args.status);
        
        return await makeTrackHSRequest(`/reservations/search?${searchParams.toString()}`);
      
      case 'get_nodes':
        const nodesParams = new URLSearchParams();
        if (args.page) nodesParams.append('page', args.page);
        if (args.size) nodesParams.append('size', args.size);
        if (args.search) nodesParams.append('search', args.search);
        
        return await makeTrackHSRequest(`/nodes?${nodesParams.toString()}`);
      
      case 'get_node':
        if (!args.nodeId) {
          throw new Error('nodeId es requerido');
        }
        return await makeTrackHSRequest(`/nodes/${args.nodeId}`);
      
      case 'get_units':
        const unitsParams = new URLSearchParams();
        if (args.page) unitsParams.append('page', args.page);
        if (args.size) unitsParams.append('size', args.size);
        if (args.search) unitsParams.append('search', args.search);
        if (args.nodeId) unitsParams.append('nodeId', args.nodeId);
        
        return await makeTrackHSRequest(`/units?${unitsParams.toString()}`);
      
      case 'get_unit':
        if (!args.unitId) {
          throw new Error('unitId es requerido');
        }
        return await makeTrackHSRequest(`/units/${args.unitId}`);
      
      case 'get_ledger_accounts':
        const ledgerParams = new URLSearchParams();
        if (args.page) ledgerParams.append('page', args.page);
        if (args.size) ledgerParams.append('size', args.size);
        if (args.search) ledgerParams.append('search', args.search);
        if (args.category) ledgerParams.append('category', args.category);
        if (args.isActive !== undefined) ledgerParams.append('isActive', args.isActive);
        
        return await makeTrackHSRequest(`/pms/accounting/accounts?${ledgerParams.toString()}`);
      
      case 'get_ledger_account':
        if (!args.accountId) {
          throw new Error('accountId es requerido');
        }
        return await makeTrackHSRequest(`/pms/accounting/accounts/${args.accountId}`);
      
      case 'get_folios_collection':
        const foliosParams = new URLSearchParams();
        if (args.page) foliosParams.append('page', args.page);
        if (args.size) foliosParams.append('size', args.size);
        if (args.search) foliosParams.append('search', args.search);
        if (args.type) foliosParams.append('type', args.type);
        if (args.status) foliosParams.append('status', args.status);
        
        return await makeTrackHSRequest(`/pms/accounting/folios?${foliosParams.toString()}`);
      
      case 'get_maintenance_work_orders':
        const maintenanceParams = new URLSearchParams();
        if (args.page) maintenanceParams.append('page', args.page);
        if (args.size) maintenanceParams.append('size', args.size);
        if (args.search) maintenanceParams.append('search', args.search);
        if (args.status) maintenanceParams.append('status', args.status);
        
        return await makeTrackHSRequest(`/maintenance/work-orders?${maintenanceParams.toString()}`);
      
      case 'get_reviews':
        const reviewsParams = new URLSearchParams();
        if (args.page) reviewsParams.append('page', args.page);
        if (args.size) reviewsParams.append('size', args.size);
        if (args.search) reviewsParams.append('search', args.search);
        if (args.updatedSince) reviewsParams.append('updatedSince', args.updatedSince);
        
        return await makeTrackHSRequest(`/channel-management/channel/reviews?${reviewsParams.toString()}`);
      
      case 'get_reservation_notes':
        if (!args.reservationId) {
          throw new Error('reservationId es requerido');
        }
        
        const notesParams = new URLSearchParams();
        if (args.page) notesParams.append('page', args.page);
        if (args.size) notesParams.append('size', args.size);
        
        return await makeTrackHSRequest(`/reservations/${args.reservationId}/notes?${notesParams.toString()}`);
      
      default:
        throw new Error(`Herramienta desconocida: ${toolName}`);
    }
  } catch (error) {
    throw new Error(`Error ejecutando herramienta ${toolName}: ${error.message}`);
  }
}

// Manejar request JSON-RPC 2.0
async function handleMCPRequest(request) {
  const { jsonrpc, id, method, params } = request;
  
  // Validar JSON-RPC 2.0
  if (jsonrpc !== '2.0') {
    return {
      jsonrpc: '2.0',
      id,
      error: {
        code: -32600,
        message: 'Invalid Request: Solo se soporta JSON-RPC 2.0'
      }
    };
  }

  try {
    switch (method) {
      case 'initialize':
        return {
          jsonrpc: '2.0',
          id,
          result: {
            protocolVersion: '2025-06-18',
            capabilities: {
              tools: {
                listChanged: true
              },
              resources: {}
            },
            serverInfo: {
              name: 'trackhs-mcp-server',
              version: '1.0.0'
            }
          }
        };

      case 'tools/list':
        return {
          jsonrpc: '2.0',
          id,
          result: {
            tools: MCP_TOOLS
          }
        };

      case 'tools/call':
        if (!params || !params.name) {
          return {
            jsonrpc: '2.0',
            id,
            error: {
              code: -32602,
              message: 'Invalid params: name is required'
            }
          };
        }
        
        const { name, arguments: args } = params;
        const result = await executeMCPTool(name, args || {});
        return {
          jsonrpc: '2.0',
          id,
          result: {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          }
        };

      default:
        return {
          jsonrpc: '2.0',
          id,
          error: {
            code: -32601,
            message: `Method not found: ${method}`
          }
        };
    }
  } catch (error) {
    console.error(`Error en MCP request ${method}:`, error);
    return {
      jsonrpc: '2.0',
      id,
      error: {
        code: -32603,
        message: error.message,
        data: process.env.NODE_ENV === 'development' ? error.stack : undefined
      }
    };
  }
}

// Parsear JSON del body
async function parseJSONBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => data += chunk);
    req.on('end', () => {
      try {
        resolve(JSON.parse(data));
      } catch (error) {
        reject(new Error('Invalid JSON'));
      }
    });
  });
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
        service: 'Track HS MCP Unified Server',
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
        tools: MCP_TOOLS,
        count: MCP_TOOLS.length
      });
      return;
    }

    // MCP JSON-RPC 2.0 endpoint
    if (req.method === 'POST') {
      const body = await parseJSONBody(req);
      const response = await handleMCPRequest(body);
      res.status(200).json(response);
      return;
    }

    // Default response
    res.status(200).json({
      message: 'Track HS MCP Unified Server',
      version: '1.0.0',
      endpoints: {
        health: '/health',
        tools: '/tools',
        mcp: 'POST / (JSON-RPC 2.0)'
      },
      tools: {
        count: MCP_TOOLS.length,
        available: MCP_TOOLS.map(t => t.name)
      }
    });

  } catch (error) {
    console.error('Error en servidor MCP unificado:', error);
    
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
        timestamp: new Date().toISOString()
      });
    }
  }
}
