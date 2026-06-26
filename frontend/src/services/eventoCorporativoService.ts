// FILE: frontend/src/services/eventoCorporativoService.ts

import api from './api';
import { EventoCorporativoBase, EventoCorporativoRead } from '@/types/eventoCorporativo'; // Assumindo que você tem este tipo

const EVENTOS_CORPORATIVOS_BASE_URL = '/eventos-corporativos';

export const getEventosCorporativos = async (ativoId?: string): Promise<EventoCorporativoRead[]> => {
  const url = ativoId ? `${EVENTOS_CORPORATIVOS_BASE_URL}?ativo_id=${ativoId}` : EVENTOS_CORPORATIVOS_BASE_URL;
  const response = await api.get<EventoCorporativoRead[]>(url);
  return response.data;
};

// Esta função pode ser removida se a getEventosCorporativos acima já lida com o filtro
// export const getEventosCorporativosPorAtivo = async (ativoId: string): Promise<EventoCorporativoRead[]> => {
//   const response = await api.get<EventoCorporativoRead[]>(`${EVENTOS_CORPORATIVOS_BASE_URL}?ativo_id=${ativoId}`);
//   return response.data;
// };

export const createEventoCorporativo = async (data: EventoCorporativoBase): Promise<EventoCorporativoRead> => {
  const response = await api.post<EventoCorporativoRead>(EVENTOS_CORPORATIVOS_BASE_URL, data);
  return response.data;
};

export const processarEventoCorporativo = async (eventoId: string): Promise<EventoCorporativoRead> => {
  const response = await api.post<EventoCorporativoRead>(`${EVENTOS_CORPORATIVOS_BASE_URL}/${eventoId}/processar`);
  return response.data;
};