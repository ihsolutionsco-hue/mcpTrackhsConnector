/**
 * Servidor MCP simplificado para Track HS
 * Versión que funciona correctamente con Cloudflare Workers
 */

import { TrackHSApiClient } from './api-client.js';
import { BaseTrackHSTool } from './base-tool.js';

// Importar herramientas
import { GetReviewsTool } from '../tools/get-reviews.js';
import { GetReservationTool } from '../tools/get-reservation.js';
import { SearchReservationsTool } from '../tools/search-reservations.js';
import { GetUnitsTool } from '../tools/get-units.js';
import { GetFoliosCollectionTool } from '../tools/get-folios-collection.js';
import { GetContactsTool } from '../tools/get-contacts.js';

export interface Env {
  TRACKHS_API_URL: string;
  TRACKHS_USERNAME: string;
  TRACKHS_PASSWORD: string;
  ENVIRONMENT?: string;
}

export class SimpleTrackHSMCPServer {
  private tools: BaseTrackHSTool[];
  private apiClient: TrackHSApiClient;

  constructor(private env: Env) {
    // Validar variables de entorno
    this.validateEnvironment();

    // Configurar cliente API
    this.apiClient = new TrackHSApiClient({
      baseUrl: this.env.TRACKHS_API_URL,
      username: this.env.TRACKHS_USERNAME,
      password: this.env.TRACKHS_PASSWORD
    });

    // Registrar herramientas
    this.tools = [
      new GetReviewsTool(this.apiClient),
      new GetReservationTool(this.apiClient),
      new SearchReservationsTool(this.apiClient),
      new GetUnitsTool(this.apiClient),
      new GetFoliosCollectionTool(this.apiClient),
      new GetContactsTool(this.apiClient)
    ];
  }

  /**
   * Valida las variables de entorno requeridas
   */
  private validateEnvironment(): void {
    const requiredVars: (keyof Env)[] = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    
    for (const varName of requiredVars) {
      if (!this.env[varName]) {
        throw new Error(`Variable de entorno requerida no configurada: ${varName}`);
      }
    }

    // Validar formato de URL
    try {
      new URL(this.env.TRACKHS_API_URL);
    } catch {
      throw new Error('TRACKHS_API_URL debe ser una URL válida');
    }
  }

  /**
   * Maneja las peticiones HTTP entrantes
   */
  async handleRequest(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      console.log(`Simple MCP Server: ${request.method} ${url.pathname}`);
      
      // Headers CORS
      const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
        'Access-Control-Allow-Credentials': 'true'
      };

