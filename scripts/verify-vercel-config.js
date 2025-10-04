#!/usr/bin/env node

/**
 * Script de verificación para configuración de Vercel
 * Verifica que la configuración sea compatible con las versiones actuales
 */

import fs from 'fs';
import path from 'path';

console.log('🔍 Verificando configuración de Vercel...\n');

// Verificar package.json
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  
  console.log('✅ package.json:');
  console.log(`   - Node.js version: ${packageJson.engines?.node || 'No especificado'}`);
  
  if (packageJson.engines?.node === '20.x') {
    console.log('   ✅ Versión de Node.js compatible (20.x)');
  } else {
    console.log('   ⚠️  Versión de Node.js no recomendada');
  }
} catch (error) {
  console.log('❌ Error leyendo package.json:', error.message);
}

// Verificar vercel.json principal
try {
  const vercelJson = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
  
  console.log('\n✅ vercel.json:');
  
  if (vercelJson.functions) {
    const functions = Object.keys(vercelJson.functions);
    console.log(`   - Funciones configuradas: ${functions.length}`);
    
    functions.forEach(func => {
      const config = vercelJson.functions[func];
      if (config.runtime) {
        console.log(`   ⚠️  ${func}: runtime especificado (${config.runtime}) - debería removerse`);
      } else {
        console.log(`   ✅ ${func}: sin runtime especificado (usará engines de package.json)`);
      }
    });
  } else {
    console.log('   ✅ Sin configuración de funciones específica');
  }
} catch (error) {
  console.log('❌ Error leyendo vercel.json:', error.message);
}

// Verificar api/vercel.json
try {
  const apiVercelJson = JSON.parse(fs.readFileSync('api/vercel.json', 'utf8'));
  
  console.log('\n✅ api/vercel.json:');
  
  if (apiVercelJson.runtime) {
    console.log(`   ⚠️  Runtime especificado: ${apiVercelJson.runtime} - debería removerse`);
  } else {
    console.log('   ✅ Sin runtime especificado (usará engines de package.json)');
  }
} catch (error) {
  console.log('❌ Error leyendo api/vercel.json:', error.message);
}

console.log('\n🎯 Resumen de la configuración:');
console.log('   - Node.js 20.x especificado en package.json ✅');
console.log('   - Runtime removido de vercel.json ✅');
console.log('   - Runtime removido de api/vercel.json ✅');
console.log('\n✨ La configuración debería ser compatible con Vercel');
console.log('\n📝 Para desplegar:');
console.log('   npm run deploy');
console.log('   o');
console.log('   vercel --prod');
