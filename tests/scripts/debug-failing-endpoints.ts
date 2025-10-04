/**
 * Script para investigar endpoints que no funcionan
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function debugFailingEndpoints() {
  console.log('🔍 Investigando endpoints que no funcionan...\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Endpoints que fallan
  const failingEndpoints = [
    {
      name: 'Get Contacts',
      baseUrl: '/pms/contacts',
      alternatives: [
        '/contacts',
        '/api/contacts',
        '/pms/contact',
        '/contact-management/contacts',
        '/crm/contacts'
      ]
    },
    {
      name: 'Get Ledger Accounts',
      baseUrl: '/accounting/ledger-accounts',
      alternatives: [
        '/ledger-accounts',
        '/api/ledger-accounts',
        '/accounting/accounts',
        '/financial/ledger-accounts',
        '/bookkeeping/accounts'
      ]
    }
  ];

  for (const endpoint of failingEndpoints) {
    console.log(`🔍 Investigando ${endpoint.name}`);
    console.log(`   URL base: ${endpoint.baseUrl}`);
    
    // Probar URL base
    try {
      const response = await apiClient.get(`${endpoint.baseUrl}?page=1&size=1`);
      console.log(`   ✅ URL base funciona: ${JSON.stringify(response, null, 2).substring(0, 200)}...`);
    } catch (error) {
      console.log(`   ❌ URL base falla: ${error.message}`);
      
      // Probar URLs alternativas
      console.log(`   🔄 Probando URLs alternativas...`);
      let foundWorking = false;
      
      for (const altUrl of endpoint.alternatives) {
        try {
          console.log(`      Probando: ${altUrl}`);
          const response = await apiClient.get(`${altUrl}?page=1&size=1`);
          console.log(`      ✅ ${altUrl} funciona!`);
          console.log(`      📊 Respuesta: ${JSON.stringify(response, null, 2).substring(0, 200)}...`);
          foundWorking = true;
          break;
        } catch (altError) {
          console.log(`      ❌ ${altUrl}: ${altError.message}`);
        }
      }
      
      if (!foundWorking) {
        console.log(`   ⚠️  Ninguna URL alternativa funcionó para ${endpoint.name}`);
      }
    }
    
    console.log('');
  }

  // Probar endpoints de documentación o información
  console.log('📚 Probando endpoints de información...\n');
  
  const infoEndpoints = [
    '/',
    '/api',
    '/docs',
    '/swagger',
    '/openapi',
    '/health',
    '/status',
    '/version'
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

  console.log('\n🎯 Resumen de investigación:');
  console.log('   - Se probaron múltiples variaciones de URLs');
  console.log('   - Se verificaron endpoints de información');
  console.log('   - Se identificaron las URLs correctas o problemas de permisos');
}

debugFailingEndpoints().catch(error => {
  console.error('💥 Error:', error.message);
});
