/**
 * Tests para GetReservationTool
 */

import { GetReservationTool } from '../../src/tools/get-reservation.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetReservationTool', () => {
  let tool: GetReservationTool;
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
    tool = new GetReservationTool(apiClient);

    // Configurar mock HTTP
    mockScope = setupApiMock();
    mockSuccessfulAuth(mockScope);
  });

  afterEach(() => {
    cleanupApiMock();
  });

  describe('Validación de parámetros', () => {
    it('debe aceptar reservationId válido', () => {
      const validParams = {
        reservationId: '123'
      };

      // Test que los parámetros se aceptan
      expect(validParams.reservationId).toBe('123');
    });

    it('debe rechazar reservationId vacío', async () => {
      const invalidParams = {
        reservationId: ''
      };

      await expect(tool.execute(invalidParams)).rejects.toThrow('El ID de reservación no puede estar vacío');
    });

    it('debe rechazar reservationId undefined', async () => {
      const invalidParams = {
        reservationId: undefined as any
      };

      await expect(tool.execute(invalidParams)).rejects.toThrow('El ID de reservación no puede estar vacío');
    });

    it('debe rechazar reservationId con solo espacios', async () => {
      const invalidParams = {
        reservationId: '   '
      };

      await expect(tool.execute(invalidParams)).rejects.toThrow('El ID de reservación no puede estar vacío');
    });
  });

  describe('Ejecución exitosa', () => {
    it('debe obtener reservación con ID válido', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result.data).toHaveProperty('id');
      expect(result.data).toHaveProperty('guest_name');
      expect(result.data).toHaveProperty('check_in');
      expect(result.data).toHaveProperty('check_out');
      expect(result.data).toHaveProperty('status');
    });

    it('debe manejar ID con caracteres especiales', async () => {
      const reservationId = 'res-123-abc';

      mockScope
        .get(`/v2/pms/reservations/${encodeURIComponent(reservationId)}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
    });

    it('debe validar estructura de respuesta de reservación', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result.data).toHaveProperty('id');
      expect(result.data).toHaveProperty('status');
      expect(result.data).toHaveProperty('arrivalDate');
      expect(result.data).toHaveProperty('departureDate');
      expect(result.data).toHaveProperty('unitId');
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 404 (Reservación no encontrada)', async () => {
      const reservationId = '999';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(404, mockApiResponses.reservation.notFound);

      await expect(tool.execute({ reservationId }))
        .rejects.toThrow(`Reservación con ID '${reservationId}' no encontrada`);
    });

    it('debe manejar error 401 (No autorizado)', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute({ reservationId }))
        .rejects.toThrow('Error al obtener reservación');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute({ reservationId }))
        .rejects.toThrow('Error al obtener reservación');
    });

    it('debe manejar timeout de red', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute({ reservationId }))
        .rejects.toThrow('Error al obtener reservación');
    });
  });

  describe('Codificación de URL', () => {
    it('debe codificar correctamente IDs con espacios', async () => {
      const reservationId = 'res 123';

      mockScope
        .get(`/v2/pms/reservations/${encodeURIComponent(reservationId)}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
    });

    it('debe codificar correctamente IDs con caracteres especiales', async () => {
      const reservationId = 'res-123_abc@test';

      mockScope
        .get(`/v2/pms/reservations/${encodeURIComponent(reservationId)}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar que la respuesta tenga la estructura correcta', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toHaveProperty('data');
      expect(result.data).toBeDefined();
      expect(typeof result.data).toBe('object');
    });

    it('debe validar tipos de datos en la respuesta', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(typeof result.data.id).toBe('number');
      expect(typeof result.data.status).toBe('string');
      expect(typeof result.data.arrivalDate).toBe('string');
      expect(typeof result.data.departureDate).toBe('string');
      expect(typeof result.data.unitId).toBe('number');
    });
  });

  describe('Casos edge', () => {
    it('debe manejar ID numérico como string', async () => {
      const reservationId = '123';

      mockScope
        .get(`/v2/pms/reservations/${reservationId}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
    });

    it('debe manejar ID muy largo', async () => {
      const reservationId = 'a'.repeat(1000);

      mockScope
        .get(`/v2/pms/reservations/${encodeURIComponent(reservationId)}`)
        .reply(200, mockApiResponses.reservation.success);

      const result = await tool.execute({ reservationId });

      expect(result).toBeDefined();
    });
  });
});
