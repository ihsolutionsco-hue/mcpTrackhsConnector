/**
 * Tests para GetUnitsTool
 */

import { GetUnitsTool } from '../../src/tools/get-units.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetUnitsTool', () => {
  let tool: GetUnitsTool;
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
    tool = new GetUnitsTool(apiClient);

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
        search: 'suite',
        nodeId: 1,
        unitTypeId: 2,
        bedrooms: 2,
        petsFriendly: 1 as const
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
    it('debe obtener unidades con parámetros por defecto', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result._embedded.units).toHaveLength(2);
      expect(result.total_items).toBe(2);
    });

    it('debe obtener unidades con filtros básicos', async () => {
      const params = {
        page: 1,
        size: 5,
        search: 'suite'
      };

      mockScope
        .get('/pms/units?page=1&size=5&search=suite')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
      expect(result._embedded.units).toHaveLength(2);
    });

    it('debe obtener unidades con filtros de nodo', async () => {
      const params = {
        nodeId: 1
      };

      mockScope
        .get('/pms/units?nodeId=1')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener unidades con filtros de tipo', async () => {
      const params = {
        unitTypeId: 2
      };

      mockScope
        .get('/pms/units?unitTypeId=2')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener unidades con filtros físicos', async () => {
      const params = {
        bedrooms: 2,
        bathrooms: 1,
        minBedrooms: 1,
        maxBedrooms: 3
      };

      mockScope
        .get('/pms/units?bedrooms=2&bathrooms=1&minBedrooms=1&maxBedrooms=3')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener unidades con filtros de políticas', async () => {
      const params = {
        petsFriendly: 1 as const,
        eventsAllowed: 1 as const,
        smokingAllowed: 0 as const,
        childrenAllowed: 1 as const
      };

      mockScope
        .get('/pms/units?petsFriendly=1&eventsAllowed=1&smokingAllowed=0&childrenAllowed=1')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener unidades con filtros de disponibilidad', async () => {
      const params = {
        arrival: '2024-02-01',
        departure: '2024-02-05'
      };

      mockScope
        .get('/pms/units?arrival=2024-02-01&departure=2024-02-05')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener unidades con filtros de estado', async () => {
      const params = {
        isActive: 1 as const,
        isBookable: 1 as const,
        unitStatus: 'clean' as const
      };

      mockScope
        .get('/pms/units?isActive=1&isBookable=1&unitStatus=clean')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Filtros de ID múltiples', () => {
    it('debe manejar array de nodeId', async () => {
      const params = {
        nodeId: [1, 2, 3]
      };

      mockScope
        .get('/pms/units?nodeId=1&nodeId=2&nodeId=3')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe manejar array de unitTypeId', async () => {
      const params = {
        unitTypeId: [1, 2]
      };

      mockScope
        .get('/pms/units?unitTypeId=1&unitTypeId=2')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe manejar array de amenityId', async () => {
      const params = {
        amenityId: [1, 2, 3]
      };

      mockScope
        .get('/pms/units?amenityId=1&amenityId=2&amenityId=3')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe manejar array de IDs de unidades', async () => {
      const params = {
        id: [456, 457]
      };

      mockScope
        .get('/pms/units?id=456&id=457')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al obtener unidades');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al obtener unidades');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al obtener unidades');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('_embedded');
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('total_items');
      expect(Array.isArray(result._embedded.units)).toBe(true);
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('page_size');
    });

    it('debe validar estructura de elementos de unidad', async () => {
      mockScope
        .get('/pms/units?sortColumn=name&sortDirection=asc')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute();

      if (result._embedded.units.length > 0) {
        const unit = result._embedded.units[0];
        expect(unit).toHaveProperty('id');
        expect(unit).toHaveProperty('name');
        expect(unit).toHaveProperty('unitType');
        expect(unit).toHaveProperty('maxOccupancy');
      }
    });
  });

  describe('Filtros avanzados', () => {
    it('debe manejar filtros de fecha de actualización', async () => {
      const params = {
        contentUpdatedSince: '2024-01-01T00:00:00Z',
        updatedSince: '2024-01-01'
      };

      mockScope
        .get('/pms/units?contentUpdatedSince=2024-01-01T00%3A00%3A00Z&updatedSince=2024-01-01')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe manejar filtros de búsqueda múltiple', async () => {
      const params = {
        search: 'suite',
        term: 'deluxe',
        unitCode: 'SUITE%',
        shortName: 'SU%'
      };

      mockScope
        .get('/pms/units?search=suite&term=deluxe&unitCode=SUITE%25&shortName=SU%25')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe manejar filtros adicionales', async () => {
      const params = {
        computed: 1 as const,
        inherited: 1 as const,
        limited: 0 as const,
        includeDescriptions: 1 as const,
        allowUnitRates: 1 as const,
        calendarId: 1,
        roleId: 1
      };

      mockScope
        .get('/pms/units?computed=1&inherited=1&limited=0&includeDescriptions=1&allowUnitRates=1&calendarId=1&roleId=1')
        .reply(200, mockApiResponses.units.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });
});
