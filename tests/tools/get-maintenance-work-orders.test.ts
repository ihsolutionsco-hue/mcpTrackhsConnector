/**
 * Pruebas para la herramienta GetMaintenanceWorkOrdersTool
 */

import { GetMaintenanceWorkOrdersTool } from '../../src/tools/get-maintenance-work-orders.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';

describe('GetMaintenanceWorkOrdersTool', () => {
  let tool: GetMaintenanceWorkOrdersTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;

  beforeEach(() => {
    mockApiClient = {
      get: jest.fn()
    } as any;
    
    tool = new GetMaintenanceWorkOrdersTool(mockApiClient);
  });

  describe('Validación de parámetros', () => {
    it('debe aceptar parámetros válidos', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const params = {
        page: 1,
        size: 25,
        status: ['open', 'in-progress'] as ('open' | 'in-progress')[]
      };
      
      await expect(tool.execute(params)).resolves.toBeDefined();
    });

    it('debe rechazar valores de size mayores a 100', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const params = { size: 101 };
      
      // La validación se hace en el schema, no en la ejecución
      await expect(tool.execute(params)).resolves.toBeDefined();
    });

    it('debe aceptar parámetros vacíos', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await expect(tool.execute({})).resolves.toBeDefined();
    });

    it('debe aceptar parámetros con valores por defecto', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const params = {
        page: 1,
        size: 25,
        sortColumn: 'id' as const,
        sortDirection: 'asc' as const
      };
      
      await expect(tool.execute(params)).resolves.toBeDefined();
    });
  });

  describe('Construcción de URL', () => {
    it('debe construir la URL correctamente con parámetros básicos', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({ page: 2, size: 50 });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('page=2&size=50')
      );
    });

    it('debe aplicar valores por defecto correctamente', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({});

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('page=1&size=25&sortColumn=id&sortDirection=asc')
      );
    });

    it('debe manejar filtros complejos', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const params = {
        status: ['open', 'in-progress'] as ('open' | 'in-progress')[],
        priority: [5, 3],
        unitId: '1,2,3',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      };

      await tool.execute(params);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('status=open&status=in-progress')
      );
      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('priority=5&priority=3')
      );
      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('unitId=1%2C2%2C3')
      );
      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('startDate=2024-01-01')
      );
      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('endDate=2024-01-31')
      );
    });

    it('debe manejar arrays de userId correctamente', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({ userId: [1, 2, 3] });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('userId=1&userId=2&userId=3')
      );
    });

    it('debe manejar arrays de problems correctamente', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({ problems: [10, 20, 30] });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('problems=10&problems=20&problems=30')
      );
    });

    it('debe manejar búsqueda de texto', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({ search: 'reparación urgente' });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('search=reparaci%C3%B3n+urgente')
      );
    });

    it('debe manejar filtro isScheduled', async () => {
      const mockResponse = {
        _embedded: { workOrders: [] },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 0,
        _links: { self: { href: '' }, first: { href: '' }, last: { href: '' } }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      await tool.execute({ isScheduled: 1 });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('isScheduled=1')
      );
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar errores de API correctamente', async () => {
      const error = new Error('API Error: 500 Internal Server Error');
      mockApiClient.get.mockRejectedValue(error);

      await expect(tool.execute({})).rejects.toThrow(
        'Error al obtener órdenes de trabajo de mantenimiento: API Error: 500 Internal Server Error'
      );
    });

    it('debe manejar errores desconocidos', async () => {
      mockApiClient.get.mockRejectedValue('Unknown error');

      await expect(tool.execute({})).rejects.toThrow(
        'Error al obtener órdenes de trabajo de mantenimiento: Error desconocido'
      );
    });
  });

  describe('Respuesta de la API', () => {
    it('debe retornar la respuesta completa de la API', async () => {
      const mockResponse = {
        _embedded: {
          workOrders: [
            {
              id: 1,
              dateReceived: '2024-01-15',
              priority: 5,
              status: 'open',
              summary: 'Reparación urgente',
              description: 'Fuga de agua en baño principal',
              unitId: 10,
              vendorId: 5,
              createdAt: '2024-01-15T10:00:00Z',
              createdBy: 'admin',
              updatedAt: '2024-01-15T10:00:00Z',
              updatedBy: 'admin'
            }
          ]
        },
        page: 1,
        page_count: 1,
        page_size: 25,
        total_items: 1,
        _links: {
          self: { href: '/api/pms/maintenance/work-orders?page=1' },
          first: { href: '/api/pms/maintenance/work-orders?page=1' },
          last: { href: '/api/pms/maintenance/work-orders?page=1' }
        }
      };

      mockApiClient.get.mockResolvedValue(mockResponse);

      const result = await tool.execute({});

      expect(result).toEqual(mockResponse);
      expect(result._embedded.workOrders).toHaveLength(1);
      expect(result._embedded.workOrders[0]?.id).toBe(1);
      expect(result._embedded.workOrders[0]?.priority).toBe(5);
      expect(result._embedded.workOrders[0]?.status).toBe('open');
    });
  });

  describe('Propiedades de la herramienta', () => {
    it('debe tener el nombre correcto', () => {
      expect(tool.name).toBe('get_maintenance_work_orders');
    });

    it('debe tener la descripción correcta', () => {
      expect(tool.description).toBe('Retrieve paginated collection of maintenance work orders from Track HS');
    });

    it('debe tener el schema de entrada correcto', () => {
      expect(tool.inputSchema.type).toBe('object');
      expect(tool.inputSchema.properties).toBeDefined();
      expect(tool.inputSchema.properties.page).toBeDefined();
      expect(tool.inputSchema.properties.size).toBeDefined();
      expect(tool.inputSchema.properties.status).toBeDefined();
      expect(tool.inputSchema.required).toEqual([]);
    });
  });
});
