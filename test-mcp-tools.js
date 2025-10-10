/**
 * Script para probar las herramientas MCP del TrackHS Connector
 */

import fetch from 'node-fetch';

const MCP_ENDPOINT = 'https://trackhs-mcp-connector.vercel.app/api/mcp';

// Función para hacer peticiones JSON-RPC
async function mcpRequest(method, params = {}) {
  const body = {
    jsonrpc: '2.0',
    method: method,
    params: params,
    id: Math.floor(Math.random() * 1000)
  };

  console.log(`\n🔧 Probando: ${method}`);
  console.log(`📤 Enviando:`, JSON.stringify(body, null, 2));

  try {
    const response = await fetch(MCP_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(body)
    });

    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.log(`❌ Error Response:`, errorText);
      return null;
    }

    const data = await response.json();
    console.log(`✅ Respuesta:`, JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.log(`❌ Error:`, error.message);
    return null;
  }
}

// Función principal de testing
async function testMCPTools() {
  console.log('🚀 Iniciando testing de herramientas MCP TrackHS...');
  console.log(`📍 Endpoint: ${MCP_ENDPOINT}`);

  // 1. Probar listado de herramientas
  console.log('\n📋 === PROBANDO LISTADO DE HERRAMIENTAS ===');
  const toolsList = await mcpRequest('tools/list');
  
  if (toolsList && toolsList.result && toolsList.result.tools) {
    console.log(`✅ Se encontraron ${toolsList.result.tools.length} herramientas:`);
    toolsList.result.tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description}`);
    });
  }

  // 2. Probar listado de recursos
  console.log('\n📚 === PROBANDO LISTADO DE RECURSOS ===');
  const resourcesList = await mcpRequest('resources/list');
  
  if (resourcesList && resourcesList.result && resourcesList.result.resources) {
    console.log(`✅ Se encontraron ${resourcesList.result.resources.length} recursos:`);
    resourcesList.result.resources.forEach(resource => {
      console.log(`  - ${resource.name}: ${resource.description}`);
    });
  }

  // 3. Probar listado de prompts
  console.log('\n💬 === PROBANDO LISTADO DE PROMPTS ===');
  const promptsList = await mcpRequest('prompts/list');
  
  if (promptsList && promptsList.result && promptsList.result.prompts) {
    console.log(`✅ Se encontraron ${promptsList.result.prompts.length} prompts:`);
    promptsList.result.prompts.forEach(prompt => {
      console.log(`  - ${prompt.name}: ${prompt.description}`);
    });
  }

  // 4. Probar herramienta get_contacts
  console.log('\n👥 === PROBANDO HERRAMIENTA GET_CONTACTS ===');
  const contactsResult = await mcpRequest('tools/call', {
    name: 'get_contacts',
    arguments: {
      page: 1,
      size: 5
    }
  });

  // 5. Probar herramienta get_units
  console.log('\n🏠 === PROBANDO HERRAMIENTA GET_UNITS ===');
  const unitsResult = await mcpRequest('tools/call', {
    name: 'get_units',
    arguments: {
      page: 1,
      size: 3
    }
  });

  // 6. Probar herramienta get_reviews
  console.log('\n⭐ === PROBANDO HERRAMIENTA GET_REVIEWS ===');
  const reviewsResult = await mcpRequest('tools/call', {
    name: 'get_reviews',
    arguments: {
      page: 1,
      size: 3
    }
  });

  console.log('\n🎉 Testing completado!');
}

// Ejecutar testing
testMCPTools().catch(console.error);
