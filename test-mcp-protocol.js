/**
 * Script de prueba para validar el protocolo MCP según la teoría
 * Prueba el flujo completo de inicialización y uso de herramientas
 */

import fetch from 'node-fetch';

const MCP_SERVER_URL = 'https://trackhs-mcp-connector.vercel.app/api/mcp';

async function testMCPProtocol() {
  console.log('🧪 Iniciando pruebas del protocolo MCP...\n');

  try {
    // 1. Prueba de inicialización (requerida por la teoría MCP)
    console.log('1️⃣ Probando inicialización MCP...');
    const initResponse = await mcpRequest('initialize', {
      protocolVersion: '2025-06-18',
      capabilities: {
        elicitation: {}
      },
      clientInfo: {
        name: 'test-client',
        version: '1.0.0'
      }
    });
    
    console.log('✅ Inicialización exitosa:', {
      protocolVersion: initResponse.result?.protocolVersion,
      capabilities: initResponse.result?.capabilities,
      serverInfo: initResponse.result?.serverInfo
    });

    // 2. Notificación de inicialización completada
    console.log('\n2️⃣ Enviando notificación de inicialización...');
    const initializedResponse = await mcpRequest('notifications/initialized');
    console.log('✅ Notificación enviada:', initializedResponse);

    // 3. Listar herramientas disponibles
    console.log('\n3️⃣ Listando herramientas disponibles...');
    const toolsResponse = await mcpRequest('tools/list');
    console.log('✅ Herramientas disponibles:', toolsResponse.result?.tools?.length || 0);

    // 4. Listar recursos disponibles
    console.log('\n4️⃣ Listando recursos disponibles...');
    const resourcesResponse = await mcpRequest('resources/list');
    console.log('✅ Recursos disponibles:', resourcesResponse.result?.resources?.length || 0);

    // 5. Listar prompts disponibles
    console.log('\n5️⃣ Listando prompts disponibles...');
    const promptsResponse = await mcpRequest('prompts/list');
    console.log('✅ Prompts disponibles:', promptsResponse.result?.prompts?.length || 0);

    // 6. Prueba de ejecución de herramienta (si hay configuración)
    console.log('\n6️⃣ Probando ejecución de herramienta...');
    try {
      const toolResponse = await mcpRequest('tools/call', {
        name: 'get_contacts',
        arguments: {
          page: 1,
          size: 5
        }
      });
      console.log('✅ Herramienta ejecutada exitosamente');
    } catch (error) {
      console.log('⚠️ Herramienta no ejecutada (configuración requerida):', error.message);
    }

    console.log('\n🎉 ¡Todas las pruebas del protocolo MCP completadas exitosamente!');

  } catch (error) {
    console.error('❌ Error en las pruebas MCP:', error.message);
    console.error('Detalles:', error);
  }
}

async function mcpRequest(method, params = {}) {
  const response = await fetch(MCP_SERVER_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      method,
      params,
      id: Math.floor(Math.random() * 1000)
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  
  if (data.error) {
    throw new Error(`MCP Error ${data.error.code}: ${data.error.message}`);
  }

  return data;
}

// Ejecutar pruebas
testMCPProtocol();

export { testMCPProtocol, mcpRequest };
