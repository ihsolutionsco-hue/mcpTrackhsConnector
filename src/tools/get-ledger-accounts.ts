/**
 * Herramienta MCP para obtener cuentas contables de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { LedgerAccountsResponse, GetLedgerAccountsParams } from '../types/ledger-accounts.js';

export class GetLedgerAccountsTool extends BaseTrackHSTool {
  name = 'get_ledger_accounts';
  description = 'Retrieve ledger accounts from Track HS accounting system. Returns an array of ledger accounts with their financial information, categories, and related stakeholder data.';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      page: { 
        type: 'number', 
        description: 'Page Number',
        minimum: 0
      },
      size: { 
        type: 'number', 
        description: 'Page Size',
        minimum: 1
      },
      sortColumn: { 
        type: 'string', 
        enum: ['id', 'name', 'type', 'relativeOrder', 'isActive'],
        description: 'Sort by id, name, type, relativeOrder, or isActive'
      },
      sortDirection: { 
        type: 'string', 
        enum: ['asc', 'desc'], 
        default: 'asc',
        description: 'Sort ascending or descending'
      },
      search: { 
        type: 'string', 
        description: 'Search ledger accounts with a string'
      },
      isActive: { 
        type: 'number', 
        description: 'Filter by active status (1 for active, 0 for inactive)'
      },
      category: { 
        type: 'string', 
        enum: ['Revenue', 'Asset', 'Equity', 'Liability', 'Expense'],
        description: 'Filter by account category'
      },
      accountType: { 
        type: 'string', 
        description: 'Filter by account type (options vary based on category)'
      },
      parentId: { 
        type: 'number', 
        description: 'Filter by parent account ID'
      },
      includeRestricted: { 
        type: 'number', 
        description: 'Include restricted accounts (1 to include, 0 to exclude)'
      },
      sortByCategoryValue: { 
        type: 'number', 
        description: 'Sort by category value'
      }
    },
    required: []
  };

  async execute(params: GetLedgerAccountsParams = {}): Promise<LedgerAccountsResponse> {
    // Validar parámetros
    this.validateParams(params);

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    // Aplicar valores por defecto
    const sortDirection = params.sortDirection || 'asc';
    const sortColumn = params.sortColumn || 'name';

    // Agregar parámetros a la query
    if (params.page !== undefined) {
      queryParams.append('page', params.page.toString());
    }

    if (params.size !== undefined) {
      queryParams.append('size', params.size.toString());
    }

    queryParams.append('sortColumn', sortColumn);
    queryParams.append('sortDirection', sortDirection);

    if (params.search) {
      queryParams.append('search', params.search);
    }

    if (params.isActive !== undefined) {
      queryParams.append('isActive', params.isActive.toString());
    }

    if (params.category) {
      queryParams.append('category', params.category);
    }

    if (params.accountType) {
      queryParams.append('accountType', params.accountType);
    }

    if (params.parentId !== undefined) {
      queryParams.append('parentId', params.parentId.toString());
    }

    if (params.includeRestricted !== undefined) {
      queryParams.append('includeRestricted', params.includeRestricted.toString());
    }

    if (params.sortByCategoryValue !== undefined) {
      queryParams.append('sortByCategoryValue', params.sortByCategoryValue.toString());
    }

    const endpoint = `/pms/accounting/accounts?${queryParams.toString()}`;
    
    try {
      const result = await this.apiClient.get<LedgerAccountsResponse>(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener cuentas contables: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
