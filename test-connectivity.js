/**
 * Script de prueba de conectividad para el MCP Connector
 * Prueba el endpoint /mcp con una petición de inicialización MCP
 */

const testUrl = 'https://trackhs-mcp-connector-cvani8166-marianos-projects-21770778.vercel.app';

async function testMCPEndpoint() {
  console.log('🧪 Probando conectividad del MCP Connector...');
  console.log(`📍 URL: ${testUrl}/mcp`);
  
  try {
    // Petición de inicialización MCP
    const initRequest = {
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
    };

    console.log('📤 Enviando petición de inicialización...');
    console.log('📋 Datos:', JSON.stringify(initRequest, null, 2));

    const response = await fetch(`${testUrl}/mcp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(initRequest)
    });

    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    console.log('📋 Headers:', Object.fromEntries(response.headers.entries()));

    if (response.ok) {
      const data = await response.json();
      console.log('✅ Respuesta exitosa:');
      console.log(JSON.stringify(data, null, 2));
      
      if (data.result && data.result.capabilities) {
        console.log('🎯 Capacidades del servidor:');
        console.log('- Tools:', data.result.capabilities.tools ? '✅' : '❌');
        console.log('- Resources:', data.result.capabilities.resources ? '✅' : '❌');
        console.log('- Prompts:', data.result.capabilities.prompts ? '✅' : '❌');
      }
    } else {
      const errorText = await response.text();
      console.log('❌ Error en la respuesta:');
      console.log(errorText);
    }

  } catch (error) {
    console.error('💥 Error de conectividad:');
    console.error(error.message);
  }
}

async function testHealthEndpoint() {
  console.log('\n🏥 Probando endpoint de salud...');
  
  try {
    const response = await fetch(`${testUrl}/health`);
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Estado del servidor:');
      console.log(JSON.stringify(data, null, 2));
    } else {
      console.log('❌ Error en endpoint de salud');
    }
  } catch (error) {
    console.error('💥 Error conectando al endpoint de salud:');
    console.error(error.message);
  }
}

async function testToolsEndpoint() {
  console.log('\n🔧 Probando endpoint de herramientas...');
  
  try {
    const response = await fetch(`${testUrl}/tools`);
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Herramientas disponibles:');
      console.log(`📊 Total: ${data.tools ? data.tools.length : 0} herramientas`);
      if (data.tools && data.tools.length > 0) {
        console.log('📋 Lista de herramientas:');
        data.tools.forEach((tool, index) => {
          console.log(`  ${index + 1}. ${tool.name} - ${tool.title}`);
        });
      }
    } else {
      console.log('❌ Error en endpoint de herramientas');
    }
  } catch (error) {
    console.error('💥 Error conectando al endpoint de herramientas:');
    console.error(error.message);
  }
}

// Ejecutar todas las pruebas
async function runAllTests() {
  console.log('🚀 Iniciando pruebas de conectividad del MCP Connector');
  console.log('=' .repeat(60));
  
  await testHealthEndpoint();
  await testToolsEndpoint();
  await testMCPEndpoint();
  
  console.log('\n' + '='.repeat(60));
  console.log('🏁 Pruebas completadas');
}

// Ejecutar si se llama directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllTests().catch(console.error);
}

export { runAllTests, testMCPEndpoint, testHealthEndpoint, testToolsEndpoint };
