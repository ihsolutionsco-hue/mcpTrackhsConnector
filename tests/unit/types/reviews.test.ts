/**
 * Tests unitarios para tipos de Reviews
 */

import {
  Review,
  GetReviewsParams,
  ReviewsResponse,
  ReviewFilters
} from '../../../src/types/reviews.js';

describe('Reviews Types', () => {
  describe('Review interface', () => {
    it('debe permitir review completo', () => {
      const review: Review = {
        id: 1,
        reviewId: 'REV-001',
        publicReview: 'Excelente servicio',
        privateReview: 'Nota privada',
        rating: 5,
        guestName: 'Juan Pérez',
        guestEmail: 'juan@example.com',
        propertyId: 'PROP-001',
        propertyName: 'Hotel Test',
        channel: 'Booking.com',
        createdAt: '2024-01-15T10:30:00Z',
        updatedAt: '2024-01-15T10:30:00Z',
        status: 'published',
        response: 'Gracias por su comentario',
        responseDate: '2024-01-16T09:00:00Z'
      };

      expect(review.id).toBe(1);
      expect(review.reviewId).toBe('REV-001');
      expect(review.publicReview).toBe('Excelente servicio');
      expect(review.privateReview).toBe('Nota privada');
      expect(review.rating).toBe(5);
      expect(review.guestName).toBe('Juan Pérez');
      expect(review.guestEmail).toBe('juan@example.com');
      expect(review.propertyId).toBe('PROP-001');
      expect(review.propertyName).toBe('Hotel Test');
      expect(review.channel).toBe('Booking.com');
      expect(review.createdAt).toBe('2024-01-15T10:30:00Z');
      expect(review.updatedAt).toBe('2024-01-15T10:30:00Z');
      expect(review.status).toBe('published');
      expect(review.response).toBe('Gracias por su comentario');
      expect(review.responseDate).toBe('2024-01-16T09:00:00Z');
    });

    it('debe permitir review mínimo', () => {
      const review: Review = {
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
      };

      expect(review.id).toBe(1);
      expect(review.privateReview).toBeUndefined();
      expect(review.response).toBeUndefined();
      expect(review.responseDate).toBeUndefined();
    });

    it('debe permitir diferentes estados', () => {
      const states: Review['status'][] = ['published', 'pending', 'rejected'];
      
      states.forEach(status => {
        const review: Review = {
          id: 1,
          reviewId: 'REV-001',
          publicReview: 'Test review',
          rating: 5,
          guestName: 'Test Guest',
          guestEmail: 'test@example.com',
          propertyId: 'PROP-001',
          propertyName: 'Test Property',
          channel: 'Test Channel',
          createdAt: '2024-01-15T10:30:00Z',
          updatedAt: '2024-01-15T10:30:00Z',
          status
        };
        
        expect(review.status).toBe(status);
      });
    });

    it('debe permitir diferentes ratings', () => {
      const ratings = [1, 2, 3, 4, 5];
      
      ratings.forEach(rating => {
        const review: Review = {
          id: 1,
          reviewId: 'REV-001',
          publicReview: 'Test review',
          rating,
          guestName: 'Test Guest',
          guestEmail: 'test@example.com',
          propertyId: 'PROP-001',
          propertyName: 'Test Property',
          channel: 'Test Channel',
          createdAt: '2024-01-15T10:30:00Z',
          updatedAt: '2024-01-15T10:30:00Z',
          status: 'published'
        };
        
        expect(review.rating).toBe(rating);
      });
    });
  });

  describe('GetReviewsParams interface', () => {
    it('debe permitir parámetros completos', () => {
      const params: GetReviewsParams = {
        page: 1,
        size: 10,
        sortColumn: 'id',
        sortDirection: 'asc',
        search: 'test search',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      expect(params.page).toBe(1);
      expect(params.size).toBe(10);
      expect(params.sortColumn).toBe('id');
      expect(params.sortDirection).toBe('asc');
      expect(params.search).toBe('test search');
      expect(params.updatedSince).toBe('2024-01-01T00:00:00Z');
    });

    it('debe permitir parámetros opcionales', () => {
      const params: GetReviewsParams = {};

      expect(params.page).toBeUndefined();
      expect(params.size).toBeUndefined();
      expect(params.sortColumn).toBeUndefined();
      expect(params.sortDirection).toBeUndefined();
      expect(params.search).toBeUndefined();
      expect(params.updatedSince).toBeUndefined();
    });

    it('debe permitir diferentes sortDirection', () => {
      const ascParams: GetReviewsParams = { sortDirection: 'asc' };
      const descParams: GetReviewsParams = { sortDirection: 'desc' };

      expect(ascParams.sortDirection).toBe('asc');
      expect(descParams.sortDirection).toBe('desc');
    });

    it('debe permitir diferentes valores de paginación', () => {
      const testCases = [
        { page: 1, size: 1 },
        { page: 10, size: 50 },
        { page: 100, size: 100 }
      ];

      testCases.forEach(({ page, size }) => {
        const params: GetReviewsParams = { page, size };
        expect(params.page).toBe(page);
        expect(params.size).toBe(size);
      });
    });
  });

  describe('ReviewsResponse interface', () => {
    it('debe permitir respuesta completa', () => {
      const response: ReviewsResponse = {
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
          page: 1,
          size: 10,
          total: 1,
          totalPages: 1,
          hasNext: false,
          hasPrevious: false
        },
        success: true,
        message: 'Reviews retrieved successfully'
      };

      expect(response.data).toHaveLength(1);
      expect(response.pagination.page).toBe(1);
      expect(response.pagination.size).toBe(10);
      expect(response.pagination.total).toBe(1);
      expect(response.pagination.totalPages).toBe(1);
      expect(response.pagination.hasNext).toBe(false);
      expect(response.pagination.hasPrevious).toBe(false);
      expect(response.success).toBe(true);
      expect(response.message).toBe('Reviews retrieved successfully');
    });

    it('debe permitir respuesta sin mensaje', () => {
      const response: ReviewsResponse = {
        data: [],
        pagination: {
          page: 1,
          size: 10,
          total: 0,
          totalPages: 0,
          hasNext: false,
          hasPrevious: false
        },
        success: true
      };

      expect(response.data).toHaveLength(0);
      expect(response.success).toBe(true);
      expect(response.message).toBeUndefined();
    });

    it('debe permitir respuesta de error', () => {
      const response: ReviewsResponse = {
        data: [],
        pagination: {
          page: 1,
          size: 10,
          total: 0,
          totalPages: 0,
          hasNext: false,
          hasPrevious: false
        },
        success: false,
        message: 'Error retrieving reviews'
      };

      expect(response.success).toBe(false);
      expect(response.message).toBe('Error retrieving reviews');
    });

    it('debe permitir diferentes valores de paginación', () => {
      const testCases = [
        { page: 1, size: 10, total: 0, totalPages: 0 },
        { page: 2, size: 20, total: 50, totalPages: 3 },
        { page: 5, size: 100, total: 500, totalPages: 5 }
      ];

      testCases.forEach(({ page, size, total, totalPages }) => {
        const response: ReviewsResponse = {
          data: [],
          pagination: {
            page,
            size,
            total,
            totalPages,
            hasNext: page < totalPages,
            hasPrevious: page > 1
          },
          success: true
        };

        expect(response.pagination.page).toBe(page);
        expect(response.pagination.size).toBe(size);
        expect(response.pagination.total).toBe(total);
        expect(response.pagination.totalPages).toBe(totalPages);
        expect(response.pagination.hasNext).toBe(page < totalPages);
        expect(response.pagination.hasPrevious).toBe(page > 1);
      });
    });
  });

  describe('ReviewFilters interface', () => {
    it('debe permitir filtros completos', () => {
      const filters: ReviewFilters = {
        status: 'published',
        channel: 'Booking.com',
        propertyId: 'PROP-001',
        rating: 5,
        dateFrom: '2024-01-01T00:00:00Z',
        dateTo: '2024-12-31T23:59:59Z'
      };

      expect(filters.status).toBe('published');
      expect(filters.channel).toBe('Booking.com');
      expect(filters.propertyId).toBe('PROP-001');
      expect(filters.rating).toBe(5);
      expect(filters.dateFrom).toBe('2024-01-01T00:00:00Z');
      expect(filters.dateTo).toBe('2024-12-31T23:59:59Z');
    });

    it('debe permitir filtros opcionales', () => {
      const filters: ReviewFilters = {};

      expect(filters.status).toBeUndefined();
      expect(filters.channel).toBeUndefined();
      expect(filters.propertyId).toBeUndefined();
      expect(filters.rating).toBeUndefined();
      expect(filters.dateFrom).toBeUndefined();
      expect(filters.dateTo).toBeUndefined();
    });

    it('debe permitir diferentes estados de filtro', () => {
      const states: ReviewFilters['status'][] = ['published', 'pending', 'rejected'];
      
      states.forEach(status => {
        const filters: ReviewFilters = {};
        if (status) {
          filters.status = status;
        }
        expect(filters.status).toBe(status);
      });
    });

    it('debe permitir diferentes ratings de filtro', () => {
      const ratings = [1, 2, 3, 4, 5];
      
      ratings.forEach(rating => {
        const filters: ReviewFilters = { rating };
        expect(filters.rating).toBe(rating);
      });
    });
  });

  describe('Integración entre tipos', () => {
    it('debe permitir flujo completo de datos', () => {
      const review: Review = {
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
      };

      const params: GetReviewsParams = {
        page: 1,
        size: 10,
        sortColumn: 'id',
        sortDirection: 'asc',
        search: 'excelente',
        updatedSince: '2024-01-01T00:00:00Z'
      };

      const response: ReviewsResponse = {
        data: [review],
        pagination: {
          page: 1,
          size: 10,
          total: 1,
          totalPages: 1,
          hasNext: false,
          hasPrevious: false
        },
        success: true,
        message: 'Reviews retrieved successfully'
      };

      const filters: ReviewFilters = {
        status: 'published',
        channel: 'Booking.com',
        rating: 5
      };

      expect(review).toBeDefined();
      expect(params).toBeDefined();
      expect(response).toBeDefined();
      expect(filters).toBeDefined();
    });
  });
});
