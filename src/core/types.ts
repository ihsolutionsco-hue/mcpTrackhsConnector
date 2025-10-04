/**
 * Tipos compartidos para el servidor MCP de Track HS
 */

export interface TrackHSConfig {
  baseUrl: string;
  username: string;
  password: string;
}

export interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: string | undefined;
}

export interface ApiError {
  message: string;
  status?: number;
  statusText?: string;
}

export interface PaginationParams {
  page?: number;
  size?: number;
  sortColumn?: string;
  sortDirection?: 'asc' | 'desc';
}

export interface SearchParams {
  search?: string;
  updatedSince?: string;
}

export interface TrackHSResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}
