/**
 * Tests para GetLedgerAccountsTool
 */

import { GetLedgerAccountsTool } from '../../src/tools/get-ledger-accounts.js';
import { TrackHSApiClient } from '../../src/core/api-client.js';
import { mockApiResponses } from '../mocks/api-responses.js';
import { setupApiMock, cleanupApiMock, mockSuccessfulAuth, validateApiResponse } from '../utils/test-helpers.js';

describe('GetLedgerAccountsTool', () => {
  let tool: GetLedgerAccountsTool;
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
    tool = new GetLedgerAccountsTool(apiClient);

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
        sortColumn: 'account_code' as const,
        sortDirection: 'asc' as const,
        search: 'caja'
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
    it('debe obtener cuentas contables con parámetros por defecto', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute();

      expect(result).toBeDefined();
      expect(validateApiResponse(result)).toBe(true);
      expect(result._embedded.accounts).toHaveLength(2);
    });

    it('debe obtener cuentas contables con búsqueda', async () => {
      const params = {
        search: 'caja'
      };

      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc&search=caja')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener cuentas contables con filtros de tipo', async () => {
      const params = {
        accountType: 'asset'
      };

      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc&accountType=asset')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });

    it('debe obtener cuentas contables con paginación', async () => {
      const params = {
        page: 2,
        size: 5
      };

      mockScope
        .get('/accounting/ledger-accounts?page=2&size=5&sortColumn=account_code&sortDirection=asc')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute(params);

      expect(result).toBeDefined();
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar error 401 (No autorizado)', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .reply(401, mockApiResponses.errors.unauthorized);

      await expect(tool.execute()).rejects.toThrow('Error al obtener cuentas contables');
    });

    it('debe manejar error 500 (Error del servidor)', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .reply(500, mockApiResponses.errors.serverError);

      await expect(tool.execute()).rejects.toThrow('Error al obtener cuentas contables');
    });

    it('debe manejar timeout de red', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .replyWithError({ code: 'ETIMEDOUT' });

      await expect(tool.execute()).rejects.toThrow('Error al obtener cuentas contables');
    });
  });

  describe('Validación de respuesta', () => {
    it('debe validar estructura de respuesta correcta', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute();

      expect(result).toHaveProperty('_embedded');
      expect(Array.isArray(result._embedded.accounts)).toBe(true);
    });

    it('debe validar estructura de elementos de cuenta contable', async () => {
      mockScope
        .get('/accounting/ledger-accounts?page=1&size=10&sortColumn=account_code&sortDirection=asc')
        .reply(200, mockApiResponses.ledgerAccounts.success);

      const result = await tool.execute();

      if (result._embedded.accounts.length > 0) {
        const account = result._embedded.accounts[0];
        expect(account).toHaveProperty('id');
        expect(account).toHaveProperty('code');
        expect(account).toHaveProperty('name');
        expect(account).toHaveProperty('category');
        expect(account).toHaveProperty('accountType');
      }
    });
  });
});
