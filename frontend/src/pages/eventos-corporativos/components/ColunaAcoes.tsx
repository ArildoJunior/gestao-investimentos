// FILE: frontend/src/pages/eventos-corporativos/components/ColunaAcoes.tsx

import { Row } from '@tanstack/react-table';
import { MoreHorizontal } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { EventoCorporativoRead } from '@/types/eventoCorporativo';
import { useEventosCorporativos } from '@/hooks/useEventosCorporativos';
import { useToast } from '@/components/ui/use-toast';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';

interface ColunaAcoesProps {
  row: Row<EventoCorporativoRead>;
}

export function ColunaAcoes({ row }: ColunaAcoesProps) {
  const evento = row.original;
  const { toast } = useToast();

  // CORREÇÃO: processarEvento já é a função mutate. isProcessing vem direto do hook.
  // Não tentar desestruturar { mutate, isPending } de uma função.
  const { processarEvento, isProcessing } = useEventosCorporativos();

  const handleProcessarEvento = () => {
    processarEvento(evento.id, {
      onSuccess: () => {
        toast({
          title: 'Sucesso!',
          description: `Evento corporativo ${evento.tipo} processado com sucesso.`,
        });
      },
      onError: (error) => {
        toast({
          title: 'Erro ao processar evento',
          description: error.message || 'Ocorreu um erro inesperado.',
          variant: 'destructive',
        });
      },
    });
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="h-8 w-8 p-0">
          <span className="sr-only">Abrir menu</span>
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>Ações</DropdownMenuLabel>
        <DropdownMenuItem
          onClick={() => navigator.clipboard.writeText(evento.id)}
        >
          Copiar ID do evento
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem disabled>Editar (Em breve)</DropdownMenuItem>
        {!evento.processado && (
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
                Processar Evento
              </DropdownMenuItem>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Tem certeza?</AlertDialogTitle>
                <AlertDialogDescription>
                  Esta ação não pode ser desfeita. Isso processará o evento corporativo
                  e ajustará as posições do ativo.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancelar</AlertDialogCancel>
                <AlertDialogAction onClick={handleProcessarEvento} disabled={isProcessing}>
                  {isProcessing ? 'Processando...' : 'Confirmar'}
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}