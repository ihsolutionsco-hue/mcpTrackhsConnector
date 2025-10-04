/**
 * Tests unitarios para GetReviewsTool
 */

import { GetReviewsTool } from '../../../src/tools/get-reviews.js';
import { TrackHSApiClient } from '../../../src/core/api-client.js';
import { ReviewsResponse, GetReviewsParams } from '../../../src/types/reviews.js';

// Mock de TrackHSApiClient
jest.mock('../../../src/core/api-client.js');
const MockedTrackHSApiClient = TrackHSApiClient as jest.MockedClass<typeof TrackHSApiClient>;

describe('GetReviewsTool', () => {
  let tool: GetReviewsTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;
  let mockResponse: ReviewsResponse;

  beforeEach(() => {
    // Mock del cliente API
    mockApiClient = {
      get: jest.fn()
    } as any;

    MockedTrackHSApiClient.mockImplementation(() => mockApiClient);
    tool = new GetReviewsTool(mockApiClient);

    // Mock response común
    mockResponse = {
      data: [
        {
          id: 1,
          reviewId: 'REV-001',
          publicReview: 'Excelente servicio',
          rating: 5,
          guestName: 'Juan Pérez',
          guestEmail: 'juan@example.com',
          propertyId: 'PROP-001',
          propertyName: 'Hotel Test',
          channel: 'Booking.com',
          createdAt: '2024-01-15T10:30:00Z',
          updatedAt: '2024-01-15T10:30:00Z',
          status: 'published'
        }
      ],
      pagination: {
        total: 1,
        page: 1,
        size: 10,
        totalPages: 1,
        hasNext: false,
        hasPrevious: false
      },
      success: true
    };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Constructor y propiedades', () => {
    it('debe inicializar correctamente', () => {
      expect(tool).toBeDefined();
      expect(tool.name).toBe('get_reviews');
      expect(tool.description).toBe('Retrieve paginated collection of property reviews from Track HS');
    });

    it('debe tener schema de entrada correcto', () => {
      expect(tool.inputSchema).toEqual({
        type: 'object',
        properties: {
          page: { 
            type: 'number', 
            description: 'Page Number (default: 1)',
            minimum: 1
          },
          size: { 
            type: 'number', 
            description: 'Page Size (default: 10, max: 100)',
            minimum: 1,
            maximum: 100
          },
          sortColumn: { 
            type: 'string', 
            enum: ['id'], 
            default: 'id',
            description: 'Column to sort by'
          },
          sortDirection: { 
            type: 'string', 
            enum: ['asc', 'desc'], 
            default: 'asc',
            description: 'Sort direction'
          },
          search: { 
            type: 'string', 
            description: 'Search by reviewId and publicReview content'
          },
          updatedSince: { 
            type: 'string', 
            format: 'date-time', 
            description: 'Filter reviews updated since this date (ISO 8601 format)'
          }
        },
        required: []
      });
    });
  });

  describe('execute method', () => {

    it('debe ejecutar con parámetros por defecto', async () => {
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute();

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc'
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con parámetros personalizados', async () => {
      const params: GetReviewsParams = {
        page: 2,
        size: 5,
        sortColumn: 'id',
        sortDirection: 'desc',
        search: 'excelente'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=2&size=5&sortColumn=id&sortDirection=desc&search=excelente'
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con filtro de fecha', async () => {
      const params: GetReviewsParams = {
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc&updatedSince=2024-01-01T00%3A00%3A00Z'
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con todos los parámetros', async () => {
      const params: GetReviewsParams = {
        page: 3,
        size: 20,
        sortColumn: 'id',
        sortDirection: 'desc',
        search: 'test search',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=3&size=20&sortColumn=id&sortDirection=desc&search=test+search&updatedSince=2024-01-01T00%3A00%3A00Z'
      );
      expect(result).toEqual(mockResponse);
    });

    it('debe manejar parámetros con caracteres especiales', async () => {
      const params: GetReviewsParams = {
        search: 'test & special chars'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc&search=test+%26+special+chars'
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error de API', async () => {
      const apiError = new Error('API Error');
      mockApiClient.get.mockRejectedValue(apiError);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener reseñas: API Error');
    });

    it('debe manejar error desconocido', async () => {
      mockApiClient.get.mockRejectedValue('Unknown error');

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener reseñas: Error desconocido');
    });

    it('debe manejar error de red', async () => {
      const networkError = new Error('Network timeout');
      mockApiClient.get.mockRejectedValue(networkError);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener reseñas: Network timeout');
    });
  });

  describe('Validación de parámetros', () => {
    it('debe validar parámetros correctamente', async () => {
      const validParams: GetReviewsParams = {
        page: 1,
        size: 10,
        sortColumn: 'id',
        sortDirection: 'asc'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await expect(tool.execute(validParams)).resolves.toBeDefined();
    });

    it('debe rechazar parámetros inválidos', async () => {
      const invalidParams = {
        page: 'invalid', // Debe ser number
        size: 'invalid'  // Debe ser number
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'page\' debe ser number');
    });

    it('debe rechazar sortDirection inválido', async () => {
      const invalidParams = {
        sortDirection: 123 // Debe ser string
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'sortDirection\' debe ser string');
    });
  });

  describe('Construcción de URL', () => {
    it('debe construir URL correctamente con parámetros mínimos', async () => {
      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute();

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc'
      );
    });

    it('debe construir URL correctamente con parámetros opcionales', async () => {
      const params: GetReviewsParams = {
        search: 'test',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc&search=test&updatedSince=2024-01-01T00%3A00%3A00Z'
      );
    });

    it('debe codificar caracteres especiales en URL', async () => {
      const params: GetReviewsParams = {
        search: 'test & special chars @#$%'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc&search=test+%26+special+chars+%40%23%24%25'
      );
    });
  });

  describe('Casos edge', () => {
    it('debe manejar parámetros undefined', async () => {
      const params: GetReviewsParams = {};

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc'
      );
    });

    it('debe manejar parámetros null', async () => {
      const params: GetReviewsParams = {};

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=10&sortColumn=id&sortDirection=asc'
      );
    });

    it('debe manejar valores límite', async () => {
      const params: GetReviewsParams = {
        page: 1,
        size: 100, // Máximo permitido
        sortDirection: 'desc'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/channel-management/channel/reviews?page=1&size=100&sortColumn=id&sortDirection=desc'
      );
    });
  });
});
