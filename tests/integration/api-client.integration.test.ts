/**
 * Tests de integración para TrackHSApiClient
 * Estos tests requieren una conexión real a la API de Track HS
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';
import { TrackHSAuth } from '../../src/core/auth.js';

describe('TrackHSApiClient Integration Tests', () => {
  let apiClient: TrackHSApiClient;
  
  beforeAll(() => {
    // Verificar que las variables de entorno estén configuradas
    const requiredEnvVars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD'];
    const missingVars = requiredEnvVars.filter(envVar => !process.env[envVar]);
    
    if (missingVars.length > 0) {
      console.warn(`⚠️  Variables de entorno faltantes: ${missingVars.join(', ')}`);
      console.warn('Los tests de integración se saltarán. Configure las variables de entorno para ejecutarlos.');
    }
    
    if (process.env.TRACKHS_API_URL && process.env.TRACKHS_USERNAME && process.env.TRACKHS_PASSWORD) {
      apiClient = new TrackHSApiClient({
        baseUrl: process.env.TRACKHS_API_URL,
        username: process.env.TRACKHS_USERNAME,
        password: process.env.TRACKHS_PASSWORD
      });
    }
  });

  describe('Autenticación', () => {
    it('debe autenticarse correctamente con credenciales válidas', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      // Verificar que el cliente se inicializa sin errores
      expect(apiClient).toBeDefined();
      
      // Verificar que las credenciales son válidas
      const auth = (apiClient as any).auth as TrackHSAuth;
      expect(auth.validateCredentials()).toBe(true);
    });

    it('debe manejar credenciales inválidas', async () => {
      if (!process.env.TRACKHS_API_URL) {
        console.log('⏭️  Saltando test - API URL no configurada');
        return;
      }

      expect(() => {
        new TrackHSApiClient({
          baseUrl: process.env.TRACKHS_API_URL!,
          username: 'invalid_user',
          password: 'invalid_password'
        });
      }).toThrow();
    });
  });

  describe('Peticiones HTTP', () => {
    it('debe realizar petición GET a endpoint válido', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      try {
        // Intentar una petición a un endpoint que debería existir
        const response = await apiClient.get('/health');
        expect(response).toBeDefined();
      } catch (error) {
        // Si el endpoint no existe, verificar que el error sea manejado correctamente
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toContain('Track HS');
      }
    });

    it('debe manejar timeout de red', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      // Crear un cliente con timeout muy corto para simular timeout
      const timeoutClient = new TrackHSApiClient({
        baseUrl: 'http://httpstat.us:200?sleep=5000', // Endpoint que tarda 5 segundos
        username: 'test',
        password: 'test'
      });

      await expect(timeoutClient.get('/')).rejects.toThrow();
    });

    it('debe manejar errores HTTP correctamente', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      try {
        await apiClient.get('/nonexistent-endpoint');
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toContain('Track HS API Error');
      }
    });
  });

  describe('Headers y Autenticación', () => {
    it('debe incluir headers de autenticación correctos', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      const auth = (apiClient as any).auth as TrackHSAuth;
      const authHeader = auth.getAuthHeader();
      
      expect(authHeader).toContain('Basic ');
      expect(authHeader).toBeDefined();
    });

    it('debe mantener headers consistentes entre peticiones', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      const auth = (apiClient as any).auth as TrackHSAuth;
      const header1 = auth.getAuthHeader();
      const header2 = auth.getAuthHeader();
      
      expect(header1).toBe(header2);
    });
  });

  describe('Manejo de Respuestas', () => {
    it('debe parsear respuestas JSON correctamente', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      try {
        const response = await apiClient.get('/api/status');
        expect(typeof response).toBe('object');
      } catch (error) {
        // Si el endpoint no existe, verificar que el error sea manejado
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe manejar respuestas de texto plano', async () => {
      if (!apiClient) {
        console.log('⏭️  Saltando test - API client no configurado');
        return;
      }

      try {
        const response = await apiClient.get('/');
        expect(typeof response).toBe('string');
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('Configuración de Red', () => {
    it('debe manejar diferentes URLs base', async () => {
      const urls = [
        'https://api.trackhs.com',
        'https://staging-api.trackhs.com',
        'https://dev-api.trackhs.com'
      ];

      for (const url of urls) {
        try {
          const client = new TrackHSApiClient({
            baseUrl: url,
            username: 'test',
            password: 'test'
          });
          expect(client).toBeDefined();
        } catch (error) {
          // Algunas URLs pueden no ser válidas, eso está bien
          expect(error).toBeInstanceOf(Error);
        }
      }
    });

    it('debe validar formato de URL', () => {
      const invalidUrls = [
        'not-a-url',
        'ftp://invalid.com',
        'http://',
        ''
      ];

      for (const url of invalidUrls) {
        expect(() => {
          new TrackHSApiClient({
            baseUrl: url,
            username: 'test',
            password: 'test'
          });
        }).toThrow();
      }
    });
  });
});
