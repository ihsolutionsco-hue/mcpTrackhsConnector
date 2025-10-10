/**
 * Endpoint MCP optimizado para Vercel
 * Implementa Streamable HTTP transport usando Express + McpServer
 * Configurado para funcionar con Claude y otros clientes MCP
 * Endpoint principal: /mcp (según especificación MCP oficial)
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { z } from 'zod';

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

  // Validar formato de URL (validación simplificada)
  try {
    const url = new URL(process.env.TRACKHS_API_URL);
    console.log('URL validada correctamente:', url.href);
  } catch (error) {
    console.error('Error validando URL:', process.env.TRACKHS_API_URL);
    console.error('Error details:', error.message);
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
    console.log(`[TrackHS API] Método: ${options.method || 'GET'}`);
    
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
      
      console.log(`[TrackHS API] Respuesta recibida: ${response.status} ${response.statusText}`);
      console.log(`[TrackHS API] Headers:`, Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`[TrackHS API] Error ${response.status}: ${errorText}`);
        throw new Error(`Track HS API Error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        console.log(`[TrackHS API] Datos JSON recibidos:`, JSON.stringify(data, null, 2));
        return data;
      } else {
        const text = await response.text();
        console.log(`[TrackHS API] Datos de texto recibidos:`, text);
        return text;
      }
    } catch (error) {
      console.error(`[TrackHS API] Error en petición:`, error);
      if (error instanceof Error) {
        throw new Error(`Error en petición a Track HS: ${error.message}`);
      }
      throw new Error('Error desconocido en petición a Track HS');
    }
  }

  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }
}

// Crear servidor MCP con high-level API
const mcpServer = new McpServer({
  name: 'trackhs-mcp-server',
  version: '1.0.0'
});

// Inicializar cliente API
let apiClient = null;

// Logging de variables de entorno para debugging
console.log('[MCP Server] Verificando variables de entorno:');
console.log('[MCP Server] TRACKHS_API_URL:', process.env.TRACKHS_API_URL ? '***configurado***' : 'NO CONFIGURADO');
console.log('[MCP Server] TRACKHS_USERNAME:', process.env.TRACKHS_USERNAME ? '***configurado***' : 'NO CONFIGURADO');
console.log('[MCP Server] TRACKHS_PASSWORD:', process.env.TRACKHS_PASSWORD ? '***configurado***' : 'NO CONFIGURADO');

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
  console.error('[MCP Server] Stack trace:', error.stack);
}

// Registrar herramientas MCP
if (apiClient) {
  console.log('[MCP Server] Registrando herramientas MCP...');
  // Herramienta: Obtener contactos
  mcpServer.registerTool(
    'get_contacts',
    {
      title: 'Obtener Contactos',
      description: 'Retrieve all contacts from Track HS CRM system',
      inputSchema: {
        sortColumn: z.enum(['id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip']).optional(),
        sortDirection: z.enum(['asc', 'desc']).default('asc'),
        search: z.string().optional(),
        term: z.string().optional(),
        email: z.string().email().optional(),
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional(),
        updatedSince: z.string().optional()
      }
    },
    async (params = {}) => {
      try {
        console.log(`[MCP Tool] get_contacts llamado con parámetros:`, params);
        
        const queryParams = new URLSearchParams();
        const sortDirection = params.sortDirection || 'asc';
        
        if (params.sortColumn) queryParams.append('sortColumn', params.sortColumn);
        queryParams.append('sortDirection', sortDirection);
        if (params.search) queryParams.append('search', params.search);
        if (params.term) queryParams.append('term', params.term);
        if (params.email) queryParams.append('email', params.email);
        if (params.page) queryParams.append('page', params.page.toString());
        if (params.size) queryParams.append('size', params.size.toString());
        if (params.updatedSince) queryParams.append('updatedSince', params.updatedSince);

        const endpoint = `/crm/contacts?${queryParams.toString()}`;
        console.log(`[MCP Tool] Endpoint construido: ${endpoint}`);
        
        const result = await apiClient.get(endpoint);
        console.log(`[MCP Tool] get_contacts exitoso, datos recibidos:`, result);
        
        // Formatear respuesta según protocolo MCP
        return formatMCPResponse(result);
      } catch (error) {
        console.error(`[MCP Tool] Error en get_contacts:`, error);
        throw new Error(`Error obteniendo contactos: ${error.message}`);
      }
    }
  );

  // Herramienta: Obtener reservación
  mcpServer.registerTool(
    'get_reservation',
    {
      title: 'Obtener Reservación',
      description: 'Get detailed information for a specific reservation by ID',
      inputSchema: {
        reservationId: z.string().describe('The ID of the reservation to retrieve')
      }
    },
    async ({ reservationId }) => {
      if (!reservationId || reservationId.trim() === '') {
        throw new Error('El ID de reservación no puede estar vacío');
      }
      const endpoint = `/v2/pms/reservations/${encodeURIComponent(reservationId)}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Buscar reservaciones
  mcpServer.registerTool(
    'search_reservations',
    {
      title: 'Buscar Reservaciones',
      description: 'Search reservations with various filters',
      inputSchema: {
        checkIn: z.string().optional(),
        checkOut: z.string().optional(),
        status: z.string().optional(),
        guestName: z.string().optional(),
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      try {
        console.log(`[MCP Tool] search_reservations llamado con parámetros:`, params);
        
        const queryParams = new URLSearchParams();
        if (params.checkIn) queryParams.append('checkIn', params.checkIn);
        if (params.checkOut) queryParams.append('checkOut', params.checkOut);
        if (params.status) queryParams.append('status', params.status);
        if (params.guestName) queryParams.append('guestName', params.guestName);
        if (params.page) queryParams.append('page', params.page.toString());
        if (params.size) queryParams.append('size', params.size.toString());

        const endpoint = `/v2/pms/reservations/search?${queryParams.toString()}`;
        console.log(`[MCP Tool] Endpoint construido: ${endpoint}`);
        
        const result = await apiClient.get(endpoint);
        console.log(`[MCP Tool] search_reservations exitoso, datos recibidos:`, result);
        
        // Formatear respuesta según protocolo MCP
        return formatMCPResponse(result);
      } catch (error) {
        console.error(`[MCP Tool] Error en search_reservations:`, error);
        throw new Error(`Error buscando reservaciones: ${error.message}`);
      }
    }
  );

  // Herramienta: Obtener unidades
  mcpServer.registerTool(
    'get_units',
    {
      title: 'Obtener Unidades',
      description: 'Get list of units/properties',
      inputSchema: {
        nodeId: z.string().optional(),
        status: z.string().optional(),
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.nodeId) queryParams.append('nodeId', params.nodeId);
      if (params.status) queryParams.append('status', params.status);
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/pms/units?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener unidad específica
  mcpServer.registerTool(
    'get_unit',
    {
      title: 'Obtener Unidad',
      description: 'Get specific unit details by ID',
      inputSchema: {
        unitId: z.string().describe('The ID of the unit to retrieve')
      }
    },
    async ({ unitId }) => {
      if (!unitId || unitId.trim() === '') {
        throw new Error('El ID de unidad no puede estar vacío');
      }
      const endpoint = `/pms/units/${encodeURIComponent(unitId)}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener reseñas
  mcpServer.registerTool(
    'get_reviews',
    {
      title: 'Obtener Reseñas',
      description: 'Get property reviews',
      inputSchema: {
        nodeId: z.string().optional(),
        rating: z.number().min(1).max(5).optional(),
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.nodeId) queryParams.append('nodeId', params.nodeId);
      if (params.rating) queryParams.append('rating', params.rating.toString());
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/pms/reviews?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener cuentas contables
  mcpServer.registerTool(
    'get_ledger_accounts',
    {
      title: 'Obtener Cuentas Contables',
      description: 'Get ledger accounts',
      inputSchema: {
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/pms/accounting/accounts?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener cuenta contable específica
  mcpServer.registerTool(
    'get_ledger_account',
    {
      title: 'Obtener Cuenta Contable',
      description: 'Get specific ledger account by ID',
      inputSchema: {
        accountId: z.string().describe('The ID of the account to retrieve')
      }
    },
    async ({ accountId }) => {
      if (!accountId || accountId.trim() === '') {
        throw new Error('El ID de cuenta no puede estar vacío');
      }
      const endpoint = `/pms/accounting/accounts/${encodeURIComponent(accountId)}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener folios
  mcpServer.registerTool(
    'get_folios_collection',
    {
      title: 'Obtener Folios',
      description: 'Get accounting folios collection',
      inputSchema: {
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/pms/accounting/folios?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener notas de reservación
  mcpServer.registerTool(
    'get_reservation_notes',
    {
      title: 'Obtener Notas de Reservación',
      description: 'Get notes for a specific reservation',
      inputSchema: {
        reservationId: z.string().describe('The ID of the reservation')
      }
    },
    async ({ reservationId }) => {
      if (!reservationId || reservationId.trim() === '') {
        throw new Error('El ID de reservación no puede estar vacío');
      }
      const endpoint = `/v2/pms/reservations/${encodeURIComponent(reservationId)}/notes`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener nodos
  mcpServer.registerTool(
    'get_nodes',
    {
      title: 'Obtener Nodos',
      description: 'Get list of nodes/properties',
      inputSchema: {
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/pms/nodes?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener nodo específico
  mcpServer.registerTool(
    'get_node',
    {
      title: 'Obtener Nodo',
      description: 'Get specific node by ID',
      inputSchema: {
        nodeId: z.string().describe('The ID of the node to retrieve')
      }
    },
    async ({ nodeId }) => {
      if (!nodeId || nodeId.trim() === '') {
        throw new Error('El ID de nodo no puede estar vacío');
      }
      const endpoint = `/pms/nodes/${encodeURIComponent(nodeId)}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );

  // Herramienta: Obtener órdenes de trabajo
  mcpServer.registerTool(
    'get_maintenance_work_orders',
    {
      title: 'Obtener Órdenes de Trabajo',
      description: 'Get maintenance work orders',
      inputSchema: {
        status: z.string().optional(),
        priority: z.string().optional(),
        page: z.number().min(1).optional(),
        size: z.number().min(1).max(100).optional()
      }
    },
    async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.status) queryParams.append('status', params.status);
      if (params.priority) queryParams.append('priority', params.priority);
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.size) queryParams.append('size', params.size.toString());

      const endpoint = `/maintenance/work-orders?${queryParams.toString()}`;
      const result = await apiClient.get(endpoint);
      return formatMCPResponse(result);
    }
  );
  
  console.log('[MCP Server] Todas las herramientas MCP registradas correctamente');
} else {
  console.error('[MCP Server] ERROR: No se pudo inicializar el cliente API. Las herramientas MCP no estarán disponibles.');
}

// Registrar recursos MCP
mcpServer.registerResource(
  'trackhs://schema/reservations',
  {
    title: 'Esquema de Reservas',
    description: 'Esquema de datos para reservas en TrackHS',
    mimeType: 'application/json'
  },
  async () => ({
    contents: [{
      uri: 'trackhs://schema/reservations',
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
    }]
  })
);

mcpServer.registerResource(
  'trackhs://status/system',
  {
    title: 'Estado del Sistema',
    description: 'Estado actual del sistema TrackHS y configuración',
    mimeType: 'application/json'
  },
  async () => ({
    contents: [{
      uri: 'trackhs://status/system',
              text: JSON.stringify({
                status: 'operational',
                timestamp: new Date().toISOString(),
                version: '1.0.0',
                apiUrl: process.env.TRACKHS_API_URL,
                capabilities: ['tools', 'resources', 'prompts']
              }, null, 2)
    }]
  })
);

// Registrar prompts MCP
mcpServer.registerPrompt(
  'check-today-reservations',
  {
          title: 'Revisar Reservas de Hoy',
          description: 'Obtener todas las reservas que llegan o salen hoy',
    argsSchema: {
      date: z.string().optional().describe('Fecha en formato YYYY-MM-DD (por defecto: hoy)')
    }
  },
  ({ date }) => ({
    messages: [{
              role: 'user',
              content: {
                type: 'text',
        text: `Por favor, revisa todas las reservas para la fecha ${date || new Date().toISOString().split('T')[0]}. Incluye:
1. Reservas que llegan hoy (check-in)
2. Reservas que salen hoy (check-out)
3. Reservas que están activas hoy
4. Un resumen de ocupación por nodo/unidad

Usa las herramientas disponibles para obtener esta información.`
              }
    }]
  })
);

mcpServer.registerPrompt(
  'unit-availability',
  {
    title: 'Consultar Disponibilidad de Unidades',
    description: 'Verificar disponibilidad de unidades para fechas específicas',
    argsSchema: {
      checkIn: z.string().describe('Fecha de entrada en formato YYYY-MM-DD'),
      checkOut: z.string().describe('Fecha de salida en formato YYYY-MM-DD'),
      nodeId: z.string().optional().describe('ID del nodo específico (opcional)')
    }
  },
  ({ checkIn, checkOut, nodeId }) => ({
    messages: [{
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
    }]
  })
);

// Configurar rutas de Express
app.post('/', async (req, res) => {
  console.log('POST request received:', {
    method: req.method,
    url: req.url,
    body: req.body
  });
  
  try {
    // Crear transport para cada petición (stateless)
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true
    });

    res.on('close', () => {
      transport.close();
    });

    await mcpServer.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error('Error handling MCP request:', error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error'
        },
        id: null
      });
    }
  }
});

// Handle OPTIONS for CORS preflight
app.options('*', (req, res) => {
  res.status(200).end();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
        status: 'healthy',
        service: 'Track HS MCP Server',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        capabilities: ['tools', 'resources', 'prompts'],
        apiUrl: process.env.TRACKHS_API_URL,
        environment: {
          trackhsConfigured: !!(process.env.TRACKHS_API_URL && process.env.TRACKHS_USERNAME && process.env.TRACKHS_PASSWORD),
          hasApiClient: !!apiClient,
          apiUrl: process.env.TRACKHS_API_URL,
          username: process.env.TRACKHS_USERNAME ? '***configured***' : 'missing',
          password: process.env.TRACKHS_PASSWORD ? '***configured***' : 'missing'
        }
        });
});

// Test Track HS connectivity endpoint
app.get('/test-connectivity', async (req, res) => {
  try {
    if (!apiClient) {
      return res.status(500).json({
        success: false,
        error: 'API Client no inicializado',
        environment: {
          trackhsConfigured: !!(process.env.TRACKHS_API_URL && process.env.TRACKHS_USERNAME && process.env.TRACKHS_PASSWORD),
          apiUrl: process.env.TRACKHS_API_URL,
          username: process.env.TRACKHS_USERNAME ? '***configured***' : 'missing',
          password: process.env.TRACKHS_PASSWORD ? '***configured***' : 'missing'
        }
      });
    }

    // Probar conectividad básica con un endpoint simple
    const testResult = await apiClient.get('/crm/contacts?page=1&size=1');
    
    res.json({
      success: true,
      message: 'Conectividad con Track HS exitosa',
      testResult: testResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error en test de conectividad:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      details: error.stack,
      timestamp: new Date().toISOString()
    });
  }
});

// Tools list endpoint
app.get('/tools', (req, res) => {
  res.json({
        success: true,
    message: 'Track HS MCP Server',
          version: '1.0.0',
    endpoints: {
      health: '/health',
      tools: '/tools',
      testConnectivity: '/test-connectivity',
      mcp: 'POST /mcp (JSON-RPC 2.0)'
    },
    capabilities: ['tools', 'resources', 'prompts'],
    documentation: {
      connection: 'Use this endpoint as a Custom Connector in Claude',
      url: 'https://trackhs-mcp-connector.vercel.app/api/mcp',
      transport: 'Streamable HTTP'
    }
  });
});

// Default GET response
app.get('/', (req, res) => {
  console.log('GET request received:', {
    method: req.method,
    url: req.url
  });
  
  res.json({
      message: 'Track HS MCP Server',
      version: '1.0.0',
      endpoints: {
        health: '/health',
        tools: '/tools',
        mcp: 'POST / (JSON-RPC 2.0)'
      },
      capabilities: ['tools', 'resources', 'prompts'],
      documentation: {
        connection: 'Use this endpoint as a Custom Connector in Claude',
        url: 'https://trackhs-mcp-connector.vercel.app/api/mcp',
        transport: 'Streamable HTTP'
      }
  });
});

// Handle /api/mcp specifically
app.get('/api/mcp', (req, res) => {
  console.log('GET /api/mcp request received:', {
    method: req.method,
    url: req.url
  });
  
  res.json({
      message: 'Track HS MCP Server',
      version: '1.0.0',
      endpoints: {
        health: '/health',
        tools: '/tools',
        mcp: 'POST /api/mcp (JSON-RPC 2.0)'
      },
      capabilities: ['tools', 'resources', 'prompts'],
      documentation: {
        connection: 'Use this endpoint as a Custom Connector in Claude',
        url: 'https://trackhs-mcp-connector.vercel.app/api/mcp',
        transport: 'Streamable HTTP'
      }
  });
});

// Endpoint MCP principal según especificación oficial
app.post('/mcp', async (req, res) => {
  console.log('POST /mcp request received:', {
    method: req.method,
    url: req.url,
    body: req.body,
    headers: req.headers
  });
  
  try {
    console.log('[MCP Handler] Iniciando manejo de petición MCP');
    console.log('[MCP Handler] Cliente API disponible:', !!apiClient);
    
    // Crear transport para cada petición (stateless) según especificación MCP
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true
    });

    // Configurar manejo de cierre de conexión
    res.on('close', () => {
      console.log('[MCP Handler] Conexión cerrada, limpiando transport');
      transport.close();
    });

    console.log('[MCP Handler] Transport creado, conectando con servidor MCP...');
    await mcpServer.connect(transport);
    
    console.log('[MCP Handler] Servidor MCP conectado, manejando petición...');
    await transport.handleRequest(req, res, req.body);
    
    console.log('[MCP Handler] Petición MCP manejada exitosamente');
  } catch (error) {
    console.error('[MCP Handler] Error handling MCP request:', error);
    console.error('[MCP Handler] Error stack:', error.stack);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
          details: error.message
        },
        id: null
      });
    }
  }
});

// Exportar handler compatible con Vercel serverless
export default async (req, res) => {
  console.log('Vercel handler called:', req.method, req.url);
  return app(req, res);
};