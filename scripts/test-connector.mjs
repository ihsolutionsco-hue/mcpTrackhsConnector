#!/usr/bin/env node

/**
 * Script de prueba del conector MCP en Vercel
 * Track HS MCP Connector
 * 
 * Este script prueba todas las funcionalidades del conector
 * después de los cambios para asegurar que funciona correctamente.
 */

import https from 'https';
import http from 'http';

// Colores para output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green');
}

function logError(message) {
  log(`❌ ${message}`, 'red');
}

function logWarning(message) {
  log(`⚠️  ${message}`, 'yellow');
}

function logInfo(message) {
  log(`ℹ️  ${message}`, 'blue');
}

// Configuración
const CONNECTOR_URL = process.env.VERCEL_URL || 'https://trackhs-mcp-connector.vercel.app';
const API_BASE = `${CONNECTOR_URL}/api`;

// Realizar petición HTTP
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const protocol = urlObj.protocol === 'https:' ? https : http;
    
    const requestOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
      },
      timeout: 10000
    };

    const req = protocol.request(requestOptions, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const response = {
            statusCode: res.statusCode,
            headers: res.headers,
            data: data ? JSON.parse(data) : null
          };
          resolve(response);
        } catch (error) {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            data: data,
            parseError: error.message
          });
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.on('timeout', () => {
      reject(new Error('Request timeout'));
      req.destroy();
    });

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }

    req.setTimeout(10000);
    req.end();
  });
}

