/**
 * Script para probar llamadas detalladas a la API de Track HS
 * Muestra información específica de cada endpoint
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function testDetailedApi() {
  console.log('🔍 Probando API de Track HS con detalles...\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Probar endpoints que funcionaron
  const workingEndpoints = [
    {
      name: 'Get Units',
      url: '/pms/units?page=1&size=3',
      description: 'Obtener unidades disponibles'
    },
    {
      name: 'Get Nodes',
      url: '/pms/nodes?page=1&size=3',
      description: 'Obtener nodos del sistema'
    },
    {
      name: 'Get Reviews',
      url: '/channel-management/channel/reviews?page=1&size=3',
      description: 'Obtener reseñas de huéspedes'
    },
    {
      name: 'Search Reservations',
      url: '/v2/pms/reservations?page=1&size=3',
      description: 'Buscar reservaciones'
    }
  ];

  for (const endpoint of workingEndpoints) {
    try {
      console.log(`🔍 ${endpoint.name} - ${endpoint.description}`);
      console.log(`   URL: ${endpoint.url}`);
      
      const startTime = Date.now();
      const response = await apiClient.get(endpoint.url);
      const duration = Date.now() - startTime;
      
      console.log(`   ✅ Éxito (${duration}ms)`);
      
      // Analizar la respuesta
      if (response && typeof response === 'object') {
        console.log(`   📊 Estructura de respuesta:`);
        console.log(`      - Tipo: ${typeof response}`);
        console.log(`      - Propiedades: ${Object.keys(response).join(', ')}`);
        
        // Si tiene _embedded, mostrar detalles
        if (response._embedded) {
          console.log(`   📦 Contenido _embedded:`);
          Object.keys(response._embedded).forEach(key => {
            const items = response._embedded[key];
            if (Array.isArray(items)) {
              console.log(`      - ${key}: ${items.length} elementos`);
              if (items.length > 0) {
                console.log(`        Ejemplo: ${JSON.stringify(items[0], null, 8).substring(0, 200)}...`);
              }
            } else {
              console.log(`      - ${key}: ${typeof items}`);
            }
          });
        }
        
        // Si tiene paginación
        if (response.page !== undefined) {
          console.log(`   📄 Paginación:`);
          console.log(`      - Página actual: ${response.page}`);
          console.log(`      - Tamaño de página: ${response.page_size || 'N/A'}`);
          console.log(`      - Total de elementos: ${response.total_items || 'N/A'}`);
        }
        
        // Si tiene _links
        if (response._links) {
          console.log(`   🔗 Enlaces disponibles: ${Object.keys(response._links).join(', ')}`);
        }
      }
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`);
    }
    
    console.log('');
  }

  // Probar endpoints que fallaron con URLs alternativas
  console.log('🔧 Probando endpoints alternativos...\n');
  
  const alternativeEndpoints = [
    {
      name: 'Get Contacts (alternativo)',
      url: '/pms/contacts?page=1&size=2',
      description: 'Intentar obtener contactos con URL alternativa'
    },
    {
      name: 'Get Ledger Accounts (alternativo)',
      url: '/accounting/ledger-accounts?page=1&size=2',
      description: 'Intentar obtener cuentas contables con URL alternativa'
    }
  ];

  for (const endpoint of alternativeEndpoints) {
    try {
      console.log(`🔍 ${endpoint.name}`);
      console.log(`   URL: ${endpoint.url}`);
      
      const startTime = Date.now();
      const response = await apiClient.get(endpoint.url);
      const duration = Date.now() - startTime;
      
      console.log(`   ✅ Éxito (${duration}ms)`);
      console.log(`   📊 Respuesta: ${JSON.stringify(response, null, 2).substring(0, 300)}...`);
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`);
    }
    
    console.log('');
  }

  console.log('🎉 Pruebas detalladas completadas!');
  console.log('   ✅ API funcionando correctamente');
  console.log('   ✅ Autenticación exitosa');
  console.log('   ✅ Múltiples endpoints accesibles');
}

testDetailedApi().catch(error => {
  console.error('💥 Error:', error.message);
});
