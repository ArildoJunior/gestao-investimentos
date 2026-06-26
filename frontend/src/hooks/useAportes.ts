// FILE: frontend/src/hooks/useAportes.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { aporteService } from '@/services/aporteService';
import { AporteCreate } from '@/types/aporte';

export const useAportes = (carteiraId?: string) => {
  const queryClient = useQueryClient();

  const { data: aportes, isLoading, error } = useQuery({
    queryKey: ['aportes', carteiraId],
    queryFn: async () => {
      if (!carteiraId) return [];
      return aporteService.getAportesByCarteira(carteiraId);
    },
  });

  const createMutation = useMutation({
    mutationFn: (data: AporteCreate) => aporteService.createAporte(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['aportes', carteiraId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: AporteCreate }) =>
      aporteService.updateAporte(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['aportes', carteiraId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => aporteService.deleteAporte(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['aportes', carteiraId] });
    },
  });

  return {
    aportes: aportes || [],
    isLoading,
    error,
    createAporte: createMutation.mutateAsync,
    updateAporte: updateMutation.mutateAsync,
    deleteAporte: deleteMutation.mutateAsync,
  };
};