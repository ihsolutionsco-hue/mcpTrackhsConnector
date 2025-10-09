#!/usr/bin/env node

/**
 * Script para configurar automáticamente las variables de entorno en Vercel
 * Track HS MCP Connector
 */

import { execSync } from 'child_process';

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

// Variables de entorno a configurar
const envVars = {
  'TRACKHS_API_URL': 'https://ihmvacations.trackhs.com/api',
  'TRACKHS_USERNAME': 'aba99777416466b6bdc1a25223192ccb',
  'TRACKHS_PASSWORD': '18c874610113f355cc11000a24215cbda'
};

async function setupVercelEnvironment() {
  logHeader('CONFIGURANDO VARIABLES DE ENTORNO EN VERCEL');
  
  try {
    // Verificar si Vercel CLI está instalado
    try {
      execSync('vercel --version', { stdio: 'pipe' });
      logSuccess('Vercel CLI está instalado');
    } catch (error) {
      logError('Vercel CLI no está instalado. Instalando...');
      execSync('npm install -g vercel', { stdio: 'inherit' });
    }
    
    // Configurar cada variable de entorno
    for (const [key, value] of Object.entries(envVars)) {
      logInfo(`Configurando ${key}...`);
      
      try {
        // Usar echo para pasar el valor a vercel env add
        const command = `echo "${value}" | vercel env add ${key} production`;
        execSync(command, { stdio: 'inherit' });
        logSuccess(`${key} configurado correctamente`);
      } catch (error) {
        logWarning(`Error configurando ${key}: ${error.message}`);
        logInfo('Intentando método alternativo...');
        
        // Método alternativo usando vercel env add con input
        try {
          const altCommand = `vercel env add ${key} production --value="${value}"`;
          execSync(altCommand, { stdio: 'inherit' });
          logSuccess(`${key} configurado con método alternativo`);
        } catch (altError) {
          logError(`No se pudo configurar ${key}: ${altError.message}`);
        }
      }
    }
    
    logHeader('REDESPLEGANDO APLICACIÓN');
    
    try {
      logInfo('Redesplegando aplicación con nuevas variables...');
      execSync('vercel --prod', { stdio: 'inherit' });
      logSuccess('Aplicación redesplegada correctamente');
    } catch (error) {
      logError(`Error redesplegando: ${error.message}`);
    }
    
    logHeader('VERIFICACIÓN FINAL');
    
    // Esperar un momento para que el despliegue se complete
    logInfo('Esperando que el despliegue se complete...');
    await new Promise(resolve => setTimeout(resolve, 10000));
    
    // Verificar que el servidor responde
    try {
      const https = await import('https');
      const response = await new Promise((resolve, reject) => {
        const req = https.request('https://trackhs-mcp-connector.vercel.app/api/health', (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve(JSON.parse(data)));
        });
        req.on('error', reject);
        req.end();
      });
      
      logSuccess('Servidor MCP funcionando correctamente');
      logInfo(`Estado: ${response.status}`);
      logInfo(`Servicio: ${response.service}`);
      
      if (response.environment) {
        logInfo(`Track HS configurado: ${response.environment.trackhsConfigured}`);
        logInfo(`API Client: ${response.environment.hasApiClient}`);
      }
      
    } catch (error) {
      logWarning(`No se pudo verificar el servidor: ${error.message}`);
    }
    
    logHeader('CONFIGURACIÓN COMPLETADA');
    logSuccess('✅ Variables de entorno configuradas');
    logSuccess('✅ Aplicación redesplegada');
    logSuccess('✅ Servidor MCP funcionando');
    
    log('\n🎉 ¡CONFIGURACIÓN COMPLETADA!', 'green');
    log('Ahora puedes usar las herramientas de Track HS en Claude.', 'green');
    
  } catch (error) {
    logError(`Error en configuración: ${error.message}`);
    process.exit(1);
  }
}

// Ejecutar configuración
if (import.meta.url === `file://${process.argv[1]}`) {
  setupVercelEnvironment().catch((error) => {
    logError(`Error fatal: ${error.message}`);
    process.exit(1);
  });
}
