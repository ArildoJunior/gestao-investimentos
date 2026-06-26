// FILE: frontend/src/pages/eventos-corporativos/components/FormEventoCorporativo.tsx

import { useEffect } from 'react'; 
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CalendarIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useToast } from '@/hooks/use-toast';

import { TipoEventoCorporativo } from '@/types/enums';
import { useAtivos } from '@/hooks/useAtivos';
import { useEventosCorporativos } from '@/hooks/useEventosCorporativos';
import { Ativo } from '@/types/ativo'; // Importar a interface Ativo

// Esquema de validação com Zod
const formSchema = z.object({
  ativo_id: z.string().uuid({ message: 'ID do Ativo inválido.' }),
  tipo: z.nativeEnum(TipoEventoCorporativo, {
    errorMap: () => ({ message: 'Tipo de evento corporativo inválido.' }),
  }),
  data_evento: z.date({ // Renomeado para data_evento para corresponder ao backend
    required_error: 'Data do Evento é obrigatória.',
    invalid_type_error: 'Data do Evento inválida.',
  }),
  data_ex: z.date({
    required_error: 'Data Ex é obrigatória.',
    invalid_type_error: 'Data Ex inválida.',
  }),
  data_pagamento: z.date().optional().nullable(), // Adicionado .nullable() para permitir null
  fator: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().min(0, { message: 'Fator deve ser um número positivo.' }).optional().nullable()
  ),
  valor: z.preprocess( // Adicionado campo valor para amortização/bonificação
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().min(0, { message: 'Valor deve ser um número positivo.' }).optional().nullable()
  ),
  ativo_destino_id: z.string().uuid({ message: 'ID do Ativo Destino inválido.' }).optional().nullable(),
  observacoes: z.string().optional().nullable(),

  // Campos condicionais (para o frontend, não fazem parte do schema base do backend)
  de_quantidade: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().int().min(1, { message: 'Quantidade deve ser um número inteiro positivo.' }).optional().nullable()
  ),
  para_quantidade: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().int().min(1, { message: 'Quantidade deve ser um número inteiro positivo.' }).optional().nullable()
  ),
  quantidade_bonificacao: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().int().min(1, { message: 'Quantidade deve ser um número inteiro positivo.' }).optional().nullable()
  ),
  valor_subscricao_por_ativo: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().min(0, { message: 'Valor de subscrição deve ser um número positivo.' }).optional().nullable()
  ),
  valor_amortizacao_por_ativo: z.preprocess(
    (val) => {
      if (val === '' || val === null || val === undefined) return undefined;
      const num = Number(val);
      return isNaN(num) ? undefined : num;
    },
    z.number().min(0, { message: 'Valor de amortização deve ser um número positivo.' }).optional().nullable()
  ),
  descricao: z.string().optional().nullable(), // Para tipo OUTRO
}).superRefine((data, ctx) => {
  // Validações condicionais baseadas no tipo de evento
  switch (data.tipo) {
    case TipoEventoCorporativo.SPLIT:
    case TipoEventoCorporativo.GRUPAMENTO:
      if (data.de_quantidade === undefined || data.de_quantidade === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Quantidade "De" é obrigatória para Split/Grupamento.',
          path: ['de_quantidade'],
        });
      }
      if (data.para_quantidade === undefined || data.para_quantidade === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Quantidade "Para" é obrigatória para Split/Grupamento.',
          path: ['para_quantidade'],
        });
      }
      if (data.fator === undefined || data.fator === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Fator é obrigatório para Split/Grupamento.',
          path: ['fator'],
        });
      }
      break;
    case TipoEventoCorporativo.BONIFICACAO:
      if (data.quantidade_bonificacao === undefined || data.quantidade_bonificacao === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Quantidade de Bonificação é obrigatória.',
          path: ['quantidade_bonificacao'],
        });
      }
      if (data.valor === undefined || data.valor === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Valor da Bonificação é obrigatório.',
          path: ['valor'],
        });
      }
      if (data.fator === undefined || data.fator === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Fator é obrigatório para Bonificação.',
          path: ['fator'],
        });
      }
      break;
    case TipoEventoCorporativo.SUBSCRICAO:
      if (data.valor_subscricao_por_ativo === undefined || data.valor_subscricao_por_ativo === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Valor de Subscrição por Ativo é obrigatório.',
          path: ['valor_subscricao_por_ativo'],
        });
      }
      if (data.fator === undefined || data.fator === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Fator é obrigatório para Subscrição.',
          path: ['fator'],
        });
      }
      break;
    case TipoEventoCorporativo.AMORTIZACAO:
      if (data.valor_amortizacao_por_ativo === undefined || data.valor_amortizacao_por_ativo === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Valor de Amortização por Ativo é obrigatório.',
          path: ['valor_amortizacao_por_ativo'],
        });
      }
      if (data.fator === undefined || data.fator === null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Fator é obrigatório para Amortização.',
          path: ['fator'],
        });
      }
      break;
    case TipoEventoCorporativo.OUTRO:
      if (data.observacoes === undefined || data.observacoes === null || data.observacoes.trim() === '') {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'Descrição é obrigatória para Outro tipo de evento.',
          path: ['observacoes'],
        });
      }
      break;
  }
});

