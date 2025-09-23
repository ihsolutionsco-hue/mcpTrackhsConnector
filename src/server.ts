/**
 * Servidor MCP principal para Track HS
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
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

export class TrackHSMCPServer {
  private server: Server;
  private tools: BaseTrackHSTool[];

  constructor() {
    // Validar variables de entorno
    this.validateEnvironment();

    // Configuración desde variables de entorno
    const apiClient = new TrackHSApiClient({
      baseUrl: process.env.TRACKHS_API_URL!,
      username: process.env.TRACKHS_USERNAME!,
      password: process.env.TRACKHS_PASSWORD!
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
    const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    
    for (const envVar of requiredEnvVars) {
      if (!process.env[envVar]) {
        throw new Error(`Variable de entorno requerida no configurada: ${envVar}`);
      }
    }

    // Validar formato de URL
    try {
      new URL(process.env.TRACKHS_API_URL!);
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
   * Inicia el servidor MCP
   */
  async start(): Promise<void> {
    try {
      // Determinar tipo de transporte basado en el entorno
      const transport = process.stdin.readable 
        ? await import('@modelcontextprotocol/sdk/server/stdio.js').then(m => new m.StdioServerTransport())
        : await import('@modelcontextprotocol/sdk/server/stdio.js').then(m => new m.StdioServerTransport());

      await this.server.connect(transport);
      console.error('Track HS MCP Server iniciado correctamente');
    } catch (error) {
      console.error('Error al iniciar Track HS MCP Server:', error);
      process.exit(1);
    }
  }

  /**
   * Detiene el servidor
   */
  async stop(): Promise<void> {
    try {
      await this.server.close();
      console.error('Track HS MCP Server detenido');
    } catch (error) {
      console.error('Error al detener el servidor:', error);
    }
  }
}
