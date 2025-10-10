/**
 * Script para probar el servidor MCP localmente
 */

// Configurar variables de entorno para testing
process.env.TRACKHS_API_URL = 'https://ihmvacations.trackhs.com/api';
process.env.TRACKHS_USERNAME = 'test_user';
process.env.TRACKHS_PASSWORD = 'test_password';
process.env.NODE_ENV = 'test';

import { TrackHSMCPServer } from './dist/mcp-server.js';

async function testLocalMCP() {
  console.log('🚀 Iniciando testing local del servidor MCP...');
  
  try {
    // Crear instancia del servidor
    const server = new TrackHSMCPServer();
    console.log('✅ Servidor MCP inicializado correctamente');
    
    // Obtener información del servidor
    const serverInfo = server.getServerInfo();
    console.log('📊 Información del servidor:', JSON.stringify(serverInfo, null, 2));
    
    // Obtener herramientas disponibles
    console.log(`🔧 Herramientas disponibles: ${server.tools.length}`);
    server.tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description}`);
    });
    
    // Probar herramienta get_contacts
    console.log('\n👥 === PROBANDO HERRAMIENTA GET_CONTACTS ===');
    try {
      const contactsResult = await server.tools.find(t => t.name === 'get_contacts')?.execute({
        page: 1,
        size: 3
      });
      console.log('✅ Resultado get_contacts:', JSON.stringify(contactsResult, null, 2));
    } catch (error) {
      console.log('❌ Error en get_contacts:', error.message);
    }
    
    // Probar herramienta get_units
    console.log('\n🏠 === PROBANDO HERRAMIENTA GET_UNITS ===');
    try {
      const unitsResult = await server.tools.find(t => t.name === 'get_units')?.execute({
        page: 1,
        size: 3
      });
      console.log('✅ Resultado get_units:', JSON.stringify(unitsResult, null, 2));
    } catch (error) {
      console.log('❌ Error en get_units:', error.message);
    }
    
    // Probar herramienta get_reviews
    console.log('\n⭐ === PROBANDO HERRAMIENTA GET_REVIEWS ===');
    try {
      const reviewsResult = await server.tools.find(t => t.name === 'get_reviews')?.execute({
        page: 1,
        size: 3
      });
      console.log('✅ Resultado get_reviews:', JSON.stringify(reviewsResult, null, 2));
    } catch (error) {
      console.log('❌ Error en get_reviews:', error.message);
    }
    
    console.log('\n🎉 Testing local completado!');
    
  } catch (error) {
    console.error('❌ Error fatal:', error.message);
    console.error('Stack trace:', error.stack);
  }
}

// Ejecutar testing
testLocalMCP().catch(console.error);
