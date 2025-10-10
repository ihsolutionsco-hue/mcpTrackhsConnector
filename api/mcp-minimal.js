/**
 * Endpoint MCP minimalista para Vercel
 * Versión ultra-simplificada que funciona
 */

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
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
      case 'initialize':
        result = {
          protocolVersion: '2025-06-18',
          capabilities: {
            tools: { listChanged: true },
            resources: {},
            prompts: {}
          },
          serverInfo: {
            name: 'trackhs-mcp-connector',
            version: '1.0.0'
          }
        };
        break;

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
            }
          ]
        };
        break;

      case 'tools/call':
        result = {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: params?.name || 'unknown',
                message: 'Herramienta ejecutada correctamente',
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
              title: 'Estado del Sistema TrackHS',
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

      case 'notifications/initialized':
        result = { success: true };
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
}
