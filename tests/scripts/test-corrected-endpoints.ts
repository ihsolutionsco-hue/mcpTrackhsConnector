/**
 * Script para probar los endpoints con las URLs correctas encontradas
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';

async function testCorrectedEndpoints() {
  console.log('🔍 Probando endpoints con URLs corregidas...\n');

  const config = {
    baseUrl: 'https://ihmvacations.trackhs.com/api',
    username: 'aba99777416466b6bdc1a25223192ccb',
    password: '18c87461011f355cc11000a24215cbda'
  };

  const apiClient = new TrackHSApiClient(config);
  console.log('✅ Cliente API configurado\n');

  // Endpoints corregidos
  const correctedEndpoints = [
    {
      name: 'Get Contacts (CORREGIDO)',
      url: '/crm/contacts',
      description: 'Obtener contactos - URL correcta encontrada'
    },
    {
      name: 'Get Ledger Accounts (probando más variaciones)',
      url: '/crm/ledger-accounts',
      description: 'Intentar con prefijo CRM'
    },
    {
      name: 'Get Ledger Accounts (probando accounting)',
      url: '/accounting/accounts',
      description: 'Intentar con accounting/accounts'
    },
    {
      name: 'Get Ledger Accounts (probando financial)',
      url: '/financial/accounts',
      description: 'Intentar con financial/accounts'
    },
    {
      name: 'Get Ledger Accounts (probando bookkeeping)',
      url: '/bookkeeping/accounts',
      description: 'Intentar con bookkeeping/accounts'
    }
  ];

  for (const endpoint of correctedEndpoints) {
    try {
      console.log(`🔍 ${endpoint.name}`);
      console.log(`   ${endpoint.description}`);
      console.log(`   URL: ${endpoint.url}`);
      
      const startTime = Date.now();
      const response = await apiClient.get(`${endpoint.url}?page=1&size=3`);
      const duration = Date.now() - startTime;
      
      console.log(`   ✅ Éxito (${duration}ms)`);
      
      // Analizar la respuesta
      if (response && typeof response === 'object') {
        console.log(`   📊 Estructura de respuesta:`);
        console.log(`      - Propiedades: ${Object.keys(response).join(', ')}`);
        
        // Si tiene _embedded, mostrar detalles
        if (response._embedded) {
          console.log(`   📦 Contenido _embedded:`);
          Object.keys(response._embedded).forEach(key => {
            const items = response._embedded[key];
            if (Array.isArray(items)) {
              console.log(`      - ${key}: ${items.length} elementos`);
              if (items.length > 0) {
                const firstItem = items[0];
                console.log(`        Ejemplo: ${JSON.stringify(firstItem, null, 8).substring(0, 300)}...`);
              }
            }
          });
        }
        
        // Si tiene paginación
        if (response.page !== undefined) {
          console.log(`   📄 Paginación: página ${response.page}, total ${response.total_items || 'N/A'} elementos`);
        }
      }
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`);
    }
    
    console.log('');
  }

  // Probar el endpoint de contacts con más parámetros
  console.log('🔍 Probando Get Contacts con parámetros adicionales...\n');
  
  const contactsTests = [
    {
      name: 'Contacts básico',
      url: '/crm/contacts?page=1&size=2'
    },
    {
      name: 'Contacts con búsqueda',
      url: '/crm/contacts?page=1&size=2&search=test'
    },
    {
      name: 'Contacts con ordenamiento',
      url: '/crm/contacts?page=1&size=2&sortColumn=name&sortDirection=asc'
    }
  ];

  for (const test of contactsTests) {
    try {
      console.log(`🔍 ${test.name}`);
      console.log(`   URL: ${test.url}`);
      
      const startTime = Date.now();
      const response = await apiClient.get(test.url);
      const duration = Date.now() - startTime;
      
      console.log(`   ✅ Éxito (${duration}ms)`);
      
      if (response && response._embedded && response._embedded.contacts) {
        console.log(`   📊 Contactos encontrados: ${response._embedded.contacts.length}`);
        if (response._embedded.contacts.length > 0) {
          const contact = response._embedded.contacts[0];
          console.log(`   👤 Ejemplo: ${contact.firstName || 'N/A'} ${contact.lastName || 'N/A'} (${contact.primaryEmail || 'N/A'})`);
        }
      }
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`);
    }
    
    console.log('');
  }

  console.log('🎉 Pruebas de endpoints corregidos completadas!');
}

testCorrectedEndpoints().catch(error => {
  console.error('💥 Error:', error.message);
});
