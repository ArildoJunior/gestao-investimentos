// FILE: frontend/src/pages/proventos/ProventosPage.tsx

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';
import { DataTable } from '@/components/ui/data-table';
import { ColumnDef } from '@tanstack/react-table';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

import { ProventoRead, TipoProvento } from '@/types/provento';
import { useProventos, useCreateProvento } from '@/services/provento_service';
import { useCarteiras } from '@/services/carteirasService';
import { useAtivos } from '@/hooks/useAtivos';
import { FormProvento } from './components/FormProvento';

interface FormProventoValues {
  carteira_id: string;
  conta_id?: string;
  ativo_id: string;
  tipo: TipoProvento;
  valor_bruto: string;
  data_com: Date;
  data_pagamento: Date;
  quantidade: string;
  reinvestido: boolean;
  observacoes?: string;
}

const ProventosPage: React.FC = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [carteiraIdSelecionada, setCarteiraIdSelecionada] = useState<string | undefined>(undefined);

  const { data: carteiras } = useCarteiras();
  const { data: ativos } = useAtivos();
  const { data: proventos, isLoading, isError } = useProventos(carteiraIdSelecionada);
  const createProventoMutation = useCreateProvento();

  const handleCreateProvento = async (formData: FormProventoValues) => {
    try {
      await createProventoMutation.mutateAsync({
        carteira_id: formData.carteira_id,
        conta_id: formData.conta_id,
        ativo_id: formData.ativo_id,
        tipo: formData.tipo,
        valor_bruto: parseFloat(formData.valor_bruto.replace(',', '.')),
        data_com: format(formData.data_com, 'yyyy-MM-dd'),
        data_pagamento: format(formData.data_pagamento, 'yyyy-MM-dd'),
        quantidade: parseFloat(formData.quantidade.replace(',', '.')),
        reinvestido: formData.reinvestido,
        observacoes: formData.observacoes,
      });
      setIsFormOpen(false);
    } catch (error) {
      console.error('Erro ao criar provento:', error);
    }
  };

  const columns: ColumnDef<ProventoRead>[] = [
    {
      accessorKey: 'data_com',
      header: 'Data Com',
      cell: ({ row }) =>
        format(new Date(row.getValue('data_com') as string), 'dd/MM/yyyy', { locale: ptBR }),
    },
    {
      accessorKey: 'data_pagamento',
      header: 'Data Pagamento',
      cell: ({ row }) =>
        format(new Date(row.getValue('data_pagamento') as string), 'dd/MM/yyyy', { locale: ptBR }),
    },
    {
      accessorKey: 'ativo_id',
      header: 'Ativo',
      cell: ({ row }) => {
        const ativoId = row.getValue('ativo_id') as string;
        const ativo = ativos?.find((a) => a.id === ativoId);
        return ativo ? ativo.ticker : ativoId;
      },
    },
    {
      accessorKey: 'tipo',
      header: 'Tipo',
      cell: ({ row }) => (
        <Badge variant="outline">{row.getValue('tipo') as TipoProvento}</Badge>
      ),
    },
    {
      accessorKey: 'valor_bruto',
      header: 'Valor Bruto',
      cell: ({ row }) =>
        new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(
          parseFloat(row.getValue('valor_bruto'))
        ),
    },
    {
      accessorKey: 'quantidade',
      header: 'Quantidade',
      cell: ({ row }) => {
        const qtd = parseFloat(row.getValue('quantidade'));
        return Number.isInteger(qtd)
          ? qtd.toString()
          : qtd.toLocaleString('pt-BR', { maximumFractionDigits: 4 });
      },
    },
    {
      accessorKey: 'reinvestido',
      header: 'Reinvestido',
      cell: ({ row }) => (row.getValue('reinvestido') ? 'Sim' : 'Não'),
    },
  ];

  return (
    <div className="p-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-2xl font-bold">Proventos</CardTitle>
          <div className="flex items-center gap-3">
            <Select
              value={carteiraIdSelecionada}
              onValueChange={(val) => setCarteiraIdSelecionada(val)}
            >
              <SelectTrigger className="w-[220px]">
                <SelectValue placeholder="Selecione a carteira" />
              </SelectTrigger>
              <SelectContent>
                {carteiras?.map((carteira) => (
                  <SelectItem key={carteira.id} value={carteira.id}>
                    {carteira.nome}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
              <DialogTrigger asChild>
                <Button size="sm" className="h-8 gap-1">
                  <PlusCircle className="h-3.5 w-3.5" />
                  <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                    Adicionar Provento
                  </span>
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px]">
                <DialogHeader>
                  <DialogTitle>Adicionar Novo Provento</DialogTitle>
                  <DialogDescription>
                    Preencha os detalhes para registrar um novo provento.
                  </DialogDescription>
                </DialogHeader>
                <FormProvento onSubmit={handleCreateProvento} />
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          {!carteiraIdSelecionada ? (
            <p className="text-center text-gray-500 py-8">
              Selecione uma carteira para visualizar os proventos.
            </p>
          ) : isLoading ? (
            <p className="text-center py-8">Carregando proventos...</p>
          ) : isError ? (
            <p className="text-center text-red-500 py-8">Erro ao carregar proventos.</p>
          ) : proventos && proventos.length > 0 ? (
            <DataTable columns={columns} data={proventos} />
          ) : (
            <p className="text-center text-gray-500 py-8">
              Nenhum provento encontrado para esta carteira.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ProventosPage;