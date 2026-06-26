// FILE: frontend/src/pages/carteiras/CarteirasPage.tsx

import React, { useState } from 'react';
import { useCarteiras } from '@/hooks/useCarteiras';
import { Carteira, TipoCarteira, ObjetivoCarteira, CarteiraCreate } from '@/types/carteira';

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

const CarteirasPage: React.FC = () => {
  const { carteiras, isLoading, error, createCarteira, updateCarteira, deleteCarteira } = useCarteiras();
  const { toast } = useToast();

  // Garantir que existe um usuario_id no localStorage
  React.useEffect(() => {
    if (!localStorage.getItem('usuario_id')) {
      // Gerar um UUID temporário para testes
      const tempUserId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
      localStorage.setItem('usuario_id', tempUserId);
    }
  }, []);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingCarteira, setEditingCarteira] = useState<Carteira | null>(null);

  // Obter usuario_id do localStorage (você precisará implementar autenticação)
  const usuarioId = localStorage.getItem('usuario_id') || '';

  const getInitialFormData = (carteira: Carteira | null): CarteiraCreate => {
    if (carteira) {
      return {
        usuario_id: carteira.usuario_id,
        nome: carteira.nome,
        tipo: carteira.tipo,
        objetivo: carteira.objetivo,
        descricao: carteira.descricao || null,
        ativa: carteira.ativa,
        saldo_inicial: carteira.saldo_inicial,
        saldo_atual: carteira.saldo_atual,
        observacoes: carteira.observacoes || null,
      };
    }
    return {
      usuario_id: usuarioId,
      nome: '',
      tipo: TipoCarteira.REAL,
      objetivo: ObjetivoCarteira.LIVRE,
      descricao: null,
      ativa: true,
      saldo_inicial: 0,
      saldo_atual: 0,
      observacoes: null,
    };
  };

  const [formData, setFormData] = useState<CarteiraCreate>(getInitialFormData(null));

  const handleOpenForm = (carteiraToEdit: Carteira | null) => {
    setEditingCarteira(carteiraToEdit);
    setFormData(getInitialFormData(carteiraToEdit));
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditingCarteira(null);
    setFormData(getInitialFormData(null));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === 'saldo_inicial' || name === 'saldo_atual') {
      const cleanValue = value.replace(',', '.');
      const numValue = cleanValue === '' ? 0 : parseFloat(cleanValue);
      setFormData((prev) => ({
        ...prev,
        [name]: isNaN(numValue) ? 0 : numValue,
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSelectChange = (name: string, value: string) => {
    const finalValue = value === '' ? null : value;
    setFormData((prev) => ({ ...prev, [name]: finalValue }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({ ...prev, [name]: checked }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Obter usuario_id do localStorage
    const usuarioId = localStorage.getItem('usuario_id');

    if (!formData.nome || !usuarioId) {
      toast({
        title: "Erro",
        description: "Por favor, preencha os campos obrigatórios. Usuário não identificado.",
        variant: "destructive",
      });
      return;
    }

    try {
      const dataToSend: CarteiraCreate = {
        usuario_id: usuarioId, // Enviando usuario_id
        nome: formData.nome,
        tipo: formData.tipo,
        objetivo: formData.objetivo,
        descricao: formData.descricao || null,
        ativa: formData.ativa,
        saldo_inicial: formData.saldo_inicial,
        saldo_atual: formData.saldo_atual,
        observacoes: formData.observacoes || null,
      };

      console.log('Enviando dados:', dataToSend); // Log para debug

      if (editingCarteira) {
        await updateCarteira({ id: editingCarteira.id, data: dataToSend });
        toast({
          title: "Sucesso!",
          description: "Carteira atualizada com sucesso.",
        });
      } else {
        await createCarteira(dataToSend);
        toast({
          title: "Sucesso!",
          description: "Carteira criada com sucesso.",
        });
      }
      handleCloseForm();
    } catch (err) {
      let errorMessage = "Erro desconhecido ao salvar carteira.";
      if (err instanceof AxiosError) {
        console.error('Erro da API:', err.response?.data); // Log do erro
        errorMessage = err.response?.data?.detail || err.message;
      }
      toast({
        title: "Erro",
        description: `Falha ao salvar carteira: ${errorMessage}`,
        variant: "destructive",
      });
      console.error('Erro ao salvar carteira:', err);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta carteira?')) {
      try {
        await deleteCarteira(id);
        toast({
          title: "Sucesso!",
          description: "Carteira excluída com sucesso.",
        });
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao excluir carteira.";
        toast({
          title: "Erro",
          description: `Falha ao excluir carteira: ${errorMessage}`,
          variant: "destructive",
        });
      }
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

  if (isLoading) return <div className="p-4">Carregando carteiras...</div>;
  if (error) return <div className="p-4 text-red-600">Erro ao carregar carteiras: {error.message}</div>;

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Carteiras</h1>
        <Dialog open={isFormOpen} onOpenChange={(open) => {
          if (!open) handleCloseForm();
          else handleOpenForm(null);
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => handleOpenForm(null)}>
              Adicionar Carteira
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>{editingCarteira ? 'Editar Carteira' : 'Adicionar Nova Carteira'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
              {/* Campo Nome */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="nome" className="text-right">
                  Nome *
                </Label>
                <Input
                  id="nome"
                  name="nome"
                  value={formData.nome}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                  placeholder="Ex: Carteira Principal"
                />
              </div>

              {/* Campo Tipo */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo" className="text-right">
                  Tipo *
                </Label>
                <Select
                  value={formData.tipo}
                  onValueChange={(value) => handleSelectChange('tipo', value as TipoCarteira)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoCarteira).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Objetivo */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="objetivo" className="text-right">
                  Objetivo *
                </Label>
                <Select
                  value={formData.objetivo}
                  onValueChange={(value) => handleSelectChange('objetivo', value as ObjetivoCarteira)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o objetivo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(ObjetivoCarteira).map((objetivo) => (
                      <SelectItem key={objetivo} value={objetivo}>
                        {objetivo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Saldo Inicial */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="saldo_inicial" className="text-right">
                  Saldo Inicial
                </Label>
                <Input
                  id="saldo_inicial"
                  name="saldo_inicial"
                  type="text"
                  inputMode="decimal"
                  value={formData.saldo_inicial}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Saldo Atual */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="saldo_atual" className="text-right">
                  Saldo Atual
                </Label>
                <Input
                  id="saldo_atual"
                  name="saldo_atual"
                  type="text"
                  inputMode="decimal"
                  value={formData.saldo_atual}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Descrição */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="descricao" className="text-right">
                  Descrição
                </Label>
                <Input
                  id="descricao"
                  name="descricao"
                  value={formData.descricao || ''}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="Descrição da carteira"
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

              {/* Campo Ativa */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="ativa" className="text-right">
                  Ativa
                </Label>
                <div className="col-span-3">
                  <input
                    id="ativa"
                    name="ativa"
                    type="checkbox"
                    checked={formData.ativa}
                    onChange={handleCheckboxChange}
                    className="w-4 h-4"
                  />
                </div>
              </div>

              <DialogFooter>
                <Button type="submit">{editingCarteira ? 'Salvar Alterações' : 'Adicionar Carteira'}</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Nome</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Objetivo</TableHead>
              <TableHead className="text-right">Saldo Inicial</TableHead>
              <TableHead className="text-right">Saldo Atual</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {carteiras && carteiras.length > 0 ? (
              carteiras.map((carteira) => (
                <TableRow key={carteira.id}>
                  <TableCell className="font-medium">{carteira.nome}</TableCell>
                  <TableCell>{carteira.tipo}</TableCell>
                  <TableCell>{carteira.objetivo}</TableCell>
                  <TableCell className="text-right">{formatarMoeda(carteira.saldo_inicial)}</TableCell>
                  <TableCell className="text-right font-semibold">{formatarMoeda(carteira.saldo_atual)}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                      carteira.ativa
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {carteira.ativa ? 'Ativa' : 'Inativa'}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleOpenForm(carteira)}
                      >
                        Editar
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(carteira.id)}
                      >
                        Excluir
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7} className="text-center py-4 text-gray-500">
                  Nenhuma carteira cadastrada. Clique em "Adicionar Carteira" para criar uma.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default CarteirasPage;