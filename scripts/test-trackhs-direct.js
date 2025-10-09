#!/usr/bin/env node

/**
 * Script para probar directamente la conectividad con Track HS
 * usando las credenciales configuradas
 */

import https from 'https';

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
  log(`🔧 ${message}`, 'cyan');
  log(`${'='.repeat(60)}`, 'cyan');
}

// Credenciales de Track HS
const TRACKHS_API_URL = 'https://ihmvacations.trackhs.com/api';
const TRACKHS_USERNAME = 'aba99777416466b6bdc1a25223192ccb';
const TRACKHS_PASSWORD = '18c874610113f355cc11000a24215cbda';

// Función para hacer petición directa a Track HS
function makeTrackHSRequest(endpoint) {
  return new Promise((resolve, reject) => {
    const url = `${TRACKHS_API_URL}${endpoint}`;
    const auth = Buffer.from(`${TRACKHS_USERNAME}:${TRACKHS_PASSWORD}`).toString('base64');
    
    logInfo(`Realizando petición a: ${url}`);
    
    const options = {
      hostname: 'ihmvacations.trackhs.com',
      port: 443,
      path: `/api${endpoint}`,
      method: 'GET',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'TrackHS-MCP-Connector/1.0.0'
      },
      timeout: 10000
    };

    const req = https.request(options, (res) => {
      let data = '';
      
      logInfo(`Respuesta recibida: ${res.statusCode} ${res.statusMessage}`);
      logInfo(`Headers: ${JSON.stringify(res.headers, null, 2)}`);
      
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
      logError(`Error en petición: ${error.message}`);
      reject(error);
    });

    req.on('timeout', () => {
      logError('Timeout en petición');
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.setTimeout(10000);
    req.end();
  });
}

// Probar diferentes endpoints de Track HS
async function testTrackHSEndpoints() {
  logHeader('PROBANDO CONECTIVIDAD DIRECTA CON TRACK HS');
  
  const endpoints = [
    { path: '/crm/contacts?page=1&size=1', name: 'Contactos' },
    { path: '/v2/pms/reservations/search?page=1&size=1', name: 'Reservaciones' },
    { path: '/pms/units?page=1&size=1', name: 'Unidades' },
    { path: '/pms/nodes?page=1&size=1', name: 'Nodos' }
  ];
  
  const results = [];
  
  for (const endpoint of endpoints) {
    logInfo(`\nProbando ${endpoint.name}...`);
    
    try {
      const response = await makeTrackHSRequest(endpoint.path);
      
      if (response.statusCode === 200) {
        logSuccess(`${endpoint.name}: Conectividad exitosa`);
        logInfo(`Datos recibidos: ${JSON.stringify(response.data, null, 2)}`);
        results.push({ name: endpoint.name, success: true, data: response.data });
      } else {
        logError(`${endpoint.name}: Error ${response.statusCode}`);
        logError(`Respuesta: ${JSON.stringify(response.data, null, 2)}`);
        results.push({ name: endpoint.name, success: false, error: response.data });
      }
    } catch (error) {
      logError(`${endpoint.name}: Error de conexión - ${error.message}`);
      results.push({ name: endpoint.name, success: false, error: error.message });
    }
    
    // Pausa entre peticiones
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return results;
}

// Función principal
async function main() {
  log('🔍 PRUEBA DIRECTA DE CONECTIVIDAD CON TRACK HS', 'bright');
  
  try {
    const results = await testTrackHSEndpoints();
    
    logHeader('RESULTADOS DE LA PRUEBA');
    
    const successful = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);
    
    log(`✅ Exitosas: ${successful.length}/${results.length}`, 'green');
    
    if (failed.length > 0) {
      log(`❌ Fallidas: ${failed.length}/${results.length}`, 'red');
      failed.forEach(result => {
        log(`- ${result.name}: ${result.error}`, 'red');
      });
    }
    
    if (successful.length > 0) {
      logSuccess('🎉 ¡La conectividad con Track HS está funcionando!');
      logInfo('El problema puede estar en la configuración del servidor MCP');
    } else {
      logError('🚨 No se pudo conectar con Track HS');
      logInfo('Verifica las credenciales y la URL de la API');
    }
    
  } catch (error) {
    logError(`Error en prueba: ${error.message}`);
    process.exit(1);
  }
}

// Ejecutar prueba
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    logError(`Error fatal: ${error.message}`);
    process.exit(1);
  });
}
