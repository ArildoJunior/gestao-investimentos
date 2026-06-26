// FILE: frontend/src/types/conta.ts

import { TipoConta, StatusConta, Moeda } from './enums';

export { TipoConta, StatusConta, Moeda };

export interface Conta {
  id: string;
  instituicao_id: string;
  nome: string;
  tipo: TipoConta;
  moeda: Moeda;
  saldo_inicial: number;
  saldo_atual: number;
  data_abertura: string;
  status: StatusConta;
  created_at: string;
  updated_at: string;
}

export interface ContaCreate {
  instituicao_id: string;
  nome: string;
  tipo: TipoConta;
  moeda: Moeda;
  saldo_inicial: number;
  saldo_atual: number;
  data_abertura: string;
  status: StatusConta;
}

export interface ContaUpdate {
  instituicao_id?: string;
  nome?: string;
  tipo?: TipoConta;
  moeda?: Moeda;
  saldo_inicial?: number;
  saldo_atual?: number;
  data_abertura?: string;
  status?: StatusConta;
}