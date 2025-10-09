#!/usr/bin/env node

/**
 * Script para verificar las variables de entorno en Vercel
 * y diagnosticar problemas de configuración
 */

import { execSync } from 'child_process';

console.log('🔍 Verificando configuración de Vercel...\n');

try {
  // Verificar si estamos en Vercel
  const isVercel = process.env.VERCEL === '1';
  console.log(`Entorno Vercel: ${isVercel ? '✅ Sí' : '❌ No'}`);
  
  // Verificar variables de entorno críticas
  const requiredVars = [
    'TRACKHS_API_URL',
    'TRACKHS_USERNAME', 
    'TRACKHS_PASSWORD'
  ];
  
  console.log('\n📋 Estado de las variables de entorno:');
  let allConfigured = true;
  
  requiredVars.forEach(varName => {
    const value = process.env[varName];
    const isConfigured = !!value;
    const status = isConfigured ? '✅' : '❌';
    const displayValue = isConfigured ? 
      (varName.includes('PASSWORD') ? '***configurado***' : value) : 
      'NO CONFIGURADO';
    
    console.log(`${status} ${varName}: ${displayValue}`);
    
    if (!isConfigured) {
      allConfigured = false;
    }
  });
  
  console.log(`\n🎯 Estado general: ${allConfigured ? '✅ Todas configuradas' : '❌ Faltan variables'}`);
  
  if (!allConfigured) {
    console.log('\n🚨 PROBLEMA IDENTIFICADO:');
    console.log('Las variables de entorno de Track HS no están configuradas en Vercel.');
    console.log('\n📝 Solución:');
    console.log('1. Ve a https://vercel.com/dashboard');
    console.log('2. Selecciona tu proyecto "trackhs-mcp-connector"');
    console.log('3. Ve a Settings > Environment Variables');
    console.log('4. Agrega las siguientes variables:');
    console.log('   - TRACKHS_API_URL: https://api.trackhs.com/api');
    console.log('   - TRACKHS_USERNAME: tu_usuario_real');
    console.log('   - TRACKHS_PASSWORD: tu_contraseña_real');
    console.log('5. Redespliega la aplicación');
  } else {
    console.log('\n✅ Configuración correcta. El problema puede estar en:');
    console.log('- Credenciales incorrectas');
    console.log('- API de Track HS no disponible');
    console.log('- Problemas de red');
  }
  
  // Información adicional del entorno
  console.log('\n🔧 Información del entorno:');
  console.log(`Node.js: ${process.version}`);
  console.log(`Plataforma: ${process.platform}`);
  console.log(`Directorio: ${process.cwd()}`);
  
  if (process.env.VERCEL_URL) {
    console.log(`URL de Vercel: ${process.env.VERCEL_URL}`);
  }
  
} catch (error) {
  console.error('❌ Error verificando configuración:', error.message);
  process.exit(1);
}
