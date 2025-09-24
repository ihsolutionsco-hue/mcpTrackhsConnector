/**
 * Cloudflare Worker para Track HS MCP Remote Server
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400'
    };

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, { 
        status: 204,
        headers: corsHeaders 
      });
    }

    try {
      // Health check endpoint
      if (url.pathname === '/health') {
        return new Response(JSON.stringify({ 
          status: 'ok',
          service: 'trackhs-mcp-remote',
          version: '1.0.0',
          timestamp: new Date().toISOString()
        }), {
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          }
        });
      }

      // MCP endpoint
      if (url.pathname === '/mcp') {
        return new Response(JSON.stringify({
          name: 'Track HS MCP Remote Server',
          version: '1.0.0',
          description: 'MCP Server para integración con Track HS API',
          tools: [
            {
              name: 'get_reviews',
              description: 'Retrieve paginated collection of property reviews from Track HS'
            },
            {
              name: 'get_reservation', 
              description: 'Get detailed information for a specific reservation by ID'
            },
            {
              name: 'search_reservations',
              description: 'Search reservations with advanced filtering options'
            },
            {
              name: 'get_units',
              description: 'Get collection of accommodation units with advanced filters'
            },
            {
              name: 'get_folios_collection',
              description: 'Get collection of folios (bills/receipts) with filtering'
            },
            {
              name: 'get_contacts',
              description: 'Retrieve all contacts from Track HS CRM system'
            }
          ],
          endpoints: {
            mcp: '/mcp',
            health: '/health',
            info: '/info'
          }
        }), {
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          }
        });
      }

      // API info endpoint
      if (url.pathname === '/info') {
        return new Response(JSON.stringify({
          name: 'Track HS MCP Remote Server',
          version: '1.0.0',
          description: 'MCP Server para integración con Track HS API',
          endpoints: {
            mcp: '/mcp',
            health: '/health',
            info: '/info'
          },
          tools: [
            'get_reviews',
            'get_reservation', 
            'search_reservations',
            'get_units',
            'get_folios_collection',
            'get_contacts'
          ]
        }), {
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          }
        });
      }

      // 404 for unknown paths
      return new Response(JSON.stringify({ 
        error: 'Not Found',
        message: 'Endpoint not found',
        availableEndpoints: ['/mcp', '/health', '/info']
      }), { 
        status: 404,
        headers: { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        }
      });

    } catch (error) {
      console.error('Worker error:', error);
      
      return new Response(JSON.stringify({ 
        error: 'Internal Server Error',
        message: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }), { 
        status: 500,
        headers: { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        }
      });
    }
  }
};