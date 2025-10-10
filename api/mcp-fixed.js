/**
 * Endpoint MCP corregido para Vercel
 * Implementa correctamente el protocolo MCP según la teoría
 */

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  console.log('[MCP] Request recibido:', {
    method: req.method,
    url: req.url,
    body: req.body
  });

  try {
    // Validar que sea POST
    if (req.method !== 'POST') {
      return res.status(405).json({
        jsonrpc: '2.0',
        error: { code: -32600, message: 'Method not allowed' },
        id: null
      });
    }

    const { jsonrpc, method, params, id } = req.body;

    // Validación básica de JSON-RPC 2.0
    if (jsonrpc !== '2.0') {
      return res.status(400).json({
        jsonrpc: '2.0',
        error: { code: -32600, message: 'Invalid Request' },
        id: null
      });
    }

    // Validación de parámetros requeridos
    if (!method) {
      return res.status(400).json({
        jsonrpc: '2.0',
        error: { code: -32600, message: 'Method is required' },
        id: id || null
      });
    }

    let result = null;

    switch (method) {
      case 'initialize':
        result = {
          protocolVersion: '2025-06-18',
          capabilities: {
            tools: {
              listChanged: true
            },
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
                  sortColumn: { type: 'string', enum: ['id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip'] },
                  sortDirection: { type: 'string', enum: ['asc', 'desc'], default: 'asc' },
                  search: { type: 'string' },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_reservation',
              description: 'Get detailed information for a specific reservation by ID',
              inputSchema: {
                type: 'object',
                properties: {
                  reservationId: { type: 'string', description: 'The ID of the reservation to retrieve' }
                },
                required: ['reservationId']
              }
            },
            {
              name: 'search_reservations',
              description: 'Search reservations with various filters',
              inputSchema: {
                type: 'object',
                properties: {
                  checkIn: { type: 'string' },
                  checkOut: { type: 'string' },
                  status: { type: 'string' },
                  guestName: { type: 'string' },
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
                  nodeId: { type: 'string' },
                  status: { type: 'string' },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            },
            {
              name: 'get_unit',
              description: 'Get specific unit details by ID',
              inputSchema: {
                type: 'object',
                properties: {
                  unitId: { type: 'string', description: 'The ID of the unit to retrieve' }
                },
                required: ['unitId']
              }
            },
            {
              name: 'get_reviews',
              description: 'Get property reviews',
              inputSchema: {
                type: 'object',
                properties: {
                  nodeId: { type: 'string' },
                  rating: { type: 'number', minimum: 1, maximum: 5 },
                  page: { type: 'number', minimum: 1 },
                  size: { type: 'number', minimum: 1, maximum: 100 }
                }
              }
            }
          ]
        };
        break;

      case 'tools/call':
        if (!params || !params.name) {
          return res.status(400).json({
            jsonrpc: '2.0',
            error: { code: -32602, message: 'Invalid params - tool name is required' },
            id
          });
        }
        
        const { name, arguments: args } = params;
        
        // Verificar configuración
        if (!process.env.TRACKHS_API_URL || !process.env.TRACKHS_USERNAME || !process.env.TRACKHS_PASSWORD) {
          result = {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: 'API no configurada',
                  message: 'Variables de entorno de TrackHS no configuradas',
                  required: ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'],
                  current: {
                    apiUrl: process.env.TRACKHS_API_URL,
                    hasUsername: !!process.env.TRACKHS_USERNAME,
                    hasPassword: !!process.env.TRACKHS_PASSWORD
                  }
                }, null, 2)
              }
            ]
          };
        } else {
          // Llamada a API real
          try {
            const apiUrl = process.env.TRACKHS_API_URL;
            const auth = Buffer.from(`${process.env.TRACKHS_USERNAME}:${process.env.TRACKHS_PASSWORD}`).toString('base64');
            
            let endpoint = '';
            let queryParams = new URLSearchParams();
            
            switch (name) {
              case 'get_contacts':
                endpoint = '/crm/contacts';
                if (args.sortColumn) queryParams.append('sortColumn', args.sortColumn);
                if (args.sortDirection) queryParams.append('sortDirection', args.sortDirection);
                if (args.search) queryParams.append('search', args.search);
                if (args.page) queryParams.append('page', args.page.toString());
                if (args.size) queryParams.append('size', args.size.toString());
                break;
                
              case 'get_reservation':
                if (!args.reservationId) throw new Error('El ID de reservación es requerido');
                endpoint = `/v2/pms/reservations/${encodeURIComponent(args.reservationId)}`;
                break;
                
              case 'search_reservations':
                endpoint = '/v2/pms/reservations/search';
                if (args.checkIn) queryParams.append('checkIn', args.checkIn);
                if (args.checkOut) queryParams.append('checkOut', args.checkOut);
                if (args.status) queryParams.append('status', args.status);
                if (args.guestName) queryParams.append('guestName', args.guestName);
                if (args.page) queryParams.append('page', args.page.toString());
                if (args.size) queryParams.append('size', args.size.toString());
                break;
                
              case 'get_units':
                endpoint = '/pms/units';
                if (args.nodeId) queryParams.append('nodeId', args.nodeId);
                if (args.status) queryParams.append('status', args.status);
                if (args.page) queryParams.append('page', args.page.toString());
                if (args.size) queryParams.append('size', args.size.toString());
                break;
                
              case 'get_unit':
                if (!args.unitId) throw new Error('El ID de unidad es requerido');
                endpoint = `/pms/units/${encodeURIComponent(args.unitId)}`;
                break;
                
              case 'get_reviews':
                endpoint = '/pms/reviews';
                if (args.nodeId) queryParams.append('nodeId', args.nodeId);
                if (args.rating) queryParams.append('rating', args.rating.toString());
                if (args.page) queryParams.append('page', args.page.toString());
                if (args.size) queryParams.append('size', args.size.toString());
                break;
                
              default:
                throw new Error(`Herramienta desconocida: ${name}`);
            }
            
            const fullUrl = `${apiUrl}${endpoint}${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
            
            console.log(`[MCP] Llamando a API: ${fullUrl}`);
            
            const response = await fetch(fullUrl, {
              method: 'GET',
              headers: {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              }
            });
            
            if (!response.ok) {
              const errorText = await response.text();
              throw new Error(`Track HS API Error: ${response.status} ${response.statusText} - ${errorText}`);
            }
            
            const data = await response.json();
            
            result = {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    tool: name,
                    arguments: args,
                    data: data,
                    meta: {
                      endpoint: fullUrl,
                      timestamp: new Date().toISOString(),
                      status: 'success'
                    }
                  }, null, 2)
                }
              ]
            };
            
          } catch (apiError) {
            result = {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    tool: name,
                    arguments: args,
                    error: 'Error en API de TrackHS',
                    message: apiError.message,
                    timestamp: new Date().toISOString()
                  }, null, 2)
                }
              ]
            };
          }
        }
        break;

      case 'resources/list':
        result = {
          resources: [
            {
              uri: 'trackhs://status/system',
              name: 'system-status',
              title: 'Estado del Sistema TrackHS',
              description: 'Estado actual del sistema TrackHS y configuración',
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
        // El cliente notifica que está listo después de initialize
        result = { success: true };
        break;

      default:
        return res.status(400).json({
          jsonrpc: '2.0',
          error: { code: -32601, message: 'Method not found' },
          id
        });
    }

    console.log('[MCP] Respuesta enviada:', { method, success: true });
    
    res.json({
      jsonrpc: '2.0',
      result,
      id
    });

  } catch (error) {
    console.error('[MCP] Error:', error);
    
    // Manejo de errores según especificación MCP
    const errorCode = error.name === 'ValidationError' ? -32602 : -32603;
    const errorMessage = error.name === 'ValidationError' ? 'Invalid params' : 'Internal server error';
    
    res.status(500).json({
      jsonrpc: '2.0',
      error: {
        code: errorCode,
        message: errorMessage,
        data: {
          details: error.message,
          timestamp: new Date().toISOString(),
          method: req.body?.method || 'unknown'
        }
      },
      id: req.body?.id || null
    });
  }
}