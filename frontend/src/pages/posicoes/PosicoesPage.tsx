// FILE: frontend/src/pages/posicoes/PosicoesPage.tsx

import React, { useState } from 'react';
import { usePosicoes } from '@/hooks/usePosicoes';
import { useCarteiras } from '@/hooks/useCarteiras';
import { useAtivos } from '@/hooks/useAtivos';
import { Posicao } from '@/types/posicao';

// Componentes shadcn/ui
import { Label } from '@/components/ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const PosicoesPage: React.FC = () => {
  const { carteiras, isLoading: isLoadingCarteiras } = useCarteiras();
  const { ativos, isLoading: isLoadingAtivos } = useAtivos();

  const [selectedCarteiraId, setSelectedCarteiraId] = useState<string>('');
  const { posicoes, isLoading: isLoadingPosicoes } = usePosicoes(selectedCarteiraId);

  const formatarMoeda = (valor: number): string => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(valor);
  };

  const getNomeCarteira = (id: string): string => {
    return carteiras?.find((c) => c.id === id)?.nome || 'Desconhecida';
  };

  const getNomeAtivo = (id: string): string => {
    const ativo = ativos?.find((a) => a.id === id);
    return ativo ? `${ativo.ticker} - ${ativo.nome}` : 'Desconhecido';
  };

  const calcularValorTotal = (posicao: Posicao): number => {
    return Number(posicao.quantidade) * Number(posicao.preco_medio);
  };

  if (isLoadingCarteiras || isLoadingAtivos) {
    return <div className="p-4">Carregando dados...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Posições</h1>

      {/* Seletor de Carteira */}
      <div className="mb-6">
        <Label htmlFor="filter-carteira">Filtrar por Carteira:</Label>
        <Select value={selectedCarteiraId} onValueChange={setSelectedCarteiraId}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Selecione uma carteira" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todas as carteiras</SelectItem>
            {carteiras?.map((carteira) => (
              <SelectItem key={carteira.id} value={carteira.id}>
                {carteira.nome}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Resumo da Carteira */}
      {selectedCarteiraId && (
        <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <h2 className="text-xl font-semibold mb-2">
            {getNomeCarteira(selectedCarteiraId)}
          </h2>
          {posicoes && posicoes.length > 0 && (
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600">Quantidade de Posições</p>
                <p className="text-2xl font-bold">{posicoes.length}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Valor Total Investido</p>
                <p className="text-2xl font-bold">
                  {formatarMoeda(
                    posicoes.reduce((acc, pos) => acc + Number(pos.custo_total), 0)
                  )}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Valor Atual</p>
                <p className="text-2xl font-bold">
                  {formatarMoeda(
                    posicoes.reduce((acc, pos) => acc + calcularValorTotal(pos), 0)
                  )}
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tabela de Posições */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Carteira</TableHead>
              <TableHead>Ativo</TableHead>
              <TableHead className="text-right">Quantidade</TableHead>
              <TableHead className="text-right">Preço Médio</TableHead>
              <TableHead className="text-right">Custo Total</TableHead>
              <TableHead className="text-right">Valor Atual</TableHead>
              <TableHead className="text-right">Ganho/Perda</TableHead>
              <TableHead className="text-right">%</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoadingPosicoes ? (
              <TableRow>
                <TableCell colSpan={8} className="text-center py-4">
                  Carregando posições...
                </TableCell>
              </TableRow>
            ) : posicoes && posicoes.length > 0 ? (
              posicoes.map((posicao) => {
                const valorAtual = calcularValorTotal(posicao);
                const custoTotal = Number(posicao.custo_total);
                const ganhoPerda = valorAtual - custoTotal;
                const percentual = custoTotal > 0 ? (ganhoPerda / custoTotal) * 100 : 0;

                return (
                  <TableRow key={posicao.id}>
                    <TableCell>{getNomeCarteira(posicao.carteira_id)}</TableCell>
                    <TableCell className="font-bold">{getNomeAtivo(posicao.ativo_id)}</TableCell>
                    <TableCell className="text-right">{posicao.quantidade}</TableCell>
                    <TableCell className="text-right">
                      {formatarMoeda(Number(posicao.preco_medio))}
                    </TableCell>
                    <TableCell className="text-right">{formatarMoeda(custoTotal)}</TableCell>
                    <TableCell className="text-right font-semibold">
                      {formatarMoeda(valorAtual)}
                    </TableCell>
                    <TableCell className={`text-right font-semibold ${
                      ganhoPerda >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {formatarMoeda(ganhoPerda)}
                    </TableCell>
                    <TableCell className={`text-right font-semibold ${
                      percentual >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {percentual.toFixed(2)}%
                    </TableCell>
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell colSpan={8} className="text-center py-4 text-gray-500">
                  {selectedCarteiraId
                    ? 'Nenhuma posição encontrada para esta carteira.'
                    : 'Selecione uma carteira para ver as posições.'}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default PosicoesPage;