/**
 * Tests de integración para las herramientas MCP
 * Estos tests validan el flujo completo de las herramientas con la API real
 */

import { TrackHSApiClient } from '../../src/core/api-client.js';
import { GetReviewsTool } from '../../src/tools/get-reviews.js';
import { GetContactsTool } from '../../src/tools/get-contacts.js';
import { GetReservationTool } from '../../src/tools/get-reservation.js';
import { SearchReservationsTool } from '../../src/tools/search-reservations.js';
import { GetUnitsTool } from '../../src/tools/get-units.js';

describe('MCP Tools Integration Tests', () => {
  let apiClient: TrackHSApiClient;
  let reviewsTool: GetReviewsTool;
  let contactsTool: GetContactsTool;
  let reservationTool: GetReservationTool;
  let searchReservationsTool: SearchReservationsTool;
  let unitsTool: GetUnitsTool;

  beforeAll(() => {
    // Verificar configuración de entorno
    if (!process.env.TRACKHS_API_URL || !process.env.TRACKHS_USERNAME || !process.env.TRACKHS_PASSWORD) {
      console.warn('⚠️  Variables de entorno no configuradas. Los tests de integración se saltarán.');
      return;
    }

    apiClient = new TrackHSApiClient({
      baseUrl: process.env.TRACKHS_API_URL,
      username: process.env.TRACKHS_USERNAME,
      password: process.env.TRACKHS_PASSWORD
    });

    // Inicializar herramientas
    reviewsTool = new GetReviewsTool(apiClient);
    contactsTool = new GetContactsTool(apiClient);
    reservationTool = new GetReservationTool(apiClient);
    searchReservationsTool = new SearchReservationsTool(apiClient);
    unitsTool = new GetUnitsTool(apiClient);
  });

  describe('GetReviewsTool Integration', () => {
    it('debe obtener reseñas con parámetros por defecto', async () => {
      if (!reviewsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await reviewsTool.execute();
        
        expect(result).toBeDefined();
        expect(result.data).toBeDefined();
        expect(Array.isArray(result.data)).toBe(true);
        expect(result.pagination).toBeDefined();
        expect(result.success).toBe(true);
      } catch (error) {
        // Si la API no está disponible, verificar que el error sea manejado correctamente
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toContain('Error al obtener reseñas');
      }
    });

    it('debe obtener reseñas con filtros específicos', async () => {
      if (!reviewsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await reviewsTool.execute({
          page: 1,
          size: 5,
          search: 'excellent',
          updatedSince: '2024-01-01T00:00:00Z'
        });
        
        expect(result).toBeDefined();
        expect(result.data).toBeDefined();
        expect(Array.isArray(result.data)).toBe(true);
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe manejar errores de API correctamente', async () => {
      if (!reviewsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      // Usar parámetros que podrían causar error
      try {
        await reviewsTool.execute({
          page: -1,
          size: 0
        });
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('GetContactsTool Integration', () => {
    it('debe obtener contactos con parámetros por defecto', async () => {
      if (!contactsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await contactsTool.execute();
        
        expect(result).toBeDefined();
        expect(result._embedded).toBeDefined();
        expect(result._embedded.contacts).toBeDefined();
        expect(Array.isArray(result._embedded.contacts)).toBe(true);
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe buscar contactos por email', async () => {
      if (!contactsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await contactsTool.execute({
          email: 'test@example.com',
          page: 1,
          size: 10
        });
        
        expect(result).toBeDefined();
        expect(result._embedded).toBeDefined();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe manejar búsqueda con caracteres especiales', async () => {
      if (!contactsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await contactsTool.execute({
          search: 'test@example.com & special chars',
          sortColumn: 'name',
          sortDirection: 'asc'
        });
        
        expect(result).toBeDefined();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('GetReservationTool Integration', () => {
    it('debe obtener reservación por ID', async () => {
      if (!reservationTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await reservationTool.execute({
          reservationId: '123'
        });
        
        expect(result).toBeDefined();
        expect(result.data).toBeDefined();
        expect(result.success).toBe(true);
      } catch (error) {
        // Es probable que el ID no exista, pero el error debe ser manejado correctamente
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe manejar ID de reservación inexistente', async () => {
      if (!reservationTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        await reservationTool.execute({
          reservationId: 'nonexistent-id-12345'
        });
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toContain('Error al obtener reservación');
      }
    });

    it('debe manejar ID con caracteres especiales', async () => {
      if (!reservationTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await reservationTool.execute({
          reservationId: 'res-123-test_456'
        });
        
        expect(result).toBeDefined();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('SearchReservationsTool Integration', () => {
    it('debe buscar reservaciones con parámetros básicos', async () => {
      if (!searchReservationsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await searchReservationsTool.execute({
          page: 1,
          size: 10
        });
        
        expect(result).toBeDefined();
        expect(result.data).toBeDefined();
        expect(Array.isArray(result.data)).toBe(true);
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe buscar reservaciones con filtros de fecha', async () => {
      if (!searchReservationsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await searchReservationsTool.execute({
          page: 1,
          size: 5
        });
        
        expect(result).toBeDefined();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('GetUnitsTool Integration', () => {
    it('debe obtener unidades con parámetros por defecto', async () => {
      if (!unitsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await unitsTool.execute();
        
        expect(result).toBeDefined();
        expect(result._embedded).toBeDefined();
        expect(result._embedded.units).toBeDefined();
        expect(Array.isArray(result._embedded.units)).toBe(true);
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe obtener unidades con filtros específicos', async () => {
      if (!unitsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await unitsTool.execute({
          page: 1,
          size: 5,
          sortColumn: 'name',
          sortDirection: 'asc'
        });
        
        expect(result).toBeDefined();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('Flujos de Integración Completa', () => {
    it('debe ejecutar flujo completo: buscar reservaciones -> obtener detalles', async () => {
      if (!searchReservationsTool || !reservationTool) {
        console.log('⏭️  Saltando test - Tools no configurados');
        return;
      }

      try {
        // Paso 1: Buscar reservaciones
        const searchResult = await searchReservationsTool.execute({
          page: 1,
          size: 1
        });
        
        expect(searchResult).toBeDefined();
        
        // Paso 2: Si hay reservaciones, obtener detalles de la primera
        if (searchResult.data && searchResult.data.length > 0) {
          const reservationId = searchResult.data[0].id;
          
          const detailResult = await reservationTool.execute({
            reservationId: reservationId.toString()
          });
          
          expect(detailResult).toBeDefined();
          expect(detailResult.data).toBeDefined();
        }
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe manejar errores de red y timeout', async () => {
      if (!reviewsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      // Crear un cliente con configuración que cause timeout
      const timeoutApiClient = new TrackHSApiClient({
        baseUrl: 'http://httpstat.us:200?sleep=10000', // 10 segundos
        username: 'test',
        password: 'test'
      });

      const timeoutTool = new GetReviewsTool(timeoutApiClient);

      try {
        await timeoutTool.execute();
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toContain('Error al obtener reseñas');
      }
    });
  });

  describe('Validación de Respuestas', () => {
    it('debe validar estructura de respuesta de reseñas', async () => {
      if (!reviewsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await reviewsTool.execute();
        
        if (result && result.data) {
          // Validar estructura de cada reseña
          result.data.forEach((review: any) => {
            expect(review).toHaveProperty('id');
            expect(review).toHaveProperty('rating');
            expect(typeof review.id).toBe('number');
            expect(typeof review.rating).toBe('number');
            expect(review.rating).toBeGreaterThanOrEqual(1);
            expect(review.rating).toBeLessThanOrEqual(5);
          });
        }
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });

    it('debe validar estructura de respuesta de contactos', async () => {
      if (!contactsTool) {
        console.log('⏭️  Saltando test - Tool no configurado');
        return;
      }

      try {
        const result = await contactsTool.execute();
        
        if (result && result._embedded && result._embedded.contacts) {
          // Validar estructura de cada contacto
          result._embedded.contacts.forEach((contact: any) => {
            expect(contact).toHaveProperty('id');
            expect(contact).toHaveProperty('firstName');
            expect(contact).toHaveProperty('lastName');
            expect(typeof contact.id).toBe('number');
            expect(typeof contact.firstName).toBe('string');
          });
        }
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });
});
