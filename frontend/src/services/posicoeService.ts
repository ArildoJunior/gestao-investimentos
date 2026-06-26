// FILE: frontend/src/services/posicoeService.ts

import api from './api';
import { Posicao } from '../types/posicao';

const POSICOES_BASE_URL = '/posicoes';

export const posicoeService = {
  getPosicoesByCarteira: async (carteiraId: string): Promise<Posicao[]> => {
    const response = await api.get<Posicao[]>(`${POSICOES_BASE_URL}/carteira/${carteiraId}`);
    return response.data;
  },

  getPosicoesByCarteiraAndConta: async (carteiraId: string, contaId: string): Promise<Posicao[]> => {
    const response = await api.get<Posicao[]>(`${POSICOES_BASE_URL}/carteira/${carteiraId}/conta/${contaId}`);
    return response.data;
  },

  getPosicaoByCarteiraAndAtivo: async (carteiraId: string, ativoId: string): Promise<Posicao> => {
    const response = await api.get<Posicao>(`${POSICOES_BASE_URL}/carteira/${carteiraId}/ativo/${ativoId}`);
    return response.data;
  },
};