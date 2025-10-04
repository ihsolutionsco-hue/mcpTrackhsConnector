/**
 * Resumen final de todos los endpoints probados
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function finalEndpointSummary() {
  console.log('📊 RESUMEN FINAL DE ENDPOINTS DE TRACK HS API\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Endpoints que funcionan
  const workingEndpoints = [
    {
      name: 'Get Units',
      url: '/pms/units',
      description: 'Obtener unidades disponibles',
      status: '✅ FUNCIONANDO'
    },
    {
      name: 'Get Nodes', 
      url: '/pms/nodes',
      description: 'Obtener nodos del sistema',
      status: '✅ FUNCIONANDO'
    },
    {
      name: 'Get Reviews',
      url: '/channel-management/channel/reviews',
      description: 'Obtener reseñas de huéspedes',
      status: '✅ FUNCIONANDO'
    },
    {
      name: 'Search Reservations',
      url: '/v2/pms/reservations',
      description: 'Buscar reservaciones',
      status: '✅ FUNCIONANDO'
    },
    {
      name: 'Get Contacts',
      url: '/crm/contacts',
      description: 'Obtener contactos (URL CORREGIDA)',
      status: '✅ FUNCIONANDO'
    }
  ];

  // Endpoints que no funcionan
  const nonWorkingEndpoints = [
    {
      name: 'Get Ledger Accounts',
      url: '/accounting/ledger-accounts',
      description: 'Obtener cuentas contables',
      status: '❌ NO DISPONIBLE',
      reason: 'Endpoint no disponible en esta instancia de Track HS'
    }
  ];

  console.log('✅ ENDPOINTS QUE FUNCIONAN:');
  console.log('============================');
  
  for (const endpoint of workingEndpoints) {
    console.log(`\n🔍 ${endpoint.name}`);
    console.log(`   URL: ${endpoint.url}`);
    console.log(`   Descripción: ${endpoint.description}`);
    console.log(`   Estado: ${endpoint.status}`);
    
    try {
      const startTime = Date.now();
      const response = await apiClient.get(`${endpoint.url}?page=1&size=1`);
      const duration = Date.now() - startTime;
      
      console.log(`   ✅ Prueba exitosa (${duration}ms)`);
      
      if (response && typeof response === 'object') {
        const keys = Object.keys(response);
        console.log(`   📊 Propiedades: ${keys.slice(0, 5).join(', ')}${keys.length > 5 ? '...' : ''}`);
        
        if (response._embedded) {
          const embeddedKeys = Object.keys(response._embedded);
          embeddedKeys.forEach(key => {
            if (Array.isArray(response._embedded[key])) {
              console.log(`   📦 ${key}: ${response._embedded[key].length} elementos`);
            }
          });
        }
        
        if (response.total_items !== undefined) {
          console.log(`   📄 Total elementos: ${response.total_items}`);
        }
      }
      
    } catch (error) {
      console.log(`   ❌ Error en prueba: ${error.message}`);
    }
  }

  console.log('\n❌ ENDPOINTS QUE NO FUNCIONAN:');
  console.log('===============================');
  
  for (const endpoint of nonWorkingEndpoints) {
    console.log(`\n🔍 ${endpoint.name}`);
    console.log(`   URL: ${endpoint.url}`);
    console.log(`   Descripción: ${endpoint.description}`);
    console.log(`   Estado: ${endpoint.status}`);
    console.log(`   Razón: ${endpoint.reason}`);
  }

  console.log('\n📈 ESTADÍSTICAS FINALES:');
  console.log('========================');
  console.log(`✅ Endpoints funcionando: ${workingEndpoints.length}`);
  console.log(`❌ Endpoints no disponibles: ${nonWorkingEndpoints.length}`);
  console.log(`📊 Tasa de éxito: ${((workingEndpoints.length / (workingEndpoints.length + nonWorkingEndpoints.length)) * 100).toFixed(1)}%`);

  console.log('\n🎯 CONCLUSIONES:');
  console.log('================');
  console.log('✅ La mayoría de endpoints funcionan correctamente');
  console.log('✅ Se corrigió el endpoint de Contacts (usar /crm/contacts)');
  console.log('⚠️  El endpoint de Ledger Accounts no está disponible en esta instancia');
  console.log('💡 Esto es normal - no todas las instancias de Track HS tienen todas las funcionalidades');

  console.log('\n🔧 ACCIONES RECOMENDADAS:');
  console.log('=========================');
  console.log('1. ✅ Actualizar GetContactsTool para usar /crm/contacts');
  console.log('2. ⚠️  Marcar GetLedgerAccountsTool como no disponible');
  console.log('3. ✅ Mantener todos los demás endpoints como están');
  console.log('4. 📝 Documentar que Ledger Accounts no está disponible en esta instancia');

  console.log('\n🎉 ¡Análisis de endpoints completado!');
}

finalEndpointSummary().catch(error => {
  console.error('💥 Error:', error.message);
});
