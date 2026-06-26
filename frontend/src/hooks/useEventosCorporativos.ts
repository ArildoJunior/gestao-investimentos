// FILE: frontend/src/hooks/useEventosCorporativos.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getEventosCorporativos,
  // getEventosCorporativosPorAtivo, // Não é mais necessário se getEventosCorporativos lida com o filtro
  createEventoCorporativo,
  processarEventoCorporativo,
} from '../services/eventoCorporativoService';
import { EventoCorporativoBase, EventoCorporativoRead } from '../types/eventoCorporativo';

// Chaves de query para o TanStack Query
const EVENTOS_CORPORATIVOS_QUERY_KEY = 'eventosCorporativos';

export const useEventosCorporativos = (ativoId?: string) => {
  const queryClient = useQueryClient();

  // Hook para buscar todos os eventos corporativos ou eventos de um ativo específico
  const {
    data: eventos,
    isLoading,
    error,
    isError,
  } = useQuery<EventoCorporativoRead[], Error>({
    queryKey: [EVENTOS_CORPORATIVOS_QUERY_KEY, ativoId],
    queryFn: () => getEventosCorporativos(ativoId), // <-- Chamar a função unificada
    // A query sempre estará habilitada, mas o serviço lidará com o parâmetro ativoId
    // enabled: !!ativoId || ativoId === undefined, // Esta linha pode ser removida ou simplificada
  });

  // Hook para criar um novo evento corporativo
  const createMutation = useMutation<EventoCorporativoRead, Error, EventoCorporativoBase>({
    mutationFn: createEventoCorporativo,
    onSuccess: () => {
      // Invalida o cache para forçar a re-busca dos eventos corporativos
      queryClient.invalidateQueries({ queryKey: [EVENTOS_CORPORATIVOS_QUERY_KEY] });
    },
  });

  // Hook para processar um evento corporativo
  const processarMutation = useMutation<EventoCorporativoRead, Error, string>({
    mutationFn: processarEventoCorporativo,
    onSuccess: () => {
      // Invalida o cache para forçar a re-busca dos eventos corporativos
      queryClient.invalidateQueries({ queryKey: [EVENTOS_CORPORATIVOS_QUERY_KEY] });
    },
  });

  return {
    eventos,
    isLoading,
    error,
    isError,
    createEvento: createMutation.mutate,
    isCreating: createMutation.isPending,
    createError: createMutation.error,
    processarEvento: processarMutation.mutate,
    isProcessing: processarMutation.isPending,
    processarError: processarMutation.error,
  };
};