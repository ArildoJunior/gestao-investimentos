# FILE: backend/app/schemas/enums.py

from enum import Enum

# Enums de Instituicao
class TipoInstituicao(str, Enum):
    BANCO = "BANCO"
    CORRETORA = "CORRETORA"
    OUTRO = "OUTRO"


class StatusInstituicao(str, Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"


# Enums de Conta
class TipoConta(str, Enum):
    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"
    INVESTIMENTO = "INVESTIMENTO"
    PAGAMENTO = "PAGAMENTO"
    OUTRO = "OUTRO"


class StatusConta(str, Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"


class Moeda(str, Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"


# Enums de Ativo
class TipoAtivo(str, Enum):
    ACAO = "ACAO"
    FII = "FII"
    ETF = "ETF"
    BDR = "BDR"
    CRIPTOMOEDA = "CRIPTOMOEDA"
    REIT = "REIT"
    STOCK = "STOCK"
    TESOURO_DIRETO = "TESOURO_DIRETO"
    CDB = "CDB"
    LCI = "LCI"
    LCA = "LCA"
    DEBENTURE = "DEBENTURE"
    CRI = "CRI"
    CRA = "CRA"
    FUNDO_INVESTIMENTO = "FUNDO_INVESTIMENTO"
    OPCAO = "OPCAO"
    OUTRO = "OUTRO"


class StatusAtivo(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class RegiaoAtivo(str, Enum):
    BRASIL = "BRASIL"
    AMERICA_NORTE = "AMERICA_NORTE"
    EUROPA = "EUROPA"
    ASIA = "ASIA"
    OUTRO = "OUTRO"


class SegmentoFII(str, Enum):
    TIJOLO = "TIJOLO"
    PAPEL = "PAPEL"
    LOGISTICO = "LOGISTICO"
    SHOPPING = "SHOPPING"
    LAJES_CORPORATIVAS = "LAJES_CORPORATIVAS"
    HIBRIDO = "HIBRIDO"
    RECEBIVEL = "RECEBIVEL"
    FUNDO_DE_FUNDOS = "FUNDO_DE_FUNDOS"
    OUTRO = "OUTRO"


# Enums de Carteira
class TipoCarteira(str, Enum):
    REAL = "REAL"
    TESTE = "TESTE"
    SIMULADA = "SIMULADA"
    ESTRATEGIA = "ESTRATEGIA"


class ObjetivoCarteira(str, Enum):
    DIVIDENDOS = "DIVIDENDOS"
    CRESCIMENTO = "CRESCIMENTO"
    APOSENTADORIA = "APOSENTADORIA"
    INTERNACIONAL = "INTERNACIONAL"
    CRIPTO = "CRIPTO"
    LIVRE = "LIVRE"
    RENDA_PASSIVA = "RENDA_PASSIVA"
    RESERVA_EMERGENCIA = "RESERVA_EMERGENCIA"
    OUTRO = "OUTRO"


# Enums de Movimentacao
class TipoMovimentacao(str, Enum):
    COMPRA = "COMPRA"
    VENDA = "VENDA"


class TipoOperacao(str, Enum):
    SWING = "SWING"
    DAY_TRADE = "DAY_TRADE"
    POSITION = "POSITION"


# Enums de Aporte
class TipoAporte(str, Enum):
    EXTERNO = "EXTERNO"
    REINVESTIMENTO = "REINVESTIMENTO"


class OrigemAporte(str, Enum):
    DIVIDENDO = "DIVIDENDO"
    JCP = "JCP"
    RENDIMENTO = "RENDIMENTO"
    JUROS_RF = "JUROS_RF"
    GANHO_CAPITAL = "GANHO_CAPITAL"
    AMORTIZACAO = "AMORTIZACAO"
    OUTRO = "OUTRO"


# Enums de SaldoConta
class TipoSaldoConta(str, Enum):
    DEPOSITO = "DEPOSITO"
    SAQUE = "SAQUE"
    TRANSFERENCIA = "TRANSFERENCIA"
    PIX = "PIX"
    TED = "TED"
    AJUSTE = "AJUSTE"


# Enums de Provento
class TipoProvento(str, Enum):
    DIVIDENDO = "DIVIDENDO"
    JCP = "JCP"
    RENDIMENTO = "RENDIMENTO"
    AMORTIZACAO = "AMORTIZACAO"
    OUTRO = "OUTRO"


# Enums de Renda Fixa
class TipoRendaFixa(str, Enum):
    CDB = "CDB"
    LCI = "LCI"
    LCA = "LCA"
    TESOURO_DIRETO = "TESOURO_DIRETO"
    DEBENTURE = "DEBENTURE"
    CRI = "CRI"
    CRA = "CRA"
    LC = "LC"
    LIG = "LIG"
    OUTRO = "OUTRO"


class IndexadorRendaFixa(str, Enum):
    CDI = "CDI"
    IPCA = "IPCA"
    SELIC = "SELIC"
    PRE = "PRE"
    IGPM = "IGPM"
    HIBRIDO = "HIBRIDO"
    OUTRO = "OUTRO"


class LiquidezRendaFixa(str, Enum):
    DIARIA = "DIARIA"
    VENCIMENTO = "VENCIMENTO"
    SEM_LIQUIDEZ = "SEM_LIQUIDEZ"


class StatusRendaFixa(str, Enum):
    ATIVO = "ATIVO"
    VENCIDO = "VENCIDO"
    RESGATADO = "RESGATADO"


# Enums de Aluguel
class StatusAluguel(str, Enum):
    ATIVO = "ATIVO"
    ENCERRADO = "ENCERRADO"


# Enums de Evento Corporativo
class TipoEventoCorporativo(str, Enum):
    SPLIT = "SPLIT"
    GRUPAMENTO = "GRUPAMENTO"
    BONIFICACAO = "BONIFICACAO"
    SUBSCRICAO = "SUBSCRICAO"
    AMORTIZACAO = "AMORTIZACAO"
    INCORPORACAO = "INCORPORACAO"
    FUSAO = "FUSAO"
    CISAO = "CISAO"
    OUTRO = "OUTRO"


# Enums de Tributacao
class TipoImposto(str, Enum):
    IRRF = "IRRF"
    ISS = "ISS"
    PIS = "PIS"
    COFINS = "COFINS"
    OUTRO = "OUTRO"


class TipoApuracaoIR(str, Enum):
    SWING = "SWING"
    DAY_TRADE = "DAY_TRADE"
    FII = "FII"
    ETF = "ETF"
    RENDA_FIXA = "RENDA_FIXA"
    CRIPTO = "CRIPTO"
    EXTERIOR = "EXTERIOR"


class StatusDARF(str, Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"


# Enums de Alerta
class TipoAlerta(str, Enum):
    PRECO_ALVO = "PRECO_ALVO"
    REBALANCEAMENTO = "REBALANCEAMENTO"
    VENCIMENTO_RF = "VENCIMENTO_RF"
    PROVENTO = "PROVENTO"
    CONCENTRACAO = "CONCENTRACAO"
    META = "META"
    VARIACAO_PRECO = "VARIACAO_PRECO"
    ISENTOMETRO = "ISENTOMETRO"
    OUTRO = "OUTRO"


# Enums de Meta
class TipoMeta(str, Enum):
    PATRIMONIO = "PATRIMONIO"
    RENDA_PASSIVA = "RENDA_PASSIVA"
    INDEPENDENCIA_FINANCEIRA = "INDEPENDENCIA_FINANCEIRA"
    DIVIDENDOS_MENSAIS = "DIVIDENDOS_MENSAIS"
    OUTRO = "OUTRO"


# Enums de Relatorio
class TipoRelatorio(str, Enum):
    EXTRATO = "EXTRATO"
    POSICOES = "POSICOES"
    MOVIMENTACOES = "MOVIMENTACOES"
    PROVENTOS = "PROVENTOS"
    IRPF = "IRPF"
    OUTRO = "OUTRO"


# Enums de Auditoria
class TipoEntidadeAuditoria(str, Enum):
    MOVIMENTACAO = "MOVIMENTACAO"
    POSICAO = "POSICAO"
    CARTEIRA = "CARTEIRA"
    ATIVO = "ATIVO"
    CONTA = "CONTA"
    INSTITUICAO = "INSTITUICAO"
    USUARIO = "USUARIO"
    OUTRO = "OUTRO"


class AcaoAuditoria(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    OUTRO = "OUTRO"


# Enums de Opcao
class TipoOpcao(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class EstiloOpcao(str, Enum):
    AMERICANA = "AMERICANA"
    EUROPEIA = "EUROPEIA"


class DirecaoOpcao(str, Enum):
    COMPRADO = "COMPRADO"
    VENDIDO = "VENDIDO"


class StatusOpcao(str, Enum):
    ABERTA = "ABERTA"
    EXERCIDA = "EXERCIDA"
    ABANDONADA = "ABANDONADA"
    ZERADA = "ZERADA"