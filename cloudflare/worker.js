/**
 * Cloudflare Worker para Track HS MCP Server
 * Implementa servidor MCP remoto con autenticación OAuth y transporte SSE
 */

import { SimpleTrackHSMCPServer } from '../src/core/simple-mcp-server.js';

export default {
  async fetch(request, env) {
    try {
      // Headers CORS estándar
      const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
        'Access-Control-Allow-Credentials': 'true'
      };

      // Manejar preflight requests
      if (request.method === 'OPTIONS') {
        return new Response(null, { 
          status: 204,
          headers: corsHeaders 
        });
      }

      // Crear instancia del servidor MCP simplificado
      const server = new SimpleTrackHSMCPServer(env);
      
      // Manejar la petición
      return await server.handleRequest(request);
      
    } catch (error) {
      console.error('Error en Cloudflare Worker:', error);
      
      // Headers CORS para errores
      const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
        'Access-Control-Allow-Credentials': 'true'
      };
      
      return new Response(JSON.stringify({
        error: 'Error interno del servidor',
        message: error instanceof Error ? error.message : 'Error desconocido',
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