interface FormEventoCorporativoProps {
  onClose: () => void;
}

export function FormEventoCorporativo({ onClose }: FormEventoCorporativoProps) {
  const { toast } = useToast();
  const { ativos, isLoading: isLoadingAtivos } = useAtivos();
  const { createEvento, isCreating } = useEventosCorporativos();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      ativo_id: undefined,
      tipo: undefined,
      data_evento: undefined,
      data_ex: undefined,
      data_pagamento: undefined,
      fator: undefined,
      valor: undefined,
      ativo_destino_id: undefined,
      observacoes: undefined,
      de_quantidade: undefined,
      para_quantidade: undefined,
      quantidade_bonificacao: undefined,
      valor_subscricao_por_ativo: undefined,
      valor_amortizacao_por_ativo: undefined,
      descricao: undefined,
    },
  });

  const tipoEventoSelecionado = form.watch('tipo');

  // Resetar campos condicionais quando o tipo de evento muda
  useEffect(() => {
    form.clearErrors(); // Limpa todos os erros ao mudar o tipo
    form.setValue('de_quantidade', undefined);
    form.setValue('para_quantidade', undefined);
    form.setValue('quantidade_bonificacao', undefined);
    form.setValue('valor_subscricao_por_ativo', undefined);
    form.setValue('valor_amortizacao_por_ativo', undefined);
    form.setValue('descricao', undefined);
    form.setValue('fator', undefined); // Resetar fator também, pois sua obrigatoriedade é condicional
    form.setValue('valor', undefined); // Resetar valor também
    form.setValue('ativo_destino_id', undefined); // Resetar ativo_destino_id
  }, [tipoEventoSelecionado, form]);

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      // Construir o payload para o backend, filtrando campos undefined/null/vazios
      const payload: Record<string, any> = { // eslint-disable-line @typescript-eslint/no-explicit-any
        ativo_id: values.ativo_id,
        tipo: values.tipo,
        data_evento: format(values.data_evento, 'yyyy-MM-dd'),
        data_ex: format(values.data_ex, 'yyyy-MM-dd'),
      };

      if (values.data_pagamento) {
        payload.data_pagamento = format(values.data_pagamento, 'yyyy-MM-dd');
      }
      if (values.fator !== undefined && values.fator !== null) {
        payload.fator = values.fator;
      }
      if (values.valor !== undefined && values.valor !== null) {
        payload.valor = values.valor;
      }
      if (values.ativo_destino_id !== undefined && values.ativo_destino_id !== null) {
        payload.ativo_destino_id = values.ativo_destino_id;
      }
      if (values.observacoes !== undefined && values.observacoes !== null && values.observacoes.trim() !== '') {
        payload.observacoes = values.observacoes;
      }

      // Adicionar campos específicos do tipo de evento ao payload se existirem e forem válidos
      switch (values.tipo) {
        case TipoEventoCorporativo.SPLIT:
        case TipoEventoCorporativo.GRUPAMENTO:
          if (values.de_quantidade !== undefined && values.de_quantidade !== null) {
            payload.de_quantidade = values.de_quantidade;
          }
          if (values.para_quantidade !== undefined && values.para_quantidade !== null) {
            payload.para_quantidade = values.para_quantidade;
          }
          break;
        case TipoEventoCorporativo.BONIFICACAO:
          if (values.quantidade_bonificacao !== undefined && values.quantidade_bonificacao !== null) {
            payload.quantidade_bonificacao = values.quantidade_bonificacao;
          }
          break;
        case TipoEventoCorporativo.SUBSCRICAO:
          if (values.valor_subscricao_por_ativo !== undefined && values.valor_subscricao_por_ativo !== null) {
            payload.valor_subscricao_por_ativo = values.valor_subscricao_por_ativo;
          }
          break;
        case TipoEventoCorporativo.AMORTIZACAO:
          if (values.valor_amortizacao_por_ativo !== undefined && values.valor_amortizacao_por_ativo !== null) {
            payload.valor_amortizacao_por_ativo = values.valor_amortizacao_por_ativo;
          }
          break;
        case TipoEventoCorporativo.OUTRO:
          // A descrição já é tratada pelo campo observacoes
          break;
      }

      // Chamar a mutação para criar o evento
      await createEvento(payload);

      toast({
        title: 'Sucesso!',
        description: 'Evento corporativo registrado com sucesso.',
      });
      onClose(); // Fechar o formulário após o sucesso
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      toast({
        title: 'Erro ao registrar evento',
        description: error.response?.data?.detail || 'Ocorreu um erro inesperado.',
        variant: 'destructive',
      });
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* Ativo ID */}
        <FormField
          control={form.control}
          name="ativo_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Ativo</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um ativo" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {isLoadingAtivos ? (
                    <SelectItem value="loading" disabled>
                      Carregando ativos...
                    </SelectItem>
                  ) : (
                    ativos?.map((ativo: Ativo) => (
                      <SelectItem key={ativo.id} value={ativo.id}>
                        {ativo.ticker} - {ativo.nome}
                      </SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Tipo de Evento */}
        <FormField
          control={form.control}
          name="tipo"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tipo de Evento</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo de evento" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {Object.values(TipoEventoCorporativo).map((tipo) => (
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

        {/* Data do Evento (data_evento) */}
        <FormField
          control={form.control}
          name="data_evento"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data do Evento</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant={'outline'}
                      className={cn(
                        'w-full pl-3 text-left font-normal',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {field.value ? (
                        format(field.value, 'PPP', { locale: ptBR })
                      ) : (
                        <span>Selecione uma data</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    disabled={(date) =>
                      date > new Date() || date < new Date('1900-01-01')
                    }
                    initialFocus
                    locale={ptBR}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Data Ex */}
        <FormField
          control={form.control}
          name="data_ex"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data Ex</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant={'outline'}
                      className={cn(
                        'w-full pl-3 text-left font-normal',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {field.value ? (
                        format(field.value, 'PPP', { locale: ptBR })
                      ) : (
                        <span>Selecione uma data</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    disabled={(date) =>
                      date > new Date() || date < new Date('1900-01-01')
                    }
                    initialFocus
                    locale={ptBR}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Data Pagamento (Opcional) */}
        <FormField
          control={form.control}
          name="data_pagamento"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data de Pagamento (Opcional)</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant={'outline'}
                      className={cn(
                        'w-full pl-3 text-left font-normal',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {field.value ? (
                        format(field.value, 'PPP', { locale: ptBR })
                      ) : (
                        <span>Selecione uma data</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    disabled={(date) =>
                      date < new Date('1900-01-01')
                    }
                    initialFocus
                    locale={ptBR}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Fator (Condicional para vários tipos) */}
        {(tipoEventoSelecionado === TipoEventoCorporativo.SPLIT ||
          tipoEventoSelecionado === TipoEventoCorporativo.GRUPAMENTO ||
          tipoEventoSelecionado === TipoEventoCorporativo.BONIFICACAO ||
          tipoEventoSelecionado === TipoEventoCorporativo.SUBSCRICAO ||
          tipoEventoSelecionado === TipoEventoCorporativo.AMORTIZACAO) && (
            <FormField
              control={form.control}
              name="fator"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Fator</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="Ex: 2.00 (para 1:2)"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => {
                        field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                      }}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}

        {/* Valor (Condicional para BONIFICACAO e AMORTIZACAO) */}
        {(tipoEventoSelecionado === TipoEventoCorporativo.BONIFICACAO ||
          tipoEventoSelecionado === TipoEventoCorporativo.AMORTIZACAO) && (
            <FormField
              control={form.control}
              name="valor"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Valor por Cota</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="Ex: 1.25"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => {
                        field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                      }}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}

        {/* Ativo Destino ID (Condicional para INCORPORACAO, FUSAO, CISAO) */}
        {(tipoEventoSelecionado === TipoEventoCorporativo.INCORPORACAO ||
          tipoEventoSelecionado === TipoEventoCorporativo.FUSAO ||
          tipoEventoSelecionado === TipoEventoCorporativo.CISAO) && (
            <FormField
              control={form.control}
              name="ativo_destino_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Ativo Destino</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione um ativo destino" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {isLoadingAtivos ? (
                        <SelectItem value="loading" disabled>
                          Carregando ativos...
                        </SelectItem>
                      ) : (
                        ativos?.map((ativo: Ativo) => (
                          <SelectItem key={ativo.id} value={ativo.id}>
                            {ativo.ticker} - {ativo.nome}
                          </SelectItem>
                        ))
                      )}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}

        {/* Campos condicionais para SPLIT/GRUPAMENTO */}
        {(tipoEventoSelecionado === TipoEventoCorporativo.SPLIT ||
          tipoEventoSelecionado === TipoEventoCorporativo.GRUPAMENTO) && (
            <>
              <FormField
                control={form.control}
                name="de_quantidade"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>De Quantidade</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        step="1"
                        placeholder="Ex: 1"
                        {...field}
                        value={field.value ?? ''}
                        onChange={(e) => {
                          field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                        }}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="para_quantidade"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Para Quantidade</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        step="1"
                        placeholder="Ex: 2 (para 1:2)"
                        {...field}
                        value={field.value ?? ''}
                        onChange={(e) => {
                          field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                        }}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </>
          )}

        {/* Campo condicional para BONIFICACAO */}
        {tipoEventoSelecionado === TipoEventoCorporativo.BONIFICACAO && (
          <FormField
            control={form.control}
            name="quantidade_bonificacao"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Quantidade de Bonificação</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    step="1"
                    placeholder="Ex: 100"
                    {...field}
                    value={field.value ?? ''}
                    onChange={(e) => {
                      field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {/* Campo condicional para SUBSCRICAO */}
        {tipoEventoSelecionado === TipoEventoCorporativo.SUBSCRICAO && (
          <FormField
            control={form.control}
            name="valor_subscricao_por_ativo"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Valor de Subscrição por Ativo</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    step="0.01"
                    placeholder="Ex: 25.50"
                    {...field}
                    value={field.value ?? ''}
                    onChange={(e) => {
                      field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {/* Campo condicional para AMORTIZACAO */}
        {tipoEventoSelecionado === TipoEventoCorporativo.AMORTIZACAO && (
          <FormField
            control={form.control}
            name="valor_amortizacao_por_ativo"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Valor de Amortização por Ativo</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    step="0.01"
                    placeholder="Ex: 1.25"
                    {...field}
                    value={field.value ?? ''}
                    onChange={(e) => {
                      field.onChange(e.target.value === '' ? undefined : Number(e.target.value));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {/* Campo condicional para OUTRO */}
        {tipoEventoSelecionado === TipoEventoCorporativo.OUTRO && (
          <FormField
            control={form.control}
            name="observacoes" // Usar 'observacoes' que já existe no schema do backend
            render={({ field }) => (
              <FormItem>
                <FormLabel>Descrição</FormLabel>
                <FormControl>
                  <Input placeholder="Descreva o evento" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        <Button type="submit" className="w-full" disabled={isCreating}>
          {isCreating ? 'Registrando...' : 'Registrar Evento'}
        </Button>
      </form>
    </Form>
  );
}