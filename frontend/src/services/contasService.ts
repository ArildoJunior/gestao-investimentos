// FILE: frontend/src/services/contasService.ts

import { useQuery } from '@tanstack/react-query';
import api from './api';
import { Conta, ContaCreate, ContaUpdate } from '../types/conta';

const CONTAS_BASE_URL = '/contas';

export const contasService = {
  getAllContas: async (): Promise<Conta[]> => {
    const response = await api.get<Conta[]>(CONTAS_BASE_URL);
    return response.data;
  },

  getContaById: async (id: string): Promise<Conta> => {
    const response = await api.get<Conta>(`${CONTAS_BASE_URL}/${id}`);
    return response.data;
  },

  getContasByInstituicaoId: async (instituicaoId: string): Promise<Conta[]> => {
    const response = await api.get<Conta[]>(`${CONTAS_BASE_URL}?instituicao_id=${instituicaoId}`);
    return response.data;
  },

  createConta: async (data: ContaCreate): Promise<Conta> => {
    const response = await api.post<Conta>(CONTAS_BASE_URL, data);
    return response.data;
  },

  updateConta: async (id: string, data: ContaUpdate): Promise<Conta> => {
    const response = await api.put<Conta>(`${CONTAS_BASE_URL}/${id}`, data);
    return response.data;
  },

  deleteConta: async (id: string): Promise<void> => {
    await api.delete(`${CONTAS_BASE_URL}/${id}`);
  },
};

export const useContas = () => {
  return useQuery<Conta[], Error>({
    queryKey: ['contas'],
    queryFn: contasService.getAllContas,
  });
};