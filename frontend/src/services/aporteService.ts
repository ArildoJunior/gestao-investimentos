// FILE: frontend/src/services/aporteService.ts

import api from './api';
import { AporteCreate, AporteRead } from '../types/aporte';

const APORTES_BASE_URL = '/aportes';

export const aporteService = {
  createAporte: async (data: AporteCreate): Promise<AporteRead> => {
    const response = await api.post(APORTES_BASE_URL, data);
    return response.data;
  },

  getAportesByCarteira: async (carteiraId: string): Promise<AporteRead[]> => {
    const response = await api.get(`${APORTES_BASE_URL}?carteira_id=${carteiraId}`);
    return response.data;
  },

  getAportesByConta: async (contaId: string): Promise<AporteRead[]> => {
    const response = await api.get(`${APORTES_BASE_URL}?conta_id=${contaId}`);
    return response.data;
  },

  getAporteById: async (id: string): Promise<AporteRead> => {
    const response = await api.get(`${APORTES_BASE_URL}/${id}`);
    return response.data;
  },

  updateAporte: async (id: string, data: AporteCreate): Promise<AporteRead> => {
    const response = await api.put(`${APORTES_BASE_URL}/${id}`, data);
    return response.data;
  },

  deleteAporte: async (id: string): Promise<void> => {
    await api.delete(`${APORTES_BASE_URL}/${id}`);
  },
};