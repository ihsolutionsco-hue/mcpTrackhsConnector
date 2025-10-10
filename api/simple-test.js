module.exports = (req, res) => {
  res.json({
    message: 'Simple test endpoint funcionando',
    method: req.method,
    timestamp: new Date().toISOString()
  });
};
