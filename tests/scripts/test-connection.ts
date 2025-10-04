/**
 * Script simple para probar la conectividad básica con Track HS
 */

import 'dotenv/config';
import { TrackHSApiClient } from '../../src/core/api-client.js';

async function testConnection() {
  console.log('🔍 Probando conectividad con Track HS...\n');

  // Verificar variables de entorno
  const API_URL = process.env.TRACKHS_API_URL;
  const USERNAME = process.env.TRACKHS_USERNAME;
  const PASSWORD = process.env.TRACKHS_PASSWORD;

  console.log('📋 Configuración:');
  console.log(`   API URL: ${API_URL || '❌ No configurada'}`);
  console.log(`   Usuario: ${USERNAME || '❌ No configurado'}`);
  console.log(`   Contraseña: ${PASSWORD ? '✅ Configurada' : '❌ No configurada'}`);
  console.log('');

  if (!API_URL || !USERNAME || !PASSWORD) {
    console.error('❌ Error: Variables de entorno faltantes');
    console.error('Asegúrate de tener configurado en tu archivo .env:');
    console.error('TRACKHS_API_URL=https://tu-api-url.com/api');
    console.error('TRACKHS_USERNAME=tu_usuario');
    console.error('TRACKHS_PASSWORD=tu_contraseña');
    return;
  }

  try {
    // Crear cliente API
    const apiClient = new TrackHSApiClient(API_URL, USERNAME, PASSWORD);
    
    console.log('🔐 Intentando autenticación...');
    const startTime = Date.now();
    
    await apiClient.authenticate();
    
    const duration = Date.now() - startTime;
    console.log(`✅ Autenticación exitosa (${duration}ms)`);
    
    // Probar una llamada simple
    console.log('🌐 Probando llamada a la API...');
    const response = await apiClient.get('/pms/units?page=1&size=1');
    
    console.log('✅ Llamada a la API exitosa');
    console.log(`📊 Respuesta recibida: ${JSON.stringify(response, null, 2).substring(0, 300)}...`);
    
    console.log('\n🎉 ¡Todo funciona correctamente!');
    console.log('   ✅ Variables de entorno configuradas');
    console.log('   ✅ Autenticación exitosa');
    console.log('   ✅ API respondiendo correctamente');
    
  } catch (error) {
    console.error('❌ Error durante la prueba:');
    console.error(`   Tipo: ${error.constructor.name}`);
    console.error(`   Mensaje: ${error.message}`);
    
    if (error.response) {
      console.error(`   Status: ${error.response.status}`);
      console.error(`   Status Text: ${error.response.statusText}`);
    }
    
    console.error('\n🔧 Posibles soluciones:');
    console.error('   1. Verifica que las credenciales sean correctas');
    console.error('   2. Verifica que la URL de la API sea correcta');
    console.error('   3. Verifica que tengas acceso a la red');
    console.error('   4. Verifica que el servidor de Track HS esté funcionando');
  }
}

testConnection();