      // Manejar preflight
      if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
      }

      // OAuth endpoints estándar
      if (url.pathname === '/.well-known/oauth-authorization-server') {
        return new Response(JSON.stringify({
          issuer: 'https://trackhs-mcp-remote.ihsolutionsco.workers.dev',
          authorization_endpoint: 'https://trackhs-mcp-remote.ihsolutionsco.workers.dev/auth/authorize',
          token_endpoint: 'https://trackhs-mcp-remote.ihsolutionsco.workers.dev/auth/token',
          response_types_supported: ['code'],
          grant_types_supported: ['authorization_code'],
          scopes_supported: ['trackhs:read', 'trackhs:write'],
          client_id: 'trackhs-mcp-client'
        }), {
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json'
          }
        });
      }

      if (url.pathname === '/.well-known/oauth-protected-resource') {
        return new Response(JSON.stringify({
          resource: 'https://trackhs-mcp-remote.ihsolutionsco.workers.dev',
          scopes: ['trackhs:read', 'trackhs:write'],
          authorization_servers: ['https://trackhs-mcp-remote.ihsolutionsco.workers.dev']
        }), {
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json'
          }
        });
      }

      // Dynamic Client Registration
      if (url.pathname === '/register' && request.method === 'POST') {
        return new Response(JSON.stringify({
          client_id: 'trackhs-mcp-client',
          client_secret: 'trackhs-mcp-secret',
          registration_access_token: 'reg_token_' + Math.random().toString(36).substring(2, 15),
          registration_client_uri: 'https://trackhs-mcp-remote.ihsolutionsco.workers.dev/register/trackhs-mcp-client',
          client_id_issued_at: Math.floor(Date.now() / 1000),
          client_secret_expires_at: 0
        }), {
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json'
          }
        });
      }

      // OAuth endpoints básicos
      if (url.pathname === '/auth/authorize' && request.method === 'GET') {
        const responseType = url.searchParams.get('response_type');
        const clientId = url.searchParams.get('client_id');
        const redirectUri = url.searchParams.get('redirect_uri');
        const scope = url.searchParams.get('scope');
        const state = url.searchParams.get('state');

        if (responseType === 'code' && clientId === 'trackhs-mcp-client') {
          const authCode = 'auth_' + Math.random().toString(36).substring(2, 15);
          const redirectUrl = new URL(redirectUri || 'https://claude.ai/api/mcp/auth_callback');
          redirectUrl.searchParams.set('code', authCode);
          if (state) {
            redirectUrl.searchParams.set('state', state);
          }
          return Response.redirect(redirectUrl.toString(), 302);
        }
      }

      if (url.pathname === '/auth/token' && request.method === 'POST') {
        const body = await request.json();
        const { grant_type, code, redirect_uri, client_id, client_secret } = body;

        if (grant_type === 'authorization_code' && client_id === 'trackhs-mcp-client') {
          const accessToken = 'access_' + Math.random().toString(36).substring(2, 15);
          const refreshToken = 'refresh_' + Math.random().toString(36).substring(2, 15);

          return new Response(JSON.stringify({
            access_token: accessToken,
            refresh_token: refreshToken,
            token_type: 'Bearer',
            expires_in: 3600,
            scope: 'trackhs:read trackhs:write'
          }), {
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json'
            }
          });
        }
      }

      // MCP endpoint básico
      if (url.pathname === '/mcp' && request.method === 'POST') {
        const body = await request.json();
        
        if (body.method === 'initialize') {
          return new Response(JSON.stringify({
            jsonrpc: '2.0',
            id: body.id,
            result: {
              protocolVersion: '2024-11-05',
              capabilities: {
                tools: {},
                prompts: {},
                resources: {}
              },
              serverInfo: {
                name: 'trackhs-mcp-server',
                version: '1.0.0'
              }
            }
          }), {
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json'
            }
          });
        }

        if (body.method === 'tools/list') {
          return new Response(JSON.stringify({
            jsonrpc: '2.0',
            id: body.id,
            result: {
              tools: this.tools.map(tool => ({
                name: tool.name,
                description: tool.description,
                inputSchema: tool.inputSchema
              }))
            }
          }), {
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json'
            }
          });
        }

        if (body.method === 'tools/call') {
          const { name, arguments: args } = body.params;
          const tool = this.tools.find(t => t.name === name);
          
          if (!tool) {
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id,
              error: {
                code: -32601,
                message: `Herramienta desconocida: ${name}`
              }
            }), {
              status: 400,
              headers: {
                ...corsHeaders,
                'Content-Type': 'application/json'
              }
            });
          }

          try {
            const result = await tool.execute(args || {});
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id,
              result: {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify(result, null, 2)
                  }
                ]
              }
            }), {
              headers: {
                ...corsHeaders,
                'Content-Type': 'application/json'
              }
            });
          } catch (error) {
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id,
              error: {
                code: -32603,
                message: 'Error interno del servidor',
                data: error instanceof Error ? error.message : 'Error desconocido'
              }
            }), {
              status: 500,
              headers: {
                ...corsHeaders,
                'Content-Type': 'application/json'
              }
            });
          }
        }

        // Método MCP no reconocido
        return new Response(JSON.stringify({
          jsonrpc: '2.0',
          id: body.id,
          error: {
            code: -32601,
            message: `Método MCP no reconocido: ${body.method}`
          }
        }), {
          status: 400,
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json'
          }
        });
      }

      // Health check
      if (url.pathname === '/health' && request.method === 'GET') {
        return new Response(JSON.stringify({ 
          status: 'ok',
          server: 'trackhs-mcp-server',
          version: '1.0.0',
          tools: this.tools.length
        }), { 
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          } 
        });
      }

      // Información del servidor
      if (url.pathname === '/' && request.method === 'GET') {
        return new Response(JSON.stringify({ 
          name: 'TrackHS MCP Server',
          version: '1.0.0',
          description: 'Servidor MCP remoto para integración con Track HS API',
          endpoints: {
            mcp: '/mcp',
            health: '/health',
            oauth: '/auth/authorize'
          },
          tools: this.tools.map(t => ({
            name: t.name,
            description: t.description
          }))
        }), { 
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          } 
        });
      }

      console.log(`Simple MCP Server: No route found for ${url.pathname}`);
      return new Response('Not Found', { 
        status: 404, 
        headers: corsHeaders 
      });
      
    } catch (error) {
      console.error('Error en servidor MCP:', error);
      
      return new Response(JSON.stringify({ 
        error: 'Error interno del servidor',
        message: error instanceof Error ? error.message : 'Error desconocido'
      }), { 
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }

  /**
   * Obtiene información sobre las herramientas disponibles
   */
  getToolsInfo(): Array<{name: string, description: string}> {
    return this.tools.map(tool => ({
      name: tool.name,
      description: tool.description
    }));
  }
}
