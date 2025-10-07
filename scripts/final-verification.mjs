#!/usr/bin/env node

/**
 * Verificación Final del Conector MCP
 * Track HS MCP Connector
 */

import fs from 'fs';
import path from 'path';

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

// Verificar archivos críticos
function checkCriticalFiles() {
  log('\n📁 Verificando archivos críticos...', 'cyan');
  
  const criticalFiles = [
    { path: 'api/index.js', description: 'API principal' },
    { path: 'vercel.json', description: 'Configuración de Vercel' },
    { path: 'package.json', description: 'Configuración del proyecto' },
    { path: 'scripts/verify-vercel-config.mjs', description: 'Script de verificación' },
    { path: 'scripts/test-connector.mjs', description: 'Script de pruebas' }
  ];
  
  let allPresent = true;
  
  criticalFiles.forEach(file => {
    if (fs.existsSync(file.path)) {
      logSuccess(`${file.description}: ${file.path}`);
    } else {
      logError(`${file.description} faltante: ${file.path}`);
      allPresent = false;
    }
  });
  
  return allPresent;
}

// Verificar contenido del API
function checkApiContent() {
  log('\n🔍 Verificando contenido del API...', 'cyan');
  
  try {
    const apiContent = fs.readFileSync('api/index.js', 'utf8');
    
    // Verificar que no esté en modo demostración
    if (apiContent.includes('respuesta de demostración') || apiContent.includes('simulación')) {
      logError('API está en modo demostración');
      return false;
    }
    
    // Verificar funciones críticas
    const criticalFunctions = [
      'makeTrackHSRequest',
      'executeTool',
      'handleHealth',
      'handleListTools',
      'handleExecuteTool'
    ];
    
    let missingFunctions = [];
    criticalFunctions.forEach(func => {
      if (!apiContent.includes(func)) {
        missingFunctions.push(func);
      }
    });
    
    if (missingFunctions.length > 0) {
      logError(`Funciones faltantes: ${missingFunctions.join(', ')}`);
      return false;
    }
    
    logSuccess('API implementado correctamente');
    return true;
    
  } catch (error) {
    logError(`Error leyendo API: ${error.message}`);
    return false;
  }
}

// Verificar configuración de Vercel
function checkVercelConfig() {
  log('\n⚙️  Verificando configuración de Vercel...', 'cyan');
  
  try {
    const vercelConfig = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    
    // Verificar configuración de función
    if (vercelConfig.functions && vercelConfig.functions['api/index.js']) {
      const funcConfig = vercelConfig.functions['api/index.js'];
      logSuccess('Configuración de función encontrada');
      
      if (funcConfig.runtime) {
        logInfo(`Runtime: ${funcConfig.runtime}`);
      }
      if (funcConfig.maxDuration) {
        logInfo(`Duración máxima: ${funcConfig.maxDuration}s`);
      }
      if (funcConfig.memory) {
        logInfo(`Memoria: ${funcConfig.memory}MB`);
      }
    }
    
    // Verificar headers CORS
    if (vercelConfig.headers && vercelConfig.headers.length > 0) {
      logSuccess('Headers CORS configurados');
    }
    
    // Verificar rutas
    if (vercelConfig.routes && vercelConfig.routes.length > 0) {
      logSuccess(`${vercelConfig.routes.length} rutas configuradas`);
    }
    
    return true;
    
  } catch (error) {
    logError(`Error en vercel.json: ${error.message}`);
    return false;
  }
}

