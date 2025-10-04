/**
 * Archivo de prueba simple para diagnosticar problemas de Vercel
 */

module.exports = async function handler(req, res) {
  // Manejar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const { method, url } = req;
    const path = url?.split('?')[0] || '';

    console.log(`[${method}] ${path}`);

    // Respuesta simple para diagnosticar
    res.status(200).json({
      status: 'ok',
      message: 'Test endpoint funcionando',
      method: method,
      path: path,
      timestamp: new Date().toISOString(),
      nodeVersion: process.version,
      environment: process.env.NODE_ENV || 'development'
    });

  } catch (error) {
    console.error('Error en test endpoint:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error instanceof Error ? error.message : 'Error desconocido',
      timestamp: new Date().toISOString()
    });
  }
};
