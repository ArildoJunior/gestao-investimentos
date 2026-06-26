// FILE: frontend/src/types/aporte.ts

import { TipoAporte, OrigemAporte } from './enums';

export { TipoAporte, OrigemAporte };

export interface AporteCreate {
  carteira_id: string;
  conta_id?: string | null;
  tipo: TipoAporte;
  origem?: OrigemAporte | null;
  data_aporte: string;
  valor: number;
  observacao?: string | null;
}

export interface AporteRead extends AporteCreate {
  id: string;
  created_at: string;
  updated_at: string;
}