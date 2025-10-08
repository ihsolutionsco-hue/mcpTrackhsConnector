/**
 * Endpoint HTTP para el servidor MCP de Track HS
 * Compatible con Vercel y servidores remotos MCP
 */

import { TrackHSMCPServer } from '../dist/server.js';

// Crear instancia del servidor
const mcpServer = new TrackHSMCPServer();

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
        }
      });
      return;
    }

    if (req.method === 'POST') {
      const { method, params } = req.body;

      if (method === 'tools/list') {
        // Listar herramientas disponibles
        const tools = mcpServer.tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema
        }));

        res.status(200).json({
          jsonrpc: '2.0',
          id: req.body.id || 1,
          result: { tools }
        });
        return;
      }

      if (method === 'tools/call') {
        // Ejecutar herramienta
        const { name, arguments: args } = params;
        
        const tool = mcpServer.tools.find(t => t.name === name);
        if (!tool) {
          res.status(400).json({
            jsonrpc: '2.0',
            id: req.body.id || 1,
            error: {
              code: -32601,
              message: `Herramienta desconocida: ${name}`
            }
          });
          return;
        }

        try {
          const result = await tool.execute(args || {});
          res.status(200).json({
            jsonrpc: '2.0',
            id: req.body.id || 1,
            result: {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2)
                }
              ]
            }
          });
        } catch (error) {
          res.status(500).json({
            jsonrpc: '2.0',
            id: req.body.id || 1,
            error: {
              code: -32603,
              message: `Error en ejecución: ${error.message}`
            }
          });
        }
        return;
      }

      // Método no soportado
      res.status(400).json({
        jsonrpc: '2.0',
        id: req.body.id || 1,
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
