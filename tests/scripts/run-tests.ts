#!/usr/bin/env tsx

/**
 * Script para ejecutar tests con configuración personalizada
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

// Configuración de colores para output
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

function log(message: string, color: keyof typeof colors = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkPrerequisites() {
  log('🔍 Verificando prerrequisitos...', 'blue');
  
  // Verificar que Jest esté instalado
  try {
    execSync('npx jest --version', { stdio: 'pipe' });
    log('✅ Jest está instalado', 'green');
  } catch (error) {
    log('❌ Jest no está instalado. Ejecutando npm install...', 'red');
    execSync('npm install', { stdio: 'inherit' });
  }

  // Verificar que las variables de entorno estén configuradas
  const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
  const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);
  
  if (missingVars.length > 0) {
    log(`⚠️  Variables de entorno faltantes: ${missingVars.join(', ')}`, 'yellow');
    log('   Usando valores por defecto para testing...', 'yellow');
  } else {
    log('✅ Variables de entorno configuradas', 'green');
  }
}

function runTests(testType: string = 'all') {
  log(`\n🚀 Ejecutando tests: ${testType}`, 'cyan');
  
  let command = 'npx jest';
  
  switch (testType) {
    case 'unit':
      command += ' tests/tools/';
      break;
    case 'integration':
      command += ' tests/integration/';
      break;
    case 'coverage':
      command += ' --coverage';
      break;
    case 'watch':
      command += ' --watch';
      break;
    case 'ci':
      command += ' --ci --coverage --watchAll=false';
      break;
    default:
      // Ejecutar todos los tests
      break;
  }
  
  try {
    execSync(command, { stdio: 'inherit' });
    log('✅ Tests completados exitosamente', 'green');
  } catch (error) {
    log('❌ Algunos tests fallaron', 'red');
    process.exit(1);
  }
}

function generateReport() {
  log('\n📊 Generando reporte de cobertura...', 'blue');
  
  try {
    execSync('npx jest --coverage --coverageReporters=text-lcov | npx coveralls', { stdio: 'inherit' });
    log('✅ Reporte de cobertura generado', 'green');
  } catch (error) {
    log('⚠️  No se pudo generar el reporte de cobertura', 'yellow');
  }
}

function main() {
  const args = process.argv.slice(2);
  const testType = args[0] || 'all';
  
  log('🧪 Track HS MCP Server - Test Runner', 'bright');
  log('=====================================', 'bright');
  
  checkPrerequisites();
  runTests(testType);
  
  if (testType === 'coverage' || testType === 'ci') {
    generateReport();
  }
  
  log('\n🎉 Proceso completado', 'green');
}

// Ejecutar si es llamado directamente
if (require.main === module) {
  main();
}

export { runTests, checkPrerequisites, generateReport };
