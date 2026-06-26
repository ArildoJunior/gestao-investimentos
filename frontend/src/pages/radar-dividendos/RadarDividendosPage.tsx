// FILE: frontend/src/pages/radar-dividendos/RadarDividendosPage.tsx

import { useState, useMemo } from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from '@tanstack/react-table';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { ArrowUpDown } from 'lucide-react';

import { RadarDividendosItem } from '@/services/radarDividendosService';
import { useRadarDividendos } from '@/hooks/useRadarDividendos';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const OPCOES_DIAS = [
  { label: 'Próximos 30 dias', value: 30 },
  { label: 'Próximos 60 dias', value: 60 },
  { label: 'Próximos 90 dias', value: 90 },
  { label: 'Próximos 180 dias', value: 180 },
  { label: 'Próximos 365 dias', value: 365 },
];

const formatarMoeda = (valor: number) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

const formatarData = (data: string) =>
  format(new Date(data + 'T00:00:00'), 'dd/MM/yyyy', { locale: ptBR });

export default function RadarDividendosPage() {
  "use no memo";

  const [dias, setDias] = useState(90);
  const [sorting, setSorting] = useState<SortingState>([]);

  const { data: itens, isLoading, isError, error } = useRadarDividendos(dias);

  const totalBruto = useMemo(
    () => (itens ?? []).reduce((acc, i) => acc + Number(i.valor_bruto), 0),
    [itens],
  );

  const totalLiquido = useMemo(
    () => (itens ?? []).reduce((acc, i) => acc + Number(i.valor_liquido), 0),
    [itens],
  );

  const columns: ColumnDef<RadarDividendosItem>[] = useMemo(
    () => [
      {
        accessorKey: 'ticker',
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
          >
            Ticker <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        ),
        cell: ({ row }) => (
          <span className="font-semibold">{row.original.ticker}</span>
        ),
      },
      {
        accessorKey: 'tipo',
        header: 'Tipo',
        cell: ({ row }) => (
          <Badge variant="secondary">{row.original.tipo}</Badge>
        ),
      },
      {
        accessorKey: 'data_com',
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
          >
            Data Com <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        ),
        cell: ({ row }) => formatarData(row.original.data_com),
      },
      {
        accessorKey: 'data_pagamento',
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
          >
            Pagamento <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        ),
        cell: ({ row }) => formatarData(row.original.data_pagamento),
      },
      {
        accessorKey: 'valor_por_cota',
        header: 'Valor/Cota',
        cell: ({ row }) =>
          formatarMoeda(Number(row.original.valor_por_cota)),
      },
      {
        accessorKey: 'quantidade',
        header: 'Qtd',
        cell: ({ row }) =>
          Number(row.original.quantidade).toLocaleString('pt-BR'),
      },
      {
        accessorKey: 'valor_bruto',
        header: 'Bruto',
        cell: ({ row }) => formatarMoeda(Number(row.original.valor_bruto)),
      },
      {
        accessorKey: 'valor_liquido',
        header: 'Líquido',
        cell: ({ row }) => formatarMoeda(Number(row.original.valor_liquido)),
      },
      {
        accessorKey: 'reinvestido',
        header: 'Reinvestido',
        cell: ({ row }) => (
          <Badge variant={row.original.reinvestido ? 'default' : 'outline'}>
            {row.original.reinvestido ? 'Sim' : 'Não'}
          </Badge>
        ),
      },
    ],
    [],
  );

  const table = useReactTable({
    data: itens ?? [],
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  if (isLoading) {
    return <div className="p-4">Carregando radar de dividendos...</div>;
  }

  if (isError) {
    return (
      <div className="p-4 text-red-500">
        Erro ao carregar radar: {error?.message}
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Radar de Dividendos</h1>
        <Select
          value={String(dias)}
          onValueChange={(v) => setDias(Number(v))}
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {OPCOES_DIAS.map((op) => (
              <SelectItem key={op.value} value={String(op.value)}>
                {op.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <div className="rounded-lg border p-4">
          <p className="text-sm text-muted-foreground">Eventos encontrados</p>
          <p className="text-2xl font-bold">{itens?.length ?? 0}</p>
        </div>
        <div className="rounded-lg border p-4">
          <p className="text-sm text-muted-foreground">Total Bruto</p>
          <p className="text-2xl font-bold">{formatarMoeda(totalBruto)}</p>
        </div>
        <div className="rounded-lg border p-4">
          <p className="text-sm text-muted-foreground">Total Líquido</p>
          <p className="text-2xl font-bold">{formatarMoeda(totalLiquido)}</p>
        </div>
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
                <TableRow key={row.id}>
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
                  Nenhum provento encontrado para o período selecionado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-end space-x-2">
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