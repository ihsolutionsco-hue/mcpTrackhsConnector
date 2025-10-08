/**
 * Endpoint de prueba para validar el protocolo MCP
 * Permite probar la comunicación con Claude Desktop
 */

export default async function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    // Página de prueba MCP
    const html = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test MCP - Track HS Connector</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .test-button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 5px; }
        .test-button:hover { background: #0056b3; }
        .result { background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 4px; margin-top: 10px; white-space: pre-wrap; font-family: monospace; }
        .success { border-color: #28a745; background: #d4edda; }
        .error { border-color: #dc3545; background: #f8d7da; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test MCP - Track HS Connector</h1>
        
        <div class="test-section">
            <h3>1. Test Initialize</h3>
            <button class="test-button" onclick="testInitialize()">Probar Initialize</button>
            <div id="init-result" class="result" style="display:none;"></div>
        </div>

        <div class="test-section">
            <h3>2. Test Tools List</h3>
            <button class="test-button" onclick="testToolsList()">Probar Tools List</button>
            <div id="tools-result" class="result" style="display:none;"></div>
        </div>

        <div class="test-section">
            <h3>3. Test Tool Call</h3>
            <button class="test-button" onclick="testToolCall()">Probar Tool Call</button>
            <div id="call-result" class="result" style="display:none;"></div>
        </div>

        <div class="test-section">
            <h3>4. Test Completo MCP</h3>
            <button class="test-button" onclick="testFullMCP()">Probar Flujo Completo</button>
            <div id="full-result" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        const baseUrl = window.location.origin + '/api/mcp';
        
        async function testInitialize() {
            const resultDiv = document.getElementById('init-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Probando initialize...';
            
            try {
                const response = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 1,
                        method: 'initialize',
                        params: {
                            protocolVersion: '2025-06-18',
                            capabilities: { tools: {} },
                            clientInfo: { name: 'test-client', version: '1.0.0' }
                        }
                    })
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
                resultDiv.className = response.ok ? 'result success' : 'result error';
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.className = 'result error';
            }
        }

        async function testToolsList() {
            const resultDiv = document.getElementById('tools-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Probando tools/list...';
            
            try {
                const response = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 2,
                        method: 'tools/list'
                    })
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
                resultDiv.className = response.ok ? 'result success' : 'result error';
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.className = 'result error';
            }
        }

        async function testToolCall() {
            const resultDiv = document.getElementById('call-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Probando tools/call...';
            
            try {
                const response = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 3,
                        method: 'tools/call',
                        params: {
                            name: 'get_reviews',
                            arguments: { property_id: 'test-123' }
                        }
                    })
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
                resultDiv.className = response.ok ? 'result success' : 'result error';
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.className = 'result error';
            }
        }

        async function testFullMCP() {
            const resultDiv = document.getElementById('full-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Probando flujo completo MCP...\n';
            
            try {
                // 1. Initialize
                resultDiv.textContent += '1. Initialize...\n';
                const initResponse = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 1,
                        method: 'initialize',
                        params: {
                            protocolVersion: '2025-06-18',
                            capabilities: { tools: {} },
                            clientInfo: { name: 'test-client', version: '1.0.0' }
                        }
                    })
                });
                
                if (!initResponse.ok) {
                    throw new Error('Initialize failed');
                }
                resultDiv.textContent += '✅ Initialize OK\n';
                
                // 2. Tools List
                resultDiv.textContent += '2. Tools List...\n';
                const toolsResponse = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 2,
                        method: 'tools/list'
                    })
                });
                
                if (!toolsResponse.ok) {
                    throw new Error('Tools list failed');
                }
                const toolsData = await toolsResponse.json();
                resultDiv.textContent += '✅ Tools List OK (' + toolsData.result.tools.length + ' tools)\n';
                
                // 3. Tool Call
                resultDiv.textContent += '3. Tool Call...\n';
                const callResponse = await fetch(baseUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        id: 3,
                        method: 'tools/call',
                        params: {
                            name: 'get_reviews',
                            arguments: { property_id: 'test-123' }
                        }
                    })
                });
                
                if (!callResponse.ok) {
                    throw new Error('Tool call failed');
                }
                resultDiv.textContent += '✅ Tool Call OK\n';
                
                resultDiv.textContent += '\n🎉 Todos los tests pasaron correctamente!';
                resultDiv.className = 'result success';
                
            } catch (error) {
                resultDiv.textContent += '\n❌ Error: ' + error.message;
                resultDiv.className = 'result error';
            }
        }
    </script>
</body>
</html>
    `;

    res.status(200).setHeader('Content-Type', 'text/html').send(html);
    return;
  }

  res.status(405).json({ error: 'Método no permitido' });
}
