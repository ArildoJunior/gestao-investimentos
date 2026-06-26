// FILE: frontend/src/hooks/useMovimentacoes.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { movimentacoesService } from '../services/movimentacoesService';
import { Movimentacao, MovimentacaoCreate } from '../types/movimentacao';

const MOVIMENTACOES_QUERY_KEY = 'movimentacoes';

export function useMovimentacoes(carteiraId?: string) {
  const queryClient = useQueryClient();

  const { data: movimentacoes, isLoading, error } = useQuery<Movimentacao[], Error>({
    queryKey: [MOVIMENTACOES_QUERY_KEY, carteiraId],
    queryFn: () => carteiraId ? movimentacoesService.getMovimentacoesByCarteira(carteiraId) : Promise.resolve([]),
    enabled: !!carteiraId,
  });

  const createMovimentacaoMutation = useMutation<Movimentacao, Error, MovimentacaoCreate>({
    mutationFn: movimentacoesService.createMovimentacao,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [MOVIMENTACOES_QUERY_KEY] });
    },
  });

  return {
    movimentacoes,
    isLoading,
    error,
    createMovimentacao: createMovimentacaoMutation.mutateAsync,
  };
}