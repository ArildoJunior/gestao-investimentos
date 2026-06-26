// FILE: frontend/src/pages/ativos/AtivosPage.tsx

import React, { useState } from 'react';
import { useAtivos } from '@/hooks/useAtivos';
import { Ativo, TipoAtivo, StatusAtivo, RegiaoAtivo, SegmentoFII, Moeda, AtivoCreate } from '@/types/ativo';

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

const AtivosPage: React.FC = () => {
  const { ativos, isLoading, error, createAtivo, updateAtivo, deleteAtivo } = useAtivos();
  const { toast } = useToast();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingAtivo, setEditingAtivo] = useState<Ativo | null>(null);

  // Função auxiliar para obter os dados iniciais do formulário
  const getInitialFormData = (ativo: Ativo | null): AtivoCreate => {
    if (ativo) {
      return {
        ticker: ativo.ticker,
        nome: ativo.nome,
        classe: ativo.classe,
        setor: ativo.setor || null,
        segmento_fii: ativo.segmento_fii || null,
        pais: ativo.pais,
        regiao: ativo.regiao,
        moeda: ativo.moeda,
        status: ativo.status,
      };
    }
    return {
      ticker: '',
      nome: '',
      classe: TipoAtivo.ACAO,
      setor: null,
      segmento_fii: null,
      pais: 'BR',
      regiao: RegiaoAtivo.BRASIL,
      moeda: Moeda.BRL,
      status: StatusAtivo.ATIVO,
    };
  };

  const [formData, setFormData] = useState<AtivoCreate>(getInitialFormData(null));

  // Função para abrir o modal e inicializar o formulário
  const handleOpenForm = (ativoToEdit: Ativo | null) => {
    setEditingAtivo(ativoToEdit);
    setFormData(getInitialFormData(ativoToEdit));
    setIsFormOpen(true);
  };

  // Função para fechar o modal e resetar o estado
  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditingAtivo(null);
    setFormData(getInitialFormData(null));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string) => {
    const finalValue = value === '' ? null : value;
    setFormData((prev) => ({ ...prev, [name]: finalValue }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validação básica
    if (!formData.nome || !formData.ticker || !formData.pais) {
      toast({
        title: "Erro",
        description: "Por favor, preencha os campos obrigatórios (Nome, Ticker e País).",
        variant: "destructive",
      });
      return;
    }

    try {
      // Prepara os dados para envio
      const dataToSend: AtivoCreate = {
        ticker: formData.ticker.toUpperCase(),
        nome: formData.nome,
        classe: formData.classe,
        setor: formData.setor || null,
        segmento_fii: formData.segmento_fii || null,
        pais: formData.pais.toUpperCase(),
        regiao: formData.regiao,
        moeda: formData.moeda,
        status: formData.status,
      };

      if (editingAtivo) {
        await updateAtivo({ id: editingAtivo.id, data: dataToSend });
        toast({
          title: "Sucesso!",
          description: "Ativo atualizado com sucesso.",
        });
      } else {
        await createAtivo(dataToSend);
        toast({
          title: "Sucesso!",
          description: "Ativo criado com sucesso.",
        });
      }
      handleCloseForm();
    } catch (err) {
      let errorMessage = "Erro desconhecido ao salvar ativo.";

      if (err instanceof AxiosError) {
        if (err.response?.data?.detail) {
          errorMessage = err.response.data.detail;
        } else if (err.response?.data) {
          errorMessage = JSON.stringify(err.response.data);
        } else {
          errorMessage = err.message;
        }
      }

      toast({
        title: "Erro",
        description: `Falha ao salvar ativo: ${errorMessage}`,
        variant: "destructive",
      });

      console.error('Erro ao salvar ativo:', err);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este ativo?')) {
      try {
        await deleteAtivo(id);
        toast({
          title: "Sucesso!",
          description: "Ativo excluído com sucesso.",
        });
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail || err.message : "Erro desconhecido ao excluir ativo.";
        toast({
          title: "Erro",
          description: `Falha ao excluir ativo: ${errorMessage}`,
          variant: "destructive",
        });
      }
    }
  };

  if (isLoading) return <div className="p-4">Carregando ativos...</div>;
  if (error) return <div className="p-4 text-red-600">Erro ao carregar ativos: {error.message}</div>;

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Ativos</h1>
        <Dialog open={isFormOpen} onOpenChange={(open) => {
          if (!open) {
            handleCloseForm();
          } else {
            handleOpenForm(null);
          }
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => handleOpenForm(null)}>
              Adicionar Ativo
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>{editingAtivo ? 'Editar Ativo' : 'Adicionar Novo Ativo'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="grid gap-4 py-4">
              {/* Campo Ticker */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="ticker" className="text-right">
                  Ticker *
                </Label>
                <Input
                  id="ticker"
                  name="ticker"
                  value={formData.ticker}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                  placeholder="Ex: PETR4"
                />
              </div>

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
                  placeholder="Ex: Petrobras"
                />
              </div>

              {/* Campo Classe (Tipo) */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="classe" className="text-right">
                  Classe *
                </Label>
                <Select
                  value={formData.classe}
                  onValueChange={(value) => handleSelectChange('classe', value as TipoAtivo)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a classe" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(TipoAtivo).map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {tipo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Setor */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="setor" className="text-right">
                  Setor
                </Label>
                <Input
                  id="setor"
                  name="setor"
                  value={formData.setor || ''}
                  onChange={handleInputChange}
                  className="col-span-3"
                  placeholder="Ex: Petróleo e Gás"
                />
              </div>

              {/* Campo País */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="pais" className="text-right">
                  País *
                </Label>
                <Input
                  id="pais"
                  name="pais"
                  value={formData.pais}
                  onChange={handleInputChange}
                  className="col-span-3"
                  required
                  placeholder="Ex: BR"
                  maxLength={10}
                />
              </div>

              {/* Campo Região */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="regiao" className="text-right">
                  Região *
                </Label>
                <Select
                  value={formData.regiao}
                  onValueChange={(value) => handleSelectChange('regiao', value as RegiaoAtivo)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione a região" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(RegiaoAtivo).map((regiao) => (
                      <SelectItem key={regiao} value={regiao}>
                        {regiao}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campo Moeda */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="moeda" className="text-right">
                  Moeda *
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

              {/* Campo Segmento FII (Condicional) */}
              {formData.classe === TipoAtivo.FII && (
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="segmento_fii" className="text-right">
                    Segmento FII
                  </Label>
                  <Select
                    value={formData.segmento_fii || ''}
                    onValueChange={(value) => handleSelectChange('segmento_fii', value)}
                  >
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Selecione o segmento" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Nenhum</SelectItem>
                      {Object.values(SegmentoFII).map((segmento) => (
                        <SelectItem key={segmento} value={segmento}>
                          {segmento}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              {/* Campo Status */}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="status" className="text-right">
                  Status *
                </Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) => handleSelectChange('status', value as StatusAtivo)}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="Selecione o status" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.values(StatusAtivo).map((status) => (
                      <SelectItem key={status} value={status}>
                        {status}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <DialogFooter>
                <Button type="submit">{editingAtivo ? 'Salvar Alterações' : 'Adicionar Ativo'}</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ticker</TableHead>
              <TableHead>Nome</TableHead>
              <TableHead>Classe</TableHead>
              <TableHead>País</TableHead>
              <TableHead>Região</TableHead>
              <TableHead>Moeda</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {ativos && ativos.length > 0 ? (
              ativos.map((ativo) => (
                <TableRow key={ativo.id}>
                  <TableCell className="font-bold text-blue-600">{ativo.ticker}</TableCell>
                  <TableCell className="font-medium">{ativo.nome}</TableCell>
                  <TableCell>{ativo.classe}</TableCell>
                  <TableCell>{ativo.pais}</TableCell>
                  <TableCell>{ativo.regiao}</TableCell>
                  <TableCell>{ativo.moeda}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                      ativo.status === StatusAtivo.ATIVO
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {ativo.status}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleOpenForm(ativo)}
                      >
                        Editar
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(ativo.id)}
                      >
                        Excluir
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={8} className="text-center py-4 text-gray-500">
                  Nenhum ativo cadastrado. Clique em "Adicionar Ativo" para criar um.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default AtivosPage;