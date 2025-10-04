/**
 * Script para encontrar el endpoint correcto de Ledger Accounts
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function findLedgerEndpoint() {
  console.log('🔍 Buscando endpoint correcto para Ledger Accounts...\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Lista exhaustiva de posibles endpoints para Ledger Accounts
  const possibleEndpoints = [
    // Variaciones con accounting
    '/accounting/ledger-accounts',
    '/accounting/accounts',
    '/accounting/ledger',
    '/accounting/chart-of-accounts',
    '/accounting/coa',
    
    // Variaciones con financial
    '/financial/ledger-accounts',
    '/financial/accounts',
    '/financial/ledger',
    '/financial/chart-of-accounts',
    
    // Variaciones con bookkeeping
    '/bookkeeping/accounts',
    '/bookkeeping/ledger',
    '/bookkeeping/chart-of-accounts',
    
    // Variaciones con crm
    '/crm/ledger-accounts',
    '/crm/accounts',
    '/crm/financial-accounts',
    
    // Variaciones con pms
    '/pms/ledger-accounts',
    '/pms/accounts',
    '/pms/financial-accounts',
    
    // Variaciones directas
    '/ledger-accounts',
    '/accounts',
    '/ledger',
    '/chart-of-accounts',
    '/coa',
    
    // Variaciones con api
    '/api/ledger-accounts',
    '/api/accounts',
    '/api/ledger',
    
    // Variaciones con management
    '/management/ledger-accounts',
    '/management/accounts',
    '/management/financial-accounts',
    
    // Variaciones con admin
    '/admin/ledger-accounts',
    '/admin/accounts',
    '/admin/financial-accounts'
  ];

  console.log(`🧪 Probando ${possibleEndpoints.length} posibles endpoints...\n`);

  const workingEndpoints = [];

  for (const endpoint of possibleEndpoints) {
    try {
      console.log(`🔍 Probando: ${endpoint}`);
      const response = await apiClient.get(`${endpoint}?page=1&size=1`);
      console.log(`   ✅ FUNCIONA! ${endpoint}`);
      console.log(`   📊 Respuesta: ${JSON.stringify(response, null, 2).substring(0, 200)}...`);
      workingEndpoints.push({ endpoint, response });
    } catch (error) {
      console.log(`   ❌ ${endpoint}: ${error.message}`);
    }
  }

  console.log('\n📊 RESUMEN DE RESULTADOS');
  console.log('========================');
  
  if (workingEndpoints.length > 0) {
    console.log(`✅ Endpoints que funcionan: ${workingEndpoints.length}`);
    workingEndpoints.forEach((item, index) => {
      console.log(`   ${index + 1}. ${item.endpoint}`);
    });
  } else {
    console.log('❌ No se encontraron endpoints de Ledger Accounts que funcionen');
    console.log('\n💡 Posibles razones:');
    console.log('   1. El endpoint no está disponible en esta instancia de Track HS');
    console.log('   2. Se requieren permisos especiales para acceder a cuentas contables');
    console.log('   3. El endpoint tiene un nombre completamente diferente');
    console.log('   4. La funcionalidad de contabilidad no está habilitada');
  }

  // Probar algunos endpoints de información que podrían dar pistas
  console.log('\n🔍 Probando endpoints de información...\n');
  
  const infoEndpoints = [
    '/api/v1',
    '/api/v2',
    '/api/version',
    '/api/endpoints',
    '/api/documentation',
    '/api/swagger.json',
    '/api/openapi.json'
  ];

  for (const infoUrl of infoEndpoints) {
    try {
      console.log(`🔍 Probando: ${infoUrl}`);
      const response = await apiClient.get(infoUrl);
      console.log(`   ✅ Funciona: ${JSON.stringify(response, null, 2).substring(0, 200)}...`);
    } catch (error) {
      console.log(`   ❌ ${infoUrl}: ${error.message}`);
    }
  }

  console.log('\n🎯 Conclusión:');
  if (workingEndpoints.length > 0) {
    console.log('   ✅ Se encontraron endpoints alternativos para Ledger Accounts');
    console.log('   📝 Se debe actualizar el código para usar la URL correcta');
  } else {
    console.log('   ⚠️  No se encontraron endpoints de Ledger Accounts');
    console.log('   💡 Es posible que esta funcionalidad no esté disponible en esta instancia');
  }
}

findLedgerEndpoint().catch(error => {
  console.error('💥 Error:', error.message);
});
