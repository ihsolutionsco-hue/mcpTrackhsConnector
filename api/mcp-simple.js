/**
 * Endpoint MCP simplificado para Vercel
 */

const express = require('express');
const app = express();

app.use(express.json());

// CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

// Endpoint principal MCP
app.post('/', async (req, res) => {
  console.log('MCP Request:', JSON.stringify(req.body, null, 2));
  
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
            }
          ]
        };
        break;

      case 'tools/call':
        const { name, arguments: args } = params;
        
        if (name === 'get_contacts') {
          // Simular respuesta de contactos
          result = {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  data: [
                    { id: 1, name: 'Juan Pérez', email: 'juan@example.com' },
                    { id: 2, name: 'María García', email: 'maria@example.com' }
                  ],
                  meta: { page: 1, total: 2 }
                }, null, 2)
              }
            ]
          };
        } else if (name === 'get_units') {
          // Simular respuesta de unidades
          result = {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  data: [
                    { id: 1, name: 'Suite Deluxe', type: 'suite', capacity: 4 },
                    { id: 2, name: 'Habitación Estándar', type: 'room', capacity: 2 }
                  ],
                  meta: { page: 1, total: 2 }
                }, null, 2)
              }
            ]
          };
        } else {
          throw new Error(`Herramienta desconocida: ${name}`);
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

    res.json({
      jsonrpc: '2.0',
      result,
      id
    });

  } catch (error) {
    console.error('Error:', error);
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
    service: 'Track HS MCP Server (Simple)',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Default GET
app.get('/', (req, res) => {
  res.json({
    message: 'Track HS MCP Server (Simple)',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      mcp: 'POST / (JSON-RPC 2.0)'
    }
  });
});

module.exports = app;
