// FILE: frontend/src/hooks/useContas.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { contasService } from '../services/contasService';
import { Conta, ContaCreate, ContaUpdate } from '../types/conta';

const CONTAS_QUERY_KEY = 'contas';

export function useContas() {
  const queryClient = useQueryClient();

  // Hook para buscar todas as contas
  const { data: contas, isLoading, error } = useQuery<Conta[], Error>({
    queryKey: [CONTAS_QUERY_KEY],
    queryFn: contasService.getAllContas,
  });

  // Hook para criar uma conta
  const createContaMutation = useMutation<Conta, Error, ContaCreate>({
    mutationFn: contasService.createConta,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CONTAS_QUERY_KEY] });
    },
  });

  // Hook para atualizar uma conta
  const updateContaMutation = useMutation<Conta, Error, { id: string; data: ContaUpdate }>({
    mutationFn: ({ id, data }) => contasService.updateConta(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CONTAS_QUERY_KEY] });
    },
  });

  // Hook para deletar uma conta
  const deleteContaMutation = useMutation<void, Error, string>({
    mutationFn: contasService.deleteConta,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CONTAS_QUERY_KEY] });
    },
  });

  return {
    contas,
    isLoading,
    error,
    createConta: createContaMutation.mutateAsync,
    updateConta: updateContaMutation.mutateAsync,
    deleteConta: deleteContaMutation.mutateAsync,
  };
}