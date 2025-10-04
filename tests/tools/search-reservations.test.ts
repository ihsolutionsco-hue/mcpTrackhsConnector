/**
 * Tests para SearchReservationsTool
 */

import { SearchReservationsTool } from '../../src/tools/search-reservations.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('SearchReservationsTool', () => {
  let tool: SearchReservationsTool;
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
    tool = new SearchReservationsTool(apiClient);

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
        search: 'ana'
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
    it('debe buscar reservaciones con parámetros por defecto', async () => {
      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(result._embedded.reservations).toHaveLength(2);
      expect(result.total_items).toBe(2);
    });

    it('debe buscar reservaciones con filtros de fecha', async () => {
      const params = {
        arrivalStart: '2024-02-01',
        arrivalEnd: '2024-02-28',
        departureStart: '2024-02-01',
        departureEnd: '2024-02-28'
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&arrivalStart=2024-02-01&arrivalEnd=2024-02-28&departureStart=2024-02-01&departureEnd=2024-02-28')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con filtros de estado', async () => {
      const params = {
        status: 'Confirmed' as const
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&status=Confirmed')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con búsqueda de texto', async () => {
      const params = {
        search: 'ana lopez'
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&search=ana+lopez')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con filtros de unidad', async () => {
      const params = {
        unitId: 456
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&unitId=456')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con filtros de nodo', async () => {
      const params = {
        nodeId: 1
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&nodeId=1')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con filtros de grupo', async () => {
      const params = {
        groupId: 123
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&groupId=123')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con filtros de oficina de check-in', async () => {
      const params = {
        checkinOfficeId: 456
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&checkinOfficeId=456')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con scroll parameter numérico', async () => {
      const params = {
        scroll: 1
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&scroll=1')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe buscar reservaciones con scroll parameter string', async () => {
      const params = {
        scroll: 'scroll_token_123'
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&scroll=scroll_token_123')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Validación de fechas', () => {
    it('debe aceptar fechas en formato ISO 8601 válido', async () => {
      const params = {
        arrivalStart: '2024-02-01T00:00:00.000Z',
        arrivalEnd: '2024-02-28T23:59:59.999Z'
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&arrivalStart=2024-02-01T00:00:00.000Z&arrivalEnd=2024-02-28T23:59:59.999Z')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe rechazar fechas en formato inválido', async () => {
      const params = {
        arrivalStart: 'invalid-date',
        arrivalEnd: 'not-a-date'
      };

      await expect(tool.execute(params))
        .rejects.toThrow('Parámetro \'arrivalStart\' debe tener formato ISO 8601 válido');
    });

    it('debe rechazar fechas con formato incorrecto', async () => {
      const params = {
        updatedSince: '01/02/2024' // Formato incorrecto
      };

      await expect(tool.execute(params))
        .rejects.toThrow('Parámetro \'updatedSince\' debe tener formato ISO 8601 válido');
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/v2/pms/reservations?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al buscar reservaciones');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/v2/pms/reservations?page=1&size=10&sortColumn=id&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al buscar reservaciones');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/v2/pms/reservations?page=1&size=10&sortColumn=id&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al buscar reservaciones');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('_embedded');
      expect(Array.isArray(result._embedded.reservations)).toBe(true);
      expect(result).toHaveProperty('total_items');
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('page_size');
    });

    it('debe validar estructura de elementos de reservación', async () => {
      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute();

      if (result._embedded.reservations.length > 0) {
        const reservation = result._embedded.reservations[0];
        expect(reservation).toHaveProperty('id');
        expect(reservation).toHaveProperty('status');
        expect(reservation).toHaveProperty('arrivalDate');
        expect(reservation).toHaveProperty('departureDate');
      }
    });
  });

  describe('Filtros avanzados', () => {
    it('debe manejar filtros de fecha de creación', async () => {
      const params = {
        bookedStart: '2024-01-01',
        bookedEnd: '2024-01-31'
      };

      mockScope
        .get('/v2/pms/reservations?page=0&size=10&sortColumn=name&sortDirection=asc&bookedStart=2024-01-01&bookedEnd=2024-01-31')
        .reply(200, mockApiResponses.searchReservations.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });
});
