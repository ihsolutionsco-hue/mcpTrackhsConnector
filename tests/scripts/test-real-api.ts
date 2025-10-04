/**
 * Script para probar llamadas reales a la API de Track HS
 * Usa las credenciales del archivo .env
 */

import 'dotenv/config';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { 
  GetReviewsTool, 
  GetReservationTool, 
  SearchReservationsTool,
  GetUnitsTool,
  GetUnitTool,
  GetContactsTool,
  GetLedgerAccountsTool,
  GetNodesTool
} from '../../src/tools/index.js';

// Configuración de la API
const API_URL = process.env.TRACKHS_API_URL;
const USERNAME = process.env.TRACKHS_USERNAME;
const PASSWORD = process.env.TRACKHS_PASSWORD;

if (!API_URL || !USERNAME || !PASSWORD) {
  console.error('❌ Error: Variables de entorno faltantes');
  console.error('Asegúrate de tener configurado:');
  console.error('- TRACKHS_API_URL');
  console.error('- TRACKHS_USERNAME');
  console.error('- TRACKHS_PASSWORD');
  process.exit(1);
}

console.log('🚀 Iniciando pruebas con API real de Track HS');
console.log(`📍 API URL: ${API_URL}`);
console.log(`👤 Usuario: ${USERNAME}`);
console.log('');

// Crear cliente API
const apiClient = new TrackHSApiClient(API_URL, USERNAME, PASSWORD);

// Crear herramientas
const tools = {
  reviews: new GetReviewsTool(apiClient),
  reservation: new GetReservationTool(apiClient),
  searchReservations: new SearchReservationsTool(apiClient),
  units: new GetUnitsTool(apiClient),
  unit: new GetUnitTool(apiClient),
  contacts: new GetContactsTool(apiClient),
  ledgerAccounts: new GetLedgerAccountsTool(apiClient),
  nodes: new GetNodesTool(apiClient)
};

// Función para probar un endpoint
async function testEndpoint(name: string, tool: any, params: any = {}) {
  try {
    console.log(`🔍 Probando ${name}...`);
    const startTime = Date.now();
    const result = await tool.execute(params);
    const duration = Date.now() - startTime;
    
    console.log(`✅ ${name} - Éxito (${duration}ms)`);
    console.log(`   📊 Resultado: ${JSON.stringify(result, null, 2).substring(0, 200)}...`);
    return { success: true, duration, result };
  } catch (error) {
    console.log(`❌ ${name} - Error: ${error.message}`);
    return { success: false, error: error.message };
  }
}

// Función principal de pruebas
async function runRealApiTests() {
  console.log('🧪 Ejecutando pruebas con API real...\n');

  const results = [];

  // 1. Probar autenticación básica
  console.log('🔐 Probando autenticación...');
  try {
    await apiClient.authenticate();
    console.log('✅ Autenticación exitosa\n');
  } catch (error) {
    console.log(`❌ Error de autenticación: ${error.message}\n`);
    return;
  }

  // 2. Probar endpoints básicos
  results.push(await testEndpoint('GetReviews', tools.reviews, { page: 1, size: 5 }));
  results.push(await testEndpoint('GetContacts', tools.contacts, { page: 1, size: 5 }));
  results.push(await testEndpoint('GetNodes', tools.nodes, { page: 1, size: 5 }));
  results.push(await testEndpoint('GetLedgerAccounts', tools.ledgerAccounts, { page: 1, size: 5 }));
  
  console.log('');

  // 3. Probar endpoints que requieren IDs específicos
  console.log('🔍 Probando endpoints que requieren IDs específicos...');
  
  // Intentar obtener una unidad específica (ID 1 es común)
  results.push(await testEndpoint('GetUnit (ID: 1)', tools.unit, { unitId: 1 }));
  
  // Intentar obtener una reservación específica (ID 1 es común)
  results.push(await testEndpoint('GetReservation (ID: 1)', tools.reservation, { reservationId: '1' }));
  
  console.log('');

  // 4. Probar búsquedas
  console.log('🔍 Probando búsquedas...');
  results.push(await testEndpoint('SearchReservations', tools.searchReservations, { 
    page: 1, 
    size: 5,
    search: 'test'
  }));
  
  results.push(await testEndpoint('GetUnits con filtros', tools.units, { 
    page: 1, 
    size: 5,
    search: 'suite'
  }));

  console.log('');

  // 5. Resumen de resultados
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
        console.log(`   ${i + 1}. ${r.error}`);
      });
  }

  console.log('\n🎉 Pruebas completadas!');
}

// Ejecutar pruebas
runRealApiTests().catch(error => {
  console.error('💥 Error fatal:', error);
  process.exit(1);
});
