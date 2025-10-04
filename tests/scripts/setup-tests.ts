#!/usr/bin/env tsx

/**
 * Script de configuración para el sistema de testing
 */

import { execSync } from 'child_process';
import { existsSync, writeFileSync, mkdirSync } from 'fs';
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

function checkNodeVersion() {
  log('🔍 Verificando versión de Node.js...', 'blue');
  
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  
  if (majorVersion < 18) {
    log('❌ Se requiere Node.js 18 o superior', 'red');
    log(`   Versión actual: ${nodeVersion}`, 'red');
    process.exit(1);
  }
  
  log(`✅ Node.js ${nodeVersion} detectado`, 'green');
}

function installDependencies() {
  log('\n📦 Instalando dependencias de testing...', 'blue');
  
  try {
    execSync('npm install --save-dev jest @types/jest ts-jest supertest @types/supertest nock', { 
      stdio: 'inherit' 
    });
    log('✅ Dependencias instaladas correctamente', 'green');
  } catch (error) {
    log('❌ Error al instalar dependencias', 'red');
    process.exit(1);
  }
}

function createTestDirectories() {
  log('\n📁 Creando directorios de testing...', 'blue');
  
  const directories = [
    'tests/coverage',
    'tests/reports',
    'tests/logs'
  ];
  
  directories.forEach(dir => {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
      log(`✅ Directorio creado: ${dir}`, 'green');
    } else {
      log(`ℹ️  Directorio ya existe: ${dir}`, 'yellow');
    }
  });
}

function createGitignore() {
  log('\n📝 Configurando .gitignore para testing...', 'blue');
  
  const gitignoreContent = `
# Testing
coverage/
test-results/
*.lcov
.nyc_output/

# Logs
logs/
*.log

# Environment
.env.test
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
`;
  
  const gitignorePath = 'tests/.gitignore';
  if (!existsSync(gitignorePath)) {
    writeFileSync(gitignorePath, gitignoreContent.trim());
    log('✅ .gitignore creado', 'green');
  } else {
    log('ℹ️  .gitignore ya existe', 'yellow');
  }
}

function createTestScripts() {
  log('\n📝 Creando scripts de testing...', 'blue');
  
  const packageJsonPath = 'package.json';
  if (existsSync(packageJsonPath)) {
    log('ℹ️  Los scripts de testing ya están configurados en package.json', 'yellow');
  } else {
    log('⚠️  package.json no encontrado', 'yellow');
  }
}

function verifyJestConfig() {
  log('\n🔧 Verificando configuración de Jest...', 'blue');
  
  const jestConfigPath = 'jest.config.js';
  if (existsSync(jestConfigPath)) {
    log('✅ jest.config.js encontrado', 'green');
  } else {
    log('❌ jest.config.js no encontrado', 'red');
    log('   Ejecuta el setup principal del proyecto primero', 'red');
  }
}

function createTestEnvironment() {
  log('\n🌍 Configurando entorno de testing...', 'blue');
  
  const envContent = `
# Configuración de entorno para testing
NODE_ENV=test

# API de Track HS para testing
TRACKHS_API_URL=https://api.trackhs.test
TRACKHS_USERNAME=test_user
TRACKHS_PASSWORD=test_password

# Configuración de Jest
JEST_TIMEOUT=10000
JEST_VERBOSE=true

# Configuración de mocks
MOCK_DELAY=100
MOCK_TIMEOUT=5000

# Configuración de cobertura
COVERAGE_THRESHOLD=80
COVERAGE_REPORTERS=text,lcov,html
`;
  
  const envPath = 'tests/env.test';
  if (!existsSync(envPath)) {
    writeFileSync(envPath, envContent.trim());
    log('✅ Archivo de entorno creado', 'green');
  } else {
    log('ℹ️  Archivo de entorno ya existe', 'yellow');
  }
}

function runInitialTest() {
  log('\n🧪 Ejecutando test inicial...', 'blue');
  
  try {
    execSync('npx jest --version', { stdio: 'pipe' });
    log('✅ Jest está funcionando correctamente', 'green');
  } catch (error) {
    log('❌ Error al verificar Jest', 'red');
    log('   Ejecuta: npm install', 'yellow');
  }
}

function showNextSteps() {
  log('\n🎯 Próximos pasos:', 'cyan');
  log('1. Configura las variables de entorno:', 'yellow');
  log('   export TRACKHS_API_URL="https://tu-api.com"', 'yellow');
  log('   export TRACKHS_USERNAME="tu_usuario"', 'yellow');
  log('   export TRACKHS_PASSWORD="tu_contraseña"', 'yellow');
  log('');
  log('2. Ejecuta los tests:', 'yellow');
  log('   npm test', 'yellow');
  log('   npm run test:watch', 'yellow');
  log('   npm run test:coverage', 'yellow');
  log('');
  log('3. Para tests específicos:', 'yellow');
  log('   npx jest tests/tools/get-reviews.test.ts', 'yellow');
  log('   npx jest tests/integration/', 'yellow');
}

function main() {
  log('🚀 Track HS MCP Server - Setup de Testing', 'bright');
  log('==========================================', 'bright');
  
  checkNodeVersion();
  installDependencies();
  createTestDirectories();
  createGitignore();
  createTestScripts();
  verifyJestConfig();
  createTestEnvironment();
  runInitialTest();
  showNextSteps();
  
  log('\n🎉 Setup completado exitosamente!', 'green');
}

// Ejecutar si es llamado directamente
if (require.main === module) {
  main();
}

export { 
  checkNodeVersion, 
  installDependencies, 
  createTestDirectories,
  createTestEnvironment,
  runInitialTest 
};
