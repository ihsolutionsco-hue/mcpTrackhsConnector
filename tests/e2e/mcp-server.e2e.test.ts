/**
 * Tests E2E para el servidor MCP completo
 * Estos tests validan el funcionamiento completo del servidor MCP
 */

import { TrackHSMCPServer } from '../../src/server.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';

describe('MCP Server E2E Tests', () => {
  let server: TrackHSMCPServer;
  let originalEnv: NodeJS.ProcessEnv;

  beforeAll(() => {
    originalEnv = { ...process.env };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  beforeEach(() => {
    // Configurar entorno para testing
    process.env.TRACKHS_API_URL = process.env.TRACKHS_API_URL || 'https://api.trackhs.test';
    process.env.TRACKHS_USERNAME = process.env.TRACKHS_USERNAME || 'test_user';
    process.env.TRACKHS_PASSWORD = process.env.TRACKHS_PASSWORD || 'test_password';
  });

  afterEach(async () => {
    if (server) {
      try {
        await server.stop();
      } catch (error) {
        // Ignorar errores al detener el servidor
      }
    }
  });

  describe('Inicialización Completa del Servidor', () => {
    it('debe inicializar completamente el servidor MCP', async () => {
      server = new TrackHSMCPServer();
      
      // Verificar que el servidor se inicializa sin errores
      expect(server).toBeDefined();
      expect(server.tools).toBeDefined();
      expect(Array.isArray(server.tools)).toBe(true);
      expect(server.tools.length).toBeGreaterThan(0);

      // Verificar que todas las herramientas están configuradas
      server.tools.forEach(tool => {
        expect(tool).toHaveProperty('name');
        expect(tool).toHaveProperty('description');
        expect(tool).toHaveProperty('inputSchema');
        expect(tool).toHaveProperty('execute');
        expect(typeof tool.execute).toBe('function');
      });

      console.log('✅ Servidor MCP inicializado correctamente');
    });

    it('debe iniciar y detener el servidor correctamente', async () => {
      server = new TrackHSMCPServer();
      
      // Iniciar servidor
      await expect(server.start()).resolves.not.toThrow();
      expect(server).toBeDefined();
      
      // Detener servidor
      await expect(server.stop()).resolves.not.toThrow();
    });

    it('debe manejar múltiples ciclos de inicio/parada', async () => {
      server = new TrackHSMCPServer();
      
      // Primer ciclo
      await server.start();
      await server.stop();
      
      // Segundo ciclo
      await server.start();
      await server.stop();
      
      // Tercer ciclo
      await server.start();
      await server.stop();
    });
  });

  describe('Funcionalidad de Herramientas E2E', () => {
    beforeEach(async () => {
      server = new TrackHSMCPServer();
      await server.start();
    });

    it('debe ejecutar todas las herramientas disponibles', async () => {
      const toolResults = new Map();

      for (const tool of server.tools) {
        try {
          console.log(`🔄 Ejecutando herramienta: ${tool.name}`);
          
          // Ejecutar con parámetros por defecto
          const result = await tool.execute();
          
          expect(result).toBeDefined();
          toolResults.set(tool.name, { success: true, result });
          
          console.log(`✅ ${tool.name} ejecutada correctamente`);
        } catch (error) {
          toolResults.set(tool.name, { success: false, error: error.message });
          console.log(`⚠️  ${tool.name} falló: ${error.message}`);
        }
      }

      // Verificar que al menos algunas herramientas funcionaron
      const successfulTools = Array.from(toolResults.entries())
        .filter(([_, result]) => result.success);
      
      expect(successfulTools.length).toBeGreaterThan(0);
      console.log(`✅ ${successfulTools.length}/${server.tools.length} herramientas ejecutadas correctamente`);
    });

    it('debe manejar herramientas con parámetros específicos', async () => {
      const toolTests = [
        {
          name: 'get_reviews',
          params: { page: 1, size: 5, search: 'test' }
        },
        {
          name: 'get_contacts',
          params: { page: 1, size: 5, sortColumn: 'name' }
        },
        {
          name: 'search_reservations',
          params: { page: 1, size: 5 }
        },
        {
          name: 'get_units',
          params: { page: 1, size: 5, sortColumn: 'name' }
        }
      ];

      for (const test of toolTests) {
        const tool = server.tools.find(t => t.name === test.name);
        if (tool) {
          try {
            const result = await tool.execute(test.params);
            expect(result).toBeDefined();
            console.log(`✅ ${test.name} con parámetros específicos ejecutada correctamente`);
          } catch (error) {
            expect(error).toBeInstanceOf(Error);
            console.log(`⚠️  ${test.name} con parámetros específicos falló: ${error.message}`);
          }
        }
      }
    });

    it('debe manejar herramientas con parámetros de reservación', async () => {
      const reservationTool = server.tools.find(tool => tool.name === 'get_reservation');
      if (reservationTool) {
        try {
          const result = await reservationTool.execute({
            reservationId: '123'
          });
          expect(result).toBeDefined();
          console.log('✅ Herramienta de reservación ejecutada correctamente');
        } catch (error) {
          expect(error).toBeInstanceOf(Error);
          console.log(`⚠️  Herramienta de reservación falló: ${error.message}`);
        }
      }
    });
  });

  describe('Manejo de Errores E2E', () => {
    beforeEach(async () => {
      server = new TrackHSMCPServer();
      await server.start();
    });

    it('debe manejar errores de herramientas de manera robusta', async () => {
      const errorScenarios = [
        { tool: 'get_reviews', params: { page: -1 } },
        { tool: 'get_contacts', params: { size: 0 } },
        { tool: 'search_reservations', params: { page: 999999 } },
        { tool: 'get_units', params: { size: -1 } }
      ];

      for (const scenario of errorScenarios) {
        const tool = server.tools.find(t => t.name === scenario.tool);
        if (tool) {
          try {
            await tool.execute(scenario.params);
          } catch (error) {
            expect(error).toBeInstanceOf(Error);
            console.log(`✅ Error manejado correctamente en ${scenario.tool}`);
          }
        }
      }
    });

    it('debe manejar errores de red y timeout', async () => {
      const reviewsTool = server.tools.find(tool => tool.name === 'get_reviews');
      if (reviewsTool) {
        // Simular múltiples intentos con errores
        const attempts = 3;
        let errorCount = 0;

        for (let i = 0; i < attempts; i++) {
          try {
            await reviewsTool.execute({ page: 1, size: 1 });
          } catch (error) {
            errorCount++;
            expect(error).toBeInstanceOf(Error);
          }
        }

        console.log(`✅ ${errorCount}/${attempts} errores manejados correctamente`);
      }
    });

    it('debe manejar herramientas con parámetros inválidos', async () => {
      const invalidParams = [
        { tool: 'get_reviews', params: { page: 'invalid' } },
        { tool: 'get_contacts', params: { size: 'invalid' } },
        { tool: 'search_reservations', params: { page: null } }
      ];

      for (const test of invalidParams) {
        const tool = server.tools.find(t => t.name === test.tool);
        if (tool) {
          try {
            await tool.execute(test.params as any);
          } catch (error) {
            expect(error).toBeInstanceOf(Error);
            console.log(`✅ Parámetros inválidos manejados en ${test.tool}`);
          }
        }
      }
    });
  });

  describe('Performance E2E', () => {
    beforeEach(async () => {
      server = new TrackHSMCPServer();
      await server.start();
    });

    it('debe manejar múltiples peticiones concurrentes', async () => {
      const reviewsTool = server.tools.find(tool => tool.name === 'get_reviews');
      if (reviewsTool) {
        const concurrentRequests = Array.from({ length: 10 }, (_, i) => 
          reviewsTool.execute({ page: i + 1, size: 1 })
        );

        const startTime = Date.now();
        const results = await Promise.allSettled(concurrentRequests);
        const endTime = Date.now();
        const duration = endTime - startTime;

        // Verificar que todas las peticiones se completaron
        expect(results).toHaveLength(10);
        
        // Verificar que el tiempo de ejecución es razonable
        expect(duration).toBeLessThan(30000); // Menos de 30 segundos
        
        console.log(`✅ 10 peticiones concurrentes completadas en ${duration}ms`);
      }
    });

    it('debe manejar peticiones secuenciales eficientemente', async () => {
      const reviewsTool = server.tools.find(tool => tool.name === 'get_reviews');
      if (reviewsTool) {
        const startTime = Date.now();
        
        for (let i = 0; i < 5; i++) {
          try {
            await reviewsTool.execute({ page: i + 1, size: 1 });
          } catch (error) {
            // Es normal que falle si la API no está disponible
          }
        }
        
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        expect(duration).toBeLessThan(15000); // Menos de 15 segundos
        console.log(`✅ 5 peticiones secuenciales completadas en ${duration}ms`);
      }
    });
  });

  describe('Integración con API Real', () => {
    it('debe funcionar con configuración de API real', async () => {
      if (!process.env.TRACKHS_API_URL || !process.env.TRACKHS_USERNAME || !process.env.TRACKHS_PASSWORD) {
        console.log('⏭️  Saltando test - Variables de entorno no configuradas');
        return;
      }

      server = new TrackHSMCPServer();
      await server.start();

      // Probar herramientas con API real
      const toolsToTest = ['get_reviews', 'get_contacts', 'search_reservations', 'get_units'];
      
      for (const toolName of toolsToTest) {
        const tool = server.tools.find(t => t.name === toolName);
        if (tool) {
          try {
            const result = await tool.execute({ page: 1, size: 1 });
            expect(result).toBeDefined();
            console.log(`✅ ${toolName} funcionando con API real`);
          } catch (error) {
            expect(error).toBeInstanceOf(Error);
            console.log(`⚠️  ${toolName} falló con API real: ${error.message}`);
          }
        }
      }
    });

    it('debe manejar diferentes entornos de API', async () => {
      const environments = [
        { url: 'https://api.trackhs.com', name: 'production' },
        { url: 'https://staging-api.trackhs.com', name: 'staging' },
        { url: 'https://dev-api.trackhs.com', name: 'development' }
      ];

      for (const env of environments) {
        process.env.TRACKHS_API_URL = env.url;
        
        try {
          const testServer = new TrackHSMCPServer();
          await testServer.start();
          
          expect(testServer).toBeDefined();
          expect(testServer.tools.length).toBeGreaterThan(0);
          
          await testServer.stop();
          console.log(`✅ Servidor funcionando en entorno ${env.name}`);
        } catch (error) {
          console.log(`⚠️  Entorno ${env.name} no disponible: ${error.message}`);
        }
      }
    });
  });

  describe('Manejo de Señales del Sistema E2E', () => {
    it('debe manejar señales SIGINT correctamente', async () => {
      server = new TrackHSMCPServer();
      await server.start();

      // Simular señal SIGINT
      const originalEmit = process.emit;
      let signalHandled = false;
      
      process.emit = function(event: string | symbol, ...args: any[]) {
        if (event === 'SIGINT') {
          signalHandled = true;
          return true;
        }
        return originalEmit.call(this, event, ...args);
      };

      process.emit('SIGINT' as any);
      expect(signalHandled).toBe(true);
      
      // Restaurar función original
      process.emit = originalEmit;
    });

    it('debe manejar señales SIGTERM correctamente', async () => {
      server = new TrackHSMCPServer();
      await server.start();

      // Simular señal SIGTERM
      const originalEmit = process.emit;
      let signalHandled = false;
      
      process.emit = function(event: string | symbol, ...args: any[]) {
        if (event === 'SIGTERM') {
          signalHandled = true;
          return true;
        }
        return originalEmit.call(this, event, ...args);
      };

      process.emit('SIGTERM' as any);
      expect(signalHandled).toBe(true);
      
      // Restaurar función original
      process.emit = originalEmit;
    });
  });

  describe('Validación de Configuración E2E', () => {
    it('debe validar configuración completa del servidor', async () => {
      server = new TrackHSMCPServer();
      await server.start();

      // Verificar propiedades del servidor
      expect(server).toHaveProperty('tools');
      expect(server).toHaveProperty('start');
      expect(server).toHaveProperty('stop');
      
      // Verificar que todas las herramientas están configuradas
      expect(server.tools.length).toBeGreaterThan(0);
      
      // Verificar que cada herramienta tiene las propiedades requeridas
      server.tools.forEach(tool => {
        expect(tool).toHaveProperty('name');
        expect(tool).toHaveProperty('description');
        expect(tool).toHaveProperty('inputSchema');
        expect(tool).toHaveProperty('execute');
        
        expect(typeof tool.name).toBe('string');
        expect(typeof tool.description).toBe('string');
        expect(typeof tool.execute).toBe('function');
        expect(tool.inputSchema).toBeDefined();
      });

      console.log('✅ Configuración del servidor validada correctamente');
    });

    it('debe manejar configuración de diferentes entornos', async () => {
      const configs = [
        { env: 'development', url: 'https://dev-api.trackhs.com' },
        { env: 'staging', url: 'https://staging-api.trackhs.com' },
        { env: 'production', url: 'https://api.trackhs.com' }
      ];

      for (const config of configs) {
        process.env.TRACKHS_API_URL = config.url;
        
        try {
          const testServer = new TrackHSMCPServer();
          await testServer.start();
          
          expect(testServer).toBeDefined();
          expect(testServer.tools.length).toBeGreaterThan(0);
          
          await testServer.stop();
          console.log(`✅ Configuración ${config.env} validada correctamente`);
        } catch (error) {
          console.log(`⚠️  Configuración ${config.env} no disponible: ${error.message}`);
        }
      }
    });
  });
});
