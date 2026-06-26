// FILE: frontend/src/pages/proventos/components/FormProvento.tsx

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CalendarIcon } from 'lucide-react';
import { Calendar } from '@/components/ui/calendar';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { cn } from '@/lib/utils';

import { TipoProvento } from '@/types/provento';
import { useCarteiras } from '@/services/carteirasService';
import { useContas } from '@/services/contasService';
import { useAtivos } from '@/hooks/useAtivos';

const formSchema = z.object({
  carteira_id: z.string().uuid({ message: 'Selecione uma carteira válida.' }),
  conta_id: z.string().uuid({ message: 'Selecione uma conta válida.' }).optional(),
  ativo_id: z.string().uuid({ message: 'Selecione um ativo válido.' }),
  tipo: z.nativeEnum(TipoProvento, { message: 'Selecione um tipo de provento válido.' }),
  valor_bruto: z.string().refine(
    (val) => {
      const num = parseFloat(val.replace(',', '.'));
      return !isNaN(num) && num > 0;
    },
    { message: 'Valor bruto deve ser um número positivo.' }
  ),
  data_com: z.date({ message: 'Data Com é obrigatória.' }),
  data_pagamento: z.date({ message: 'Data de Pagamento é obrigatória.' }),
  quantidade: z.string().refine(
    (val) => {
      const num = parseFloat(val.replace(',', '.'));
      return !isNaN(num) && num > 0;
    },
    { message: 'Quantidade deve ser um número positivo.' }
  ),
  reinvestido: z.boolean().default(false),
  observacoes: z.string().optional(),
});

type FormProventoValues = z.infer<typeof formSchema>;

interface FormProventoProps {
  onSubmit: (data: FormProventoValues) => void;
  defaultValues?: Partial<FormProventoValues>;
}

export const FormProvento: React.FC<FormProventoProps> = ({ onSubmit, defaultValues }) => {
  const form = useForm<FormProventoValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      reinvestido: false,
      valor_bruto: '',
      quantidade: '',
      ...defaultValues,
    },
  });

  const { data: carteiras } = useCarteiras();
  const { data: contas } = useContas();
  const { data: ativos } = useAtivos();

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">

        {/* Carteira */}
        <FormField
          control={form.control}
          name="carteira_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Carteira</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione a carteira" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {carteiras?.map((carteira) => (
                    <SelectItem key={carteira.id} value={carteira.id}>
                      {carteira.nome}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Conta */}
        <FormField
          control={form.control}
          name="conta_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Conta (Opcional)</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione a conta" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {contas?.map((conta) => (
                    <SelectItem key={conta.id} value={conta.id}>
                      {conta.nome}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Ativo */}
        <FormField
          control={form.control}
          name="ativo_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Ativo</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o ativo" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {ativos?.map((ativo) => (
                    <SelectItem key={ativo.id} value={ativo.id}>
                      {ativo.ticker} - {ativo.nome}  {/* ticker, não codigo */}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Tipo */}
        <FormField
          control={form.control}
          name="tipo"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tipo de Provento</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {Object.values(TipoProvento).map((tipo) => (
                    <SelectItem key={tipo} value={tipo}>
                      {tipo}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Valor Bruto */}
        <FormField
          control={form.control}
          name="valor_bruto"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Valor Bruto</FormLabel>
              <FormControl>
                <Input placeholder="0.00" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Quantidade */}
        <FormField
          control={form.control}
          name="quantidade"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Quantidade</FormLabel>
              <FormControl>
                <Input placeholder="0" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Data Com */}
        <FormField
          control={form.control}
          name="data_com"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data Com</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant="outline"
                      className={cn(
                        'w-[240px] pl-3 text-left font-normal',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {field.value
                        ? format(field.value, 'dd/MM/yyyy', { locale: ptBR })
                        : 'Selecione uma data'}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    initialFocus
                    locale={ptBR}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Data Pagamento */}
        <FormField
          control={form.control}
          name="data_pagamento"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data de Pagamento</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant="outline"
                      className={cn(
                        'w-[240px] pl-3 text-left font-normal',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {field.value
                        ? format(field.value, 'dd/MM/yyyy', { locale: ptBR })
                        : 'Selecione uma data'}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    initialFocus
                    locale={ptBR}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Reinvestido */}
        <FormField
          control={form.control}
          name="reinvestido"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
              <FormControl>
                <Checkbox checked={field.value} onCheckedChange={field.onChange} />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>Reinvestido</FormLabel>
                <FormDescription>
                  Marque se o provento foi reinvestido automaticamente.
                </FormDescription>
              </div>
            </FormItem>
          )}
        />

        {/* Observações */}
        <FormField
          control={form.control}
          name="observacoes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Observações (Opcional)</FormLabel>
              <FormControl>
                <Textarea placeholder="Detalhes adicionais..." {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" className="w-full" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Salvando...' : 'Salvar Provento'}
        </Button>
      </form>
    </Form>
  );
};