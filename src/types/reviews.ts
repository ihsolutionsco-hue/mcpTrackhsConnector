/**
 * Tipos específicos para el API de Reviews de Track HS
 */

export interface Review {
  id: number;
  reviewId: string;
  publicReview: string;
  privateReview?: string;
  rating: number;
  guestName: string;
  guestEmail: string;
  propertyId: string;
  propertyName: string;
  channel: string;
  createdAt: string;
  updatedAt: string;
  status: 'published' | 'pending' | 'rejected';
  response?: string;
  responseDate?: string;
}

export interface GetReviewsParams {
  page?: number;
  size?: number;
  sortColumn?: 'id';
  sortDirection?: 'asc' | 'desc';
  search?: string;
  updatedSince?: string;
}

export interface ReviewsResponse {
  data: Review[];
  pagination: {
    page: number;
    size: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
  success: boolean;
  message?: string;
}

export interface ReviewFilters {
  status?: 'published' | 'pending' | 'rejected';
  channel?: string;
  propertyId?: string;
  rating?: number;
  dateFrom?: string;
  dateTo?: string;
}
