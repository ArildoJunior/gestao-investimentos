// FILE: frontend/src/types/provento.ts

import { TipoProvento } from './enums';

export { TipoProvento };

export interface ProventoRead {
  id: string;
  carteira_id: string;
  conta_id?: string;
  ativo_id: string;
  tipo: TipoProvento;
  valor_bruto: number;
  valor_liquido: number;
  data_com: string;
  data_pagamento: string;
  quantidade: number;
  reinvestido: boolean;
  observacoes?: string;
  created_at: string;
  updated_at: string;
}

export interface ProventoCreate {
  carteira_id: string;
  conta_id?: string;
  ativo_id: string;
  tipo: TipoProvento;
  valor_bruto: number;
  data_com: string;
  data_pagamento: string;
  quantidade: number;
  reinvestido: boolean;
  observacoes?: string;
}

export type ProventoList = ProventoRead[];

export interface FormProventoValues {
  carteira_id: string;
  conta_id?: string;
  ativo_id: string;
  tipo: TipoProvento;
  valor_bruto: number;
  data_com: Date;
  data_pagamento: Date;
  quantidade: number;
  reinvestido: boolean;
  observacoes?: string;
}