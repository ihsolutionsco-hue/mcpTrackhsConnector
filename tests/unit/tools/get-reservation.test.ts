/**
 * Tests unitarios para GetReservationTool
 */

import { GetReservationTool } from '../../../src/tools/get-reservation.js';
import { TrackHSApiClient } from '../../../src/core/api-client.js';
import { ReservationResponse } from '../../../src/types/reservations.js';

// Mock de TrackHSApiClient
jest.mock('../../../src/core/api-client.js');
const MockedTrackHSApiClient = TrackHSApiClient as jest.MockedClass<typeof TrackHSApiClient>;

describe('GetReservationTool', () => {
  let tool: GetReservationTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;

  beforeEach(() => {
    // Mock del cliente API
    mockApiClient = {
      get: jest.fn()
    } as any;

    MockedTrackHSApiClient.mockImplementation(() => mockApiClient);
    tool = new GetReservationTool(mockApiClient);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Constructor y propiedades', () => {
    it('debe inicializar correctamente', () => {
      expect(tool).toBeDefined();
      expect(tool.name).toBe('get_reservation');
      expect(tool.description).toBe('Get detailed information for a specific reservation by ID');
    });

    it('debe tener schema de entrada correcto', () => {
      expect(tool.inputSchema).toEqual({
        type: 'object',
        properties: {
          reservationId: { 
            type: 'string', 
            description: 'The ID of the reservation to retrieve'
          }
        },
        required: ['reservationId']
      });
    });
  });

  describe('execute method', () => {
    const mockResponse: ReservationResponse = {
      data: {
        id: 123,
        alternates: [],
        currency: 'USD',
        unitId: 456,
        isUnitLocked: false,
        isUnitAssigned: true,
        isUnitTypeLocked: false,
        unitTypeId: 1,
        arrivalDate: '2024-02-01',
        departureDate: '2024-02-05',
        earlyArrival: false,
        lateDeparture: false,
        arrivalTime: '15:00',
        departureTime: '11:00',
        nights: 4,
        status: 'Confirmed',
        occupants: [],
        securityDeposit: {
          required: '100.00'
        },
        updatedAt: '2024-01-15T10:30:00Z',
        createdAt: '2024-01-01T00:00:00Z',
        bookedAt: '2024-01-01T00:00:00Z',
        guestBreakdown: {
          grossRent: '500.00',
          guestGrossDisplayRent: '500.00',
          discount: '0.00',
          promoValue: '0.00',
          discountTotal: 0,
          netRent: '500.00',
          guestNetDisplayRent: '500.00',
          actualAdr: '125.00',
          guestAdr: '125.00',
          totalGuestFees: '0.00',
          totalRentFees: '0.00',
          totalItemizedFees: '0.00',
          totalTaxFees: '0.00',
          totalServiceFees: '0.00',
          folioCharges: '0.00',
          subtotal: '500.00',
          guestSubtotal: '500.00',
          totalTaxes: '0.00',
          totalGuestTaxes: '0.00',
          total: '500.00',
          grandTotal: '500.00',
          netPayments: '0.00',
          payments: '0.00',
          refunds: '0.00',
          netTransfers: '0.00',
          balance: '500.00',
          rates: [],
          guestFees: [],
          taxes: []
        },
        type: {
          id: 1,
          name: 'Standard'
        },
        guaranteePolicy: {
          id: 1,
          name: 'Standard',
          type: 'Guarantee',
          hold: {
            limit: 24
          }
        },
        cancellationPolicy: {
          id: 1,
          name: 'Standard',
          time: '24:00',
          timezone: 'UTC',
          breakpoints: []
        },
        paymentPlan: [],
        rateType: {
          id: 1,
          name: 'Standard',
          code: 'STD'
        },
        travelInsuranceProducts: [],
        _embedded: {
          unit: {
            id: 456,
            name: 'Room 101',
            shortName: 'R101',
            unitCode: 'R101',
            shortDescription: 'Standard room',
            longDescription: 'Comfortable standard room',
            nodeId: 1,
            unitType: {
              id: 1,
              name: 'Standard'
            },
            lodgingType: {
              id: 1,
              name: 'Hotel'
            },
            timezone: 'UTC',
            checkinTime: '15:00',
            hasEarlyCheckin: false,
            checkoutTime: '11:00',
            hasLateCheckout: false,
            minBookingWindow: 0,
            maxBookingWindow: 365,
            streetAddress: '123 Main St',
            locality: 'City',
            region: 'State',
            postalCode: '12345',
            country: 'US',
            longitude: 0,
            latitude: 0,
            petsFriendly: false,
            maxPets: 0,
            eventsAllowed: false,
            smokingAllowed: false,
            childrenAllowed: true,
            isAccessible: false,
            maxOccupancy: 2,
            securityDeposit: '100.00',
            bedrooms: 1,
            fullBathrooms: 1,
            threeQuarterBathrooms: 0,
            halfBathrooms: 0,
            bedTypes: [],
            rooms: [],
            amenities: [],
            amenityDescription: '',
            coverImage: '',
            taxId: 1,
            localOffice: {
              name: 'Main Office',
              directions: 'Directions',
              email: 'office@hotel.com',
              phone: '+1234567890',
              latitude: '0',
              longitude: '0',
              streetAddress: '123 Main St',
              extendedAddress: '',
              locality: 'City',
              region: 'State',
              postalCode: '12345',
              country: 'US'
            },
            regulations: [],
            updated: {
              availability: '2024-01-15T10:30:00Z',
              content: '2024-01-15T10:30:00Z',
              pricing: '2024-01-15T10:30:00Z'
            },
            updatedAt: '2024-01-15T10:30:00Z',
            createdAt: '2024-01-01T00:00:00Z',
            isActive: true,
            _links: {
              self: {
                href: '/units/456'
              }
            }
          },
          contact: {
            id: 1,
            firstName: 'Ana',
            lastName: 'López',
            name: 'Ana López',
            primaryEmail: 'ana@example.com',
            country: 'US',
            tags: [],
            references: [],
            custom: {},
            updatedBy: 'admin',
            createdBy: 'system',
            updatedAt: '2024-01-15T10:30:00Z',
            createdAt: '2024-01-01T00:00:00Z',
            isOwnerContact: false,
            _links: {
              self: {
                href: '/contacts/1'
              }
            }
          }
        },
        _links: {
          self: {
            href: '/reservations/123'
          },
          cancel: {
            href: '/reservations/123/cancel'
          }
        }
      },
      success: true
    };

    it('debe ejecutar con ID válido', async () => {
      const params = { reservationId: '123' };
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/123');
      expect(result).toEqual(mockResponse);
    });

    it('debe codificar ID en URL correctamente', async () => {
      const params = { reservationId: 'res-123/456' };
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/res-123%2F456');
      expect(result).toEqual(mockResponse);
    });

    it('debe manejar ID con caracteres especiales', async () => {
      const params = { reservationId: 'res-123 & special' };
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/res-123%20%26%20special');
      expect(result).toEqual(mockResponse);
    });

    it('debe manejar ID numérico como string', async () => {
      const params = { reservationId: '12345' };
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/12345');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Validación de parámetros', () => {
    it('debe validar parámetros requeridos', async () => {
      const validParams = { reservationId: '123' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await expect(tool.execute(validParams)).resolves.toBeDefined();
    });

    it('debe rechazar parámetros faltantes', async () => {
      const invalidParams = {};

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro requerido faltante: reservationId');
    });

    it('debe rechazar ID vacío', async () => {
      const params = { reservationId: '' };

      await expect(tool.execute(params))
        .rejects
        .toThrow('El ID de reservación no puede estar vacío');
    });

    it('debe rechazar ID con solo espacios', async () => {
      const params = { reservationId: '   ' };

      await expect(tool.execute(params))
        .rejects
        .toThrow('El ID de reservación no puede estar vacío');
    });

    it('debe rechazar ID undefined', async () => {
      const params = { reservationId: undefined as any };

      await expect(tool.execute(params))
        .rejects
        .toThrow('El ID de reservación no puede estar vacío');
    });

    it('debe rechazar ID null', async () => {
      const params = { reservationId: null as any };

      await expect(tool.execute(params))
        .rejects
        .toThrow('Parámetro \'reservationId\' debe ser string');
    });

    it('debe rechazar tipo de dato incorrecto', async () => {
      const params = { reservationId: 123 as any };

      await expect(tool.execute(params))
        .rejects
        .toThrow('Parámetro \'reservationId\' debe ser string');
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 404 específicamente', async () => {
      const params = { reservationId: 'nonexistent' };
      const error404 = new Error('Track HS API Error: 404 Not Found');
      mockApiClient.get.mockRejectedValue(error404);

      await expect(tool.execute(params))
        .rejects
        .toThrow('Reservación con ID \'nonexistent\' no encontrada');
    });

    it('debe manejar otros errores de API', async () => {
      const params = { reservationId: '123' };
      const apiError = new Error('Track HS API Error: 500 Internal Server Error');
      mockApiClient.get.mockRejectedValue(apiError);

      await expect(tool.execute(params))
        .rejects
        .toThrow('Error al obtener reservación: Track HS API Error: 500 Internal Server Error');
    });

    it('debe manejar error de red', async () => {
      const params = { reservationId: '123' };
      const networkError = new Error('Network timeout');
      mockApiClient.get.mockRejectedValue(networkError);

      await expect(tool.execute(params))
        .rejects
        .toThrow('Error al obtener reservación: Network timeout');
    });

    it('debe manejar error desconocido', async () => {
      const params = { reservationId: '123' };
      mockApiClient.get.mockRejectedValue('Unknown error');

      await expect(tool.execute(params))
        .rejects
        .toThrow('Error al obtener reservación: Error desconocido');
    });

    it('debe manejar error 401 (No autorizado)', async () => {
      const params = { reservationId: '123' };
      const error401 = new Error('Track HS API Error: 401 Unauthorized');
      mockApiClient.get.mockRejectedValue(error401);

      await expect(tool.execute(params))
        .rejects
        .toThrow('Error al obtener reservación: Track HS API Error: 401 Unauthorized');
    });

    it('debe manejar error 403 (Prohibido)', async () => {
      const params = { reservationId: '123' };
      const error403 = new Error('Track HS API Error: 403 Forbidden');
      mockApiClient.get.mockRejectedValue(error403);

      await expect(tool.execute(params))
        .rejects
        .toThrow('Error al obtener reservación: Track HS API Error: 403 Forbidden');
    });
  });

  describe('Construcción de endpoint', () => {
    it('debe construir endpoint correctamente', async () => {
      const params = { reservationId: 'test-id' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/test-id');
    });

    it('debe manejar IDs con caracteres especiales en endpoint', async () => {
      const params = { reservationId: 'id with spaces & symbols' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/id%20with%20spaces%20%26%20symbols');
    });

    it('debe manejar IDs con barras', async () => {
      const params = { reservationId: 'res/123/456' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/res%2F123%2F456');
    });
  });

  describe('Casos edge', () => {
    it('debe manejar ID muy largo', async () => {
      const longId = 'a'.repeat(1000);
      const params = { reservationId: longId };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(`/v2/pms/reservations/${encodeURIComponent(longId)}`);
    });

    it('debe manejar ID con caracteres Unicode', async () => {
      const params = { reservationId: 'res-123-ñáéíóú' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/res-123-%C3%B1%C3%A1%C3%A9%C3%AD%C3%B3%C3%BA');
    });

    it('debe manejar ID con números y letras', async () => {
      const params = { reservationId: 'RES-2024-001' };
      mockApiClient.get.mockResolvedValue({ data: {} });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/v2/pms/reservations/RES-2024-001');
    });
  });
});
