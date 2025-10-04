/**
 * Script para diagnosticar el archivo .env
 */

import fs from 'fs';
import path from 'path';

console.log('🔍 Diagnosticando archivo .env...\n');

const envPath = path.join(process.cwd(), '.env');

if (!fs.existsSync(envPath)) {
  console.log('❌ Archivo .env no encontrado');
  process.exit(1);
}

console.log('📁 Información del archivo:');
console.log(`   Ruta: ${envPath}`);
console.log(`   Existe: ✅ Sí`);

try {
  const content = fs.readFileSync(envPath, 'utf8');
  console.log(`   Tamaño: ${content.length} caracteres`);
  console.log(`   Líneas: ${content.split('\n').length}`);
  
  console.log('\n📄 Contenido del archivo:');
  console.log('--- INICIO ---');
  console.log(content);
  console.log('--- FIN ---');
  
  console.log('\n🔍 Análisis línea por línea:');
  const lines = content.split('\n');
  lines.forEach((line, index) => {
    const lineNum = index + 1;
    const trimmed = line.trim();
    
    if (trimmed === '') {
      console.log(`   Línea ${lineNum}: (vacía)`);
    } else if (trimmed.startsWith('#')) {
      console.log(`   Línea ${lineNum}: (comentario) ${trimmed}`);
    } else if (trimmed.includes('=')) {
      const [key, ...valueParts] = trimmed.split('=');
      const value = valueParts.join('=');
      console.log(`   Línea ${lineNum}: ${key.trim()} = "${value}"`);
    } else {
      console.log(`   Línea ${lineNum}: (sin formato) "${trimmed}"`);
    }
  });
  
  console.log('\n🧪 Probando parseo manual:');
  const envVars: Record<string, string> = {};
  
  lines.forEach((line, index) => {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#')) {
      if (trimmed.includes('=')) {
        const [key, ...valueParts] = trimmed.split('=');
        if (key && valueParts.length > 0) {
          const cleanKey = key.trim();
          const cleanValue = valueParts.join('=').trim();
          envVars[cleanKey] = cleanValue;
          console.log(`   ✅ ${cleanKey} = "${cleanValue}"`);
        }
      } else {
        console.log(`   ❌ Línea ${index + 1} sin formato válido: "${trimmed}"`);
      }
    }
  });
  
  console.log('\n📊 Variables encontradas:');
  Object.keys(envVars).forEach(key => {
    console.log(`   ${key}: "${envVars[key]}"`);
  });
  
} catch (error) {
  console.error('❌ Error leyendo archivo:', error.message);
}
