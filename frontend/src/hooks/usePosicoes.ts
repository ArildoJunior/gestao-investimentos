// FILE: frontend/src/hooks/usePosicoes.ts

import { useQuery } from '@tanstack/react-query';
import { posicoeService } from '../services/posicoeService';
import { Posicao } from '../types/posicao';

const POSICOES_QUERY_KEY = 'posicoes';

export function usePosicoes(carteiraId?: string) {
  const { data: posicoes, isLoading, error } = useQuery<Posicao[], Error>({
    queryKey: [POSICOES_QUERY_KEY, carteiraId],
    queryFn: () => carteiraId ? posicoeService.getPosicoesByCarteira(carteiraId) : Promise.resolve([]),
    enabled: !!carteiraId,
  });

  return {
    posicoes,
    isLoading,
    error,
  };
}