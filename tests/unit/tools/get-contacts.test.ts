/**
 * Tests unitarios para GetContactsTool
 */

import { GetContactsTool } from '../../../src/tools/get-contacts.js';
import { TrackHSApiClient } from '../../../src/core/api-client.js';
import { ContactsResponse, GetContactsParams } from '../../../src/types/contacts.js';

// Mock de TrackHSApiClient
jest.mock('../../../src/core/api-client.js');
const MockedTrackHSApiClient = TrackHSApiClient as jest.MockedClass<typeof TrackHSApiClient>;

describe('GetContactsTool', () => {
  let tool: GetContactsTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;

  beforeEach(() => {
    // Mock del cliente API
    mockApiClient = {
      get: jest.fn()
    } as any;

    MockedTrackHSApiClient.mockImplementation(() => mockApiClient);
    tool = new GetContactsTool(mockApiClient);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Constructor y propiedades', () => {
    it('debe inicializar correctamente', () => {
      expect(tool).toBeDefined();
      expect(tool.name).toBe('get_contacts');
      expect(tool.description).toBe('Retrieve all contacts from Track HS CRM system. Contacts include guests, owners, or vendor employees.');
    });

    it('debe tener schema de entrada correcto', () => {
      expect(tool.inputSchema).toEqual({
        type: 'object',
        properties: {
          sortColumn: { 
            type: 'string', 
            enum: ['id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip'],
            description: 'Sort by id, name, email, mobile phone, home phone, other phone, vip'
          },
          sortDirection: { 
            type: 'string', 
            enum: ['asc', 'desc'], 
            default: 'asc',
            description: 'Sort ascending or descending'
          },
          search: { 
            type: 'string', 
            description: 'Search by first name, last name, email, mobile phone, home phone, other phone with right side wildcard'
          },
          term: { 
            type: 'string', 
            description: 'Locate contact based on a precise value such as ID or name'
          },
          email: { 
            type: 'string', 
            format: 'email',
            description: 'Search contact by primary or secondary email address'
          },
          page: { 
            type: 'number', 
            description: 'Page Number',
            minimum: 1
          },
          size: { 
            type: 'number', 
            description: 'Page Size',
            minimum: 1,
            maximum: 100
          },
          updatedSince: { 
            type: 'string', 
            format: 'date-time', 
            description: 'Date in ISO 8601 format. Will return all contacts updated since timestamp'
          }
        },
        required: []
      });
    });
  });

  describe('execute method', () => {
    const mockResponse: ContactsResponse = {
      _embedded: {
        contacts: [
          {
            id: 101,
            firstName: 'Juan',
            lastName: 'Pérez',
            primaryEmail: 'juan@example.com',
            cellPhone: '+1234567890',
            isVip: false,
            isBlacklist: false,
            noIdentity: false,
            updatedAt: '2024-01-15T10:30:00Z',
            updatedBy: 'admin',
            createdAt: '2024-01-01T00:00:00Z',
            createdBy: 'system'
          },
          {
            id: 102,
            firstName: 'María',
            lastName: 'García',
            primaryEmail: 'maria@example.com',
            cellPhone: '+0987654321',
            isVip: true,
            isBlacklist: false,
            noIdentity: false,
            updatedAt: '2024-01-15T10:30:00Z',
            updatedBy: 'admin',
            createdAt: '2024-01-01T00:00:00Z',
            createdBy: 'system'
          }
        ]
      }
    };

    it('debe ejecutar con parámetros por defecto', async () => {
      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute();

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc');
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con parámetros de ordenamiento', async () => {
      const params: GetContactsParams = {
        sortColumn: 'name',
        sortDirection: 'desc'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortColumn=name&sortDirection=desc');
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con parámetros de búsqueda', async () => {
      const params: GetContactsParams = {
        search: 'Juan',
        term: 'Pérez',
        email: 'juan@example.com'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&search=Juan&term=P%C3%A9rez&email=juan%40example.com');
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con parámetros de paginación', async () => {
      const params: GetContactsParams = {
        page: 2,
        size: 20
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&page=2&size=20');
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con filtro de fecha', async () => {
      const params: GetContactsParams = {
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&updatedSince=2024-01-01T00%3A00%3A00Z');
      expect(result).toEqual(mockResponse);
    });

    it('debe ejecutar con todos los parámetros', async () => {
      const params: GetContactsParams = {
        sortColumn: 'email',
        sortDirection: 'desc',
        search: 'test search',
        term: 'precise term',
        email: 'test@example.com',
        page: 3,
        size: 50,
        updatedSince: '2024-01-01T00:00:00Z'
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortColumn=email&sortDirection=desc&search=test+search&term=precise+term&email=test%40example.com&page=3&size=50&updatedSince=2024-01-01T00%3A00%3A00Z');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error de API', async () => {
      const apiError = new Error('API Error');
      mockApiClient.get.mockRejectedValue(apiError);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener contactos: API Error');
    });

    it('debe manejar error desconocido', async () => {
      mockApiClient.get.mockRejectedValue('Unknown error');

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener contactos: Error desconocido');
    });

    it('debe manejar error de red', async () => {
      const networkError = new Error('Network timeout');
      mockApiClient.get.mockRejectedValue(networkError);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener contactos: Network timeout');
    });

    it('debe manejar error 401 (No autorizado)', async () => {
      const error401 = new Error('Track HS API Error: 401 Unauthorized');
      mockApiClient.get.mockRejectedValue(error401);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener contactos: Track HS API Error: 401 Unauthorized');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      const error500 = new Error('Track HS API Error: 500 Internal Server Error');
      mockApiClient.get.mockRejectedValue(error500);

      await expect(tool.execute())
        .rejects
        .toThrow('Error al obtener contactos: Track HS API Error: 500 Internal Server Error');
    });
  });

  describe('Validación de parámetros', () => {
    it('debe validar parámetros correctamente', async () => {
      const validParams: GetContactsParams = {
        sortColumn: 'name',
        sortDirection: 'asc',
        page: 1,
        size: 10
      };

      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await expect(tool.execute(validParams)).resolves.toBeDefined();
    });

    it('debe rechazar sortColumn inválido', async () => {
      const invalidParams = {
        sortColumn: 123 // Debe ser string
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'sortColumn\' debe ser string');
    });

    it('debe rechazar sortDirection inválido', async () => {
      const invalidParams = {
        sortDirection: 123 // Debe ser string
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'sortDirection\' debe ser string');
    });

    it('debe rechazar page inválido', async () => {
      const invalidParams = {
        page: 'invalid_page'
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'page\' debe ser number');
    });

    it('debe rechazar size inválido', async () => {
      const invalidParams = {
        size: 'invalid_size'
      };

      await expect(tool.execute(invalidParams as any))
        .rejects
        .toThrow('Parámetro \'size\' debe ser number');
    });
  });

  describe('Construcción de URL', () => {
    it('debe construir URL correctamente con parámetros mínimos', async () => {
      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await tool.execute();

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc');
    });

    it('debe construir URL correctamente con parámetros opcionales', async () => {
      const params: GetContactsParams = {
        search: 'test',
        email: 'test@example.com'
      };

      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&search=test&email=test%40example.com');
    });

    it('debe codificar caracteres especiales en URL', async () => {
      const params: GetContactsParams = {
        search: 'test & special chars @#$%',
        term: 'término con acentos'
      };

      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&search=test+%26+special+chars+%40%23%24%25&term=t%C3%A9rmino+con+acentos');
    });
  });

  describe('Casos edge', () => {
    it('debe manejar parámetros undefined', async () => {
      const params: GetContactsParams = {};

      mockApiClient.get.mockResolvedValue({ _embedded: { contacts: [] } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc');
    });

    it('debe manejar parámetros null', async () => {
      const params: GetContactsParams = {};

      mockApiClient.get.mockResolvedValue({ _embedded: { contacts: [] } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc');
    });

    it('debe manejar valores límite', async () => {
      const params: GetContactsParams = {
        page: 1,
        size: 100, // Máximo permitido
        sortDirection: 'desc'
      };

      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=desc&page=1&size=100');
    });

    it('debe manejar email con caracteres especiales', async () => {
      const params: GetContactsParams = {
        email: 'test+tag@example.com'
      };

      mockApiClient.get.mockResolvedValue({ data: [], pagination: { total: 0, page: 1, size: 10, total_pages: 0 } });

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith('/crm/contacts?sortDirection=asc&email=test%2Btag%40example.com');
    });
  });
});
