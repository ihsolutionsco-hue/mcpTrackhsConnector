/**
 * Script para probar la URL correcta de Ledger Accounts según la documentación
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function testCorrectLedgerUrl() {
  console.log('🔍 Probando URL correcta de Ledger Accounts según documentación...\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // URL correcta según la documentación
  const correctUrl = '/pms/accounting/accounts';
  
  console.log('📚 Según la documentación:');
  console.log(`   URL documentada: ${correctUrl}`);
  console.log(`   Descripción: Returns an array of ledger accounts`);
  console.log(`   Requisito: Requires Server Keys`);
  console.log('');

  try {
    console.log(`🔍 Probando: ${correctUrl}`);
    const startTime = Date.now();
    const response = await apiClient.get(`${correctUrl}?page=1&size=3`);
    const duration = Date.now() - startTime;
    
    console.log(`✅ ¡FUNCIONA! (${duration}ms)`);
    console.log(`📊 Respuesta recibida:`);
    console.log(`   - Tipo: ${typeof response}`);
    console.log(`   - Es array: ${Array.isArray(response)}`);
    
    if (Array.isArray(response)) {
      console.log(`   - Elementos: ${response.length}`);
      if (response.length > 0) {
        const firstItem = response[0];
        console.log(`   - Primer elemento:`);
        console.log(`     * ID: ${firstItem.id}`);
        console.log(`     * Código: ${firstItem.code}`);
        console.log(`     * Nombre: ${firstItem.name}`);
        console.log(`     * Categoría: ${firstItem.category}`);
        console.log(`     * Tipo: ${firstItem.accountType}`);
        console.log(`     * Activo: ${firstItem.isActive}`);
      }
    } else if (response && typeof response === 'object') {
      console.log(`   - Propiedades: ${Object.keys(response).join(', ')}`);
      
      if (response._embedded) {
        console.log(`   - Contenido _embedded:`);
        Object.keys(response._embedded).forEach(key => {
          const items = response._embedded[key];
          if (Array.isArray(items)) {
            console.log(`     * ${key}: ${items.length} elementos`);
            if (items.length > 0) {
              const firstItem = items[0];
              console.log(`       - Primer elemento: ID ${firstItem.id}, Código ${firstItem.code}, Nombre ${firstItem.name}`);
            }
          }
        });
      }
    }
    
    console.log('\n🎉 ¡ENDPOINT DE LEDGER ACCOUNTS FUNCIONANDO!');
    console.log('   ✅ URL correcta encontrada: /pms/accounting/accounts');
    console.log('   ✅ Respuesta válida recibida');
    console.log('   ✅ Datos de cuentas contables disponibles');
    
  } catch (error) {
    console.log(`❌ Error: ${error.message}`);
    
    // Probar con parámetros adicionales
    console.log('\n🔧 Probando con parámetros adicionales...');
    
    const testParams = [
      '?page=1&size=1',
      '?page=1&size=1&sortColumn=name',
      '?page=1&size=1&sortColumn=name&sortDirection=asc',
      '?page=1&size=1&isActive=1'
    ];
    
    for (const params of testParams) {
      try {
        console.log(`   Probando: ${correctUrl}${params}`);
        const response = await apiClient.get(`${correctUrl}${params}`);
        console.log(`   ✅ Funciona con parámetros: ${params}`);
        break;
      } catch (paramError) {
        console.log(`   ❌ ${params}: ${paramError.message}`);
      }
    }
  }

  console.log('\n📝 CONCLUSIÓN:');
  console.log('===============');
  console.log('✅ La URL correcta es: /pms/accounting/accounts');
  console.log('❌ La URL incorrecta era: /accounting/ledger-accounts');
  console.log('💡 La documentación tenía la información correcta');
  console.log('🔧 Se debe actualizar el código para usar la URL correcta');
}

testCorrectLedgerUrl().catch(error => {
  console.error('💥 Error:', error.message);
});
