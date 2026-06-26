// FILE: frontend/src/services/carteirasService.ts

import { useQuery } from '@tanstack/react-query';
import api from './api';
import { Carteira, CarteiraCreate, CarteiraUpdate } from '../types/carteira';

const CARTEIRAS_BASE_URL = '/carteiras';

export const carteirasService = {
  getAllCarteiras: async (): Promise<Carteira[]> => {
    const response = await api.get<Carteira[]>(CARTEIRAS_BASE_URL);
    return response.data;
  },

  getCarteiraById: async (id: string): Promise<Carteira> => {
    const response = await api.get<Carteira>(`${CARTEIRAS_BASE_URL}/${id}`);
    return response.data;
  },

  createCarteira: async (data: CarteiraCreate): Promise<Carteira> => {
    const response = await api.post<Carteira>(CARTEIRAS_BASE_URL, data);
    return response.data;
  },

  updateCarteira: async (id: string, data: CarteiraUpdate): Promise<Carteira> => {
    const response = await api.put<Carteira>(`${CARTEIRAS_BASE_URL}/${id}`, data);
    return response.data;
  },

  deleteCarteira: async (id: string): Promise<void> => {
    await api.delete(`${CARTEIRAS_BASE_URL}/${id}`);
  },
};

export const useCarteiras = () => {
  return useQuery<Carteira[], Error>({
    queryKey: ['carteiras'],
    queryFn: carteirasService.getAllCarteiras,
  });
};