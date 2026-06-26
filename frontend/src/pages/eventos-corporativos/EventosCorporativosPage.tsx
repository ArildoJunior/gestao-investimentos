// FILE: frontend/src/pages/eventos-corporativos/EventosCorporativosPage.tsx

import { useState, useMemo } from 'react';
import { ColumnDef, flexRender, getCoreRowModel, useReactTable, getPaginationRowModel, getFilteredRowModel } from '@tanstack/react-table';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { PlusCircle, Search } from 'lucide-react';

import { EventoCorporativoRead } from '@/types/eventoCorporativo';
import { TipoEventoCorporativo } from '@/types/enums';
import { useEventosCorporativos } from '@/hooks/useEventosCorporativos';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ColunaAcoes } from './components/ColunaAcoes';
import { FormEventoCorporativo } from './components/FormEventoCorporativo';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';

export default function EventosCorporativosPage() {
  "use no memo"; // DEVE ser o primeiro statement da função, sem comentários antes

  const [ativoIdFilter, setAtivoIdFilter] = useState<string | undefined>(undefined);
  const [tipoEventoFilter, setTipoEventoFilter] = useState<TipoEventoCorporativo | 'TODOS'>('TODOS');
  const [isFormOpen, setIsFormOpen] = useState(false);

  const { eventos, isLoading, isError, error } = useEventosCorporativos(ativoIdFilter);

  const filteredEventos = useMemo(() => {
    if (!eventos) return [];
    if (tipoEventoFilter === 'TODOS') return eventos;
    return eventos.filter(evento => evento.tipo === tipoEventoFilter);
  }, [eventos, tipoEventoFilter]);

  const getTipoEventoBadgeVariant = (tipo: TipoEventoCorporativo) => {
    switch (tipo) {
      case TipoEventoCorporativo.SPLIT:
      case TipoEventoCorporativo.GRUPAMENTO:
        return 'default';
      case TipoEventoCorporativo.BONIFICACAO:
      case TipoEventoCorporativo.SUBSCRICAO:
        return 'secondary';
      case TipoEventoCorporativo.AMORTIZACAO:
        return 'outline';
      default:
        return 'default';
    }
  };

  const columns: ColumnDef<EventoCorporativoRead>[] = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: 'ID',
        cell: ({ row }) => <div className="w-[80px] truncate">{row.original.id}</div>,
      },
      {
        accessorKey: 'ativo_id',
        header: 'Ativo',
        cell: ({ row }) => row.original.ativo_id,
      },
      {
        accessorKey: 'tipo',
        header: 'Tipo',
        cell: ({ row }) => (
          <Badge variant={getTipoEventoBadgeVariant(row.original.tipo)}>
            {row.original.tipo}
          </Badge>
        ),
      },
      {
        accessorKey: 'data_evento',
        header: 'Data Evento',
        cell: ({ row }) =>
          row.original.data_evento
            ? format(new Date(row.original.data_evento), 'dd/MM/yyyy', { locale: ptBR })
            : '-',
      },
      {
        accessorKey: 'data_ex',
        header: 'Data Ex',
        cell: ({ row }) =>
          row.original.data_ex
            ? format(new Date(row.original.data_ex), 'dd/MM/yyyy', { locale: ptBR })
            : '-',
      },
      {
        accessorKey: 'data_pagamento',
        header: 'Pagamento',
        cell: ({ row }) =>
          row.original.data_pagamento
            ? format(new Date(row.original.data_pagamento), 'dd/MM/yyyy', { locale: ptBR })
            : '-',
      },
      {
        accessorKey: 'fator',
        header: 'Fator',
        cell: ({ row }) => row.original.fator ?? '-',
      },
      {
        accessorKey: 'processado',
        header: 'Processado',
        cell: ({ row }) => (
          <Badge variant={row.original.processado ? 'default' : 'destructive'}>
            {row.original.processado ? 'Sim' : 'Não'}
          </Badge>
        ),
      },
      {
        id: 'acoes',
        header: 'Ajustes',
        cell: ({ row }) => <ColunaAcoes row={row} />,
      },
    ],
    []
  );

  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    data: filteredEventos,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      globalFilter: ativoIdFilter,
    },
    onGlobalFilterChange: (value) => setAtivoIdFilter(value || undefined),
  });

  if (isLoading) {
    return <div className="p-4">Carregando eventos corporativos...</div>;
  }

  if (isError) {
    return (
      <div className="p-4 text-red-500">
        Erro ao carregar eventos corporativos: {error?.message}
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Eventos Corporativos</h1>
        <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setIsFormOpen(true)}>
              <PlusCircle className="mr-2 h-4 w-4" /> Novo Evento
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Registrar Novo Evento Corporativo</DialogTitle>
            </DialogHeader>
            <FormEventoCorporativo onClose={() => setIsFormOpen(false)} />
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex items-center gap-2 py-4">
        <div className="relative flex-1">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Filtrar por ID do Ativo..."
            value={ativoIdFilter || ''}
            onChange={(event) => setAtivoIdFilter(event.target.value || undefined)}
            className="pl-8 max-w-sm"
          />
        </div>
        <Select
          value={tipoEventoFilter}
          onValueChange={(value: TipoEventoCorporativo | 'TODOS') => setTipoEventoFilter(value)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filtrar por Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="TODOS">Todos os Tipos</SelectItem>
            {Object.values(TipoEventoCorporativo).map((tipo) => (
              <SelectItem key={tipo} value={tipo}>
                {tipo}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && 'selected'}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  Nenhum evento corporativo encontrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-end space-x-2 py-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Anterior
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Próxima
        </Button>
      </div>
    </div>
  );
}