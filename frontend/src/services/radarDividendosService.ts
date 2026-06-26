// FILE: frontend/src/services/radarDividendosService.ts

import api from './api';

export interface RadarDividendosItem {
  id: string;
  ativo_id: string;
  ticker: string;
  carteira_id: string;
  tipo: string;
  data_com: string;
  data_pagamento: string;
  valor_bruto: number;
  valor_liquido: number;
  quantidade: number;
  valor_por_cota: number;
  reinvestido: boolean;
}

const RADAR_BASE_URL = '/radar-dividendos';

export const getRadarDividendos = async (
  dias: number = 90,
  ativoId?: string,
): Promise<RadarDividendosItem[]> => {
  const params = new URLSearchParams();
  params.set('dias', String(dias));
  if (ativoId) params.set('ativo_id', ativoId);

  const response = await api.get<RadarDividendosItem[]>(
    `${RADAR_BASE_URL}/?${params.toString()}`,
  );
  return response.data;
};