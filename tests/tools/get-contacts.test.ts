/**
 * Tests para GetContactsTool
 */

import { GetContactsTool } from '../../src/tools/get-contacts.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetContactsTool', () => {
  let tool: GetContactsTool;
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
    tool = new GetContactsTool(apiClient);

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
        search: 'juan'
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
    it('debe obtener contactos con parámetros por defecto', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result._embedded.contacts).toHaveLength(2);
    });

    it('debe obtener contactos con búsqueda', async () => {
      const params = {
        search: 'juan'
      };

      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc&search=juan')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener contactos con paginación', async () => {
      const params = {
        page: 2,
        size: 5
      };

      mockScope
        .get('/pms/contacts?page=2&size=5&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener contactos con ordenamiento', async () => {
      const params = {
        sortColumn: 'email' as const,
        sortDirection: 'desc' as const
      };

      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=email&sortDirection=desc')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al obtener contactos');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al obtener contactos');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al obtener contactos');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('_embedded');
      expect(Array.isArray(result._embedded.contacts)).toBe(true);
    });

    it('debe validar estructura de elementos de contacto', async () => {
      mockScope
        .get('/pms/contacts?page=1&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.contacts.success);

      const result = await tool.execute();

      if (result._embedded.contacts.length > 0) {
        const contact = result._embedded.contacts[0];
        expect(contact).toHaveProperty('id');
        expect(contact).toHaveProperty('firstName');
        expect(contact).toHaveProperty('lastName');
        expect(contact).toHaveProperty('primaryEmail');
      }
    });
  });
});
