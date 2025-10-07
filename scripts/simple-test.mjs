#!/usr/bin/env node

/**
 * Script simple de prueba
 */

console.log('🚀 Script de prueba funcionando');
console.log('📁 Directorio actual:', process.cwd());
console.log('🔧 Node.js versión:', process.version);

// Verificar archivos importantes
import fs from 'fs';
import path from 'path';

const files = [
  'api/index.js',
  'vercel.json',
  'package.json'
];

console.log('\n📋 Verificando archivos:');
files.forEach(file => {
  const exists = fs.existsSync(file);
  console.log(`${exists ? '✅' : '❌'} ${file}`);
});

console.log('\n🎉 Prueba completada');
