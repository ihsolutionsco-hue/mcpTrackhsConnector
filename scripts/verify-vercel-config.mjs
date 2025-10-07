#!/usr/bin/env node

/**
 * Script de verificación de configuración para Vercel
 * Track HS MCP Connector
 * 
 * Este script verifica que todas las variables de entorno
 * estén configuradas correctamente para el despliegue en Vercel.
 */

import https from 'https';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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

// Verificar variables de entorno
function checkEnvironmentVariables() {
  log('\n🔍 Verificando variables de entorno...', 'cyan');
  
  const requiredVars = [
    'TRACKHS_API_URL',
    'TRACKHS_USERNAME', 
    'TRACKHS_PASSWORD'
  ];
  
  const missingVars = [];
  const presentVars = [];
  
  for (const varName of requiredVars) {
    if (process.env[varName]) {
      presentVars.push(varName);
      logSuccess(`${varName} está configurada`);
    } else {
      missingVars.push(varName);
      logError(`${varName} NO está configurada`);
    }
  }
  
  if (missingVars.length > 0) {
    logError(`\n❌ Variables faltantes: ${missingVars.join(', ')}`);
    logWarning('\n📋 Para configurar en Vercel:');
    log('1. Ve a https://vercel.com/dashboard');
    log('2. Selecciona tu proyecto');
    log('3. Ve a Settings → Environment Variables');
    log('4. Agrega las variables faltantes');
    log('5. Re-despliega el proyecto');
    return false;
  }
  
  logSuccess(`\n✅ Todas las variables de entorno están configuradas`);
  return true;
}

// Verificar formato de URL
function checkApiUrl() {
  log('\n🌐 Verificando URL de API...', 'cyan');
  
  const apiUrl = process.env.TRACKHS_API_URL;
  
  try {
    const url = new URL(apiUrl);
    
    if (url.protocol !== 'https:') {
      logWarning('La URL debería usar HTTPS para mayor seguridad');
    }
    
    logSuccess(`URL válida: ${apiUrl}`);
    return true;
  } catch (error) {
    logError(`URL inválida: ${apiUrl}`);
    logError(`Error: ${error.message}`);
    return false;
  }
}

// Probar conectividad con Track HS API
async function testTrackHSConnection() {
  log('\n🔗 Probando conectividad con Track HS API...', 'cyan');
  
  const apiUrl = process.env.TRACKHS_API_URL;
  const username = process.env.TRACKHS_USERNAME;
  const password = process.env.TRACKHS_PASSWORD;
  
  return new Promise((resolve) => {
    try {
      const url = new URL(apiUrl);
      const credentials = Buffer.from(`${username}:${password}`).toString('base64');
      
      const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname,
        method: 'GET',
        headers: {
          'Authorization': `Basic ${credentials}`,
          'Accept': 'application/json',
          'User-Agent': 'TrackHS-MCP-Connector/1.0.0'
        },
        timeout: 10000
      };
      
      const req = https.request(options, (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          logSuccess(`Conexión exitosa (${res.statusCode})`);
          resolve(true);
        } else if (res.statusCode === 401) {
          logError('Error de autenticación (401) - Verifica credenciales');
          resolve(false);
        } else if (res.statusCode === 404) {
          logWarning('Endpoint no encontrado (404) - Verifica la URL');
          resolve(false);
        } else {
          logError(`Error HTTP: ${res.statusCode}`);
          resolve(false);
        }
      });
      
      req.on('error', (error) => {
        logError(`Error de conexión: ${error.message}`);
        resolve(false);
      });
      
      req.on('timeout', () => {
        logError('Timeout de conexión');
        req.destroy();
        resolve(false);
      });
      
      req.setTimeout(10000);
      req.end();
      
    } catch (error) {
      logError(`Error en la prueba: ${error.message}`);
      resolve(false);
    }
  });
}

