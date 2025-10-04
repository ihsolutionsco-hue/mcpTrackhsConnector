/**
 * Tests unitarios para BaseTrackHSTool
 */

import { BaseTrackHSTool, MCPToolSchema } from '../../../src/core/base-tool.js';
import { TrackHSApiClient } from '../../../src/core/api-client.js';

// Mock de TrackHSApiClient
jest.mock('../../../src/core/api-client.js');
const MockedTrackHSApiClient = TrackHSApiClient as jest.MockedClass<typeof TrackHSApiClient>;

// Clase de prueba que extiende BaseTrackHSTool
class TestTool extends BaseTrackHSTool {
  name = 'test_tool';
  description = 'Test tool for unit testing';
  inputSchema: MCPToolSchema = {
    type: 'object',
    properties: {
      id: { type: 'string' },
      name: { type: 'string' },
      count: { type: 'number' },
      active: { type: 'boolean' }
    },
    required: ['id']
  };

  async execute(params: any): Promise<any> {
    this.validateParams(params);
    return { success: true, params };
  }
}

describe('BaseTrackHSTool', () => {
  let testTool: TestTool;
  let mockApiClient: jest.Mocked<TrackHSApiClient>;

  beforeEach(() => {
    // Mock del cliente API
    mockApiClient = {
      get: jest.fn(),
      post: jest.fn(),
      request: jest.fn()
    } as any;

    MockedTrackHSApiClient.mockImplementation(() => mockApiClient);

    testTool = new TestTool(mockApiClient);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Constructor', () => {
    it('debe inicializar correctamente con cliente API', () => {
      expect(testTool).toBeDefined();
      expect(testTool.name).toBe('test_tool');
      expect(testTool.description).toBe('Test tool for unit testing');
    });

    it('debe almacenar referencia al cliente API', () => {
      // Verificar que el cliente API se pasa correctamente
      expect(testTool).toBeDefined();
      expect(testTool['apiClient']).toBe(mockApiClient);
    });
  });

  describe('validateParams', () => {
    it('debe validar parámetros requeridos correctamente', async () => {
      const validParams = { id: '123' };
      
      await expect(testTool.execute(validParams)).resolves.toBeDefined();
    });

    it('debe rechazar parámetros faltantes requeridos', async () => {
      const invalidParams = { name: 'test' }; // Falta 'id' requerido
      
      await expect(testTool.execute(invalidParams))
        .rejects
        .toThrow('Parámetro requerido faltante: id');
    });

    it('debe validar tipos de datos correctamente', async () => {
      const validParams = {
        id: '123',
        name: 'test',
        count: 42,
        active: true
      };
      
      await expect(testTool.execute(validParams)).resolves.toBeDefined();
    });

    it('debe rechazar tipos de datos incorrectos', async () => {
      const invalidParams = {
        id: '123',
        name: 123, // Debe ser string
        count: 'not_a_number', // Debe ser number
        active: 'not_a_boolean' // Debe ser boolean
      };
      
      await expect(testTool.execute(invalidParams))
        .rejects
        .toThrow('Parámetro \'name\' debe ser string');
    });

    it('debe manejar parámetros opcionales', async () => {
      const paramsWithOptional = {
        id: '123',
        name: 'test',
        count: 42
        // active es opcional
      };
      
      await expect(testTool.execute(paramsWithOptional)).resolves.toBeDefined();
    });

    it('debe validar parámetros con valores undefined', async () => {
      const paramsWithUndefined = {
        id: '123'
      };
      
      await expect(testTool.execute(paramsWithUndefined)).resolves.toBeDefined();
    });

    it('debe manejar parámetros extra no definidos en el schema', async () => {
      const paramsWithExtra = {
        id: '123',
        extraParam: 'extra_value',
        anotherExtra: 999
      };
      
      await expect(testTool.execute(paramsWithExtra)).resolves.toBeDefined();
    });
  });

  describe('execute method', () => {
    it('debe ejecutar correctamente con parámetros válidos', async () => {
      const params = { id: '123', name: 'test' };
      
      const result = await testTool.execute(params);
      
      expect(result).toEqual({
        success: true,
        params
      });
    });

    it('debe lanzar error con parámetros inválidos', async () => {
      const invalidParams = { name: 'test' }; // Falta 'id' requerido
      
      await expect(testTool.execute(invalidParams))
        .rejects
        .toThrow('Parámetro requerido faltante: id');
    });

    it('debe validar parámetros antes de ejecutar', async () => {
      const params = { id: 123 }; // id debe ser string
      
      await expect(testTool.execute(params))
        .rejects
        .toThrow('Parámetro \'id\' debe ser string');
    });
  });

  describe('Manejo de diferentes tipos de schema', () => {
    class StringOnlyTool extends BaseTrackHSTool {
      name = 'string_tool';
      description = 'String only tool';
      inputSchema: MCPToolSchema = {
        type: 'object',
        properties: {
          text: { type: 'string' }
        },
        required: ['text']
      };

      async execute(params: any): Promise<any> {
        this.validateParams(params);
        return { text: params.text };
      }
    }

    class NumberOnlyTool extends BaseTrackHSTool {
      name = 'number_tool';
      description = 'Number only tool';
      inputSchema: MCPToolSchema = {
        type: 'object',
        properties: {
          value: { type: 'number' }
        },
        required: ['value']
      };

      async execute(params: any): Promise<any> {
        this.validateParams(params);
        return { value: params.value };
      }
    }

    class BooleanOnlyTool extends BaseTrackHSTool {
      name = 'boolean_tool';
      description = 'Boolean only tool';
      inputSchema: MCPToolSchema = {
        type: 'object',
        properties: {
          flag: { type: 'boolean' }
        },
        required: ['flag']
      };

      async execute(params: any): Promise<any> {
        this.validateParams(params);
        return { flag: params.flag };
      }
    }

    it('debe validar strings correctamente', async () => {
      const stringTool = new StringOnlyTool(mockApiClient);
      
      await expect(stringTool.execute({ text: 'valid string' }))
        .resolves
        .toEqual({ text: 'valid string' });
      
      await expect(stringTool.execute({ text: 123 }))
        .rejects
        .toThrow('Parámetro \'text\' debe ser string');
    });

    it('debe validar numbers correctamente', async () => {
      const numberTool = new NumberOnlyTool(mockApiClient);
      
      await expect(numberTool.execute({ value: 42 }))
        .resolves
        .toEqual({ value: 42 });
      
      await expect(numberTool.execute({ value: 'not a number' }))
        .rejects
        .toThrow('Parámetro \'value\' debe ser number');
    });

    it('debe validar booleans correctamente', async () => {
      const booleanTool = new BooleanOnlyTool(mockApiClient);
      
      await expect(booleanTool.execute({ flag: true }))
        .resolves
        .toEqual({ flag: true });
      
      await expect(booleanTool.execute({ flag: false }))
        .resolves
        .toEqual({ flag: false });
      
      await expect(booleanTool.execute({ flag: 'not a boolean' }))
        .rejects
        .toThrow('Parámetro \'flag\' debe ser boolean');
    });
  });

  describe('Casos edge', () => {
    it('debe manejar parámetros vacíos', async () => {
      await expect(testTool.execute({}))
        .rejects
        .toThrow('Parámetro requerido faltante: id');
    });

    it('debe manejar parámetros null', async () => {
      await expect(testTool.execute(null as any))
        .rejects
        .toThrow('Parámetro requerido faltante: id');
    });

    it('debe manejar parámetros undefined', async () => {
      await expect(testTool.execute(undefined as any))
        .rejects
        .toThrow('Parámetro requerido faltante: id');
    });

    it('debe manejar schema sin propiedades requeridas', async () => {
      class NoRequiredTool extends BaseTrackHSTool {
        name = 'no_required_tool';
        description = 'Tool with no required properties';
        inputSchema: MCPToolSchema = {
          type: 'object',
          properties: {
            optional: { type: 'string' }
          }
        };

        async execute(params: any): Promise<any> {
          this.validateParams(params);
          return { success: true };
        }
      }

      const noRequiredTool = new NoRequiredTool(mockApiClient);
      
      await expect(noRequiredTool.execute({})).resolves.toBeDefined();
      await expect(noRequiredTool.execute({ optional: 'test' })).resolves.toBeDefined();
    });

    it('debe manejar schema sin propiedades', async () => {
      class EmptySchemaTool extends BaseTrackHSTool {
        name = 'empty_schema_tool';
        description = 'Tool with empty schema';
        inputSchema: MCPToolSchema = {
          type: 'object',
          properties: {}
        };

        async execute(params: any): Promise<any> {
          this.validateParams(params);
          return { success: true };
        }
      }

      const emptySchemaTool = new EmptySchemaTool(mockApiClient);
      
      await expect(emptySchemaTool.execute({})).resolves.toBeDefined();
      await expect(emptySchemaTool.execute({ any: 'value' })).resolves.toBeDefined();
    });
  });
});