// Probar Health Check
async function testHealthCheck() {
  log('\n🏥 Probando Health Check...', 'cyan');
  
  try {
    const response = await makeRequest(`${API_BASE}/health`);
    
    if (response.statusCode === 200) {
      logSuccess('Health check exitoso');
      
      if (response.data) {
        logInfo(`Servicio: ${response.data.service}`);
        logInfo(`Versión: ${response.data.version}`);
        logInfo(`Estado: ${response.data.status}`);
        
        if (response.data.tools) {
          logInfo(`Herramientas disponibles: ${response.data.tools.count}`);
        }
        
        if (response.data.environment) {
          logInfo(`Track HS configurado: ${response.data.environment.trackhsConfigured}`);
        }
      }
      
      return true;
    } else {
      logError(`Health check falló: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    logError(`Error en health check: ${error.message}`);
    return false;
  }
}

// Probar Lista de Herramientas
async function testListTools() {
  log('\n🛠️  Probando Lista de Herramientas...', 'cyan');
  
  try {
    const response = await makeRequest(`${API_BASE}/tools`);
    
    if (response.statusCode === 200) {
      logSuccess('Lista de herramientas exitosa');
      
      if (response.data && response.data.tools) {
        logInfo(`Total de herramientas: ${response.data.tools.length}`);
        
        // Mostrar primeras 5 herramientas
        const tools = response.data.tools.slice(0, 5);
        tools.forEach(tool => {
          logInfo(`- ${tool.name}: ${tool.description}`);
        });
        
        if (response.data.tools.length > 5) {
          logInfo(`... y ${response.data.tools.length - 5} más`);
        }
      }
      
      return true;
    } else {
      logError(`Lista de herramientas falló: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    logError(`Error en lista de herramientas: ${error.message}`);
    return false;
  }
}

// Probar Herramienta Específica
async function testToolExecution(toolName, args = {}) {
  log(`\n🔧 Probando herramienta: ${toolName}...`, 'cyan');
  
  try {
    const response = await makeRequest(`${API_BASE}/tools/${toolName}/execute`, {
      method: 'POST',
      body: {
        name: toolName,
        arguments: args
      }
    });
    
    if (response.statusCode === 200) {
      logSuccess(`Herramienta ${toolName} ejecutada exitosamente`);
      
      if (response.data && response.data.result) {
        const result = response.data.result;
        logInfo(`Estado: ${result.status}`);
        logInfo(`Tiempo de ejecución: ${response.data.executionTime}`);
        
        if (result.status === 'success') {
          logInfo('✅ Respuesta exitosa de Track HS API');
        } else if (result.status === 'error') {
          logWarning(`⚠️  Error en la herramienta: ${result.error}`);
        }
      }
      
      return true;
    } else {
      logError(`Herramienta ${toolName} falló: ${response.statusCode}`);
      if (response.data) {
        logError(`Error: ${response.data.error || 'Error desconocido'}`);
      }
      return false;
    }
  } catch (error) {
    logError(`Error ejecutando ${toolName}: ${error.message}`);
    return false;
  }
}

// Probar Múltiples Herramientas
async function testMultipleTools() {
  log('\n🧪 Probando múltiples herramientas...', 'cyan');
  
  const testCases = [
    {
      name: 'get_reviews',
      args: { page: 1, size: 5 },
      description: 'Obtener reseñas (página 1, 5 elementos)'
    },
    {
      name: 'get_contacts',
      args: { page: 1, size: 5 },
      description: 'Obtener contactos (página 1, 5 elementos)'
    },
    {
      name: 'get_units',
      args: { page: 1, size: 5 },
      description: 'Obtener unidades (página 1, 5 elementos)'
    }
  ];
  
  const results = [];
  
  for (const testCase of testCases) {
    logInfo(`\nProbando: ${testCase.description}`);
    const success = await testToolExecution(testCase.name, testCase.args);
    results.push({ name: testCase.name, success });
    
    // Pausa entre pruebas para no sobrecargar la API
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return results;
}

// Probar CORS
async function testCORS() {
  log('\n🌐 Probando CORS...', 'cyan');
  
  try {
    const response = await makeRequest(`${API_BASE}/health`, {
      headers: {
        'Origin': 'https://example.com',
        'Access-Control-Request-Method': 'GET'
      }
    });
    
    const corsHeaders = response.headers;
    const hasCORS = corsHeaders['access-control-allow-origin'] || 
                   corsHeaders['Access-Control-Allow-Origin'];
    
    if (hasCORS) {
      logSuccess('Headers CORS configurados correctamente');
      logInfo(`Allow-Origin: ${corsHeaders['access-control-allow-origin'] || corsHeaders['Access-Control-Allow-Origin']}`);
      return true;
    } else {
      logWarning('Headers CORS no detectados');
      return false;
    }
  } catch (error) {
    logError(`Error probando CORS: ${error.message}`);
    return false;
  }
}

// Probar Endpoint por Defecto
async function testDefaultEndpoint() {
  log('\n🏠 Probando endpoint por defecto...', 'cyan');
  
  try {
    const response = await makeRequest(`${CONNECTOR_URL}/`);
    
    if (response.statusCode === 200) {
      logSuccess('Endpoint por defecto funciona');
      
      if (response.data && response.data.service) {
        logInfo(`Servicio: ${response.data.service}`);
        logInfo(`Descripción: ${response.data.description}`);
      }
      
      return true;
    } else {
      logError(`Endpoint por defecto falló: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    logError(`Error en endpoint por defecto: ${error.message}`);
    return false;
  }
}

// Generar reporte de pruebas
function generateTestReport(results) {
  log('\n📊 Reporte de Pruebas del Conector', 'magenta');
  log('='.repeat(50), 'magenta');
  
  const totalTests = Object.keys(results).length;
  const passedTests = Object.values(results).filter(Boolean).length;
  const failedTests = totalTests - passedTests;
  
  log(`\n✅ Pruebas exitosas: ${passedTests}/${totalTests}`, 'green');
  
  if (failedTests > 0) {
    log(`❌ Pruebas fallidas: ${failedTests}/${totalTests}`, 'red');
    
    log('\n🔧 Pruebas fallidas:', 'yellow');
    Object.entries(results).forEach(([test, passed]) => {
      if (!passed) {
        log(`- ${test}`, 'red');
      }
    });
  } else {
    log('\n🎉 ¡Todas las pruebas pasaron!', 'green');
    log('Tu conector MCP está funcionando correctamente.', 'green');
  }
  
  log('\n📚 Próximos pasos:', 'blue');
  log('1. Configurar en Claude Desktop o Make.com');
  log('2. Probar con datos reales de Track HS');
  log('3. Monitorear logs en Vercel Dashboard');
  log('4. Configurar alertas de monitoreo');
}

// Función principal
async function main() {
  log('🧪 Probador del Conector MCP - Track HS', 'bright');
  log('='.repeat(50), 'bright');
  log(`URL del conector: ${CONNECTOR_URL}`, 'blue');
  
  const results = {
    healthCheck: await testHealthCheck(),
    listTools: await testListTools(),
    defaultEndpoint: await testDefaultEndpoint(),
    cors: await testCORS()
  };
  
  // Probar herramientas solo si el health check pasó
  if (results.healthCheck) {
    const toolResults = await testMultipleTools();
    results.tools = toolResults.every(r => r.success);
    
    if (toolResults.length > 0) {
      log('\n📋 Resultados de herramientas:', 'blue');
      toolResults.forEach(result => {
        const status = result.success ? '✅' : '❌';
        log(`${status} ${result.name}`);
      });
    }
  } else {
    logWarning('Saltando pruebas de herramientas - Health check falló');
    results.tools = false;
  }
  
  generateTestReport(results);
  
  // Exit code basado en resultados
  const allPassed = Object.values(results).every(Boolean);
  process.exit(allPassed ? 0 : 1);
}

// Manejar errores no capturados
process.on('uncaughtException', (error) => {
  logError(`Error no capturado: ${error.message}`);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logError(`Promesa rechazada: ${reason}`);
  process.exit(1);
});

// Ejecutar si es llamado directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    logError(`Error en pruebas: ${error.message}`);
    process.exit(1);
  });
}

export {
  testHealthCheck,
  testListTools,
  testToolExecution,
  testMultipleTools,
  testCORS,
  testDefaultEndpoint
};
