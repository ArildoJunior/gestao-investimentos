// FILE: frontend/src/services/ativosService.ts

import api from './api';
import { Ativo, AtivoCreate, AtivoUpdate } from '../types/ativo'; // Importe Ativo, AtivoCreate, AtivoUpdate

const ATIVOS_BASE_URL = '/ativos';

export const ativosService = {
  getAllAtivos: async (): Promise<Ativo[]> => {
    const response = await api.get<Ativo[]>(ATIVOS_BASE_URL);
    return response.data;
  },

  getAtivoById: async (id: string): Promise<Ativo> => {
    const response = await api.get<Ativo>(`${ATIVOS_BASE_URL}/${id}`);
    return response.data;
  },

  getAtivosByTipo: async (tipo: string): Promise<Ativo[]> => {
    const response = await api.get<Ativo[]>(`${ATIVOS_BASE_URL}?tipo=${tipo}`);
    return response.data;
  },

  getAtivoByTicker: async (ticker: string): Promise<Ativo> => {
    const response = await api.get<Ativo>(`${ATIVOS_BASE_URL}?ticker=${ticker}`);
    return response.data;
  },

  createAtivo: async (data: AtivoCreate): Promise<Ativo> => {
    const response = await api.post<Ativo>(ATIVOS_BASE_URL, data);
    return response.data;
  },

  updateAtivo: async (id: string, data: AtivoUpdate): Promise<Ativo> => {
    const response = await api.put<Ativo>(`${ATIVOS_BASE_URL}/${id}`, data);
    return response.data;
  },

  deleteAtivo: async (id: string): Promise<void> => {
    await api.delete(`${ATIVOS_BASE_URL}/${id}`);
  },
};

// REMOVA ESTE BLOCO SE ELE ESTIVER NO SEU ARQUIVO:
// export const useAtivos = () => {
//   return useQuery<Ativo[], Error>({
//     queryKey: ['ativos'],
//     queryFn: ativosService.getAllAtivos,
//   });
// };