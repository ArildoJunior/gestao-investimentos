// FILE: frontend/src/types/ativo.ts

import { TipoAtivo, StatusAtivo, RegiaoAtivo, SegmentoFII, Moeda } from './enums';

export { TipoAtivo, StatusAtivo, RegiaoAtivo, SegmentoFII, Moeda };

export interface Ativo {
  id: string;
  ticker: string;
  nome: string;
  classe: TipoAtivo;
  setor?: string | null;
  segmento_fii?: string | null;
  pais: string;
  regiao: RegiaoAtivo;
  moeda: Moeda;
  status: StatusAtivo;
  created_at: string;
  updated_at: string;
}

export interface AtivoCreate {
  ticker: string;
  nome: string;
  classe: TipoAtivo;
  setor?: string | null;
  segmento_fii?: string | null;
  pais: string;
  regiao: RegiaoAtivo;
  moeda: Moeda;
  status: StatusAtivo;
}

export interface AtivoUpdate {
  ticker?: string;
  nome?: string;
  classe?: TipoAtivo;
  setor?: string | null;
  segmento_fii?: string | null;
  pais?: string;
  regiao?: RegiaoAtivo;
  moeda?: Moeda;
  status?: StatusAtivo;
}