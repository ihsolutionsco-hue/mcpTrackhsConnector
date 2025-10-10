/**
 * Tests para GetReviewsTool
 */

import { GetReviewsTool } from '../../src/tools/get-reviews.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetReviewsTool', () => {
  let tool: GetReviewsTool;
  let apiClient: TrackHSApiClient;
  let mockScope: any;

  beforeEach(() => {
    // Configurar cliente API mock
    apiClient = new TrackHSApiClient({
      baseUrl: process.env.TRACKHS_API_URL!,
      username: process.env.TRACKHS_USERNAME!,
      password: process.env.TRACKHS_PASSWORD!
    });

    // Crear herramienta
    tool = new GetReviewsTool(apiClient);

    // Configurar mock HTTP
    mockScope = setupApiMock();
    mockSuccessfulAuth(mockScope);
  });

  afterEach(() => {
    cleanupApiMock();
  });

  describe('Validación de parámetros', () => {
    it('debe aceptar parámetros válidos', () => {
      const validParams = {
        page: 1,
        size: 10,
        sortColumn: 'id' as const,
        sortDirection: 'asc' as const,
        search: 'test',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      // No podemos acceder a validateParams directamente, probamos con execute
      expect(() => tool.execute(validParams)).not.toThrow();
    });

    it('debe manejar parámetros por defecto', () => {
      // Test con parámetros mínimos
      expect(() => tool.execute({})).not.toThrow();
    });
  });

  describe('Ejecución exitosa', () => {
    it('debe obtener reseñas con parámetros por defecto', async () => {
      // Mock de respuesta exitosa
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(200, mockApiResponses.reviews.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result.data).toHaveLength(2);
      expect(result.meta.total).toBe(2);
    });

    it('debe obtener reseñas con parámetros personalizados', async () => {
      const params = {
        page: 2,
        size: 5,
        sortColumn: 'id' as const,
        sortDirection: 'desc' as const,
        search: 'excelente'
      };

      mockScope
        .get('/channel-management/channel/reviews?page=2&size=5&sortColumn=id&sortDirection=desc&search=excelente')
        .reply(200, mockApiResponses.reviews.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
      expect(result.data).toHaveLength(2);
    });

    it('debe filtrar por fecha de actualización', async () => {
      const params = {
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc&updatedSince=2024-01-01T00%3A00%3A00Z')
        .reply(200, mockApiResponses.reviews.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al obtener reseñas');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al obtener reseñas');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al obtener reseñas');
    });
  });

  describe('Construcción de query parameters', () => {
    it('debe construir query string correctamente con todos los parámetros', () => {
      const params = {
        page: 2,
        size: 20,
        sortColumn: 'id' as const,
        sortDirection: 'desc' as const,
        search: 'test search',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockScope
        .get('/channel-management/channel/reviews?page=2&size=20&sortColumn=id&sortDirection=desc&search=test+search&updatedSince=2024-01-01T00%3A00%3A00Z')
        .reply(200, mockApiResponses.reviews.success);

      expect(() => tool.execute(params)).not.toThrow();
    });

    it('debe usar valores por defecto cuando no se proporcionan parámetros', () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(200, mockApiResponses.reviews.success);

      expect(() => tool.execute({})).not.toThrow();
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(200, mockApiResponses.reviews.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('data');
      expect(result).toHaveProperty('meta');
      expect(Array.isArray(result.data)).toBe(true);
      expect(result.meta).toHaveProperty('total');
      expect(result.meta).toHaveProperty('page');
      expect(result.meta).toHaveProperty('per_page');
    });

    it('debe validar estructura de elementos de reseña', async () => {
      mockScope
        .get('/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(200, mockApiResponses.reviews.success);

      const result = await tool.execute();

      if (result.data.length > 0) {
        const review = result.data[0];
        expect(review).toHaveProperty('id');
        expect(review).toHaveProperty('rating');
        expect(review).toHaveProperty('comment');
        expect(review).toHaveProperty('guest_name');
        expect(review).toHaveProperty('created_at');
      }
    });
  });
});
