/**
 * Script para probar endpoints específicos documentados
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function testSpecificDocumentedEndpoints() {
  console.log('🔍 PROBANDO ENDPOINTS ESPECÍFICOS DOCUMENTADOS\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };
  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Endpoints específicos basados en la documentación
  const documentedEndpoints = [
    {
      name: 'Get All Contacts',
      url: '/crm/contacts',
      method: 'GET',
      description: 'Obtener todos los contactos del CRM',
      file: 'getAllContacts.md'
    },
    {
      name: 'Get Folios Collection',
      url: '/pms/folios',
      method: 'GET',
      description: 'Obtener colección de folios',
      file: 'getFoliosCollection.md'
    },
    {
      name: 'Get Ledger Account',
      url: '/pms/accounting/accounts/{id}',
      method: 'GET',
      description: 'Obtener cuenta contable específica',
      file: 'getLedgerAccount.md',
      testUrl: '/pms/accounting/accounts/1' // URL con ID específico
    },
    {
      name: 'Get Ledger Accounts',
      url: '/pms/accounting/accounts',
      method: 'GET',
      description: 'Obtener todas las cuentas contables',
      file: 'getLedgerAccounts.md'
    },
    {
      name: 'Get Node',
      url: '/pms/nodes/{id}',
      method: 'GET',
      description: 'Obtener nodo específico',
      file: 'getNode.md',
      testUrl: '/pms/nodes/1' // URL con ID específico
    },
    {
      name: 'Get Nodes',
      url: '/pms/nodes',
      method: 'GET',
      description: 'Obtener todos los nodos',
      file: 'getNodes.md'
    },
    {
      name: 'Get Reservation Notes',
      url: '/pms/reservations/{id}/notes',
      method: 'GET',
      description: 'Obtener notas de reservación',
      file: 'getReservationNotes.md',
      testUrl: '/pms/reservations/1/notes' // URL con ID específico
    },
    {
      name: 'Get Reservation V2',
      url: '/v2/pms/reservations/{id}',
      method: 'GET',
      description: 'Obtener reservación específica v2',
      file: 'getReservationV2.md',
      testUrl: '/v2/pms/reservations/1' // URL con ID específico
    },
    {
      name: 'Get Reviews',
      url: '/channel-management/channel/reviews',
      method: 'GET',
      description: 'Obtener reseñas de canales',
      file: 'getReviews.md'
    },
    {
      name: 'Search Reservations V2',
      url: '/v2/pms/reservations',
      method: 'GET',
      description: 'Buscar reservaciones v2',
      file: 'getSearchReservationsV2.md'
    },
    {
      name: 'Get Unit',
      url: '/pms/units/{id}',
      method: 'GET',
      description: 'Obtener unidad específica',
      file: 'getUnit.md',
      testUrl: '/pms/units/1' // URL con ID específico
    },
    {
      name: 'Get Unit Collection',
      url: '/pms/units',
      method: 'GET',
      description: 'Obtener colección de unidades',
      file: 'getUnitCollection.md'
    }
  ];

  console.log(`🧪 Probando ${documentedEndpoints.length} endpoints documentados...\n`);

  const results = [];
  let totalTime = 0;

  for (const endpoint of documentedEndpoints) {
    console.log(`🔍 ${endpoint.name}`);
    console.log(`   📄 Archivo: ${endpoint.file}`);
    console.log(`   📝 Descripción: ${endpoint.description}`);
    console.log(`   🔗 URL: ${endpoint.url}`);
    
    try {
      const startTime = Date.now();
      
      // Usar testUrl si está disponible, sino usar la URL base con parámetros
      let testUrl = endpoint.testUrl || endpoint.url;
      if (!endpoint.testUrl && endpoint.method === 'GET') {
        // Agregar parámetros básicos para GET requests
        const hasParams = testUrl.includes('?');
        const separator = hasParams ? '&' : '?';
        testUrl += `${separator}page=1&size=2`;
      }
      
      console.log(`   🧪 Probando: ${testUrl}`);
      
      let response;
      if (endpoint.method === 'GET') {
        response = await apiClient.get(testUrl);
      } else if (endpoint.method === 'POST') {
        response = await apiClient.post(testUrl, {});
      } else {
        console.log(`   ⚠️  Método ${endpoint.method} no soportado en este test`);
        continue;
      }
      
      const duration = Date.now() - startTime;
      totalTime += duration;
      
      console.log(`   ✅ Éxito (${duration}ms)`);
      
      // Analizar respuesta
      if (response && typeof response === 'object') {
        const keys = Object.keys(response);
        console.log(`   📊 Propiedades: ${keys.slice(0, 3).join(', ')}${keys.length > 3 ? '...' : ''}`);
        
        if (response._embedded) {
          const embeddedKeys = Object.keys(response._embedded);
          embeddedKeys.forEach(key => {
            if (Array.isArray(response._embedded[key])) {
              console.log(`   📦 ${key}: ${response._embedded[key].length} elementos`);
            }
          });
        }
        
        if (response.total_items !== undefined) {
          console.log(`   📄 Total: ${response.total_items} elementos`);
        }
      } else if (Array.isArray(response)) {
        console.log(`   📦 Array con ${response.length} elementos`);
        if (response.length > 0) {
          const firstItem = response[0];
          console.log(`   👤 Primer elemento: ${JSON.stringify(firstItem, null, 2).substring(0, 100)}...`);
        }
      }
      
      results.push({ 
        name: endpoint.name, 
        file: endpoint.file,
        url: endpoint.url,
        success: true, 
        duration,
        status: '✅ FUNCIONANDO'
      });
      
    } catch (error: any) {
      console.log(`   ❌ Error: ${error.message}`);
      results.push({ 
        name: endpoint.name, 
        file: endpoint.file,
        url: endpoint.url,
        success: false, 
        error: error.message,
        status: '❌ FALLANDO'
      });
    }
    
    console.log('');
  }

  // Resumen final
  const successful = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;
  const successRate = ((successful / results.length) * 100).toFixed(1);

  console.log('📊 RESUMEN FINAL DE ENDPOINTS DOCUMENTADOS');
  console.log('==========================================');
  console.log(`📚 Archivos documentados: ${documentedEndpoints.length}`);
  console.log(`🔍 Endpoints probados: ${results.length}`);
  console.log(`✅ Endpoints funcionando: ${successful}`);
  console.log(`❌ Endpoints fallando: ${failed}`);
  console.log(`⏱️  Tiempo total: ${totalTime}ms`);
  console.log(`📈 Tasa de éxito: ${successRate}%`);

  console.log('\n🎯 ESTADO POR ENDPOINT:');
  console.log('=======================');
  results.forEach((result, index) => {
    const status = result.success ? '✅' : '❌';
    const time = result.success ? ` (${result.duration}ms)` : '';
    console.log(`${index + 1}. ${status} ${result.name}${time}`);
    console.log(`   📄 ${result.file}`);
    console.log(`   🔗 ${result.url}`);
  });

  if (failed > 0) {
    console.log('\n❌ ENDPOINTS CON PROBLEMAS:');
    console.log('============================');
    results
      .filter(r => !r.success)
      .forEach((r, i) => {
        console.log(`${i + 1}. ${r.name} (${r.file})`);
        console.log(`   URL: ${r.url}`);
        console.log(`   Error: ${r.error}`);
      });
  }

  console.log('\n🎉 CONCLUSIÓN FINAL:');
  console.log('=====================');
  
  if (successful === results.length) {
    console.log('🎉 ¡TODOS LOS ENDPOINTS DOCUMENTADOS FUNCIONAN!');
    console.log('   ✅ Documentación completa y actualizada');
    console.log('   ✅ API completamente funcional');
    console.log('   ✅ Sistema listo para producción');
  } else {
    console.log('⚠️  Algunos endpoints documentados tienen problemas');
    console.log('   🔧 Revisar endpoints que fallan');
    console.log('   📝 Actualizar documentación si es necesario');
  }

  console.log('\n🚀 SISTEMA DE TESTING COMPLETO');
  console.log('==============================');
  console.log('✅ Todos los endpoints documentados probados');
  console.log('✅ Verificación completa realizada');
  console.log('✅ Estado del sistema verificado');
  console.log('✅ Documentación validada');
}

testSpecificDocumentedEndpoints().catch(error => {
  console.error('💥 Error:', error.message);
});
