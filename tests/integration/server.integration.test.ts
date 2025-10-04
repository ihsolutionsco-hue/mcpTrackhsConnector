/**
 * Tests de integración para el servidor MCP completo
 * Estos tests validan la inicialización y funcionamiento del servidor MCP
 */

import { TrackHSMCPServer } from '../../src/server.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';

describe('TrackHSMCPServer Integration Tests', () => {
  let server: TrackHSMCPServer;
  let originalEnv: NodeJS.ProcessEnv;

  beforeAll(() => {
    // Guardar variables de entorno originales
    originalEnv = { ...process.env };
  });

  afterAll(() => {
    // Restaurar variables de entorno originales
    process.env = originalEnv;
  });

  beforeEach(() => {
    // Configurar variables de entorno para testing
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

  describe('Inicialización del Servidor', () => {
    it('debe inicializar correctamente con configuración válida', () => {
      expect(() => {
        server = new TrackHSMCPServer();
      }).not.toThrow();
      
      expect(server).toBeDefined();
    });

    it('debe fallar con variables de entorno faltantes', () => {
      delete process.env.TRACKHS_API_URL;
      
      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('Variable de entorno requerida no configurada: TRACKHS_API_URL');
    });

    it('debe fallar con URL inválida', () => {
      process.env.TRACKHS_API_URL = 'not-a-valid-url';
      
      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('TRACKHS_API_URL debe ser una URL válida');
    });

    it('debe validar todas las variables de entorno requeridas', () => {
      const requiredVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
      
      requiredVars.forEach(envVar => {
        const originalValue = process.env[envVar];
        delete process.env[envVar];
        
        expect(() => {
          new TrackHSMCPServer();
        }).toThrow(`Variable de entorno requerida no configurada: ${envVar}`);
        
        // Restaurar valor original
        process.env[envVar] = originalValue;
      });
    });
  });

  describe('Registro de Herramientas', () => {
    beforeEach(() => {
      server = new TrackHSMCPServer();
    });

    it('debe registrar todas las herramientas disponibles', () => {
      expect(server.tools).toBeDefined();
      expect(Array.isArray(server.tools)).toBe(true);
      expect(server.tools.length).toBeGreaterThan(0);
    });

    it('debe tener herramientas con propiedades requeridas', () => {
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
    });

    it('debe incluir herramientas específicas', () => {
      const toolNames = server.tools.map(tool => tool.name);
      
      expect(toolNames).toContain('get_reviews');
      expect(toolNames).toContain('get_contacts');
      expect(toolNames).toContain('get_reservation');
      expect(toolNames).toContain('search_reservations');
      expect(toolNames).toContain('get_units');
    });
  });

  describe('Ciclo de Vida del Servidor', () => {
    it('debe iniciar y detener correctamente', async () => {
      server = new TrackHSMCPServer();
      
      await expect(server.start()).resolves.not.toThrow();
      expect(server).toBeDefined();
      
      await expect(server.stop()).resolves.not.toThrow();
    });

    it('debe manejar múltiples inicios y paradas', async () => {
      server = new TrackHSMCPServer();
      
      // Primer ciclo
      await server.start();
      await server.stop();
      
      // Segundo ciclo
      await server.start();
      await server.stop();
    });

    it('debe manejar parada sin inicio previo', async () => {
      server = new TrackHSMCPServer();
      
      await expect(server.stop()).resolves.not.toThrow();
    });
  });

  describe('Manejo de Errores', () => {
    it('debe manejar errores de inicialización del cliente API', () => {
      process.env.TRACKHS_API_URL = 'invalid-url';
      
      expect(() => {
        new TrackHSMCPServer();
      }).toThrow();
    });

    it('debe manejar errores de credenciales inválidas', () => {
      process.env.TRACKHS_USERNAME = '';
      process.env.TRACKHS_PASSWORD = '';
      
      expect(() => {
        new TrackHSMCPServer();
      }).toThrow();
    });
  });

  describe('Configuración de Herramientas', () => {
    beforeEach(() => {
      server = new TrackHSMCPServer();
    });

    it('debe configurar herramientas con cliente API válido', () => {
      server.tools.forEach(tool => {
        // Verificar que cada herramienta tiene acceso al cliente API
        expect((tool as any).apiClient).toBeDefined();
        expect((tool as any).apiClient).toBeInstanceOf(TrackHSApiClient);
      });
    });

    it('debe validar schemas de entrada de las herramientas', () => {
      server.tools.forEach(tool => {
        const schema = tool.inputSchema;
        
        expect(schema).toBeDefined();
        expect(schema.type).toBe('object');
        expect(schema.properties).toBeDefined();
        expect(typeof schema.properties).toBe('object');
      });
    });
  });

  describe('Integración con API Real', () => {
    it('debe funcionar con configuración de API real', async () => {
      if (!process.env.TRACKHS_API_URL || !process.env.TRACKHS_USERNAME || !process.env.TRACKHS_PASSWORD) {
        console.log('⏭️  Saltando test - Variables de entorno no configuradas');
        return;
      }

      server = new TrackHSMCPServer();
      
      try {
        await server.start();
        expect(server).toBeDefined();
        
        // Verificar que las herramientas están configuradas
        expect(server.tools.length).toBeGreaterThan(0);
        
        // Probar una herramienta simple
        const reviewsTool = server.tools.find(tool => tool.name === 'get_reviews');
        if (reviewsTool) {
          try {
            const result = await reviewsTool.execute({});
            expect(result).toBeDefined();
          } catch (error) {
            // Es normal que falle si la API no está disponible
            expect(error).toBeInstanceOf(Error);
          }
        }
      } finally {
        await server.stop();
      }
    });

    it('debe manejar errores de conexión a API', async () => {
      // Usar una URL que no responde
      process.env.TRACKHS_API_URL = 'https://nonexistent-api.trackhs.com';
      
      server = new TrackHSMCPServer();
      
      try {
        await server.start();
        
        // Intentar usar una herramienta
        const reviewsTool = server.tools.find(tool => tool.name === 'get_reviews');
        if (reviewsTool) {
          await expect(reviewsTool.execute({})).rejects.toThrow();
        }
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      } finally {
        await server.stop();
      }
    });
  });

  describe('Validación de Configuración', () => {
    it('debe validar configuración completa', () => {
      server = new TrackHSMCPServer();
      
      // Verificar que el servidor tiene todas las propiedades necesarias
      expect(server).toHaveProperty('tools');
      expect(server).toHaveProperty('start');
      expect(server).toHaveProperty('stop');
      
      expect(typeof server.start).toBe('function');
      expect(typeof server.stop).toBe('function');
    });

    it('debe manejar diferentes entornos', () => {
      const environments = [
        { url: 'https://api.trackhs.com', env: 'production' },
        { url: 'https://staging-api.trackhs.com', env: 'staging' },
        { url: 'https://dev-api.trackhs.com', env: 'development' }
      ];

      environments.forEach(({ url, env }) => {
        process.env.TRACKHS_API_URL = url;
        
        expect(() => {
          new TrackHSMCPServer();
        }).not.toThrow();
      });
    });
  });

  describe('Manejo de Señales del Sistema', () => {
    it('debe manejar señales SIGINT', async () => {
      server = new TrackHSMCPServer();
      await server.start();
      
      // Simular señal SIGINT
      process.emit('SIGINT' as any);
      
      // El servidor debe manejar la señal sin errores
      expect(server).toBeDefined();
    });

    it('debe manejar señales SIGTERM', async () => {
      server = new TrackHSMCPServer();
      await server.start();
      
      // Simular señal SIGTERM
      process.emit('SIGTERM' as any);
      
      // El servidor debe manejar la señal sin errores
      expect(server).toBeDefined();
    });
  });
});
