// FILE: frontend/src/pages/instituicoes/InstituicoesPage.tsx

import React, { useState } from 'react';
import { useInstituicoes } from '@/hooks/useInstituicoes';
import { Instituicao, TipoInstituicao, StatusInstituicao, InstituicaoCreate } from '@/types/instituicao';

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

const InstituicoesPage: React.FC = () => {
  const { instituicoes, isLoading, error, createInstituicao, updateInstituicao, deleteInstituicao } = useInstituicoes();
  const { toast } = useToast();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingInstituicao, setEditingInstituicao] = useState<Instituicao | null>(null);

  // Função auxiliar para obter os dados iniciais do formulário
  const getInitialFormData = (instituicao: Instituicao | null): InstituicaoCreate => {
    if (instituicao) {
      return {
        nome: instituicao.nome,
        tipo: instituicao.tipo,
        status: instituicao.status,
      };
    }
    return {
      nome: '',
      tipo: TipoInstituicao.CORRETORA,
      status: StatusInstituicao.ATIVA,
    };
  };

  // O formData será inicializado com valores padrão.
  // Ele será atualizado no momento em que o modal for aberto para edição/criação.
  const [formData, setFormData] = useState<InstituicaoCreate>(getInitialFormData(null));

  // Função para abrir o modal e inicializar o formulário
  const handleOpenForm = (instituicaoToEdit: Instituicao | null) => {
    setEditingInstituicao(instituicaoToEdit);
    setFormData(getInitialFormData(instituicaoToEdit)); // Inicializa o formData aqui
    setIsFormOpen(true);
  };

  // Função para fechar o modal e resetar o estado
  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditingInstituicao(null);
    setFormData(getInitialFormData(null)); // Reseta o formulário para valores padrão
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingInstituicao) {
        await updateInstituicao({ id: editingInstituicao.id, data: formData });
        toast({
          title: "Sucesso!",
          description: "Instituição atualizada com sucesso.",
        });
      } else {
        await createInstituicao(formData);
        toast({
          title: "Sucesso!",
          description: "Instituição criada com sucesso.",
        });
      }
      handleCloseForm(); // Fecha e reseta o formulário
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao salvar instituição.";
      toast({
        title: "Erro",
        description: `Falha ao salvar instituição: ${errorMessage}`,
        variant: "destructive",
      });
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta instituição?')) {
      try {
        await deleteInstituicao(id);
        toast({
          title: "Sucesso!",
          description: "Instituição excluída com sucesso.",
        });
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao excluir instituição.";
        toast({
          title: "Erro",
          description: `Falha ao excluir instituição: ${errorMessage}`,
          variant: "destructive",
        });
      }
    }
  };

  if (isLoading) return <div>Carregando instituições...</div>;
  if (error) return <div>Erro ao carregar instituições: {error.message}</div>;

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Instituições Financeiras</h1>
        <Dialog open={isFormOpen} onOpenChange={(open) => {
          if (!open) { // Se o modal está sendo fechado
            handleCloseForm();
          } else { // Se o modal está sendo aberto (para nova criação)
            handleOpenForm(null);
          }
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => handleOpenForm(null)}> {/* Botão para adicionar nova */}
              Adicionar Instituição
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>{editingInstituicao ? 'Editar Instituição' : 'Adicionar Nova Instituição'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
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
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="tipo" className="text-right">
                  Tipo
                </Label>
                <Select
                  name="tipo"
                  value={formData.tipo}
                  onValueChange={(value) => handleSelectChange('tipo', value as TipoInstituicao)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoInstituicao).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="status" className="text-right">
                  Status
                </Label>
                <Select
                  name="status"
                  value={formData.status}
                  onValueChange={(value) => handleSelectChange('status', value as StatusInstituicao)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o status" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(StatusInstituicao).map((status) => (
                      <SelectItem key={status} value={status}>
                        {status}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <DialogFooter>
                <Button type="submit">{editingInstituicao ? 'Salvar Alterações' : 'Adicionar Instituição'}</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Nome</TableHead>
            <TableHead>Tipo</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {instituicoes?.map((instituicao) => (
            <TableRow key={instituicao.id}>
              <TableCell className="font-medium">{instituicao.nome}</TableCell>
              <TableCell>{instituicao.tipo}</TableCell>
              <TableCell>{instituicao.status}</TableCell>
              <TableCell>
                <Button
                  variant="outline"
                  size="sm"
                  className="mr-2"
                  onClick={() => handleOpenForm(instituicao)} // Abre para edição
                >
                  Editar
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDelete(instituicao.id)}
                >
                  Excluir
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default InstituicoesPage;