// Verificar package.json
function checkPackageJson() {
  log('\n📦 Verificando package.json...', 'cyan');
  
  try {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    
    // Verificar scripts importantes
    const importantScripts = [
      'verify:vercel',
      'test:connector',
      'deploy'
    ];
    
    importantScripts.forEach(script => {
      if (packageJson.scripts && packageJson.scripts[script]) {
        logSuccess(`Script ${script} configurado`);
      } else {
        logWarning(`Script ${script} no encontrado`);
      }
    });
    
    // Verificar dependencias críticas
    const criticalDeps = [
      '@modelcontextprotocol/sdk',
      'dotenv'
    ];
    
    criticalDeps.forEach(dep => {
      if (packageJson.dependencies && packageJson.dependencies[dep]) {
        logSuccess(`Dependencia ${dep} encontrada`);
      } else {
        logWarning(`Dependencia ${dep} no encontrada`);
      }
    });
    
    return true;
    
  } catch (error) {
    logError(`Error en package.json: ${error.message}`);
    return false;
  }
}

// Verificar variables de entorno (solo si están configuradas)
function checkEnvironmentVariables() {
  log('\n🔐 Verificando variables de entorno...', 'cyan');
  
  const requiredVars = [
    'TRACKHS_API_URL',
    'TRACKHS_USERNAME',
    'TRACKHS_PASSWORD'
  ];
  
  const presentVars = [];
  const missingVars = [];
  
  requiredVars.forEach(varName => {
    if (process.env[varName]) {
      presentVars.push(varName);
      logSuccess(`${varName} configurada`);
    } else {
      missingVars.push(varName);
      logWarning(`${varName} no configurada`);
    }
  });
  
  if (missingVars.length > 0) {
    logWarning('\n📋 Para configurar en Vercel:');
    log('1. Ve a https://vercel.com/dashboard');
    log('2. Selecciona tu proyecto');
    log('3. Ve a Settings → Environment Variables');
    log('4. Agrega las variables faltantes');
    log('5. Re-despliega el proyecto');
  }
  
  return presentVars.length > 0;
}

// Generar reporte final
function generateFinalReport(results) {
  log('\n📊 Reporte Final de Verificación', 'magenta');
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
    log('\n🎉 ¡Todas las verificaciones pasaron!', 'green');
    log('Tu conector MCP está listo para desplegarse.', 'green');
    
    log('\n🚀 Próximos pasos:', 'blue');
    log('1. Configurar variables de entorno en Vercel');
    log('2. Hacer commit y push de los cambios');
    log('3. Verificar el despliegue en Vercel');
    log('4. Probar el conector con: npm run test:connector');
  } else {
    log('\n🔧 Acciones requeridas:', 'yellow');
    if (!results.files) {
      log('- Verificar que todos los archivos estén presentes');
    }
    if (!results.api) {
      log('- Revisar implementación en api/index.js');
    }
    if (!results.vercel) {
      log('- Verificar configuración en vercel.json');
    }
    if (!results.package) {
      log('- Revisar configuración en package.json');
    }
  }
  
  log('\n📚 Documentación:', 'blue');
  log('- Guía rápida: QUICK_START_VERCEL.md');
  log('- Despliegue: docs/VERCEL_DEPLOYMENT.md');
  log('- Troubleshooting: README.md');
}

// Función principal
async function main() {
  log('🔍 Verificación Final - Track HS MCP Connector', 'bright');
  log('='.repeat(60), 'bright');
  
  const results = {
    files: checkCriticalFiles(),
    api: checkApiContent(),
    vercel: checkVercelConfig(),
    package: checkPackageJson(),
    environment: checkEnvironmentVariables()
  };
  
  generateFinalReport(results);
  
  // Exit code basado en resultados
  const criticalChecks = ['files', 'api', 'vercel', 'package'];
  const criticalPassed = criticalChecks.every(check => results[check]);
  
  if (criticalPassed) {
    log('\n🎯 Estado: LISTO PARA DESPLIEGUE', 'green');
    process.exit(0);
  } else {
    log('\n⚠️  Estado: REQUIERE CORRECCIONES', 'yellow');
    process.exit(1);
  }
}

// Ejecutar
main().catch((error) => {
  logError(`Error en verificación: ${error.message}`);
  process.exit(1);
});
