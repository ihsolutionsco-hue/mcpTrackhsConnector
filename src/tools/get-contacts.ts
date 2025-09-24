/**
 * Herramienta MCP para obtener contactos de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { ContactsResponse, GetContactsParams } from '../types/contacts.js';

export class GetContactsTool extends BaseTrackHSTool {
  name = 'get_contacts';
  description = 'Retrieve all contacts from Track HS CRM system. Contacts include guests, owners, or vendor employees.';
  
  inputSchema = {
    type: 'object' as const,
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
  };

  async execute(params: GetContactsParams = {}): Promise<ContactsResponse> {
    // Validar parámetros
    this.validateParams(params);

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    // Aplicar valores por defecto
    const sortDirection = params.sortDirection || 'asc';

    // Agregar parámetros a la query
    if (params.sortColumn) {
      queryParams.append('sortColumn', params.sortColumn);
    }
    queryParams.append('sortDirection', sortDirection);

    if (params.search) {
      queryParams.append('search', params.search);
    }

    if (params.term) {
      queryParams.append('term', params.term);
    }

    if (params.email) {
      queryParams.append('email', params.email);
    }

    if (params.page) {
      queryParams.append('page', params.page.toString());
    }

    if (params.size) {
      queryParams.append('size', params.size.toString());
    }

    if (params.updatedSince) {
      queryParams.append('updatedSince', params.updatedSince);
    }

    const endpoint = `/crm/contacts?${queryParams.toString()}`;
    
    try {
      const result = await this.apiClient.get<ContactsResponse>(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener contactos: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}