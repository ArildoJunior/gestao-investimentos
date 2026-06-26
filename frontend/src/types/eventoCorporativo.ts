// FILE: frontend/src/types/eventoCorporativo.ts

import { TipoEventoCorporativo } from "./enums";

export interface EventoCorporativoBase {
  ativo_id: string;
  tipo: TipoEventoCorporativo; // Corrigido para 'tipo'
  data_evento: string; // Corrigido para 'data_evento' e tipo string (ISO 8601)
  data_ex: string; // Mantido, pois o backend tem data_ex
  data_pagamento?: string | null; // Adicionado
  fator?: number | null; // Tornar opcional e nullable
  valor?: number | null; // Adicionado
  ativo_destino_id?: string | null;
  observacoes?: string | null;
}

export interface EventoCorporativoRead extends EventoCorporativoBase {
  id: string;
  processado: boolean;
  created_at: string;
  updated_at: string;
}