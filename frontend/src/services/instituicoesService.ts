// FILE: frontend/src/services/instituicoesService.ts

import api from './api'; // Importa a instância do Axios configurada
import { Instituicao, InstituicaoCreate, InstituicaoUpdate } from '../types/instituicao';

const INSTITUICOES_BASE_URL = '/instituicoes';

export const instituicoesService = {
  // Buscar todas as instituições
  getAllInstituicoes: async (): Promise<Instituicao[]> => {
    const response = await api.get<Instituicao[]>(INSTITUICOES_BASE_URL);
    return response.data;
  },

  // Buscar uma instituição por ID
  getInstituicaoById: async (id: string): Promise<Instituicao> => {
    const response = await api.get<Instituicao>(`${INSTITUICOES_BASE_URL}/${id}`);
    return response.data;
  },

  // Criar uma nova instituição
  createInstituicao: async (data: InstituicaoCreate): Promise<Instituicao> => {
    const response = await api.post<Instituicao>(INSTITUICOES_BASE_URL, data);
    return response.data;
  },

  // Atualizar uma instituição existente
  updateInstituicao: async (id: string, data: InstituicaoUpdate): Promise<Instituicao> => {
    const response = await api.put<Instituicao>(`${INSTITUICOES_BASE_URL}/${id}`, data);
    return response.data;
  },

  // Deletar uma instituição
  deleteInstituicao: async (id: string): Promise<void> => {
    await api.delete(`${INSTITUICOES_BASE_URL}/${id}`);
  },
};