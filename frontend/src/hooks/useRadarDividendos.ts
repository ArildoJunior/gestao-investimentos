// FILE: frontend/src/hooks/useRadarDividendos.ts

import { useQuery } from '@tanstack/react-query';
import { getRadarDividendos, RadarDividendosItem } from '@/services/radarDividendosService';

export const useRadarDividendos = (dias: number = 90, ativoId?: string) => {
  return useQuery<RadarDividendosItem[], Error>({
    queryKey: ['radarDividendos', dias, ativoId],
    queryFn: () => getRadarDividendos(dias, ativoId),
  });
};