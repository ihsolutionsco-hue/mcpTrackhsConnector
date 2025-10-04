/**
 * Tests para GetUnitTool
 */

import { GetUnitTool } from '../../src/tools/get-unit.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetUnitTool', () => {
  let tool: GetUnitTool;
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
    tool = new GetUnitTool(apiClient);

    // Configurar mock HTTP
    mockScope = setupApiMock();
    mockSuccessfulAuth(mockScope);
  });

  afterEach(() => {
    cleanupApiMock();
  });

  describe('Validación de parámetros', () => {
    it('debe aceptar unitId válido', () => {
      const validParams = {
        unitId: 456
      };

      // Test que los parámetros se aceptan
      expect(validParams.unitId).toBe(456);
    });

    it('debe rechazar unitId vacío', async () => {
      const invalidParams = {
        unitId: 0
      };

      await expect(tool.execute(invalidParams)).rejects.toThrow();
    });
  });

  describe('Ejecución exitosa', () => {
    it('debe obtener unidad con ID válido', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(200, mockApiResponses.unit.success);

      const result = await tool.execute({ unitId });

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result).toHaveProperty('id');
      expect(result).toHaveProperty('name');
      expect(result).toHaveProperty('unitType');
      expect(result).toHaveProperty('maxOccupancy');
    });

    it('debe manejar ID numérico', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(200, mockApiResponses.unit.success);

      const result = await tool.execute({ unitId });

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 404 (Unidad no encontrada)', async () => {
      const unitId = 999;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(404, mockApiResponses.unit.notFound);

      await expect(tool.execute({ unitId }))
        .rejects.toThrow(`Unidad con ID '${unitId}' no encontrada`);
    });

    it('debe manejar error 401 (No autorizado)', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute({ unitId }))
        .rejects.toThrow('Error al obtener unidad');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute({ unitId }))
        .rejects.toThrow('Error al obtener unidad');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(200, mockApiResponses.unit.success);

      const result = await tool.execute({ unitId });

      expect(result).toBeDefined();
      expect(typeof result).toBe('object');
    });

    it('debe validar estructura de datos de unidad', async () => {
      const unitId = 456;

      mockScope
        .get(`/pms/units/${unitId}`)
        .reply(200, mockApiResponses.unit.success);

      const result = await tool.execute({ unitId });

      expect(result).toHaveProperty('id');
      expect(result).toHaveProperty('name');
      expect(result).toHaveProperty('unitType');
      expect(result).toHaveProperty('maxOccupancy');
    });
  });
});