// Verificar configuración de Vercel
function checkVercelConfig() {
  log('\n⚙️  Verificando configuración de Vercel...', 'cyan');
  
  const vercelJsonPath = path.join(process.cwd(), 'vercel.json');
  
  if (!fs.existsSync(vercelJsonPath)) {
    logError('vercel.json no encontrado');
    return false;
  }
  
  try {
    const vercelConfig = JSON.parse(fs.readFileSync(vercelJsonPath, 'utf8'));
    
    // Verificar configuración de función
    if (vercelConfig.functions && vercelConfig.functions['api/index.js']) {
      const funcConfig = vercelConfig.functions['api/index.js'];
      logSuccess('Configuración de función encontrada');
      
      if (funcConfig.maxDuration) {
        logInfo(`Duración máxima: ${funcConfig.maxDuration}s`);
      }
      
      if (funcConfig.memory) {
        logInfo(`Memoria: ${funcConfig.memory}MB`);
      }
      
      if (funcConfig.runtime) {
        logInfo(`Runtime: ${funcConfig.runtime}`);
      }
    }
    
    // Verificar rutas
    if (vercelConfig.routes && vercelConfig.routes.length > 0) {
      logSuccess(`${vercelConfig.routes.length} rutas configuradas`);
    }
    
    // Verificar headers CORS
    if (vercelConfig.headers && vercelConfig.headers.length > 0) {
      logSuccess('Headers CORS configurados');
    }
    
    logSuccess('Configuración de Vercel válida');
    return true;
    
  } catch (error) {
    logError(`Error leyendo vercel.json: ${error.message}`);
    return false;
  }
}

// Verificar archivo API
function checkApiFile() {
  log('\n📁 Verificando archivo API...', 'cyan');
  
  const apiFilePath = path.join(process.cwd(), 'api', 'index.js');
  
  if (!fs.existsSync(apiFilePath)) {
    logError('api/index.js no encontrado');
    return false;
  }
  
  const apiContent = fs.readFileSync(apiFilePath, 'utf8');
  
  // Verificar que no esté en modo demostración
  if (apiContent.includes('respuesta de demostración') || apiContent.includes('simulación')) {
    logError('El archivo API está en modo demostración');
    logWarning('Necesitas implementar la conexión real con Track HS API');
    return false;
  }
  
  // Verificar que tenga las funciones necesarias
  const requiredFunctions = [
    'executeTool',
    'makeTrackHSRequest',
    'handleHealth',
    'handleListTools',
    'handleExecuteTool'
  ];
  
  let missingFunctions = [];
  for (const funcName of requiredFunctions) {
    if (!apiContent.includes(funcName)) {
      missingFunctions.push(funcName);
    }
  }
  
  if (missingFunctions.length > 0) {
    logError(`Funciones faltantes: ${missingFunctions.join(', ')}`);
    return false;
  }
  
  logSuccess('Archivo API válido');
  return true;
}

// Generar reporte
function generateReport(results) {
  log('\n📊 Reporte de Verificación', 'magenta');
  log('='.repeat(50), 'magenta');
  
  const totalChecks = Object.keys(results).length;
  const passedChecks = Object.values(results).filter(Boolean).length;
  const failedChecks = totalChecks - passedChecks;
  
  log(`\n✅ Verificaciones exitosas: ${passedChecks}/${totalChecks}`, 'green');
  
  if (failedChecks > 0) {
    log(`❌ Verificaciones fallidas: ${failedChecks}/${totalChecks}`, 'red');
    
    log('\n🔧 Acciones recomendadas:', 'yellow');
    
    if (!results.environment) {
      log('1. Configurar variables de entorno en Vercel Dashboard');
    }
    
    if (!results.apiUrl) {
      log('2. Verificar que TRACKHS_API_URL sea una URL válida');
    }
    
    if (!results.connection) {
      log('3. Verificar credenciales y conectividad con Track HS');
    }
    
    if (!results.vercelConfig) {
      log('4. Verificar configuración en vercel.json');
    }
    
    if (!results.apiFile) {
      log('5. Verificar implementación en api/index.js');
    }
  } else {
    log('\n🎉 ¡Todas las verificaciones pasaron!', 'green');
    log('Tu conector MCP está listo para desplegarse en Vercel.', 'green');
  }
  
  log('\n📚 Documentación:', 'blue');
  log('- Guía de despliegue: docs/VERCEL_DEPLOYMENT.md');
  log('- Configuración rápida: QUICK_START_VERCEL.md');
  log('- Troubleshooting: README.md');
}

// Función principal
async function main() {
  log('🚀 Verificador de Configuración - Track HS MCP Connector', 'bright');
  log('='.repeat(60), 'bright');
  
  const results = {
    environment: checkEnvironmentVariables(),
    apiUrl: checkApiUrl(),
    vercelConfig: checkVercelConfig(),
    apiFile: checkApiFile()
  };
  
  // Solo probar conexión si las variables están configuradas
  if (results.environment && results.apiUrl) {
    results.connection = await testTrackHSConnection();
  } else {
    logWarning('Saltando prueba de conexión - Variables de entorno faltantes');
    results.connection = false;
  }
  
  generateReport(results);
  
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
    logError(`Error en verificación: ${error.message}`);
    process.exit(1);
  });
}

export {
  checkEnvironmentVariables,
  checkApiUrl,
  testTrackHSConnection,
  checkVercelConfig,
  checkApiFile
};
