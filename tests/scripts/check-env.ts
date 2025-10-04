/**
 * Script para verificar las variables de entorno
 */

import fs from 'fs';
import path from 'path';

console.log('🔍 Verificando configuración de entorno...\n');

// Verificar si existe el archivo .env
const envPath = path.join(process.cwd(), '.env');
const envExists = fs.existsSync(envPath);

console.log('📁 Archivos de configuración:');
console.log(`   .env existe: ${envExists ? '✅ Sí' : '❌ No'}`);
console.log(`   Ruta: ${envPath}`);

if (envExists) {
  try {
    const envContent = fs.readFileSync(envPath, 'utf8');
    const lines = envContent.split('\n').filter(line => line.trim() && !line.startsWith('#'));
    console.log(`   Líneas de configuración: ${lines.length}`);
    
    // Mostrar las variables (sin valores por seguridad)
    console.log('\n📋 Variables encontradas:');
    lines.forEach(line => {
      const [key] = line.split('=');
      console.log(`   ${key}`);
    });
  } catch (error) {
    console.log(`   Error leyendo archivo: ${error.message}`);
  }
}

console.log('\n🌍 Variables de entorno actuales:');
console.log(`   TRACKHS_API_URL: ${process.env.TRACKHS_API_URL ? '✅ Configurada' : '❌ No configurada'}`);
console.log(`   TRACKHS_USERNAME: ${process.env.TRACKHS_USERNAME ? '✅ Configurada' : '❌ No configurada'}`);
console.log(`   TRACKHS_PASSWORD: ${process.env.TRACKHS_PASSWORD ? '✅ Configurada' : '❌ No configurada'}`);

if (process.env.TRACKHS_API_URL) {
  console.log(`   URL: ${process.env.TRACKHS_API_URL}`);
}
if (process.env.TRACKHS_USERNAME) {
  console.log(`   Usuario: ${process.env.TRACKHS_USERNAME}`);
}

console.log('\n💡 Si las variables no están configuradas, asegúrate de que tu archivo .env contenga:');
console.log('TRACKHS_API_URL=https://tu-api-url.com/api');
console.log('TRACKHS_USERNAME=tu_usuario');
console.log('TRACKHS_PASSWORD=tu_contraseña');
