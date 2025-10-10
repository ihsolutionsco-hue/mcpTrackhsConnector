/**
 * Endpoint MCP optimizado para Vercel
 * Versión simplificada que funciona correctamente
 */

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  console.log('[MCP] Request:', {
    method: req.method,
    url: req.url,
    body: req.body
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
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_reviews',
              description: 'Get property reviews',
              inputSchema: {
                type: 'object',
                properties: {
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
        
        // Simular respuesta para testing
        result = {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: name,
                arguments: args,
                data: [
                  { id: 1, name: 'Datos simulados', type: 'test' }
                ],
                meta: { page: 1, total: 1, simulated: true },
                timestamp: new Date().toISOString()
              }, null, 2)
            }
          ]
        };
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

    console.log('[MCP] Respuesta:', { method, result: result ? 'OK' : 'NULL' });
    
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
      id: req.body?.id || null
    });
  }
};
