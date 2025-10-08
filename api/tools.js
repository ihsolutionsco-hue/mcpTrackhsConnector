/**
 * Endpoint para listar herramientas disponibles del Track HS MCP Connector
 */

export default function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Método no permitido' });
    return;
  }

  try {
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
      tools,
      count: tools.length,
      service: 'Track HS MCP Connector',
      version: '1.0.0'
    });
  } catch (error) {
    console.error('Error al obtener herramientas:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error.message
    });
  }
}