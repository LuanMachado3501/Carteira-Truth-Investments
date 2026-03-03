"""
Carteira Momentum v2 — Fator Puro sobre Universo IBOV
======================================================
Frequência recomendada de execução:
    - Mensal → recalcula momentum scores e rebalanceia a carteira
      Na primeira execução: define preço de entrada (hoje)
      Nas seguintes: compara com preço de entrada registrado

Metodologia:
    - Universo: ativos do IBOV organizados por setor
    - Filtro: retorno 12-1 meses positivo
      (retorno entre t-12m e t-1m, excluindo o mês mais recente)
    - Seleção: até 2 ativos por setor com maior momentum score
    - Pesos: inverse volatility nos ativos selecionados
    - Entrada: preço de fechamento da execução de hoje

Autor: [Seu Nome]
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

CAPITAL_INICIAL = 100_000

hoje           = date.today()
HOJE_STR       = hoje.strftime('%Y-%m-%d')

# Uma única janela de 13 meses até hoje — calculamos 12-1 internamente
JANELA_START   = (hoje - timedelta(days=400)).strftime('%Y-%m-%d')
JANELA_END     = HOJE_STR

# =============================================================================
# UNIVERSO IBOV POR SETOR (máx 2 por setor)
# Tickers com histórico de problemas no yfinance removidos
# =============================================================================

IBOV_UNIVERSE = {
    'Petróleo e Gás':    ['PETR4.SA', 'PETR3.SA', 'PRIO3.SA', 'RECV3.SA', 'ENEV3.SA'],
    'Mineração':         ['VALE3.SA', 'CMIN3.SA', 'CSNA3.SA'],
    'Siderurgia':        ['GGBR4.SA', 'USIM5.SA', 'GOAU4.SA'],
    'Energia Elétrica':  ['EGIE3.SA', 'NEOE3.SA', 'CPFE3.SA', 'ENGI11.SA', 'EQTL3.SA', 'CMIG4.SA'],
    'Bancos':            ['ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'SANB11.SA', 'BPAC11.SA'],
    'Fintechs':          ['ROXO34.SA', 'INBR32.SA'],
    'Seguros':           ['BBSE3.SA', 'IRBR3.SA', 'PSSA3.SA'],
    'Varejo':            ['MGLU3.SA', 'AZZA3.SA', 'LREN3.SA'],
    'Alimentos':         ['ABEV3.SA', 'BEEF3.SA', 'BRFS3.SA', 'JBSS3.SA'],
    'Saúde':             ['RDOR3.SA', 'HAPV3.SA', 'HYPE3.SA', 'FLRY3.SA', 'RADL3.SA'],
    'Telecom':           ['VIVT3.SA', 'TIMS3.SA'],
    'Tecnologia':        ['TOTS3.SA', 'LWSA3.SA', 'CASH3.SA'],
    'Construção Civil':  ['CYRE3.SA', 'MRVE3.SA', 'EVEN3.SA', 'DIRR3.SA', 'EZTC3.SA'],
    'Logística':         ['RAIL3.SA', 'ECOR3.SA', 'AZUL4.SA'],
    'Agro/Insumos':      ['KEPL3.SA', 'SLCE3.SA', 'RANI3.SA', 'AGRO3.SA'],
    'Papel e Celulose':  ['SUZB3.SA', 'KLBN11.SA'],
    'Utilidades':        ['SBSP3.SA', 'CSMG3.SA', 'SAPR11.SA'],
    'Indústria':         ['WEGE3.SA', 'ROMI3.SA'],
    'Distribuição':      ['GMAT3.SA', 'ASAI3.SA', 'PCAR3.SA'],
    'Shoppings':         ['MULT3.SA', 'IGTI11.SA'],
}

ALL_TICKERS = list({t for tickers in IBOV_UNIVERSE.values() for t in tickers})

# =============================================================================
# 1. COLETA — uma única janela de 13 meses
# =============================================================================

print(f"\nBaixando dados da Carteira Momentum...")
print(f"Universo: {len(ALL_TICKERS)} ativos | Data de entrada: {HOJE_STR}")

data = yf.download(
    ALL_TICKERS,
    start=JANELA_START,
    end=JANELA_END,
    auto_adjust=True,
    progress=True
)['Close']

# Mantém só colunas com dados suficientes (mínimo 200 pregões)
data = data.dropna(axis=1, thresh=200)
data.ffill(inplace=True)

tickers_disponiveis = list(data.columns)
print(f"Tickers com dados suficientes: {len(tickers_disponiveis)}")

# =============================================================================
# 2. CÁLCULO DE MOMENTUM 12-1
#    - Preço de 12 meses atrás: iloc mais próximo de t-365 dias
#    - Preço de 1 mês atrás: iloc mais próximo de t-30 dias
#    - Score = retorno entre esses dois pontos (exclui volatilidade recente)
# =============================================================================

idx = data.index

# Datas de referência
data_12m = hoje - timedelta(days=365)
data_1m  = hoje - timedelta(days=30)

# Encontra o índice mais próximo disponível
def idx_mais_proximo(datas_index, data_alvo):
    diffs = abs(datas_index - pd.Timestamp(data_alvo))
    return diffs.argmin()

i_12m = idx_mais_proximo(idx, data_12m)
i_1m  = idx_mais_proximo(idx, data_1m)

momentum_scores = {}
for t in tickers_disponiveis:
    p_12m = data[t].iloc[i_12m]
    p_1m  = data[t].iloc[i_1m]
    if pd.isna(p_12m) or pd.isna(p_1m) or p_12m == 0:
        momentum_scores[t] = np.nan
    else:
        momentum_scores[t] = (p_1m / p_12m) - 1

# =============================================================================
# 3. SELEÇÃO POR SETOR (top 2 momentum positivo)
# =============================================================================

ativos_selecionados = []
selecao_por_setor   = []

for setor, tickers in IBOV_UNIVERSE.items():
    candidatos = []
    for t in tickers:
        if t not in tickers_disponiveis:
            continue
        score = momentum_scores.get(t, np.nan)
        if not pd.isna(score) and score > 0:
            candidatos.append((t, score))

    candidatos.sort(key=lambda x: x[1], reverse=True)
    for t, score in candidatos[:2]:
        ativos_selecionados.append(t)
        selecao_por_setor.append({
            'Setor':         setor,
            'Ticker':        t.replace('.SA', ''),
            'Score Mom (%)': round(score * 100, 2),
        })

# =============================================================================
# 4. VOLATILIDADE E PESOS
# =============================================================================

retornos = data[ativos_selecionados].pct_change().dropna()
vol      = retornos.std()
vol      = vol[vol > 0].dropna()

ativos_validos = [t for t in ativos_selecionados if t in vol.index]

if not ativos_validos:
    print("\n⚠️  Nenhum ativo passou todos os filtros.")
    exit()

inv_vol = 1 / vol[ativos_validos]
pesos   = inv_vol / inv_vol.sum()

# =============================================================================
# 5. CARTEIRA DE ENTRADA (preços de hoje)
# =============================================================================

precos_hoje = data.iloc[-1]

resultado = []
for t in ativos_validos:
    peso          = pesos[t]
    valor_alocado = CAPITAL_INICIAL * peso
    preco_entrada = precos_hoje[t]
    cotas         = valor_alocado / preco_entrada if preco_entrada > 0 else 0
    setor_ativo   = next((s for s, ts in IBOV_UNIVERSE.items() if t in ts), 'N/A')
    score         = momentum_scores.get(t, np.nan)
    vol_anual     = vol[t] * np.sqrt(252)

    resultado.append({
        'Setor':           setor_ativo,
        'Ticker':          t.replace('.SA', ''),
        'Peso (%)':        round(peso * 100, 2),
        'Score Mom (%)':   round(score * 100, 2) if not pd.isna(score) else 'N/A',
        'Preço Entrada':   round(preco_entrada, 2),
        'Cotas':           round(cotas, 4),
        'Valor Alocado':   round(valor_alocado, 2),
        'Vol Anual':       round(vol_anual, 4),
        'Stop (%)':        round(-2 * vol_anual * 100, 2),
    })

df_resultado = pd.DataFrame(resultado).sort_values('Peso (%)', ascending=False)

# =============================================================================
# 6. RELATÓRIO
# =============================================================================

sep  = "=" * 78
sep2 = "-" * 78

print(f"\n{sep}")
print("  CARTEIRA MOMENTUM v2 — FATOR PURO | UNIVERSO IBOV")
print(f"  Data de entrada : {HOJE_STR}  |  Capital: R$ {CAPITAL_INICIAL:,.2f}")
print(f"  Ativos selecionados: {len(ativos_validos)} | Setores cobertos: {df_resultado['Setor'].nunique()}")
print(f"  Score calculado entre: {data.index[i_12m].date()} → {data.index[i_1m].date()}")
print(f"{sep}")
print(df_resultado[['Setor','Ticker','Peso (%)','Score Mom (%)','Preço Entrada','Cotas','Valor Alocado','Stop (%)']].to_string(index=False))

print(f"\n{sep2}")
print(f"  Total alocado  : R$ {df_resultado['Valor Alocado'].sum():>12,.2f}")

print(f"\n{sep}")
print("  RANKING COMPLETO DE MOMENTUM POR SETOR (todos os candidatos)")
print(f"{sep}")
df_sel = pd.DataFrame(selecao_por_setor).sort_values('Score Mom (%)', ascending=False)
print(df_sel.to_string(index=False))

proxima = (hoje + timedelta(days=30)).strftime('%Y-%m-%d')
print(f"\n{sep2}")
print(f"  Próximo rebalanceamento recomendado: {proxima}")
print(f"  Rode novamente em {proxima} para recalcular momentum e ajustar posições.")
print(f"{sep}\n")