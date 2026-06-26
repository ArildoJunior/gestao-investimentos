// FILE: frontend/src/pages/contas/ContasPage.tsx

import React, { useState } from 'react';
import { useContas } from '@/hooks/useContas';
import { useInstituicoesSelect } from '@/hooks/useInstituicoesSelect';
import { Conta, TipoConta, StatusConta, Moeda, ContaCreate } from '@/types/conta';

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

// Função auxiliar para formatar valores monetários
const formatarMoeda = (valor: number | string, moeda: string): string => {
  const numValue = typeof valor === 'string' ? parseFloat(valor) : valor;
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: moeda,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numValue);
};

const ContasPage: React.FC = () => {
  const { contas, isLoading, error, createConta, updateConta, deleteConta } = useContas();
  const { instituicoes, isLoading: isLoadingInstituicoes } = useInstituicoesSelect();
  const { toast } = useToast();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingConta, setEditingConta] = useState<Conta | null>(null);

  // Função auxiliar para obter os dados iniciais do formulário
  const getInitialFormData = (conta: Conta | null): ContaCreate => {
    if (conta) {
      return {
        instituicao_id: conta.instituicao_id,
        nome: conta.nome,
        tipo: conta.tipo,
        moeda: conta.moeda,
        saldo_inicial: conta.saldo_inicial,
        saldo_atual: conta.saldo_atual,
        data_abertura: conta.data_abertura,
        status: conta.status,
      };
    }
    return {
      instituicao_id: '',
      nome: '',
      tipo: TipoConta.CORRENTE,
      moeda: Moeda.BRL,
      saldo_inicial: 0,
      saldo_atual: 0,
      data_abertura: new Date().toISOString().split('T')[0],
      status: StatusConta.ATIVA,
    };
  };

  const [formData, setFormData] = useState<ContaCreate>(getInitialFormData(null));

  // Função para abrir o modal e inicializar o formulário
  const handleOpenForm = (contaToEdit: Conta | null) => {
    setEditingConta(contaToEdit);
    setFormData(getInitialFormData(contaToEdit));
    setIsFormOpen(true);
  };

  // Função para fechar o modal e resetar o estado
  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditingConta(null);
    setFormData(getInitialFormData(null));
  };

  // Função auxiliar para selecionar todo o texto quando o input recebe foco
  const handleNumberInputFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    e.target.select();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === 'saldo_inicial' || name === 'saldo_atual') {
      // Converte o valor digitado diretamente para número
      // Aceita valores como "300", "300.50", "300,50"
      const cleanValue = value.replace(',', '.');
      const numValue = cleanValue === '' ? 0 : parseFloat(cleanValue);
      setFormData((prev) => ({ 
        ...prev, 
        [name]: isNaN(numValue) ? 0 : numValue 
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validação básica
    if (!formData.instituicao_id) {
      toast({
        title: "Erro",
        description: "Por favor, selecione uma instituição.",
        variant: "destructive",
      });
      return;
    }

    try {
      if (editingConta) {
        await updateConta({ id: editingConta.id, data: formData });
        toast({
          title: "Sucesso!",
          description: "Conta atualizada com sucesso.",
        });
      } else {
        await createConta(formData);
        toast({
          title: "Sucesso!",
          description: "Conta criada com sucesso.",
        });
      }
      handleCloseForm();
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao salvar conta.";
      toast({
        title: "Erro",
        description: `Falha ao salvar conta: ${errorMessage}`,
        variant: "destructive",
      });
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta conta?')) {
      try {
        await deleteConta(id);
        toast({
          title: "Sucesso!",
          description: "Conta excluída com sucesso.",
        });
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao excluir conta.";
        toast({
          title: "Erro",
          description: `Falha ao excluir conta: ${errorMessage}`,
          variant: "destructive",
        });
      }
    }
  };

  // Função auxiliar para obter o nome da instituição pelo ID
  const getInstituicaoNome = (instituicaoId: string): string => {
    return instituicoes?.find((inst) => inst.id === instituicaoId)?.nome || 'Desconhecida';
  };

  if (isLoading) return <div className="p-4">Carregando contas...</div>;
  if (error) return <div className="p-4 text-red-600">Erro ao carregar contas: {error.message}</div>;

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Contas</h1>
        <Dialog open={isFormOpen} onOpenChange={(open) => {
          if (!open) {
            handleCloseForm();
          } else {
            handleOpenForm(null);
          }
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => handleOpenForm(null)}>
              Adicionar Conta
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>{editingConta ? 'Editar Conta' : 'Adicionar Nova Conta'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
              {/* Campo Instituição */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="instituicao_id" className="text-right">
                  Instituição
                </Label>
                <Select
                  value={formData.instituicao_id}
                  onValueChange={(value) => handleSelectChange('instituicao_id', value)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione uma instituição" />
                  </SelectTrigger>
                  <SelectContent>
                    {isLoadingInstituicoes ? (
                      <div className="p-2 text-sm text-gray-500">Carregando instituições...</div>
                    ) : instituicoes && instituicoes.length > 0 ? (
                      instituicoes.map((inst) => (
                        <SelectItem key={inst.id} value={inst.id}>
                          {inst.nome}
                        </SelectItem>
                      ))
                    ) : (
                      <div className="p-2 text-sm text-gray-500">Nenhuma instituição disponível</div>
                    )}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Nome */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="nome" className="text-right">
                  Nome
                </Label>
                <Input
                  id="nome"
                  name="nome"
                  value={formData.nome}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                />
              </div>

              {/* Campo Tipo */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo" className="text-right">
                  Tipo
                </Label>
                <Select
                  value={formData.tipo}
                  onValueChange={(value) => handleSelectChange('tipo', value as TipoConta)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoConta).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Moeda */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="moeda" className="text-right">
                  Moeda
                </Label>
                <Select
                  value={formData.moeda}
                  onValueChange={(value) => handleSelectChange('moeda', value as Moeda)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a moeda" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(Moeda).map((moeda) => (
                      <SelectItem key={moeda} value={moeda}>
                        {moeda}
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
                  onFocus={handleNumberInputFocus}
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
                  onFocus={handleNumberInputFocus}
                  className="col-span-3"
                  placeholder="0.00"
                />
              </div>

              {/* Campo Data de Abertura */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="data_abertura" className="text-right">
                  Data de Abertura
                </Label>
                <Input
                  id="data_abertura"
                  name="data_abertura"
                  type="date"
                  value={formData.data_abertura}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                />
              </div>

              {/* Campo Status */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="status" className="text-right">
                  Status
                </Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) => handleSelectChange('status', value as StatusConta)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o status" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(StatusConta).map((status) => (
                      <SelectItem key={status} value={status}>
                        {status}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <DialogFooter>
                <Button type="submit">{editingConta ? 'Salvar Alterações' : 'Adicionar Conta'}</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Instituição</TableHead>
              <TableHead>Nome</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Moeda</TableHead>
              <TableHead className="text-right">Saldo Atual</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {contas && contas.length > 0 ? (
              contas.map((conta) => (
                <TableRow key={conta.id}>
                  <TableCell>{getInstituicaoNome(conta.instituicao_id)}</TableCell>
                  <TableCell className="font-medium">{conta.nome}</TableCell>
                  <TableCell>{conta.tipo}</TableCell>
                  <TableCell>{conta.moeda}</TableCell>
                  <TableCell className="text-right font-semibold">
                    {formatarMoeda(conta.saldo_atual, conta.moeda)}
                  </TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                      conta.status === StatusConta.ATIVA
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {conta.status}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleOpenForm(conta)}
                      >
                        Editar
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(conta.id)}
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
                  Nenhuma conta cadastrada. Clique em "Adicionar Conta" para criar uma.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default ContasPage;