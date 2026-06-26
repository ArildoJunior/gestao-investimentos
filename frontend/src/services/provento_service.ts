// FILE: frontend/src/services/provento_service.ts

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from './api';
import { ProventoCreate, ProventoRead } from '../types/provento';

const BASE_URL = '/proventos/';

export const getProventos = async (carteiraId: string): Promise<ProventoRead[]> => {
  const response = await api.get<ProventoRead[]>(BASE_URL, {
    params: { carteira_id: carteiraId },
  });
  return response.data;
};

export const createProvento = async (provento: ProventoCreate): Promise<ProventoRead> => {
  const response = await api.post<ProventoRead>(BASE_URL, provento);
  return response.data;
};

export const useProventos = (carteiraId?: string) => {
  return useQuery<ProventoRead[], Error>({
    queryKey: ['proventos', carteiraId],
    queryFn: () => getProventos(carteiraId!),
    enabled: !!carteiraId,
  });
};

export const useCreateProvento = () => {
  const queryClient = useQueryClient();
  return useMutation<ProventoRead, Error, ProventoCreate>({
    mutationFn: createProvento,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['proventos'] });
    },
  });
};