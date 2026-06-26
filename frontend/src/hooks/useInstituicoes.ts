// FILE: frontend/src/hooks/useInstituicoes.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { instituicoesService } from '../services/instituicoesService';
import { Instituicao, InstituicaoCreate, InstituicaoUpdate } from '../types/instituicao';

const INSTITUICOES_QUERY_KEY = 'instituicoes';

export function useInstituicoes() {
  const queryClient = useQueryClient();

  // Hook para buscar todas as instituições
  const { data: instituicoes, isLoading, error } = useQuery<Instituicao[], Error>({
    queryKey: [INSTITUICOES_QUERY_KEY],
    queryFn: instituicoesService.getAllInstituicoes,
  });

  // Hook para criar uma instituição
  const createInstituicaoMutation = useMutation<Instituicao, Error, InstituicaoCreate>({
    mutationFn: instituicoesService.createInstituicao,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [INSTITUICOES_QUERY_KEY] }); // Invalida o cache para buscar novamente
    },
  });

  // Hook para atualizar uma instituição
  const updateInstituicaoMutation = useMutation<Instituicao, Error, { id: string; data: InstituicaoUpdate }>({
    mutationFn: ({ id, data }) => instituicoesService.updateInstituicao(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [INSTITUICOES_QUERY_KEY] });
    },
  });

  // Hook para deletar uma instituição
  const deleteInstituicaoMutation = useMutation<void, Error, string>({
    mutationFn: instituicoesService.deleteInstituicao,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [INSTITUICOES_QUERY_KEY] });
    },
  });

  return {
    instituicoes,
    isLoading,
    error,
    createInstituicao: createInstituicaoMutation.mutateAsync,
    updateInstituicao: updateInstituicaoMutation.mutateAsync,
    deleteInstituicao: deleteInstituicaoMutation.mutateAsync,
  };
}