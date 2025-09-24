/**
 * Herramienta MCP para obtener reseñas de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { ReviewsResponse, GetReviewsParams } from '../types/reviews.js';

export class GetReviewsTool extends BaseTrackHSTool {
  name = 'get_reviews';
  description = 'Retrieve paginated collection of property reviews from Track HS';
  
  inputSchema = {
    type: 'object' as const,
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
  };

  async execute(params: GetReviewsParams = {}): Promise<ReviewsResponse> {
    // Validar parámetros
    this.validateParams(params);

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    // Aplicar valores por defecto
    const page = params.page || 1;
    const size = params.size || 10;
    const sortColumn = params.sortColumn || 'id';
    const sortDirection = params.sortDirection || 'asc';

    // Agregar parámetros a la query
    queryParams.append('page', page.toString());
    queryParams.append('size', size.toString());
    queryParams.append('sortColumn', sortColumn);
    queryParams.append('sortDirection', sortDirection);

    if (params.search) {
      queryParams.append('search', params.search);
    }

    if (params.updatedSince) {
      queryParams.append('updatedSince', params.updatedSince);
    }

    const endpoint = `/channel-management/channel/reviews?${queryParams.toString()}`;
    
    try {
      const result = await this.apiClient.get<ReviewsResponse>(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener reseñas: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}