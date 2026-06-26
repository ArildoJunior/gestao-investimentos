// FILE: frontend/src/services/movimentacoesService.ts

import api from './api';
import { MovimentacaoCreate } from '../types/movimentacao';

const MOVIMENTACOES_BASE_URL = '/movimentacoes';

export const movimentacoesService = {
  createMovimentacao: async (data: MovimentacaoCreate) => {
    const response = await api.post(MOVIMENTACOES_BASE_URL, data);
    return response.data;
  },

  getMovimentacoesByCarteira: async (carteiraId: string) => {
    const response = await api.get(`${MOVIMENTACOES_BASE_URL}?carteira_id=${carteiraId}`);
    return response.data;
  },
};