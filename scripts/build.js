#!/usr/bin/env node

/**
 * Script de build personalizado para Vercel
 * Soluciona problemas de compilación de TypeScript en Vercel
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('🔨 Iniciando build personalizado...');

try {
  // Verificar que tsconfig.json existe
  if (!fs.existsSync('tsconfig.json')) {
    console.error('❌ tsconfig.json no encontrado');
    process.exit(1);
  }

  console.log('✅ tsconfig.json encontrado');

  // Ejecutar TypeScript compiler con parámetros explícitos
  console.log('📦 Compilando TypeScript...');
  
  const tscCommand = 'npx tsc --noEmit false --declaration --declarationMap --sourceMap --outDir ./dist --rootDir ./src';
  
  try {
    execSync(tscCommand, { stdio: 'inherit' });
    console.log('✅ Compilación exitosa');
  } catch (error) {
    console.error('❌ Error en compilación:', error.message);
    process.exit(1);
  }

  // Verificar que se generaron los archivos
  if (fs.existsSync('dist')) {
    const files = fs.readdirSync('dist');
    console.log(`✅ Se generaron ${files.length} archivos en dist/`);
  } else {
    console.error('❌ No se generó el directorio dist/');
    process.exit(1);
  }

  console.log('🎉 Build completado exitosamente');

} catch (error) {
  console.error('❌ Error en build:', error.message);
  process.exit(1);
}
