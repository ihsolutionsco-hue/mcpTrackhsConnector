/**
 * Servidor MCP principal para Track HS
 * Integra autenticación OAuth, transporte SSE y herramientas MCP
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  InitializeRequestSchema,
  ListPromptsRequestSchema,
  ListResourcesRequestSchema,
  GetPromptRequestSchema,
  ReadResourceRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

import { TrackHSApiClient } from './api-client.js';
import { BaseTrackHSTool } from './base-tool.js';
import { OAuthHandler, OAuthConfig } from './oauth-handler.js';
import { SSETransport, MCPRequest, MCPResponse } from '../transport/sse-transport.js';

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
  OAUTH_CLIENT_ID?: string;
  OAUTH_CLIENT_SECRET?: string;
  ENVIRONMENT?: string;
}

export class TrackHSMCPServer {
  private server: Server;
  private tools: BaseTrackHSTool[];
  private oauthHandler: OAuthHandler;
  private sseTransport: SSETransport;
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

    // Configurar OAuth
    this.oauthHandler = new OAuthHandler({
      clientId: this.env.OAUTH_CLIENT_ID || 'trackhs-mcp-client',
      clientSecret: this.env.OAUTH_CLIENT_SECRET || 'trackhs-mcp-secret',
      redirectUri: 'https://claude.ai/api/mcp/auth_callback',
      authorizationUrl: '/auth/authorize',
      tokenUrl: '/auth/token',
      scope: 'trackhs:read trackhs:write'
    });

    // Configurar transporte SSE
    this.sseTransport = new SSETransport();

    // Registrar herramientas
    this.tools = [
      new GetReviewsTool(this.apiClient),
      new GetReservationTool(this.apiClient),
      new SearchReservationsTool(this.apiClient),
      new GetUnitsTool(this.apiClient),
      new GetFoliosCollectionTool(this.apiClient),
      new GetContactsTool(this.apiClient)
    ];

    // Configurar servidor MCP
    this.server = new Server({
      name: 'trackhs-mcp-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {},
        prompts: {},
        resources: {}
      }
    });

    this.setupMCPHandlers();
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
   * Configura los manejadores MCP
   */
  private setupMCPHandlers(): void {
    // Inicialización del servidor
    this.server.setRequestHandler(InitializeRequestSchema, async () => {
      return {
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
      };
    });

    // Listar herramientas
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: this.tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema
        }))
      };
    });

    // Ejecutar herramientas
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      const tool = this.tools.find(t => t.name === name);
      if (!tool) {
        throw new Error(`Herramienta desconocida: ${name}`);
      }

      try {
        const result = await tool.execute(args || {});
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
        throw new Error(`Error en ejecución de herramienta: ${errorMessage}`);
      }
    });

    // Listar prompts (vacío por ahora)
    this.server.setRequestHandler(ListPromptsRequestSchema, async () => {
      return { prompts: [] };
    });

    // Obtener prompt (no implementado)
    this.server.setRequestHandler(GetPromptRequestSchema, async () => {
      throw new Error('Prompts no implementados');
    });

    // Listar recursos (vacío por ahora)
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return { resources: [] };
    });

    // Leer recurso (no implementado)
    this.server.setRequestHandler(ReadResourceRequestSchema, async () => {
      throw new Error('Recursos no implementados');
    });
  }

  /**
   * Maneja las peticiones HTTP entrantes
   */
  async handleRequest(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      console.log(`MCP Server: ${request.method} ${url.pathname}`);
      
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
          client_id: this.env.OAUTH_CLIENT_ID || 'trackhs-mcp-client'
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
        const body = await request.json();
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

      // OAuth endpoints
      if (url.pathname.startsWith('/auth/')) {
        return this.oauthHandler.handleRequest(request);
      }

      // MCP SSE endpoint
      if (url.pathname === '/mcp') {
        return this.handleMCPConnection(request);
      }

      // Health check
      if (url.pathname === '/health' && request.method === 'GET') {
        return new Response(JSON.stringify({ 
          status: 'ok',
          server: 'trackhs-mcp-server',
          version: '1.0.0',
          tools: this.tools.length,
          connections: this.sseTransport.getActiveConnectionsCount()
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
          })),
          connections: this.sseTransport.getActiveConnectionsCount()
        }), { 
          headers: { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          } 
        });
      }

      console.log(`MCP Server: No route found for ${url.pathname}`);
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
   * Maneja la conexión MCP SSE
   */
  private async handleMCPConnection(request: Request): Promise<Response> {
    const connectionId = this.generateConnectionId();
    
    // Verificar autenticación si es necesario
    const authHeader = request.headers.get('authorization');
    if (authHeader && !authHeader.startsWith('Bearer ')) {
      return new Response('Token de autorización inválido', { status: 401 });
    }

    // Crear conexión SSE
    return this.sseTransport.handleConnection(request, connectionId);
  }

  /**
   * Procesa una petición MCP
   */
  async processMCPRequest(connectionId: string, request: MCPRequest): Promise<void> {
    try {
      // Procesar petición MCP manualmente
      let response: any;
      
      switch (request.method) {
        case 'initialize':
          response = {
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
          };
          break;
          
        case 'tools/list':
          response = {
            tools: this.tools.map(tool => ({
              name: tool.name,
              description: tool.description,
              inputSchema: tool.inputSchema
            }))
          };
          break;
          
        case 'tools/call':
          const { name, arguments: args } = request.params;
          const tool = this.tools.find(t => t.name === name);
          
          if (!tool) {
            throw new Error(`Herramienta desconocida: ${name}`);
          }
          
          const result = await tool.execute(args || {});
          response = {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          };
          break;
          
        default:
          throw new Error(`Método no soportado: ${request.method}`);
      }
      
      // Enviar respuesta via SSE
      await this.sseTransport.sendMessage(connectionId, {
        id: request.id.toString(),
        event: 'mcp-response',
        data: JSON.stringify({
          jsonrpc: '2.0',
          id: request.id,
          result: response
        })
      });

    } catch (error) {
      const errorResponse: MCPResponse = {
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32603,
          message: 'Error interno del servidor',
          data: error instanceof Error ? error.message : 'Error desconocido'
        }
      };

      await this.sseTransport.sendMessage(connectionId, {
        id: request.id.toString(),
        event: 'mcp-error',
        data: JSON.stringify(errorResponse)
      });
    }
  }

  /**
   * Genera un ID único para la conexión
   */
  private generateConnectionId(): string {
    return 'conn_' + Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
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

  /**
   * Obtiene estadísticas del servidor
   */
  getStats(): {
    toolsCount: number;
    connectionsCount: number;
    environment: string;
  } {
    return {
      toolsCount: this.tools.length,
      connectionsCount: this.sseTransport.getActiveConnectionsCount(),
      environment: this.env.ENVIRONMENT || 'production'
    };
  }

  /**
   * Cierra todas las conexiones
   */
  async shutdown(): Promise<void> {
    await this.sseTransport.closeAllConnections();
  }
}
