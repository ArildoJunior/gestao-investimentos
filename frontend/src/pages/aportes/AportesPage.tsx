// FILE: frontend/src/pages/aportes/AportesPage.tsx

import React, { useState } from 'react';
import { useAportes } from '@/hooks/useAportes';
import { useCarteiras } from '@/hooks/useCarteiras';
import { useContas } from '@/hooks/useContas';
import { TipoAporte, OrigemAporte, AporteCreate } from '@/types/aporte';

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

const AportesPage: React.FC = () => {
  const { carteiras, isLoading: isLoadingCarteiras } = useCarteiras();
  const { contas, isLoading: isLoadingContas } = useContas();
  const { toast } = useToast();

  const [selectedCarteiraId, setSelectedCarteiraId] = useState<string>('');
  const { aportes, createAporte } = useAportes(selectedCarteiraId);

  const [isFormOpen, setIsFormOpen] = useState(false);

  const getInitialFormData = (): AporteCreate => ({
    conta_id: '',
    carteira_id: selectedCarteiraId,
    tipo: TipoAporte.EXTERNO,
    origem: OrigemAporte.OUTRO,
    data_aporte: new Date().toISOString().split('T')[0],
    valor: 0,
    observacoes: null,
  });

  const [formData, setFormData] = useState<AporteCreate>(getInitialFormData());

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setFormData(getInitialFormData());
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    if (name === 'valor') {
      const cleanValue = value.replace(',', '.');
      if (cleanValue === '' || cleanValue === '.') {
        setFormData((prev) => ({ ...prev, [name]: 0 }));
      } else {
        const numValue = parseFloat(cleanValue);
        if (!isNaN(numValue)) {
          setFormData((prev) => ({ ...prev, [name]: numValue }));
        }
      }
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.carteira_id || !formData.conta_id || formData.valor <= 0) {
      toast({
        title: 'Erro',
        description: 'Por favor, preencha os campos obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    try {
      await createAporte(formData);
      toast({
        title: 'Sucesso!',
        description: 'Aporte registrado com sucesso.',
      });
      handleCloseForm();
    } catch (err) {
      let errorMessage = 'Erro desconhecido ao registrar aporte.';
      if (err instanceof AxiosError) {
        errorMessage = err.response?.data?.detail || err.message;
      }
      toast({
        title: 'Erro',
        description: `Falha ao registrar aporte: ${errorMessage}`,
        variant: 'destructive',
      });
    }
  };

  const formatarMoeda = (valor: number): string => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(valor);
  };

  const getNomeCarteira = (id: string): string => {
    return carteiras?.find((c) => c.id === id)?.nome || 'Desconhecida';
  };

  const getNomeConta = (id: string): string => {
    return contas?.find((c) => c.id === id)?.nome || 'Desconhecida';
  };

  if (isLoadingCarteiras || isLoadingContas) {
    return <div className="p-4">Carregando dados...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Aportes</h1>
        <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setIsFormOpen(true)}>Registrar Aporte</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>Registrar Novo Aporte</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
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

              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo" className="text-right">
                  Tipo *
                </Label>
                <Select
                  value={formData.tipo}
                  onValueChange={(value) => handleSelectChange('tipo', value as TipoAporte)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoAporte).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="origem" className="text-right">
                  Origem *
                </Label>
                <Select
                  value={formData.origem}
                  onValueChange={(value) => handleSelectChange('origem', value as OrigemAporte)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a origem" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(OrigemAporte).map((origem) => (
                      <SelectItem key={origem} value={origem}>
                        {origem}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="data_aporte" className="text-right">
                  Data *
                </Label>
                <Input
                  id="data_aporte"
                  name="data_aporte"
                  type="date"
                  value={formData.data_aporte}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                />
              </div>

              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="valor" className="text-right">
                  Valor *
                </Label>
                <Input
                  id="valor"
                  name="valor"
                  type="number"
                  step="0.01"
                  value={formData.valor}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                  required
                />
              </div>

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
                <Button type="submit">Registrar Aporte</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

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
              <TableHead>Conta</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Origem</TableHead>
              <TableHead className="text-right">Valor</TableHead>
              <TableHead>Data</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {aportes && aportes.length > 0 ? (
              aportes.map((aporte) => (
                <TableRow key={aporte.id}>
                  <TableCell>{getNomeCarteira(aporte.carteira_id)}</TableCell>
                  <TableCell>{getNomeConta(aporte.conta_id)}</TableCell>
                  <TableCell>{aporte.tipo}</TableCell>
                  <TableCell>{aporte.origem}</TableCell>
                  <TableCell className="text-right font-semibold">
                    {formatarMoeda(aporte.valor)}
                  </TableCell>
                  <TableCell>{aporte.data_aporte}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-4 text-gray-500">
                  Nenhum aporte registrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default AportesPage;