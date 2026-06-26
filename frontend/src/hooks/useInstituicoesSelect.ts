// FILE: frontend/src/hooks/useInstituicoesSelect.ts

import { useQuery } from '@tanstack/react-query';
import { instituicoesService } from '../services/instituicoesService';
import { Instituicao } from '../types/instituicao';

const INSTITUICOES_SELECT_QUERY_KEY = 'instituicoes-select';

export function useInstituicoesSelect() {
  const { data: instituicoes, isLoading, error } = useQuery<Instituicao[], Error>({
    queryKey: [INSTITUICOES_SELECT_QUERY_KEY],
    queryFn: instituicoesService.getAllInstituicoes,
  });

  return {
    instituicoes,
    isLoading,
    error,
  };
}