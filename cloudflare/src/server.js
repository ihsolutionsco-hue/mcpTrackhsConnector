/**
 * Servidor MCP remoto para Track HS
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { TrackHSApiClient } from './core/api-client.js';
import { GetReviewsTool } from './tools/get-reviews.js';
import { GetReservationTool } from './tools/get-reservation.js';
import { SearchReservationsTool } from './tools/search-reservations.js';
import { GetUnitsTool } from './tools/get-units.js';
import { GetFoliosCollectionTool } from './tools/get-folios-collection.js';
import { GetContactsTool } from './tools/get-contacts.js';
export class TrackHSMCPServer {
    env;
    server;
    tools;
    constructor(env) {
        this.env = env;
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
    validateEnvironment() {
        const requiredVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
        for (const varName of requiredVars) {
            if (!this.env[varName]) {
                throw new Error(`Variable de entorno requerida no configurada: ${varName}`);
            }
        }
        // Validar formato de URL
        try {
            new URL(this.env.TRACKHS_API_URL);
        }
        catch {
            throw new Error('TRACKHS_API_URL debe ser una URL válida');
        }
    }
    /**
     * Configura los manejadores de peticiones MCP
     */
    setupHandlers() {
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
            }
            catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
                throw new Error(`Error en ejecución de herramienta: ${errorMessage}`);
            }
        });
    }
    /**
     * Maneja las peticiones HTTP entrantes
     */
    async handleRequest(request) {
        try {
            // Crear transporte SSE
            const transport = new SSEServerTransport('/mcp', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Max-Age': '86400'
                }
            });
            // Conectar servidor al transporte
            await this.server.connect(transport);
            // Procesar petición a través del transporte
            return new Response(JSON.stringify({
                error: 'MCP transport not implemented for Cloudflare Workers',
                message: 'This server is designed for Cloudflare Workers environment'
            }), {
                status: 501,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        catch (error) {
            console.error('Error en servidor MCP:', error);
            return new Response(JSON.stringify({
                error: 'Error interno del servidor MCP',
                message: error instanceof Error ? error.message : 'Error desconocido',
                timestamp: new Date().toISOString()
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
    getToolsInfo() {
        return this.tools.map(tool => ({
            name: tool.name,
            description: tool.description
        }));
    }
    /**
     * Obtiene estadísticas del servidor
     */
    getStats() {
        return {
            toolsCount: this.tools.length,
            environment: this.env.ENVIRONMENT || 'production'
        };
    }
}
