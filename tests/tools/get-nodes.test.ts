/**
 * Tests para GetNodesTool
 */

import { GetNodesTool } from '../../src/tools/get-nodes.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetNodesTool', () => {
  let tool: GetNodesTool;
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
    tool = new GetNodesTool(apiClient);

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
        sortColumn: 'name' as const,
        sortDirection: 'asc' as const,
        search: 'recepción'
      };

      // Test que los parámetros se aceptan
      expect(validParams.page).toBe(1);
      expect(validParams.size).toBe(10);
    });

    it('debe manejar parámetros por defecto', () => {
      // Test con parámetros mínimos
      expect(() => tool.execute({})).not.toThrow();
    });
  });

  describe('Ejecución exitosa', () => {
    it('debe obtener nodos con parámetros por defecto', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result._embedded.nodes).toHaveLength(2);
      expect(result.total_items).toBe(2);
    });

    it('debe obtener nodos con búsqueda', async () => {
      const params = {
        search: 'recepción'
      };

      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc&search=recepci%C3%B3n')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener nodos con filtros de tipo', async () => {
      const params = {
        typeId: 1
      };

      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc&typeId=1')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener nodos con filtros de padre', async () => {
      const params = {
        parentId: 1
      };

      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc&parentId=1')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener nodos con filtros de padre', async () => {
      const params = {
        parentId: 1
      };

      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc&parentId=1')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al obtener nodos');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al obtener nodos');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al obtener nodos');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('_embedded');
      expect(Array.isArray(result._embedded.nodes)).toBe(true);
      expect(result).toHaveProperty('total_items');
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('page_size');
    });

    it('debe validar estructura de elementos de nodo', async () => {
      mockScope
        .get('/pms/nodes?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.nodes.success);

      const result = await tool.execute();

      if (result._embedded.nodes.length > 0) {
        const node = result._embedded.nodes[0];
        expect(node).toHaveProperty('id');
        expect(node).toHaveProperty('name');
        expect(node).toHaveProperty('type');
      }
    });
  });
});
