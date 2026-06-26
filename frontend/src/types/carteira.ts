// FILE: frontend/src/types/carteira.ts

import { TipoCarteira, ObjetivoCarteira } from './enums';

export { TipoCarteira, ObjetivoCarteira };

export interface Carteira {
  id: string;
  usuario_id: string;
  nome: string;
  tipo: TipoCarteira;
  objetivo: ObjetivoCarteira;
  descricao: string | null;
  ativa: boolean;
  saldo_inicial: number;
  saldo_atual: number;
  observacoes: string | null;
  created_at: string;
  updated_at: string;
}

export interface CarteiraCreate {
  usuario_id: string;
  nome: string;
  tipo: TipoCarteira;
  objetivo: ObjetivoCarteira;
  descricao: string | null;
  ativa: boolean;
  saldo_inicial: number;
  saldo_atual: number;
  observacoes: string | null;
}

export interface CarteiraUpdate {
  nome?: string;
  tipo?: TipoCarteira;
  objetivo?: ObjetivoCarteira;
  descricao?: string | null;
  ativa?: boolean;
  saldo_inicial?: number;
  saldo_atual?: number;
  observacoes?: string | null;
}