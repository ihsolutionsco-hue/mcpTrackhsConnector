/**
 * Endpoint de prueba para Vercel
 */

module.exports = (req, res) => {
  res.json({
    message: 'Test endpoint funcionando',
    method: req.method,
    url: req.url,
    timestamp: new Date().toISOString(),
    body: req.body
  });
};
