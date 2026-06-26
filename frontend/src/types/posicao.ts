// FILE: frontend/src/types/posicao.ts

export interface Posicao {
  id: string; // UUID
  carteira_id: string; // UUID
  conta_id: string; // UUID
  ativo_id: string; // UUID
  quantidade: number;
  preco_medio: number;
  custo_total: number;
}