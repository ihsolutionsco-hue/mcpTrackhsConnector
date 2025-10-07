#!/usr/bin/env node

/**
 * Script de verificación del despliegue en Vercel
 * Track HS MCP Connector
 */

import https from 'https';

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

// URL del conector
const CONNECTOR_URL = 'https://trackhs-mcp-connector.vercel.app';

// Realizar petición HTTP
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
        'Accept': 'application/json',
        'User-Agent': 'TrackHS-MCP-Connector/1.0.0',
        ...options.headers
      },
      timeout: 10000
    };

    const req = https.request(requestOptions, (res) => {
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

// Verificar estado del despliegue
async function checkDeploymentStatus() {
  log('\n🚀 Verificando estado del despliegue...', 'cyan');
  
  try {
    const response = await makeRequest(`${CONNECTOR_URL}/api/health`);
    
    if (response.statusCode === 200) {
      logSuccess('Despliegue funcionando correctamente');
      
      if (response.data) {
        logInfo(`Servicio: ${response.data.service}`);
        logInfo(`Versión: ${response.data.version}`);
        logInfo(`Estado: ${response.data.status}`);
        
        if (response.data.tools) {
          logInfo(`Herramientas disponibles: ${response.data.tools.count}`);
        }
        
        if (response.data.environment) {
          const trackhsConfigured = response.data.environment.trackhsConfigured;
          if (trackhsConfigured) {
            logSuccess('Track HS configurado correctamente');
          } else {
            logWarning('Track HS no configurado - Variables de entorno faltantes');
          }
        }
      }
      
      return true;
    } else {
      logError(`Despliegue falló: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    logError(`Error verificando despliegue: ${error.message}`);
    return false;
  }
}

// Verificar herramientas disponibles
async function checkAvailableTools() {
  log('\n🛠️  Verificando herramientas disponibles...', 'cyan');
  
  try {
    const response = await makeRequest(`${CONNECTOR_URL}/api/tools`);
    
    if (response.statusCode === 200) {
      logSuccess('Herramientas accesibles');
      
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
      logError(`Error accediendo a herramientas: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    logError(`Error verificando herramientas: ${error.message}`);
    return false;
  }
}

// Probar una herramienta específica
async function testToolExecution() {
  log('\n🧪 Probando ejecución de herramienta...', 'cyan');
  
  try {
    const response = await makeRequest(`${CONNECTOR_URL}/api/tools/get_reviews/execute`, {
      method: 'POST',
      body: {
        name: 'get_reviews',
        arguments: { page: 1, size: 3 }
      }
    });
    
    if (response.statusCode === 200) {
      logSuccess('Herramienta ejecutada correctamente');
      
      if (response.data && response.data.result) {
        const result = response.data.result;
        logInfo(`Estado: ${result.status}`);
        logInfo(`Tiempo de ejecución: ${response.data.executionTime}`);
        
        if (result.status === 'success') {
          logSuccess('✅ Respuesta exitosa de Track HS API');
        } else if (result.status === 'error') {
          logWarning(`⚠️  Error en la herramienta: ${result.error}`);
          logInfo('Esto puede ser normal si las variables de entorno no están configuradas');
        }
      }
      
      return true;
    } else {
      logError(`Error ejecutando herramienta: ${response.statusCode}`);
      if (response.data) {
        logError(`Error: ${response.data.error || 'Error desconocido'}`);
      }
      return false;
    }
  } catch (error) {
    logError(`Error probando herramienta: ${error.message}`);
    return false;
  }
}

// Verificar CORS
async function checkCORS() {
  log('\n🌐 Verificando CORS...', 'cyan');
  
  try {
    const response = await makeRequest(`${CONNECTOR_URL}/api/health`, {
      headers: {
        'Origin': 'https://example.com'
      }
    });
    
    const corsHeaders = response.headers;
    const hasCORS = corsHeaders['access-control-allow-origin'] || 
                   corsHeaders['Access-Control-Allow-Origin'];
    
    if (hasCORS) {
      logSuccess('CORS configurado correctamente');
      return true;
    } else {
      logWarning('CORS no detectado');
      return false;
    }
  } catch (error) {
    logError(`Error verificando CORS: ${error.message}`);
    return false;
  }
}

// Generar reporte de despliegue
function generateDeploymentReport(results) {
  log('\n📊 Reporte de Despliegue', 'magenta');
  log('='.repeat(50), 'magenta');
  
  const totalChecks = Object.keys(results).length;
  const passedChecks = Object.values(results).filter(Boolean).length;
  const failedChecks = totalChecks - passedChecks;
  
  log(`\n✅ Verificaciones exitosas: ${passedChecks}/${totalChecks}`, 'green');
  
  if (failedChecks > 0) {
    log(`❌ Verificaciones fallidas: ${failedChecks}/${totalChecks}`, 'red');
  }
  
  log('\n📋 Estado de cada verificación:', 'blue');
  Object.entries(results).forEach(([check, passed]) => {
    const status = passed ? '✅' : '❌';
    log(`${status} ${check}`);
  });
  
  if (passedChecks === totalChecks) {
    log('\n🎉 ¡Despliegue completamente funcional!', 'green');
    log('Tu conector MCP está listo para usar.', 'green');
    
    log('\n🔗 URLs del conector:', 'blue');
    log(`- Health Check: ${CONNECTOR_URL}/api/health`);
    log(`- Herramientas: ${CONNECTOR_URL}/api/tools`);
    log(`- Ejecutar herramienta: ${CONNECTOR_URL}/api/tools/{name}/execute`);
    
    log('\n📚 Próximos pasos:', 'blue');
    log('1. Configurar en Claude Desktop o Make.com');
    log('2. Configurar variables de entorno en Vercel si no están configuradas');
    log('3. Probar con datos reales de Track HS');
    log('4. Monitorear logs en Vercel Dashboard');
  } else {
    log('\n🔧 Acciones requeridas:', 'yellow');
    if (!results.deployment) {
      log('- Verificar que el despliegue esté completo en Vercel');
    }
    if (!results.tools) {
      log('- Verificar que las herramientas estén implementadas');
    }
    if (!results.execution) {
      log('- Verificar variables de entorno en Vercel');
    }
    if (!results.cors) {
      log('- Verificar configuración de CORS');
    }
  }
  
  log('\n📚 Documentación:', 'blue');
  log('- Resumen de despliegue: DEPLOYMENT_SUMMARY.md');
  log('- Actualizaciones: DEPENDENCY_UPDATE_SUMMARY.md');
  log('- Guía rápida: QUICK_START_VERCEL.md');
}

// Función principal
async function main() {
  log('🔍 Verificador de Despliegue - Track HS MCP Connector', 'bright');
  log('='.repeat(60), 'bright');
  log(`URL del conector: ${CONNECTOR_URL}`, 'blue');
  
  const results = {
    deployment: await checkDeploymentStatus(),
    tools: await checkAvailableTools(),
    execution: await testToolExecution(),
    cors: await checkCORS()
  };
  
  generateDeploymentReport(results);
  
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

// Ejecutar
main().catch((error) => {
  logError(`Error en verificación: ${error.message}`);
  process.exit(1);
});
