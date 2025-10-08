#!/usr/bin/env node

/**
 * Script de build para Track HS MCP Connector
 */

import { execSync } from 'child_process';
import { existsSync, rmSync } from 'fs';
import { join } from 'path';

const projectRoot = process.cwd();
const distDir = join(projectRoot, 'dist');

console.log('🚀 Iniciando build de Track HS MCP Connector...\n');

try {
  // Limpiar directorio dist
  if (existsSync(distDir)) {
    console.log('🧹 Limpiando directorio dist...');
    rmSync(distDir, { recursive: true, force: true });
  }

  // Compilar TypeScript
  console.log('📦 Compilando TypeScript...');
  execSync('npx tsc --outDir dist --rootDir src --target ES2022 --module ESNext --moduleResolution bundler --allowSyntheticDefaultImports --esModuleInterop --allowJs --strict --skipLibCheck --forceConsistentCasingInFileNames --declaration --declarationMap --sourceMap --resolveJsonModule --isolatedModules', { stdio: 'inherit' });

  // Verificar que se generaron los archivos
  const mainFile = join(distDir, 'index.js');
  if (!existsSync(mainFile)) {
    throw new Error('Error: No se generó el archivo principal dist/index.js');
  }

  console.log('✅ Build completado exitosamente!');
  console.log(`📁 Archivos generados en: ${distDir}`);
  console.log('🎯 Archivo principal: dist/index.js');

} catch (error) {
  console.error('❌ Error durante el build:', error.message);
  process.exit(1);
}