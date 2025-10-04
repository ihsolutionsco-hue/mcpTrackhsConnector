/**
 * Tests unitarios para TrackHSApiClient
 */

import { TrackHSApiClient } from '../../../src/core/api-client.js';
import { TrackHSAuth } from '../../../src/core/auth.js';
import { TrackHSConfig } from '../../../src/core/types.js';

// Mock de fetch global
global.fetch = jest.fn();

// Mock de TrackHSAuth
jest.mock('../../../src/core/auth.js');
const MockedTrackHSAuth = TrackHSAuth as jest.MockedClass<typeof TrackHSAuth>;

describe('TrackHSApiClient', () => {
  let apiClient: TrackHSApiClient;
  let mockConfig: TrackHSConfig;
  let mockAuth: jest.Mocked<TrackHSAuth>;

  beforeEach(() => {
    // Configuración de prueba
    mockConfig = {
      baseUrl: 'https://api.trackhs.test',
      username: 'test_user',
      password: 'test_password'
    };

    // Mock de autenticación
    mockAuth = {
      getAuthHeader: jest.fn().mockReturnValue('Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ='),
      validateCredentials: jest.fn().mockReturnValue(true)
    } as any;

    MockedTrackHSAuth.mockImplementation(() => mockAuth);

    // Limpiar mocks
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockClear();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('Constructor', () => {
    it('debe inicializar correctamente con configuración válida', () => {
      expect(() => {
        apiClient = new TrackHSApiClient(mockConfig);
      }).not.toThrow();
    });

    it('debe crear instancia de TrackHSAuth con la configuración', () => {
      apiClient = new TrackHSApiClient(mockConfig);
      expect(MockedTrackHSAuth).toHaveBeenCalledWith(mockConfig);
    });

    it('debe validar credenciales en el constructor', () => {
      apiClient = new TrackHSApiClient(mockConfig);
      expect(mockAuth.validateCredentials).toHaveBeenCalled();
    });

    it('debe lanzar error si las credenciales no son válidas', () => {
      mockAuth.validateCredentials.mockReturnValue(false);
      
      expect(() => {
        apiClient = new TrackHSApiClient(mockConfig);
      }).toThrow('Credenciales de Track HS no configuradas correctamente');
    });
  });

  describe('request method', () => {
    beforeEach(() => {
      apiClient = new TrackHSApiClient(mockConfig);
    });

    it('debe realizar petición GET exitosa', async () => {
      const mockResponse = { data: 'test data' };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const result = await apiClient.request('/test-endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Authorization': 'Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          })
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe realizar petición POST con datos', async () => {
      const mockResponse = { success: true };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const testData = { name: 'test' };
      const result = await apiClient.request('/test-endpoint', {
        method: 'POST',
        body: JSON.stringify(testData)
      });

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(testData)
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe manejar respuesta de texto plano', async () => {
      const mockTextResponse = 'plain text response';
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('text/plain')
        },
        text: jest.fn().mockResolvedValue(mockTextResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const result = await apiClient.request('/test-endpoint');

      expect(result).toBe(mockTextResponse);
    });

    it('debe manejar errores HTTP', async () => {
      const mockFetchResponse = {
        ok: false,
        status: 404,
        statusText: 'Not Found'
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error en petición a Track HS: Track HS API Error: 404 Not Found');
    });

    it('debe manejar errores de red', async () => {
      const networkError = new Error('Network error');
      (global.fetch as jest.Mock).mockRejectedValue(networkError);

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error en petición a Track HS: Network error');
    });

    it('debe manejar errores desconocidos', async () => {
      (global.fetch as jest.Mock).mockRejectedValue('unknown error');

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error desconocido en petición a Track HS');
    });

    it('debe incluir headers personalizados', async () => {
      const mockResponse = { data: 'test' };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      await apiClient.request('/test-endpoint', {
        headers: {
          'Custom-Header': 'custom-value'
        }
      });

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Custom-Header': 'custom-value'
          })
        })
      );
    });
  });

  describe('get method', () => {
    beforeEach(() => {
      apiClient = new TrackHSApiClient(mockConfig);
    });

    it('debe realizar petición GET', async () => {
      const mockResponse = { data: 'test' };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const result = await apiClient.get('/test-endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'GET'
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe pasar opciones adicionales', async () => {
      const mockResponse = { data: 'test' };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      await apiClient.get('/test-endpoint', {
        headers: { 'Custom-Header': 'value' }
      });

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Custom-Header': 'value'
          })
        })
      );
    });
  });

  describe('post method', () => {
    beforeEach(() => {
      apiClient = new TrackHSApiClient(mockConfig);
    });

    it('debe realizar petición POST con datos', async () => {
      const mockResponse = { success: true };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const testData = { name: 'test' };
      const result = await apiClient.post('/test-endpoint', testData);

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(testData)
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe realizar petición POST sin datos', async () => {
      const mockResponse = { success: true };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const result = await apiClient.post('/test-endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'POST'
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe pasar opciones adicionales', async () => {
      const mockResponse = { success: true };
      const mockFetchResponse = {
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: {
          get: jest.fn().mockReturnValue('application/json')
        },
        json: jest.fn().mockResolvedValue(mockResponse)
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      const testData = { name: 'test' };
      await apiClient.post('/test-endpoint', testData, {
        headers: { 'Custom-Header': 'value' }
      });

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.trackhs.test/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(testData),
          headers: expect.objectContaining({
            'Custom-Header': 'value'
          })
        })
      );
    });
  });

  describe('Manejo de errores', () => {
    beforeEach(() => {
      apiClient = new TrackHSApiClient(mockConfig);
    });

    it('debe manejar error 401 (No autorizado)', async () => {
      const mockFetchResponse = {
        ok: false,
        status: 401,
        statusText: 'Unauthorized'
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error en petición a Track HS: Track HS API Error: 401 Unauthorized');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      const mockFetchResponse = {
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockFetchResponse);

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error en petición a Track HS: Track HS API Error: 500 Internal Server Error');
    });

    it('debe manejar timeout de red', async () => {
      const timeoutError = new Error('Request timeout');
      timeoutError.name = 'AbortError';
      (global.fetch as jest.Mock).mockRejectedValue(timeoutError);

      await expect(apiClient.request('/test-endpoint'))
        .rejects
        .toThrow('Error en petición a Track HS: Request timeout');
    });
  });
});
