/**
 * Servidor MCP remoto para Track HS
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

import { TrackHSApiClient } from './core/api-client.js';
import { BaseTrackHSTool } from './core/base-tool.js';
import { GetReviewsTool } from './tools/get-reviews.js';
import { GetReservationTool } from './tools/get-reservation.js';
import { SearchReservationsTool } from './tools/search-reservations.js';
import { GetUnitsTool } from './tools/get-units.js';
import { GetFoliosCollectionTool } from './tools/get-folios-collection.js';
import { GetContactsTool } from './tools/get-contacts.js';

// Tipos para variables de entorno
interface Env {
  TRACKHS_API_URL: string;
  TRACKHS_USERNAME: string;
  TRACKHS_PASSWORD: string;
  ENVIRONMENT?: string;
}

export class TrackHSMCPServer {
  private server: Server;
  private tools: BaseTrackHSTool[];

  constructor(private env: any) {
    // Validar variables de entorno
    this.validateEnvironment();

    // Configuración desde variables de entorno
    const apiClient = new TrackHSApiClient({
      baseUrl: this.env.TRACKHS_API_URL,
      username: this.env.TRACKHS_USERNAME,
      password: this.env.TRACKHS_PASSWORD
    });

    // Registrar herramientas
    this.tools = [
      new GetReviewsTool(apiClient),
      new GetReservationTool(apiClient),
      new SearchReservationsTool(apiClient),
      new GetUnitsTool(apiClient),
      new GetFoliosCollectionTool(apiClient),
      new GetContactsTool(apiClient)
    ];

    // Configurar servidor MCP
    this.server = new Server({
      name: 'trackhs-mcp-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {}
      }
    });

    this.setupHandlers();
  }

  /**
   * Valida que las variables de entorno estén configuradas
   */
  private validateEnvironment(): void {
    const requiredVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    
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
   * Configura los manejadores de peticiones MCP
   */
  private setupHandlers(): void {
    // Listar herramientas disponibles
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
  }

  /**
   * Maneja las peticiones HTTP entrantes
   */
  async handleRequest(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      
      // Headers CORS
      const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
      };

      // Manejar preflight
      if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
      }

      // Obtener herramientas disponibles
      if (url.pathname === '/mcp/tools' && request.method === 'GET') {
        const tools = this.tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema
        }));
        
        return new Response(JSON.stringify({ tools }), { headers: corsHeaders });
      }

      // Ejecutar herramienta
      if (url.pathname === '/mcp/call' && request.method === 'POST') {
        const body = await request.json();
        const { name, arguments: args } = body;
        
        const tool = this.tools.find(t => t.name === name);
        if (!tool) {
          return new Response(JSON.stringify({ 
            error: `Herramienta desconocida: ${name}` 
          }), { 
            status: 404, 
            headers: corsHeaders 
          });
        }

        try {
          const result = await tool.execute(args || {});
          return new Response(JSON.stringify({ result }), { headers: corsHeaders });
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
          return new Response(JSON.stringify({ 
            error: `Error en ejecución: ${errorMessage}` 
          }), { 
            status: 500, 
            headers: corsHeaders 
          });
        }
      }

      // Endpoint por defecto
      return new Response(JSON.stringify({ 
        message: 'TrackHS MCP Server',
        endpoints: ['/mcp/tools', '/mcp/call'],
        tools: this.tools.map(t => t.name)
      }), { headers: corsHeaders });
      
    } catch (error) {
      console.error('Error en servidor MCP:', error);
      
      return new Response(JSON.stringify({ 
        error: 'Error interno del servidor',
        message: error instanceof Error ? error.message : 'Error desconocido'
      }), { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
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

  /**
   * Obtiene estadísticas del servidor
   */
  getStats(): {toolsCount: number, environment: string} {
    return {
      toolsCount: this.tools.length,
      environment: this.env.ENVIRONMENT || 'production'
    };
  }
}