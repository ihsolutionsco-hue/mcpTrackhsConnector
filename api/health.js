/**
 * Health check endpoint para el Track HS MCP Connector
 */

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

  const healthStatus = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'Track HS MCP Connector',
    version: '1.0.0',
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'production',
    endpoints: {
      mcp: '/api/mcp',
      tools: '/api/tools',
      health: '/api/health'
    }
  };

  res.status(200).json(healthStatus);
}
