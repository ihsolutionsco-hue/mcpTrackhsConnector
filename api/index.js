/**
 * Servidor MCP Remoto para Track HS - Vercel API (JavaScript)
 *
 * Este archivo implementa el servidor API para Vercel que expone
 * las herramientas MCP de Track HS como endpoints REST.
 */

const { TrackHSMCPServer } = require('../dist/server.js');

// Instancia global del servidor MCP
let mcpServer = null;

/**
 * Inicializa el servidor MCP si no existe
 */
function getMCPServer() {
  if (!mcpServer) {
    try {
      mcpServer = new TrackHSMCPServer();
    } catch (error) {
      console.error('Error al inicializar servidor MCP:', error);
      throw new Error('Error al inicializar servidor MCP');
    }
  }
  return mcpServer;
}

/**
 * Maneja las peticiones CORS
 */
function handleCORS(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

/**
 * Parse el body de la request si es JSON
 */
async function parseBody(req) {
  return new Promise((resolve, reject) => {
    if (req.method !== 'POST') {
      resolve({});
      return;
    }

    // Si Vercel ya parseó el body
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

/**
 * Endpoint principal - Health Check
 */
module.exports = async function handler(req, res) {
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
    if (path === '/api/health' || path === '/health' || path === '/api') {
      return handleHealth(req, res);
    }

    if (path === '/api/tools' || path === '/tools') {
      return handleListTools(req, res);
    }

    if (path.startsWith('/api/tools/') || (path.startsWith('/tools/') && path.includes('/execute'))) {
      return handleExecuteTool(req, res);
    }

    // Endpoint por defecto
    return handleDefault(req, res);

  } catch (error) {
    console.error('Error en servidor MCP:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error instanceof Error ? error.message : 'Error desconocido',
      timestamp: new Date().toISOString()
    });
  }
};

/**
 * Health Check - Verifica el estado del servidor
 */
async function handleHealth(req, res) {
  try {
    const server = getMCPServer();
    const tools = server.tools.map(tool => tool.name);
    
    res.status(200).json({
      status: 'healthy',
      service: 'Track HS MCP Connector',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      tools: {
        count: tools.length,
        available: tools
      },
      environment: {
        nodeEnv: process.env.NODE_ENV || 'development',
        vercelUrl: process.env.VERCEL_URL || 'local'
      }
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      error: error instanceof Error ? error.message : 'Error desconocido',
      timestamp: new Date().toISOString()
    });
  }
}

/**
 * Listar herramientas disponibles
 */
async function handleListTools(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ 
      error: 'Método no permitido',
      allowed: ['GET']
    });
    return;
  }

  try {
    const server = getMCPServer();
    const tools = server.tools.map(tool => ({
      name: tool.name,
      description: tool.description,
      inputSchema: tool.inputSchema
    }));

    res.status(200).json({
      success: true,
      tools,
      count: tools.length,
      service: 'Track HS MCP Connector',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Error al obtener herramientas',
      message: error instanceof Error ? error.message : 'Error desconocido'
    });
  }
}

/**
 * Ejecutar herramienta específica
 */
async function handleExecuteTool(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({
      error: 'Método no permitido',
      allowed: ['POST']
    });
    return;
  }

  try {
    const server = getMCPServer();

    // Parse body correctamente
    const body = await parseBody(req);
    const { name, arguments: args } = body;

    if (!name) {
      res.status(400).json({
        success: false,
        error: 'Nombre de herramienta requerido',
        required: ['name'],
        example: {
          name: 'get_reviews',
          arguments: { page: 1, size: 10 }
        }
      });
      return;
    }

    const tool = server.tools.find(t => t.name === name);
    if (!tool) {
      res.status(404).json({
        success: false,
        error: `Herramienta '${name}' no encontrada`,
        available: server.tools.map(t => t.name)
      });
      return;
    }

    console.log(`Ejecutando herramienta: ${name}`, args);

    const startTime = Date.now();
    const result = await tool.execute(args || {});
    const executionTime = Date.now() - startTime;

    res.status(200).json({
      success: true,
      result,
      tool: name,
      timestamp: new Date().toISOString(),
      executionTime: `${executionTime}ms`
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
    console.error(`Error ejecutando herramienta:`, error);

    res.status(500).json({
      success: false,
      error: `Error en ejecución de herramienta: ${errorMessage}`,
      timestamp: new Date().toISOString()
    });
  }
}

/**
 * Endpoint por defecto - Información del servicio
 */
async function handleDefault(req, res) {
  res.status(200).json({
    service: 'Track HS MCP Connector',
    version: '1.0.0',
    description: 'Conector MCP remoto para Track HS API',
    endpoints: {
      health: {
        method: 'GET',
        path: '/api/health',
        description: 'Health check del servicio'
      },
      tools: {
        method: 'GET',
        path: '/api/tools',
        description: 'Listar herramientas disponibles'
      },
      execute: {
        method: 'POST',
        path: '/api/tools/{name}/execute',
        description: 'Ejecutar herramienta específica',
        body: {
          name: 'string (required)',
          arguments: 'object (optional)'
        }
      }
    },
    documentation: 'https://github.com/your-repo/trackhs-mcp-connector',
    timestamp: new Date().toISOString()
  });
}
