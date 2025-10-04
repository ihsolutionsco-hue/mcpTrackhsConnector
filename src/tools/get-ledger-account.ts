/**
 * Herramienta MCP para obtener una cuenta contable específica de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { LedgerAccount, GetLedgerAccountParams } from '../types/ledger-accounts.js';

export class GetLedgerAccountTool extends BaseTrackHSTool {
  name = 'get_ledger_account';
  description = 'Retrieve a specific ledger account by ID from Track HS accounting system. Returns complete account information including balances, banking details, stakeholder data, and financial configuration.';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      accountId: { 
        type: 'number', 
        description: 'The unique identifier of the ledger account to retrieve',
        minimum: 1
      }
    },
    required: ['accountId']
  };

  async execute(params: GetLedgerAccountParams): Promise<LedgerAccount> {
    // Validar parámetros
    this.validateParams(params);

    // Validar que accountId sea un entero positivo
    if (!Number.isInteger(params.accountId) || params.accountId < 1) {
      throw new Error('accountId debe ser un entero positivo mayor a 0');
    }

    const endpoint = `/pms/accounting/accounts/${params.accountId}`;
    
    try {
      const result = await this.apiClient.get<LedgerAccount>(endpoint);
      return result;
    } catch (error) {
      if (error instanceof Error && error.message.includes('404')) {
        throw new Error(`Cuenta contable con ID ${params.accountId} no encontrada`);
      }
      throw new Error(`Error al obtener cuenta contable: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
