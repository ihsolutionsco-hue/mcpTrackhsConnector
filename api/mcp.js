/**
 * Endpoint HTTP para el servidor MCP de Track HS
 * Compatible con Vercel y servidores remotos MCP
 * Implementa el protocolo MCP completo para Claude Desktop
 */

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
    if (req.method === 'GET') {
      // Endpoint de información del servidor
      res.status(200).json({
        name: 'Track HS MCP Server',
        version: '1.0.0',
        description: 'MCP Server para Track HS API',
        endpoints: {
          tools: '/api/mcp/tools',
          execute: '/api/mcp/execute'
        },
        status: 'active'
      });
      return;
    }

    if (req.method === 'POST') {
      const { method, params, id } = req.body;

      // 1. INICIALIZACIÓN MCP - Requerido por Claude Desktop
      if (method === 'initialize') {
        res.status(200).json({
          jsonrpc: '2.0',
          id: id || 1,
          result: {
            protocolVersion: '2025-06-18',
            capabilities: {
              tools: {
                listChanged: true
              },
              resources: {},
              prompts: {}
            },
            serverInfo: {
              name: 'trackhs-mcp-server',
              version: '1.0.0'
            }
          }
        });
        return;
      }

      // 2. NOTIFICACIÓN DE INICIALIZACIÓN COMPLETADA
      if (method === 'notifications/initialized') {
        res.status(200).json({
          jsonrpc: '2.0',
          result: { success: true }
        });
        return;
      }

      // 3. LISTAR HERRAMIENTAS DISPONIBLES
      if (method === 'tools/list') {
        const tools = [
          {
            name: 'get_reviews',
            description: 'Obtener reseñas de propiedades',
            inputSchema: {
              type: 'object',
              properties: {
                property_id: { type: 'string', description: 'ID de la propiedad' }
              }
            }
          },
          {
            name: 'get_reservation',
            description: 'Obtener detalles de una reserva específica',
            inputSchema: {
              type: 'object',
              properties: {
                reservation_id: { type: 'string', description: 'ID de la reserva' }
              },
              required: ['reservation_id']
            }
          },
          {
            name: 'search_reservations',
            description: 'Buscar reservas con filtros',
            inputSchema: {
              type: 'object',
              properties: {
                query: { type: 'string', description: 'Término de búsqueda' },
                status: { type: 'string', description: 'Estado de la reserva' }
              }
            }
          },
          {
            name: 'get_units',
            description: 'Listar unidades disponibles',
            inputSchema: {
              type: 'object',
              properties: {
                property_id: { type: 'string', description: 'ID de la propiedad' }
              }
            }
          },
          {
            name: 'get_unit',
            description: 'Obtener detalles de una unidad específica',
            inputSchema: {
              type: 'object',
              properties: {
                unit_id: { type: 'string', description: 'ID de la unidad' }
              },
              required: ['unit_id']
            }
          },
          {
            name: 'get_contacts',
            description: 'Obtener lista de contactos',
            inputSchema: {
              type: 'object',
              properties: {
                limit: { type: 'number', description: 'Número máximo de contactos' }
              }
            }
          },
          {
            name: 'get_ledger_accounts',
            description: 'Listar cuentas contables',
            inputSchema: {
              type: 'object',
              properties: {
                account_type: { type: 'string', description: 'Tipo de cuenta' }
              }
            }
          },
          {
            name: 'get_ledger_account',
            description: 'Obtener cuenta contable específica',
            inputSchema: {
              type: 'object',
              properties: {
                account_id: { type: 'string', description: 'ID de la cuenta' }
              },
              required: ['account_id']
            }
          },
          {
            name: 'get_reservation_notes',
            description: 'Obtener notas de una reserva',
            inputSchema: {
              type: 'object',
              properties: {
                reservation_id: { type: 'string', description: 'ID de la reserva' }
              },
              required: ['reservation_id']
            }
          },
          {
            name: 'get_nodes',
            description: 'Listar nodos del sistema',
            inputSchema: {
              type: 'object',
              properties: {
                node_type: { type: 'string', description: 'Tipo de nodo' }
              }
            }
          },
          {
            name: 'get_node',
            description: 'Obtener nodo específico',
            inputSchema: {
              type: 'object',
              properties: {
                node_id: { type: 'string', description: 'ID del nodo' }
              },
              required: ['node_id']
            }
          },
          {
            name: 'get_maintenance_work_orders',
            description: 'Obtener órdenes de trabajo de mantenimiento',
            inputSchema: {
              type: 'object',
              properties: {
                status: { type: 'string', description: 'Estado de la orden' }
              }
            }
          },
          {
            name: 'get_folios_collection',
            description: 'Obtener colección de folios',
            inputSchema: {
              type: 'object',
              properties: {
                date_from: { type: 'string', description: 'Fecha desde' },
                date_to: { type: 'string', description: 'Fecha hasta' }
              }
            }
          }
        ];

        res.status(200).json({
          jsonrpc: '2.0',
          id: id || 1,
          result: { tools }
        });
        return;
      }

      // 4. EJECUTAR HERRAMIENTAS
      if (method === 'tools/call') {
        const { name, arguments: args } = params;
        
        // Simular respuesta para herramientas (en producción esto conectaría con la API real)
        const mockResponse = {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: name,
                arguments: args,
                result: `Ejecutando herramienta ${name} con argumentos: ${JSON.stringify(args)}`,
                timestamp: new Date().toISOString(),
                status: 'success'
              }, null, 2)
            }
          ]
        };

        res.status(200).json({
          jsonrpc: '2.0',
          id: id || 1,
          result: mockResponse
        });
        return;
      }

      // 5. RECURSOS (opcional para MCP)
      if (method === 'resources/list') {
        res.status(200).json({
          jsonrpc: '2.0',
          id: id || 1,
          result: { resources: [] }
        });
        return;
      }

      // 6. PROMPTS (opcional para MCP)
      if (method === 'prompts/list') {
        res.status(200).json({
          jsonrpc: '2.0',
          id: id || 1,
          result: { prompts: [] }
        });
        return;
      }

      // Método no soportado
      res.status(400).json({
        jsonrpc: '2.0',
        id: id || 1,
        error: {
          code: -32601,
          message: `Método no soportado: ${method}`
        }
      });
      return;
    }

    res.status(405).json({ error: 'Método no permitido' });
  } catch (error) {
    console.error('Error en endpoint MCP:', error);
    res.status(500).json({
      jsonrpc: '2.0',
      id: req.body?.id || 1,
      error: {
        code: -32603,
        message: 'Error interno del servidor'
      }
    });
  }
}