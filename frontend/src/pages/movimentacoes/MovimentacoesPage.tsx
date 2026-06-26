// FILE: frontend/src/pages/movimentacoes/MovimentacoesPage.tsx

import React, { useState } from 'react';
import { useMovimentacoes } from '@/hooks/useMovimentacoes';
import { useCarteiras } from '@/hooks/useCarteiras';
import { useContas } from '@/hooks/useContas';
import { useAtivos } from '@/hooks/useAtivos';
import { TipoMovimentacao, TipoOperacao, MovimentacaoCreate } from '@/types/movimentacao';

// Componentes shadcn/ui
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
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
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { AxiosError } from 'axios';

const MovimentacoesPage: React.FC = () => {
  const { carteiras, isLoading: isLoadingCarteiras } = useCarteiras();
  const { contas, isLoading: isLoadingContas } = useContas();
  const { ativos, isLoading: isLoadingAtivos } = useAtivos();
  const { toast } = useToast();

  const [selectedCarteiraId, setSelectedCarteiraId] = useState<string>('');
  const { movimentacoes, createMovimentacao } = useMovimentacoes(selectedCarteiraId);

  const [isFormOpen, setIsFormOpen] = useState(false);

  const getInitialFormData = (): MovimentacaoCreate => ({
    carteira_id: selectedCarteiraId,
    conta_id: '',
    ativo_id: '',
    tipo_movimentacao: TipoMovimentacao.COMPRA,
    tipo_operacao: TipoOperacao.POSITION,
    data_operacao: new Date().toISOString().split('T')[0],
    data_liquidacao: new Date().toISOString().split('T')[0],
    quantidade: 0,
    preco_unitario: 0,
    corretagem: 0,
    emolumentos: 0,
    iss: 0,
    outras_taxas: 0,
    observacoes: null,
  });

  const [formData, setFormData] = useState<MovimentacaoCreate>(getInitialFormData());

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setFormData(getInitialFormData());
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    // Campos que devem ser tratados como decimal
    const decimalFields = [
      'quantidade',
      'preco_unitario',
      'corretagem',
      'emolumentos',
      'iss',
      'outras_taxas',
    ];

    if (decimalFields.includes(name)) {
      // Permitir números, ponto e vírgula
      const cleanValue = value.replace(',', '.');

      // Se estiver vazio, usar 0
      if (cleanValue === '' || cleanValue === '.') {
        setFormData((prev) => ({
          ...prev,
          [name]: 0,
        }));
      } else {
        // Tentar converter para número
        const numValue = parseFloat(cleanValue);
        if (!isNaN(numValue)) {
          setFormData((prev) => ({
            ...prev,
            [name]: numValue,
          }));
        }
      }
    } else {
      // Outros campos são strings normais
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSelectChange = (name: string, value: string) => {
    const finalValue = value === '' ? null : value;
    setFormData((prev) => ({ ...prev, [name]: finalValue }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.carteira_id || !formData.conta_id || !formData.ativo_id) {
      toast({
        title: 'Erro',
        description: 'Por favor, preencha os campos obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    if (formData.quantidade <= 0 || formData.preco_unitario <= 0) {
      toast({
        title: 'Erro',
        description: 'Quantidade e Preço Unitário devem ser maiores que zero.',
        variant: 'destructive',
      });
      return;
    }

    try {
      const dataToSend: MovimentacaoCreate = {
        carteira_id: formData.carteira_id,
        conta_id: formData.conta_id,
        ativo_id: formData.ativo_id,
        tipo_movimentacao: formData.tipo_movimentacao,
        tipo_operacao: formData.tipo_operacao,
        data_operacao: formData.data_operacao,
        data_liquidacao: formData.data_liquidacao,
        quantidade: formData.quantidade,
        preco_unitario: formData.preco_unitario,
        corretagem: formData.corretagem,
        emolumentos: formData.emolumentos,
        iss: formData.iss,
        outras_taxas: formData.outras_taxas,
        observacoes: formData.observacoes || null,
      };

      console.log('Enviando dados:', dataToSend);

      await createMovimentacao(dataToSend);
      toast({
        title: 'Sucesso!',
        description: 'Movimentação registrada com sucesso.',
      });
      handleCloseForm();
    } catch (err) {
      let errorMessage = 'Erro desconhecido ao registrar movimentação.';
      if (err instanceof AxiosError) {
        console.error('Erro da API:', err.response?.data);
        errorMessage = err.response?.data?.detail || err.message;
      }
      toast({
        title: 'Erro',
        description: `Falha ao registrar movimentação: ${errorMessage}`,
        variant: 'destructive',
      });
      console.error('Erro ao registrar movimentação:', err);
    }
  };

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
    return ativos?.find((a) => a.id === id)?.ticker || 'Desconhecido';
  };

  if (isLoadingCarteiras || isLoadingContas || isLoadingAtivos) {
    return <div className="p-4">Carregando dados...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Movimentações</h1>
        <Dialog open={isFormOpen} onOpenChange={(open) => {
          if (!open) handleCloseForm();
          else setIsFormOpen(true);
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => setIsFormOpen(true)}>
              Registrar Movimentação
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Registrar Nova Movimentação</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
              {/* Campo Carteira */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="carteira_id" className="text-right">
                  Carteira *
                </Label>
                <Select
                  value={formData.carteira_id}
                  onValueChange={(value) => {
                    setSelectedCarteiraId(value);
                    handleSelectChange('carteira_id', value);
                  }}
                >
                  <SelectTrigger className="col-span-3">
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
              </div>

              {/* Campo Conta */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="conta_id" className="text-right">
                  Conta *
                </Label>
                <Select
                  value={formData.conta_id}
                  onValueChange={(value) => handleSelectChange('conta_id', value)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a conta" />
                  </SelectTrigger>
                  <SelectContent>
                    {contas?.map((conta) => (
                      <SelectItem key={conta.id} value={conta.id}>
                        {conta.nome}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Ativo */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="ativo_id" className="text-right">
                  Ativo *
                </Label>
                <Select
                  value={formData.ativo_id}
                  onValueChange={(value) => handleSelectChange('ativo_id', value)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o ativo" />
                  </SelectTrigger>
                  <SelectContent>
                    {ativos?.map((ativo) => (
                      <SelectItem key={ativo.id} value={ativo.id}>
                        {ativo.ticker} - {ativo.nome}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Tipo Movimentação */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo_movimentacao" className="text-right">
                  Tipo *
                </Label>
                <Select
                  value={formData.tipo_movimentacao}
                  onValueChange={(value) =>
                    handleSelectChange('tipo_movimentacao', value as TipoMovimentacao)
                  }
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoMovimentacao).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Tipo Operação */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo_operacao" className="text-right">
                  Operação *
                </Label>
                <Select
                  value={formData.tipo_operacao}
                  onValueChange={(value) =>
                    handleSelectChange('tipo_operacao', value as TipoOperacao)
                  }
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a operação" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoOperacao).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Data Operação */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="data_operacao" className="text-right">
                  Data Operação *
                </Label>
                <Input
                  id="data_operacao"
                  name="data_operacao"
                  type="date"
                  value={formData.data_operacao}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                />
              </div>

              {/* Campo Data Liquidação */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="data_liquidacao" className="text-right">
                  Data Liquidação *
                </Label>
                <Input
                  id="data_liquidacao"
                  name="data_liquidacao"
                  type="date"
                  value={formData.data_liquidacao}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                />
              </div>

              {/* Campo Quantidade */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="quantidade" className="text-right">
                  Quantidade *
                </Label>
                <Input
                  id="quantidade"
                  name="quantidade"
                  type="number"
                  step="0.01"
                  value={formData.quantidade}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                  required
                />
              </div>

              {/* Campo Preço Unitário */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="preco_unitario" className="text-right">
                  Preço Unitário *
                </Label>
                <Input
                  id="preco_unitario"
                  name="preco_unitario"
                  type="number"
                  step="0.01"
                  value={formData.preco_unitario}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                  required
                />
              </div>

              {/* Campo Corretagem */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="corretagem" className="text-right">
                  Corretagem
                </Label>
                <Input
                  id="corretagem"
                  name="corretagem"
                  type="number"
                  step="0.01"
                  value={formData.corretagem}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Emolumentos */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="emolumentos" className="text-right">
                  Emolumentos
                </Label>
                <Input
                  id="emolumentos"
                  name="emolumentos"
                  type="number"
                  step="0.01"
                  value={formData.emolumentos}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo ISS */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="iss" className="text-right">
                  ISS
                </Label>
                <Input
                  id="iss"
                  name="iss"
                  type="number"
                  step="0.01"
                  value={formData.iss}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Outras Taxas */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="outras_taxas" className="text-right">
                  Outras Taxas
                </Label>
                <Input
                  id="outras_taxas"
                  name="outras_taxas"
                  type="number"
                  step="0.01"
                  value={formData.outras_taxas}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Observações */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="observacoes" className="text-right">
                  Observações
                </Label>
                <Input
                  id="observacoes"
                  name="observacoes"
                  value={formData.observacoes || ''}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="Observações adicionais"
                />
              </div>

              <DialogFooter>
                <Button type="submit">Registrar Movimentação</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Seletor de Carteira para Filtro */}
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

      <div className="rounded-md border overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Carteira</TableHead>
              <TableHead>Ativo</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Operação</TableHead>
              <TableHead className="text-right">Quantidade</TableHead>
              <TableHead className="text-right">Preço Unit.</TableHead>
              <TableHead className="text-right">Valor Bruto</TableHead>
              <TableHead className="text-right">Taxas</TableHead>
              <TableHead className="text-right">Valor Líquido</TableHead>
              <TableHead>Data</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {movimentacoes && movimentacoes.length > 0 ? (
              movimentacoes.map((mov) => (
                <TableRow key={mov.id}>
                  <TableCell>{getNomeCarteira(mov.carteira_id)}</TableCell>
                  <TableCell className="font-bold">{getNomeAtivo(mov.ativo_id)}</TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 rounded text-xs font-semibold ${
                        mov.tipo_movimentacao === TipoMovimentacao.COMPRA
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {mov.tipo_movimentacao}
                    </span>
                  </TableCell>
                  <TableCell>{mov.tipo_operacao}</TableCell>
                  <TableCell className="text-right">{Number(mov.quantidade).toFixed(2)}</TableCell>
                  <TableCell className="text-right">
                    {formatarMoeda(Number(mov.preco_unitario))}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatarMoeda(Number(mov.valor_bruto))}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatarMoeda(
                      Number(mov.corretagem) +
                        Number(mov.emolumentos) +
                        Number(mov.iss) +
                        Number(mov.outras_taxas)
                    )}
                  </TableCell>
                  <TableCell className="text-right font-semibold">
                    {formatarMoeda(Number(mov.valor_liquido))}
                  </TableCell>
                  <TableCell>{mov.data_operacao}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={10} className="text-center py-4 text-gray-500">
                  Nenhuma movimentação registrada.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default MovimentacoesPage;