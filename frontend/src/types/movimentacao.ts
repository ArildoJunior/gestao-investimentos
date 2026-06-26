// FILE: frontend/src/types/movimentacao.ts

import { TipoMovimentacao, TipoOperacao } from './enums';

export { TipoMovimentacao, TipoOperacao };

export interface Movimentacao {
  id: string;
  carteira_id: string;
  conta_id: string;
  ativo_id: string;
  tipo_movimentacao: TipoMovimentacao;
  tipo_operacao: TipoOperacao;
  data_operacao: string;
  data_liquidacao: string;
  quantidade: number;
  preco_unitario: number;
  corretagem: number;
  emolumentos: number;
  iss: number;
  outras_taxas: number;
  valor_bruto: number;
  valor_liquido: number;
  observacoes: string | null;
}

export interface MovimentacaoCreate {
  carteira_id: string;
  conta_id: string;
  ativo_id: string;
  tipo_movimentacao: TipoMovimentacao;
  tipo_operacao: TipoOperacao;
  data_operacao: string;
  data_liquidacao: string;
  quantidade: number;
  preco_unitario: number;
  corretagem: number;
  emolumentos: number;
  iss: number;
  outras_taxas: number;
  observacoes: string | null;
}