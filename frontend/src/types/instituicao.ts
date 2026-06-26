// FILE: frontend/src/types/instituicao.ts

import { TipoInstituicao, StatusInstituicao } from './enums';

export { TipoInstituicao, StatusInstituicao };

export interface InstituicaoCreate {
  nome: string;
  tipo: TipoInstituicao;
  status: StatusInstituicao;
  site?: string | null;
  observacoes?: string | null;
}

export interface InstituicaoRead extends InstituicaoCreate {
  id: string;
  created_at: string;
  updated_at: string;
}