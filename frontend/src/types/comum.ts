// FILE: frontend/src/types/comum.ts

export type UUID = string;

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginationResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export interface ErrorResponse {
  detail: string | { loc: (string | number)[], msg: string, type: string }[];
}

export interface Timestamped {
  created_at: string;
  updated_at: string;
}

export interface BaseQueryParams {
  page?: number;
  size?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}