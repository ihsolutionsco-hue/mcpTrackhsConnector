#!/usr/bin/env node

/**
 * Script de configuración para Track HS MCP Remote Server
 */

import { execSync } from 'child_process';
import { existsSync, writeFileSync } from 'fs';
import { join } from 'path';

console.log('🚀 Configurando Track HS MCP Remote Server...\n');

// Verificar Node.js
try {
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  
  if (majorVersion < 18) {
    console.error('❌ Se requiere Node.js 18 o superior. Versión actual:', nodeVersion);
    process.exit(1);
  }
  
  console.log('✅ Node.js version:', nodeVersion);
} catch (error) {
  console.error('❌ Error al verificar Node.js:', error.message);
  process.exit(1);
}

// Instalar dependencias
console.log('\n📦 Instalando dependencias...');
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log('✅ Dependencias instaladas correctamente');
} catch (error) {
  console.error('❌ Error al instalar dependencias:', error.message);
  process.exit(1);
}

// Compilar TypeScript
console.log('\n🔨 Compilando TypeScript...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('✅ Compilación exitosa');
} catch (error) {
  console.error('❌ Error en compilación:', error.message);
  process.exit(1);
}

// Crear archivo de configuración si no existe
const configPath = join(process.cwd(), '.env');
if (!existsSync(configPath)) {
  console.log('\n📝 Creando archivo de configuración...');
  const envContent = `# Configuración de Track HS API
TRACKHS_API_URL=https://api-integration-example.tracksandbox.io/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
`;
  writeFileSync(configPath, envContent);
  console.log('✅ Archivo .env creado. Por favor, configura tus credenciales.');
} else {
  console.log('✅ Archivo .env ya existe');
}

console.log('\n🎉 ¡Configuración completada!');
console.log('\n📋 Próximos pasos:');
console.log('1. Edita el archivo .env con tus credenciales de Track HS');
console.log('2. Configura las variables secretas en Cloudflare:');
console.log('   wrangler secret put TRACKHS_API_URL');
console.log('   wrangler secret put TRACKHS_USERNAME');
console.log('   wrangler secret put TRACKHS_PASSWORD');
console.log('3. Despliega: npm run deploy');
console.log('4. Configura Claude Desktop con la URL del conector');