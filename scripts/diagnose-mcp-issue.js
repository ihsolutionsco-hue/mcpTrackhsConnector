#!/usr/bin/env node

/**
 * Script de diagnóstico completo para el problema de Track HS MCP
 * Verifica configuración, conectividad y proporciona soluciones
 */

import https from 'https';
import http from 'http';

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

function logHeader(message) {
  log(`\n${'='.repeat(60)}`, 'cyan');
  log(`🔍 ${message}`, 'cyan');
  log(`${'='.repeat(60)}`, 'cyan');
}

// Función para hacer peticiones HTTP
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

// 1. Verificar estado del servidor MCP
async function checkMCPServerStatus() {
  logHeader('VERIFICANDO ESTADO DEL SERVIDOR MCP');
  
  try {
    const response = await makeRequest('https://trackhs-mcp-connector.vercel.app/api/health');
    
    if (response.statusCode === 200) {
      logSuccess('Servidor MCP está funcionando');
      logInfo(`Servicio: ${response.data.service}`);
      logInfo(`Versión: ${response.data.version}`);
      logInfo(`Estado: ${response.data.status}`);
      
      if (response.data.environment) {
        logInfo(`Track HS configurado: ${response.data.environment.trackhsConfigured}`);
        logInfo(`API Client: ${response.data.environment.hasApiClient}`);
        logInfo(`URL API: ${response.data.environment.apiUrl}`);
        logInfo(`Usuario: ${response.data.environment.username}`);
        logInfo(`Contraseña: ${response.data.environment.password}`);
      }
      
      return response.data;
    } else {
      logError(`Servidor MCP no responde correctamente: ${response.statusCode}`);
      return null;
    }
  } catch (error) {
    logError(`Error conectando con servidor MCP: ${error.message}`);
    return null;
  }
}

// 2. Probar conectividad con Track HS
async function testTrackHSConnectivity() {
  logHeader('PROBANDO CONECTIVIDAD CON TRACK HS');
  
  try {
    const response = await makeRequest('https://trackhs-mcp-connector.vercel.app/api/test-connectivity');
    
    if (response.statusCode === 200) {
      logSuccess('Conectividad con Track HS exitosa');
      logInfo(`Resultado: ${JSON.stringify(response.data, null, 2)}`);
      return true;
    } else {
      logError(`Error en conectividad: ${response.statusCode}`);
      if (response.data) {
        logError(`Detalles: ${JSON.stringify(response.data, null, 2)}`);
      }
      return false;
    }
  } catch (error) {
    logError(`Error probando conectividad: ${error.message}`);
    return false;
  }
}

// 3. Probar herramienta específica
async function testSpecificTool() {
  logHeader('PROBANDO HERRAMIENTA ESPECÍFICA');
  
  try {
    // Simular llamada MCP
    const mcpRequest = {
      jsonrpc: '2.0',
      method: 'tools/call',
      params: {
        name: 'search_reservations',
        arguments: {}
      },
      id: 1
    };
    
    const response = await makeRequest('https://trackhs-mcp-connector.vercel.app/api/mcp', {
      method: 'POST',
      body: mcpRequest
    });
    
    if (response.statusCode === 200) {
      logSuccess('Herramienta ejecutada correctamente');
      logInfo(`Respuesta: ${JSON.stringify(response.data, null, 2)}`);
      return true;
    } else {
      logError(`Error ejecutando herramienta: ${response.statusCode}`);
      if (response.data) {
        logError(`Detalles: ${JSON.stringify(response.data, null, 2)}`);
      }
      return false;
    }
  } catch (error) {
    logError(`Error probando herramienta: ${error.message}`);
    return false;
  }
}

// 4. Generar reporte de diagnóstico
function generateDiagnosticReport(results) {
  logHeader('REPORTE DE DIAGNÓSTICO');
  
  const issues = [];
  const solutions = [];
  
  if (!results.serverStatus) {
    issues.push('❌ Servidor MCP no está funcionando');
    solutions.push('Verificar despliegue en Vercel');
  }
  
  if (!results.connectivity) {
    issues.push('❌ No hay conectividad con Track HS');
    solutions.push('Configurar variables de entorno en Vercel');
    solutions.push('Verificar credenciales de Track HS');
  }
  
  if (!results.toolTest) {
    issues.push('❌ Las herramientas MCP no funcionan');
    solutions.push('Revisar configuración de credenciales');
    solutions.push('Verificar que la API de Track HS esté disponible');
  }
  
  if (issues.length === 0) {
    logSuccess('🎉 ¡Todo está funcionando correctamente!');
    logInfo('El problema puede estar en la configuración de Claude Desktop');
  } else {
    logError('🚨 PROBLEMAS IDENTIFICADOS:');
    issues.forEach(issue => log(issue, 'red'));
    
    logWarning('\n💡 SOLUCIONES RECOMENDADAS:');
    solutions.forEach(solution => log(`• ${solution}`, 'yellow'));
  }
  
  logHeader('PASOS PARA RESOLVER');
  
  log('1. 📋 Configurar Variables de Entorno en Vercel:', 'blue');
  log('   - Ve a https://vercel.com/dashboard', 'cyan');
  log('   - Selecciona tu proyecto "trackhs-mcp-connector"', 'cyan');
  log('   - Ve a Settings > Environment Variables', 'cyan');
  log('   - Agrega las variables requeridas', 'cyan');
  
  log('\n2. 🔑 Variables requeridas:', 'blue');
  log('   TRACKHS_API_URL=https://api.trackhs.com/api', 'cyan');
  log('   TRACKHS_USERNAME=tu_usuario_real', 'cyan');
  log('   TRACKHS_PASSWORD=tu_contraseña_real', 'cyan');
  
  log('\n3. 🚀 Redesplegar la aplicación:', 'blue');
  log('   npm run deploy', 'cyan');
  
  log('\n4. ✅ Verificar funcionamiento:', 'blue');
  log('   curl https://trackhs-mcp-connector.vercel.app/api/health', 'cyan');
}

// Función principal
async function main() {
  log('🔍 DIAGNÓSTICO COMPLETO - TRACK HS MCP CONNECTOR', 'bright');
  
  const results = {
    serverStatus: await checkMCPServerStatus(),
    connectivity: false,
    toolTest: false
  };
  
  if (results.serverStatus) {
    results.connectivity = await testTrackHSConnectivity();
    if (results.connectivity) {
      results.toolTest = await testSpecificTool();
    }
  }
  
  generateDiagnosticReport(results);
  
  // Exit code basado en resultados
  const allWorking = results.serverStatus && results.connectivity && results.toolTest;
  process.exit(allWorking ? 0 : 1);
}

// Manejar errores
process.on('uncaughtException', (error) => {
  logError(`Error no capturado: ${error.message}`);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logError(`Promesa rechazada: ${reason}`);
  process.exit(1);
});

// Ejecutar diagnóstico
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    logError(`Error en diagnóstico: ${error.message}`);
    process.exit(1);
  });
}
