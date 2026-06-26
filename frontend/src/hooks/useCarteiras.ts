// FILE: frontend/src/hooks/useCarteiras.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { carteirasService } from '../services/carteirasService';
import { Carteira, CarteiraCreate, CarteiraUpdate } from '../types/carteira';

const CARTEIRAS_QUERY_KEY = 'carteiras';

export function useCarteiras() {
  const queryClient = useQueryClient();

  const { data: carteiras, isLoading, error } = useQuery<Carteira[], Error>({
    queryKey: [CARTEIRAS_QUERY_KEY],
    queryFn: carteirasService.getAllCarteiras,
  });

  const createCarteiraMutation = useMutation<Carteira, Error, CarteiraCreate>({
    mutationFn: carteirasService.createCarteira,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CARTEIRAS_QUERY_KEY] });
    },
  });

  const updateCarteiraMutation = useMutation<Carteira, Error, { id: string; data: CarteiraUpdate }>({
    mutationFn: ({ id, data }) => carteirasService.updateCarteira(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CARTEIRAS_QUERY_KEY] });
    },
  });

  const deleteCarteiraMutation = useMutation<void, Error, string>({
    mutationFn: carteirasService.deleteCarteira,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CARTEIRAS_QUERY_KEY] });
    },
  });

  return {
    carteiras,
    isLoading,
    error,
    createCarteira: createCarteiraMutation.mutateAsync,
    updateCarteira: updateCarteiraMutation.mutateAsync,
    deleteCarteira: deleteCarteiraMutation.mutateAsync,
  };
}