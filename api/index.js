/**
 * Página principal del Track HS MCP Connector
 */

export default function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const html = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Track HS MCP Connector</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 40px 30px;
        }
        .status {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
        }
        .status-icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .endpoints {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .endpoint {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .method {
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .method.post {
            background: #007bff;
        }
        .config {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .code {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin: 10px 0;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Track HS MCP Connector</h1>
            <p>Conector MCP remoto para Track HS API</p>
        </div>
        
        <div class="content">
            <div class="status">
                <span class="status-icon">✅</span>
                <div>
                    <strong>Servidor Activo</strong><br>
                    Conector MCP remoto para Track HS API funcionando correctamente.
                </div>
            </div>

            <h2>📡 Endpoints Disponibles</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <div>
                        <span class="method">GET</span>
                        <strong>/api/health</strong> - Health check del servicio
                    </div>
                </div>
                <div class="endpoint">
                    <div>
                        <span class="method">GET</span>
                        <strong>/api/tools</strong> - Listar herramientas disponibles
                    </div>
                </div>
                <div class="endpoint">
                    <div>
                        <span class="method post">POST</span>
                        <strong>/api/mcp</strong> - Endpoint principal MCP
                    </div>
                </div>
            </div>

            <h2>🔧 Configuración en Claude Desktop</h2>
            <div class="config">
                <p><strong>Para usar este conector en Claude Desktop, agrega la siguiente configuración:</strong></p>
                <div class="code">
{
  "mcpServers": {
    "trackhs-remote": {
      "url": "https://trackhs-mcp-connector.vercel.app/api/mcp"
    }
  }
}
                </div>
            </div>

            <h2>🛠️ Herramientas Disponibles</h2>
            <p>Este conector proporciona acceso a las siguientes herramientas de Track HS:</p>
            <ul>
                <li><strong>get_reviews</strong> - Obtener reseñas de propiedades</li>
                <li><strong>get_reservation</strong> - Obtener detalles de reservas</li>
                <li><strong>search_reservations</strong> - Buscar reservas</li>
                <li><strong>get_units</strong> - Listar unidades disponibles</li>
                <li><strong>get_unit</strong> - Obtener detalles de una unidad</li>
                <li><strong>get_contacts</strong> - Obtener contactos</li>
                <li><strong>get_ledger_accounts</strong> - Listar cuentas contables</li>
                <li><strong>get_ledger_account</strong> - Obtener cuenta contable específica</li>
                <li><strong>get_reservation_notes</strong> - Obtener notas de reservas</li>
                <li><strong>get_nodes</strong> - Listar nodos</li>
                <li><strong>get_node</strong> - Obtener nodo específico</li>
                <li><strong>get_maintenance_work_orders</strong> - Obtener órdenes de trabajo</li>
                <li><strong>get_folios_collection</strong> - Obtener colección de folios</li>
            </ul>

            <h2>📚 Documentación</h2>
            <p>Para más información sobre cómo usar este conector, consulta la documentación del proyecto en el repositorio.</p>
        </div>

        <div class="footer">
            <p>Track HS MCP Connector v1.0.0 | Desplegado en Vercel</p>
        </div>
    </div>
</body>
</html>
  `;

  res.status(200).setHeader('Content-Type', 'text/html').send(html);
}