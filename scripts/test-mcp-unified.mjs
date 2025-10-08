/**
 * Script de testing para el servidor MCP unificado
 * Prueba todas las funcionalidades del protocolo MCP
 */

import https from 'https';

const BASE_URL = 'https://trackhs-mcp-connector.vercel.app/api';

// Función helper para hacer requests
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const requestOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    };

    const req = https.request(requestOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, data: parsed });
        } catch (error) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });

    req.on('error', reject);
    
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    
    req.end();
  });
}

// Test 1: Health Check
async function testHealthCheck() {
  console.log('🔍 Testing Health Check...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp/health`);
    console.log('✅ Health Check:', response.status === 200 ? 'PASS' : 'FAIL');
    console.log('   Response:', response.data);
  } catch (error) {
    console.log('❌ Health Check FAIL:', error.message);
  }
}

// Test 2: Tools List
async function testToolsList() {
  console.log('\n🔍 Testing Tools List...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp/tools`);
    console.log('✅ Tools List:', response.status === 200 ? 'PASS' : 'FAIL');
    console.log('   Tools count:', response.data.tools?.length || 0);
    console.log('   Available tools:', response.data.tools?.map(t => t.name).join(', ') || 'None');
  } catch (error) {
    console.log('❌ Tools List FAIL:', error.message);
  }
}

// Test 3: MCP Initialize
async function testMCPInitialize() {
  console.log('\n🔍 Testing MCP Initialize...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp`, {
      method: 'POST',
      body: {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2025-06-18',
          capabilities: {
            tools: {}
          },
          clientInfo: {
            name: 'test-client',
            version: '1.0.0'
          }
        }
      }
    });
    
    console.log('✅ MCP Initialize:', response.status === 200 ? 'PASS' : 'FAIL');
    console.log('   Protocol Version:', response.data.result?.protocolVersion);
    console.log('   Server Name:', response.data.result?.serverInfo?.name);
    console.log('   Capabilities:', response.data.result?.capabilities);
  } catch (error) {
    console.log('❌ MCP Initialize FAIL:', error.message);
  }
}

// Test 4: MCP Tools List
async function testMCPToolsList() {
  console.log('\n🔍 Testing MCP Tools List...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp`, {
      method: 'POST',
      body: {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list'
      }
    });
    
    console.log('✅ MCP Tools List:', response.status === 200 ? 'PASS' : 'FAIL');
    console.log('   Tools count:', response.data.result?.tools?.length || 0);
    console.log('   First tool:', response.data.result?.tools?.[0]?.name || 'None');
  } catch (error) {
    console.log('❌ MCP Tools List FAIL:', error.message);
  }
}

// Test 5: MCP Tool Call (sin credenciales)
async function testMCPToolCall() {
  console.log('\n🔍 Testing MCP Tool Call...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp`, {
      method: 'POST',
      body: {
        jsonrpc: '2.0',
        id: 3,
        method: 'tools/call',
        params: {
          name: 'get_contacts',
          arguments: {
            page: 1,
            size: 5
          }
        }
      }
    });
    
    console.log('✅ MCP Tool Call:', response.status === 200 ? 'PASS' : 'FAIL');
    if (response.data.error) {
      console.log('   Error (expected without credentials):', response.data.error.message);
    } else {
      console.log('   Result:', response.data.result?.content?.[0]?.text?.substring(0, 100) + '...');
    }
  } catch (error) {
    console.log('❌ MCP Tool Call FAIL:', error.message);
  }
}

// Test 6: Invalid Method
async function testInvalidMethod() {
  console.log('\n🔍 Testing Invalid Method...');
  try {
    const response = await makeRequest(`${BASE_URL}/mcp`, {
      method: 'POST',
      body: {
        jsonrpc: '2.0',
        id: 4,
        method: 'invalid_method'
      }
    });
    
    console.log('✅ Invalid Method:', response.data.error ? 'PASS' : 'FAIL');
    console.log('   Error Code:', response.data.error?.code);
    console.log('   Error Message:', response.data.error?.message);
  } catch (error) {
    console.log('❌ Invalid Method FAIL:', error.message);
  }
}

// Ejecutar todos los tests
async function runAllTests() {
  console.log('🚀 Iniciando tests del servidor MCP unificado...\n');
  
  await testHealthCheck();
  await testToolsList();
  await testMCPInitialize();
  await testMCPToolsList();
  await testMCPToolCall();
  await testInvalidMethod();
  
  console.log('\n✅ Tests completados!');
  console.log('\n📋 Resumen:');
  console.log('   - Health Check: Verifica que el servidor esté funcionando');
  console.log('   - Tools List: Lista herramientas disponibles');
  console.log('   - MCP Initialize: Inicializa el protocolo MCP');
  console.log('   - MCP Tools List: Lista herramientas via MCP');
  console.log('   - MCP Tool Call: Ejecuta una herramienta (requiere credenciales)');
  console.log('   - Invalid Method: Prueba manejo de errores');
}

// Ejecutar tests
runAllTests().catch(console.error);
