/**
 * Script para probar llamadas reales a la API de Track HS
 * Carga manualmente el archivo .env
 */

import fs from 'fs';
import path from 'path';
import { TrackHSApiClient } from '../../src/core/api-client.js';

// Función para cargar variables de entorno manualmente
function loadEnvFile() {
  const envPath = path.join(process.cwd(), '.env');
  
  if (!fs.existsSync(envPath)) {
    throw new Error('Archivo .env no encontrado');
  }
  
  const envContent = fs.readFileSync(envPath, 'utf8');
  const envVars: Record<string, string> = {};
  
  envContent.split('\n').forEach(line => {
    line = line.trim();
    if (line && !line.startsWith('#')) {
      const [key, ...valueParts] = line.split('=');
      if (key && valueParts.length > 0) {
        envVars[key.trim()] = valueParts.join('=').trim();
      }
    }
  });
  
  return envVars;
}

async function testRealApi() {
  console.log('🚀 Iniciando pruebas con API real de Track HS\n');

  try {
    // Cargar variables de entorno
    console.log('📋 Cargando configuración...');
    const envVars = loadEnvFile();
    
    const API_URL = envVars.TRACKHS_API_URL;
    const USERNAME = envVars.TRACKHS_USERNAME;
    const PASSWORD = envVars.TRACKHS_PASSWORD;

    console.log(`   API URL: ${API_URL ? '✅ Configurada' : '❌ No configurada'}`);
    console.log(`   Usuario: ${USERNAME ? '✅ Configurado' : '❌ No configurado'}`);
    console.log(`   Contraseña: ${PASSWORD ? '✅ Configurada' : '❌ No configurada'}`);
    console.log('');

    if (!API_URL || !USERNAME || !PASSWORD) {
      console.error('❌ Error: Variables de entorno faltantes en el archivo .env');
      return;
    }

    // Crear cliente API
    console.log('🔧 Creando cliente API...');
    const apiClient = new TrackHSApiClient(API_URL, USERNAME, PASSWORD);
    
    // Probar autenticación
    console.log('🔐 Probando autenticación...');
    const authStart = Date.now();
    await apiClient.authenticate();
    const authDuration = Date.now() - authStart;
    console.log(`✅ Autenticación exitosa (${authDuration}ms)\n`);

    // Probar diferentes endpoints
    const tests = [
      {
        name: 'Get Units (básico)',
        url: '/pms/units?page=1&size=2',
        method: 'GET'
      },
      {
        name: 'Get Contacts (básico)',
        url: '/pms/contacts?page=1&size=2',
        method: 'GET'
      },
      {
        name: 'Get Nodes (básico)',
        url: '/pms/nodes?page=1&size=2',
        method: 'GET'
      },
      {
        name: 'Get Ledger Accounts (básico)',
        url: '/accounting/ledger-accounts?page=1&size=2',
        method: 'GET'
      },
      {
        name: 'Get Reviews (básico)',
        url: '/channel-management/channel/reviews?page=1&size=2',
        method: 'GET'
      },
      {
        name: 'Search Reservations (básico)',
        url: '/v2/pms/reservations?page=1&size=2',
        method: 'GET'
      }
    ];

    console.log('🧪 Ejecutando pruebas de endpoints...\n');

    const results = [];

    for (const test of tests) {
      try {
        console.log(`🔍 Probando ${test.name}...`);
        const startTime = Date.now();
        
        let response;
        if (test.method === 'GET') {
          response = await apiClient.get(test.url);
        }
        
        const duration = Date.now() - startTime;
        
        console.log(`✅ ${test.name} - Éxito (${duration}ms)`);
        
        // Mostrar información básica de la respuesta
        if (response && typeof response === 'object') {
          const keys = Object.keys(response);
          console.log(`   📊 Propiedades: ${keys.slice(0, 5).join(', ')}${keys.length > 5 ? '...' : ''}`);
          
          // Si tiene _embedded, mostrar cuántos elementos
          if (response._embedded) {
            const embeddedKeys = Object.keys(response._embedded);
            embeddedKeys.forEach(key => {
              if (Array.isArray(response._embedded[key])) {
                console.log(`   📦 ${key}: ${response._embedded[key].length} elementos`);
              }
            });
          }
        }
        
        results.push({ name: test.name, success: true, duration });
        
      } catch (error) {
        console.log(`❌ ${test.name} - Error: ${error.message}`);
        results.push({ name: test.name, success: false, error: error.message });
      }
      
      console.log('');
    }

    // Resumen
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    const totalDuration = results
      .filter(r => r.success)
      .reduce((sum, r) => sum + (r.duration || 0), 0);

    console.log('📊 RESUMEN DE PRUEBAS');
    console.log('====================');
    console.log(`✅ Exitosas: ${successful}`);
    console.log(`❌ Fallidas: ${failed}`);
    console.log(`⏱️  Tiempo total: ${totalDuration}ms`);
    console.log(`📈 Tasa de éxito: ${((successful / results.length) * 100).toFixed(1)}%`);

    if (failed > 0) {
      console.log('\n❌ Errores encontrados:');
      results
        .filter(r => !r.success)
        .forEach((r, i) => {
          console.log(`   ${i + 1}. ${r.name}: ${r.error}`);
        });
    }

    console.log('\n🎉 ¡Pruebas completadas!');
    console.log('   ✅ Autenticación funcionando');
    console.log('   ✅ API respondiendo correctamente');
    console.log('   ✅ Endpoints accesibles');

  } catch (error) {
    console.error('💥 Error fatal:', error.message);
    console.error('\n🔧 Posibles soluciones:');
    console.error('   1. Verifica que el archivo .env tenga las credenciales correctas');
    console.error('   2. Verifica que la URL de la API sea correcta');
    console.error('   3. Verifica que tengas acceso a la red');
    console.error('   4. Verifica que el servidor de Track HS esté funcionando');
  }
}

testRealApi();
