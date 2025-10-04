/**
 * Tests unitarios para tipos de datos del core
 */

import {
  TrackHSConfig,
  RequestOptions,
  ApiError,
  PaginationParams,
  SearchParams,
  TrackHSResponse
} from '../../../src/core/types.js';

describe('Core Types', () => {
  describe('TrackHSConfig', () => {
    it('debe permitir configuración válida', () => {
      const config: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.com',
        username: 'test_user',
        password: 'test_password'
      };

      expect(config.baseUrl).toBe('https://api.trackhs.com');
      expect(config.username).toBe('test_user');
      expect(config.password).toBe('test_password');
    });

    it('debe permitir URLs con diferentes protocolos', () => {
      const configs: TrackHSConfig[] = [
        { baseUrl: 'https://api.trackhs.com', username: 'user', password: 'pass' },
        { baseUrl: 'http://localhost:3000', username: 'user', password: 'pass' },
        { baseUrl: 'https://staging-api.trackhs.com', username: 'user', password: 'pass' }
      ];

      configs.forEach(config => {
        expect(config.baseUrl).toMatch(/^https?:\/\//);
        expect(config.username).toBeDefined();
        expect(config.password).toBeDefined();
      });
    });

    it('debe permitir credenciales con caracteres especiales', () => {
      const config: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.com',
        username: 'user@domain.com',
        password: 'p@ssw0rd!'
      };

      expect(config.username).toBe('user@domain.com');
      expect(config.password).toBe('p@ssw0rd!');
    });
  });

  describe('RequestOptions', () => {
    it('debe permitir opciones básicas', () => {
      const options: RequestOptions = {
        method: 'GET'
      };

      expect(options.method).toBe('GET');
    });

    it('debe permitir headers personalizados', () => {
      const options: RequestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token',
          'Custom-Header': 'custom-value'
        }
      };

      expect(options.method).toBe('POST');
      expect(options.headers).toBeDefined();
      expect(options.headers!['Content-Type']).toBe('application/json');
      expect(options.headers!['Authorization']).toBe('Bearer token');
      expect(options.headers!['Custom-Header']).toBe('custom-value');
    });

    it('debe permitir body como string', () => {
      const options: RequestOptions = {
        method: 'POST',
        body: JSON.stringify({ data: 'test' })
      };

      expect(options.body).toBe('{"data":"test"}');
    });

    it('debe permitir body undefined', () => {
      const options: RequestOptions = {
        method: 'GET',
        body: undefined
      };

      expect(options.body).toBeUndefined();
    });

    it('debe permitir todos los métodos HTTP', () => {
      const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'];
      
      methods.forEach(method => {
        const options: RequestOptions = { method };
        expect(options.method).toBe(method);
      });
    });
  });

  describe('ApiError', () => {
    it('debe permitir error básico', () => {
      const error: ApiError = {
        message: 'Something went wrong'
      };

      expect(error.message).toBe('Something went wrong');
      expect(error.status).toBeUndefined();
      expect(error.statusText).toBeUndefined();
    });

    it('debe permitir error con status', () => {
      const error: ApiError = {
        message: 'Not Found',
        status: 404,
        statusText: 'Not Found'
      };

      expect(error.message).toBe('Not Found');
      expect(error.status).toBe(404);
      expect(error.statusText).toBe('Not Found');
    });

    it('debe permitir diferentes códigos de estado', () => {
      const errors: ApiError[] = [
        { message: 'Bad Request', status: 400, statusText: 'Bad Request' },
        { message: 'Unauthorized', status: 401, statusText: 'Unauthorized' },
        { message: 'Forbidden', status: 403, statusText: 'Forbidden' },
        { message: 'Not Found', status: 404, statusText: 'Not Found' },
        { message: 'Internal Server Error', status: 500, statusText: 'Internal Server Error' }
      ];

      errors.forEach(error => {
        expect(error.message).toBeDefined();
        expect(error.status).toBeGreaterThan(0);
        expect(error.statusText).toBeDefined();
      });
    });
  });

  describe('PaginationParams', () => {
    it('debe permitir parámetros básicos de paginación', () => {
      const params: PaginationParams = {
        page: 1,
        size: 10
      };

      expect(params.page).toBe(1);
      expect(params.size).toBe(10);
    });

    it('debe permitir parámetros de ordenamiento', () => {
      const params: PaginationParams = {
        page: 2,
        size: 20,
        sortColumn: 'created_at',
        sortDirection: 'desc'
      };

      expect(params.page).toBe(2);
      expect(params.size).toBe(20);
      expect(params.sortColumn).toBe('created_at');
      expect(params.sortDirection).toBe('desc');
    });

    it('debe permitir sortDirection asc', () => {
      const params: PaginationParams = {
        sortDirection: 'asc'
      };

      expect(params.sortDirection).toBe('asc');
    });

    it('debe permitir sortDirection desc', () => {
      const params: PaginationParams = {
        sortDirection: 'desc'
      };

      expect(params.sortDirection).toBe('desc');
    });

    it('debe permitir parámetros opcionales', () => {
      const params: PaginationParams = {};

      expect(params.page).toBeUndefined();
      expect(params.size).toBeUndefined();
      expect(params.sortColumn).toBeUndefined();
      expect(params.sortDirection).toBeUndefined();
    });

    it('debe permitir diferentes valores de página y tamaño', () => {
      const testCases = [
        { page: 1, size: 1 },
        { page: 10, size: 50 },
        { page: 100, size: 1000 }
      ];

      testCases.forEach(({ page, size }) => {
        const params: PaginationParams = { page, size };
        expect(params.page).toBe(page);
        expect(params.size).toBe(size);
      });
    });
  });

  describe('SearchParams', () => {
    it('debe permitir parámetros de búsqueda básicos', () => {
      const params: SearchParams = {
        search: 'test query'
      };

      expect(params.search).toBe('test query');
    });

    it('debe permitir filtro por fecha', () => {
      const params: SearchParams = {
        search: 'test',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      expect(params.search).toBe('test');
      expect(params.updatedSince).toBe('2024-01-01T00:00:00Z');
    });

    it('debe permitir solo filtro por fecha', () => {
      const params: SearchParams = {
        updatedSince: '2024-01-01T00:00:00Z'
      };

      expect(params.search).toBeUndefined();
      expect(params.updatedSince).toBe('2024-01-01T00:00:00Z');
    });

    it('debe permitir parámetros opcionales', () => {
      const params: SearchParams = {};

      expect(params.search).toBeUndefined();
      expect(params.updatedSince).toBeUndefined();
    });

    it('debe permitir diferentes formatos de fecha', () => {
      const dateFormats = [
        '2024-01-01T00:00:00Z',
        '2024-01-01T12:30:45Z',
        '2024-12-31T23:59:59Z'
      ];

      dateFormats.forEach(date => {
        const params: SearchParams = { updatedSince: date };
        expect(params.updatedSince).toBe(date);
      });
    });
  });

  describe('TrackHSResponse', () => {
    it('debe permitir respuesta exitosa con datos', () => {
      const response: TrackHSResponse<string> = {
        data: 'test data',
        success: true
      };

      expect(response.data).toBe('test data');
      expect(response.success).toBe(true);
      expect(response.message).toBeUndefined();
    });

    it('debe permitir respuesta con mensaje', () => {
      const response: TrackHSResponse<number[]> = {
        data: [1, 2, 3],
        success: true,
        message: 'Data retrieved successfully'
      };

      expect(response.data).toEqual([1, 2, 3]);
      expect(response.success).toBe(true);
      expect(response.message).toBe('Data retrieved successfully');
    });

    it('debe permitir respuesta de error', () => {
      const response: TrackHSResponse<null> = {
        data: null,
        success: false,
        message: 'Error occurred'
      };

      expect(response.data).toBeNull();
      expect(response.success).toBe(false);
      expect(response.message).toBe('Error occurred');
    });

    it('debe permitir diferentes tipos de datos', () => {
      const stringResponse: TrackHSResponse<string> = {
        data: 'string data',
        success: true
      };

      const numberResponse: TrackHSResponse<number> = {
        data: 42,
        success: true
      };

      const objectResponse: TrackHSResponse<{ id: number; name: string }> = {
        data: { id: 1, name: 'test' },
        success: true
      };

      const arrayResponse: TrackHSResponse<string[]> = {
        data: ['item1', 'item2'],
        success: true
      };

      expect(stringResponse.data).toBe('string data');
      expect(numberResponse.data).toBe(42);
      expect(objectResponse.data).toEqual({ id: 1, name: 'test' });
      expect(arrayResponse.data).toEqual(['item1', 'item2']);
    });

    it('debe permitir respuesta sin datos', () => {
      const response: TrackHSResponse<undefined> = {
        data: undefined,
        success: true,
        message: 'Operation completed'
      };

      expect(response.data).toBeUndefined();
      expect(response.success).toBe(true);
      expect(response.message).toBe('Operation completed');
    });
  });

  describe('Integración entre tipos', () => {
    it('debe permitir configuración completa con todos los tipos', () => {
      const config: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.com',
        username: 'user',
        password: 'pass'
      };

      const requestOptions: RequestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ test: 'data' })
      };

      const paginationParams: PaginationParams = {
        page: 1,
        size: 10,
        sortColumn: 'id',
        sortDirection: 'asc'
      };

      const searchParams: SearchParams = {
        search: 'test',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      const response: TrackHSResponse<any> = {
        data: { result: 'success' },
        success: true,
        message: 'Request completed'
      };

      expect(config).toBeDefined();
      expect(requestOptions).toBeDefined();
      expect(paginationParams).toBeDefined();
      expect(searchParams).toBeDefined();
      expect(response).toBeDefined();
    });
  });
});
