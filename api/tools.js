/**
 * Endpoint para listar herramientas disponibles del Track HS MCP Connector
 */

import { TrackHSMCPServer } from '../dist/server.js';

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
    // Crear instancia temporal del servidor para obtener herramientas
    const mcpServer = new TrackHSMCPServer();
    
    const tools = mcpServer.tools.map(tool => ({
      name: tool.name,
      description: tool.description,
      inputSchema: tool.inputSchema
    }));

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
