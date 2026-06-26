// FILE: frontend/src/hooks/useAtivos.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ativosService } from '@/services/ativosService'; // Ajuste o caminho de importação
import { Ativo, AtivoCreate, AtivoUpdate } from '@/types/ativo'; // Ajuste o caminho de importação

const ATIVOS_QUERY_KEY = 'ativos';

export function useAtivos() {
  const queryClient = useQueryClient();

  // Hook para buscar todos os ativos
  const { data: ativos, isLoading, error } = useQuery<Ativo[], Error>({
    queryKey: [ATIVOS_QUERY_KEY],
    queryFn: ativosService.getAllAtivos,
    staleTime: 1000 * 60 * 5, // Dados considerados "frescos" por 5 minutos
  });

  // Hook para criar um ativo
  const createAtivoMutation = useMutation<Ativo, Error, AtivoCreate>({
    mutationFn: ativosService.createAtivo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [ATIVOS_QUERY_KEY] });
    },
  });

  // Hook para atualizar um ativo
  const updateAtivoMutation = useMutation<Ativo, Error, { id: string; data: AtivoUpdate }>({
    mutationFn: ({ id, data }) => ativosService.updateAtivo(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [ATIVOS_QUERY_KEY] });
    },
  });

  // Hook para deletar um ativo
  const deleteAtivoMutation = useMutation<void, Error, string>({
    mutationFn: ativosService.deleteAtivo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [ATIVOS_QUERY_KEY] });
    },
  });

  return {
    ativos,
    isLoading,
    error,
    createAtivo: createAtivoMutation.mutateAsync,
    updateAtivo: updateAtivoMutation.mutateAsync,
    deleteAtivo: deleteAtivoMutation.mutateAsync,
  };
}