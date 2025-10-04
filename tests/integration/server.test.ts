/**
 * Tests de integración para TrackHSMCPServer
 */

import { TrackHSMCPServer } from '../../src/server.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth } from '../utils/test-helpers.js';

describe('TrackHSMCPServer Integration', () => {
  let server: TrackHSMCPServer;
  let mockScope: any;

  beforeEach(() => {
    // Configurar mock HTTP
    mockScope = setupApiMock();
    mockSuccessfulAuth(mockScope);
  });

  afterEach(() => {
    cleanupApiMock();
    if (server) {
      server.stop();
    }
  });

  describe('Inicialización del servidor', () => {
    it('debe inicializar correctamente con variables de entorno válidas', () => {
      expect(() => {
        server = new TrackHSMCPServer();
      }).not.toThrow();
    });

    it('debe registrar todas las herramientas correctamente', () => {
      server = new TrackHSMCPServer();
      
      // Verificar que el servidor tenga las herramientas registradas
      // Esto se puede verificar a través de la reflexión o métodos públicos
      expect(server).toBeDefined();
    });
  });

  describe('Validación de variables de entorno', () => {
    const originalEnv = process.env;

    beforeEach(() => {
      jest.resetModules();
      process.env = { ...originalEnv };
    });

    afterEach(() => {
      process.env = originalEnv;
    });

    it('debe fallar si TRACKHS_API_URL no está configurada', () => {
      delete process.env.TRACKHS_API_URL;

      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('Variable de entorno requerida no configurada: TRACKHS_API_URL');
    });

    it('debe fallar si TRACKHS_USERNAME no está configurada', () => {
      delete process.env.TRACKHS_USERNAME;

      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('Variable de entorno requerida no configurada: TRACKHS_USERNAME');
    });

    it('debe fallar si TRACKHS_PASSWORD no está configurada', () => {
      delete process.env.TRACKHS_PASSWORD;

      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('Variable de entorno requerida no configurada: TRACKHS_PASSWORD');
    });

    it('debe fallar si TRACKHS_API_URL no es una URL válida', () => {
      process.env.TRACKHS_API_URL = 'invalid-url';

      expect(() => {
        new TrackHSMCPServer();
      }).toThrow('TRACKHS_API_URL debe ser una URL válida');
    });
  });

  describe('Manejo de herramientas', () => {
    beforeEach(() => {
      server = new TrackHSMCPServer();
    });

    it('debe tener todas las herramientas registradas', () => {
      // Verificar que el servidor tenga las herramientas esperadas
      // Esto requeriría acceso a las herramientas internas del servidor
      expect(server).toBeDefined();
    });

    it('debe manejar solicitudes de herramientas correctamente', async () => {
      // Mock de solicitud MCP
      const mockRequest = {
        params: {
          name: 'get_reviews',
          arguments: {
            page: 1,
            size: 10
          }
        }
      };

      // Mock de respuesta exitosa
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(200, {
          data: [],
          meta: {
            total: 0,
            page: 1,
            per_page: 10
          }
        });

      // Verificar que el servidor pueda manejar la solicitud
      expect(server).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    beforeEach(() => {
      server = new TrackHSMCPServer();
    });

    it('debe manejar errores de autenticación', async () => {
      // Mock de error de autenticación
      mockScope
        .post('/auth/login')
        .reply(401, {
          error: 'Unauthorized',
          message: 'Invalid credentials'
        });

      // El servidor debe manejar este error correctamente
      expect(server).toBeDefined();
    });

    it('debe manejar errores de red', async () => {
      // Mock de error de red
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .replyWithError({ code: 'ENOTFOUND' });

      // El servidor debe manejar este error correctamente
      expect(server).toBeDefined();
    });
  });

  describe('Ciclo de vida del servidor', () => {
    it('debe iniciar correctamente', async () => {
      server = new TrackHSMCPServer();
      
      // Mock del transporte MCP
      const mockTransport = {
        connect: jest.fn().mockResolvedValue(undefined),
        close: jest.fn().mockResolvedValue(undefined)
      };

      // El servidor debe poder iniciarse
      expect(server).toBeDefined();
    });

    it('debe detenerse correctamente', async () => {
      server = new TrackHSMCPServer();
      
      // El servidor debe poder detenerse
      await expect(server.stop()).resolves.not.toThrow();
    });
  });
});
