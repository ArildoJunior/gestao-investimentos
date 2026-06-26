// FILE: frontend/src/types/enums.ts

// Instituição
export enum TipoInstituicao {
  BANCO = "BANCO",
  CORRETORA = "CORRETORA",
  OUTRO = "OUTRO",
}

export enum StatusInstituicao {
  ATIVA = "ATIVA",
  INATIVA = "INATIVA",
}

// Conta
export enum TipoConta {
  CORRENTE = "CORRENTE",
  POUPANCA = "POUPANCA",
  INVESTIMENTO = "INVESTIMENTO",
  PAGAMENTO = "PAGAMENTO",
  OUTRO = "OUTRO",
}

export enum StatusConta {
  ATIVA = "ATIVA",
  INATIVA = "INATIVA",
}

export enum Moeda {
  BRL = "BRL",
  USD = "USD",
  EUR = "EUR",
}

// Ativo
export enum TipoAtivo {
  ACAO = "ACAO",
  FII = "FII",
  ETF = "ETF",
  BDR = "BDR",
  CRIPTOMOEDA = "CRIPTOMOEDA",
  REIT = "REIT",
  STOCK = "STOCK",
  TESOURO_DIRETO = "TESOURO_DIRETO",
  CDB = "CDB",
  LCI = "LCI",
  LCA = "LCA",
  DEBENTURE = "DEBENTURE",
  CRI = "CRI",
  CRA = "CRA",
  FUNDO_INVESTIMENTO = "FUNDO_INVESTIMENTO",
  OPCAO = "OPCAO",
  OUTRO = "OUTRO",
}

export enum StatusAtivo {
  ATIVO = "ATIVO",
  INATIVO = "INATIVO",
}

export enum RegiaoAtivo {
  BRASIL = "BRASIL",
  AMERICA_NORTE = "AMERICA_NORTE",
  EUROPA = "EUROPA",
  ASIA = "ASIA",
  OUTRO = "OUTRO",
}

export enum SegmentoFII {
  TIJOLO = "TIJOLO",
  PAPEL = "PAPEL",
  LOGISTICO = "LOGISTICO",
  SHOPPING = "SHOPPING",
  LAJES_CORPORATIVAS = "LAJES_CORPORATIVAS",
  HIBRIDO = "HIBRIDO",
  RECEBIVEL = "RECEBIVEL",
  FUNDO_DE_FUNDOS = "FUNDO_DE_FUNDOS",
  OUTRO = "OUTRO",
}

// Carteira
export enum TipoCarteira {
  REAL = "REAL",
  TESTE = "TESTE",
  SIMULADA = "SIMULADA",
  ESTRATEGIA = "ESTRATEGIA",
}

export enum ObjetivoCarteira {
  DIVIDENDOS = "DIVIDENDOS",
  CRESCIMENTO = "CRESCIMENTO",
  APOSENTADORIA = "APOSENTADORIA",
  INTERNACIONAL = "INTERNACIONAL",
  CRIPTO = "CRIPTO",
  LIVRE = "LIVRE",
  RENDA_PASSIVA = "RENDA_PASSIVA",
  RESERVA_EMERGENCIA = "RESERVA_EMERGENCIA",
  OUTRO = "OUTRO",
}

// Movimentação
export enum TipoMovimentacao {
  COMPRA = "COMPRA",
  VENDA = "VENDA",
}

export enum TipoOperacao {
  SWING = "SWING",
  DAY_TRADE = "DAY_TRADE",
  POSITION = "POSITION",
}

// Aporte
export enum TipoAporte {
  EXTERNO = "EXTERNO",
  REINVESTIMENTO = "REINVESTIMENTO",
}

export enum OrigemAporte {
  DIVIDENDO = "DIVIDENDO",
  JCP = "JCP",
  RENDIMENTO = "RENDIMENTO",
  JUROS_RF = "JUROS_RF",
  GANHO_CAPITAL = "GANHO_CAPITAL",
  AMORTIZACAO = "AMORTIZACAO",
  OUTRO = "OUTRO",
}

// Provento
export enum TipoProvento {
  DIVIDENDO = "DIVIDENDO",
  JCP = "JCP",
  RENDIMENTO = "RENDIMENTO",
  AMORTIZACAO = "AMORTIZACAO",
  OUTRO = "OUTRO",
}

// Evento Corporativo
export enum TipoEventoCorporativo {
  SPLIT = "SPLIT",
  GRUPAMENTO = "GRUPAMENTO",
  BONIFICACAO = "BONIFICACAO",
  SUBSCRICAO = "SUBSCRICAO",
  AMORTIZACAO = "AMORTIZACAO",
  INCORPORACAO = "INCORPORACAO",
  FUSAO = "FUSAO",
  CISAO = "CISAO",
  OUTRO = "OUTRO",
}