/**
 * Script de diagnóstico para identificar la causa del Error 500
 */

import fetch from 'node-fetch';

const MCP_SERVER_URL = 'https://trackhs-mcp-connector.vercel.app/api/mcp';

async function diagnoseMCPError() {
  console.log('🔍 Diagnóstico del Error 500 en MCP...\n');

  // 1. Probar health check primero
  console.log('1️⃣ Probando health check...');
  try {
    const healthResponse = await fetch('https://trackhs-mcp-connector.vercel.app/api/health');
    console.log('Health check status:', healthResponse.status);
    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      console.log('✅ Health check OK:', healthData);
    } else {
      console.log('❌ Health check falló');
    }
  } catch (error) {
    console.log('❌ Error en health check:', error.message);
  }

  // 2. Probar con request mínimo
  console.log('\n2️⃣ Probando request mínimo...');
  try {
    const response = await fetch(MCP_SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'initialize',
        params: {},
        id: 1
      })
    });

    console.log('Status:', response.status);
    console.log('Headers:', Object.fromEntries(response.headers.entries()));
    
    const text = await response.text();
    console.log('Response body:', text);
    
    if (response.ok) {
      console.log('✅ Request mínimo exitoso');
    } else {
      console.log('❌ Request mínimo falló');
    }
  } catch (error) {
    console.log('❌ Error en request mínimo:', error.message);
  }

  // 3. Probar con diferentes métodos
  console.log('\n3️⃣ Probando diferentes métodos...');
  const methods = ['initialize', 'tools/list', 'resources/list'];
  
  for (const method of methods) {
    try {
      console.log(`\nProbando método: ${method}`);
      const response = await fetch(MCP_SERVER_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method,
          params: {},
          id: Math.floor(Math.random() * 1000)
        })
      });

      console.log(`Status: ${response.status}`);
      const text = await response.text();
      console.log(`Response: ${text.substring(0, 200)}...`);
      
    } catch (error) {
      console.log(`❌ Error con método ${method}:`, error.message);
    }
  }

  // 4. Probar con request malformado
  console.log('\n4️⃣ Probando request malformado...');
  try {
    const response = await fetch(MCP_SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        // Sin method - debería dar error 400, no 500
        params: {},
        id: 1
      })
    });

    console.log('Status con request malformado:', response.status);
    const text = await response.text();
    console.log('Response:', text);
    
  } catch (error) {
    console.log('❌ Error con request malformado:', error.message);
  }

  console.log('\n🏁 Diagnóstico completado');
}

diagnoseMCPError();
