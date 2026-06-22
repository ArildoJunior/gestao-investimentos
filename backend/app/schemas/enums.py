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
    OUTRO = "OUTRO" # Adicionado para cobrir casos gerais

class StatusConta(str, Enum): # Adicionado com base no modelo de dados
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

class StatusAtivo(str, Enum): # Adicionado com base no modelo de dados
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"

class RegiaoAtivo(str, Enum): # Adicionado com base no modelo de dados
    BRASIL = "BRASIL"
    AMERICA_NORTE = "AMERICA_NORTE"
    EUROPA = "EUROPA"
    ASIA = "ASIA"
    OUTRO = "OUTRO"

class SegmentoFII(str, Enum): # Adicionado com base no modelo de dados
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
    DIVIDENDOS = "DIVIDENDOS" # Corrigido conforme docx
    CRESCIMENTO = "CRESCIMENTO"
    APOSENTADORIA = "APOSENTADORIA"
    INTERNACIONAL = "INTERNACIONAL" # Adicionado conforme docx
    CRIPTO = "CRIPTO" # Adicionado conforme docx
    LIVRE = "LIVRE" # Adicionado conforme docx
    RENDA_PASSIVA = "RENDA_PASSIVA"
    RESERVA_EMERGENCIA = "RESERVA_EMERGENCIA"
    OUTRO = "OUTRO"

# Enums de Movimentacao
class TipoMovimentacao(str, Enum):
    COMPRA = "COMPRA"
    VENDA = "VENDA"

class TipoOperacao(str, Enum):
    SWING = "SWING" # Corrigido conforme docx
    DAY_TRADE = "DAY_TRADE"
    POSITION = "POSITION"

# NOVO: Enums de Aporte
class TipoAporte(str, Enum):
    EXTERNO = "EXTERNO"
    REINVESTIMENTO = "REINVESTIMENTO"

class OrigemAporte(str, Enum):
    DIVIDENDO = "DIVIDENDO"
    JCP = "JCP"
    RENDIMENTO = "RENDIMENTO"
    JUROS_RF = "JUROS_RF"
    GANHO_CAPITAL = "GANHO_CAPITAL"
    OUTRO = "OUTRO"
    # O dossiê técnico menciona "NULL" para origem, mas em um Enum,
    # geralmente representamos a ausência com Optional ou None no modelo,
    # não como um membro do Enum. Se for estritamente necessário ter um
    # membro para "NULL", ele pode ser adicionado.

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
    LC = "LC" # Adicionado conforme docx
    LIG = "LIG" # Adicionado conforme docx
    OUTRO = "OUTRO"

class IndexadorRendaFixa(str, Enum):
    CDI = "CDI"
    IPCA = "IPCA"
    SELIC = "SELIC"
    PRE = "PRE" # Corrigido conforme docx
    IGPM = "IGPM"
    HIBRIDO = "HIBRIDO" # Adicionado conforme docx
    OUTRO = "OUTRO"

class LiquidezRendaFixa(str, Enum): # Adicionado com base no modelo de dados
    DIARIA = "DIARIA"
    VENCIMENTO = "VENCIMENTO"
    SEM_LIQUIDEZ = "SEM_LIQUIDEZ"

class StatusRendaFixa(str, Enum): # Adicionado com base no modelo de dados
    ATIVO = "ATIVO"
    VENCIDO = "VENCIDO"
    RESGATADO = "RESGATADO"

# Enums de Aluguel
class StatusAluguel(str, Enum): # Adicionado com base no modelo de dados
    ATIVO = "ATIVO"
    ENCERRADO = "ENCERRADO"

# Enums de Evento Corporativo
class TipoEventoCorporativo(str, Enum):
    SPLIT = "SPLIT" # Adicionado conforme docx
    GRUPAMENTO = "GRUPAMENTO"
    BONIFICACAO = "BONIFICACAO"
    SUBSCRICAO = "SUBSCRICAO" # Corrigido para SUBSCRICAO
    AMORTIZACAO = "AMORTIZACAO"
    INCORPORACAO = "INCORPORACAO"
    FUSAO = "FUSAO"
    CISAO = "CISAO" # Corrigido para CISAO
    OUTRO = "OUTRO"

# Enums de Tributacao
class TipoImposto(str, Enum): # Este enum não aparece no docx, mas é genérico.
    IRRF = "IRRF"
    ISS = "ISS"
    PIS = "PIS"
    COFINS = "COFINS"
    OUTRO = "OUTRO"

class TipoApuracaoIR(str, Enum): # Adicionado com base no modelo de dados
    SWING = "SWING"
    DAY_TRADE = "DAY_TRADE"
    FII = "FII"
    ETF = "ETF"
    RENDA_FIXA = "RENDA_FIXA"
    CRIPTO = "CRIPTO"
    EXTERIOR = "EXTERIOR"

class StatusDARF(str, Enum): # Adicionado com base no modelo de dados
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"

# Enums de Alerta
class TipoAlerta(str, Enum):
    PRECO_ALVO = "PRECO_ALVO"
    REBALANCEAMENTO = "REBALANCEAMENTO"
    VENCIMENTO_RF = "VENCIMENTO_RF" # Corrigido conforme docx
    PROVENTO = "PROVENTO"
    CONCENTRACAO = "CONCENTRACAO" # Adicionado conforme docx
    META = "META"
    VARIACAO_PRECO = "VARIACAO_PRECO" # Adicionado conforme docx
    ISENTOMETRO = "ISENTOMETRO" # Adicionado conforme docx
    OUTRO = "OUTRO"

# Enums de Meta
class TipoMeta(str, Enum):
    PATRIMONIO = "PATRIMONIO"
    RENDA_PASSIVA = "RENDA_PASSIVA"
    INDEPENDENCIA_FINANCEIRA = "INDEPENDENCIA_FINANCEIRA" # Adicionado conforme docx
    DIVIDENDOS_MENSAIS = "DIVIDENDOS_MENSAIS" # Adicionado conforme docx
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
    INSERT = "INSERT" # Corrigido conforme docx
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    # LEITURA não está no docx, mas se for necessário, pode ser adicionado.
    OUTRO = "OUTRO"

# Enums de Opcao (Grupo 11 - Avançado)
class TipoOpcao(str, Enum): # Adicionado com base no modelo de dados
    CALL = "CALL"
    PUT = "PUT"

class EstiloOpcao(str, Enum): # Adicionado com base no modelo de dados
    AMERICANA = "AMERICANA"
    EUROPEIA = "EUROPEIA"

class DirecaoOpcao(str, Enum): # Adicionado com base no modelo de dados
    COMPRADO = "COMPRADO"
    VENDIDO = "VENDIDO"

class StatusOpcao(str, Enum): # Adicionado com base no modelo de dados
    ABERTA = "ABERTA"
    EXERCIDA = "EXERCIDA"
    ABANDONADA = "ABANDONADA"
    ZERADA = "ZERADA"
