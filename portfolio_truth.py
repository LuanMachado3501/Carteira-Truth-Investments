"""
Carteira Truth — Análise de Portfólio com Inverse Volatility Weighting
=======================================================================
Metodologia:
    - Pesos calculados pelo inverso da volatilidade histórica (2025)
    - Ativos mais estáveis recebem maior alocação
    - Stop loss baseado em 2x a volatilidade anualizada de cada ativo

Autor: [Seu Nome]
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

CAPITAL_INICIAL = 100_000
CALIBRACAO_START = '2025-01-01'
CALIBRACAO_END   = '2025-12-31'
AVALIACAO_START  = '2026-01-02'
AVALIACAO_END    = date.today().strftime('%Y-%m-%d')

TICKERS = [
    'BPAC11.SA', 'ROXO34.SA', 'INBR32.SA', 'VALE3.SA', 'PETR4.SA',
    'ENEV3.SA',  'NEOE3.SA',  'EGIE3.SA',  'AZZA3.SA', 'KEPL3.SA',
    'TOTS3.SA',  'WEGE3.SA',  'GMAT3.SA'
]

# =============================================================================
# 1. COLETA DE DADOS
# =============================================================================

# Dados de 2025 para calibrar os pesos
data_2025 = yf.download(TICKERS, start=CALIBRACAO_START, end=CALIBRACAO_END, auto_adjust=True)['Close']

# Dados de 2026 para avaliar a performance
data_2026 = yf.download(TICKERS, start=AVALIACAO_START, end=AVALIACAO_END, auto_adjust=True)['Close']
data_2026 = data_2026.ffill().bfill()

# Benchmark
ibov = yf.download('^BVSP', start=AVALIACAO_START, end=AVALIACAO_END, auto_adjust=True)['Close']
ibov = ibov.ffill().bfill()

# =============================================================================
# 2. CÁLCULO DOS PESOS (INVERSE VOLATILITY)
# =============================================================================

retornos_2025 = data_2025.pct_change().dropna()
volatilidade   = retornos_2025.std()
vol_anualizada = volatilidade * np.sqrt(252)

inv_vol = 1 / volatilidade
pesos   = inv_vol / inv_vol.sum()

# =============================================================================
# 3. PERFORMANCE DA CARTEIRA EM 2026
# =============================================================================

precos_ini = data_2026.iloc[0]
precos_fim = data_2026.iloc[-1]

patrimonio_total = 0
performance = []

for t in TICKERS:
    peso          = pesos[t]
    valor_alocado = CAPITAL_INICIAL * peso
    retorno       = (precos_fim[t] / precos_ini[t]) - 1
    valor_final   = valor_alocado * (1 + retorno)
    patrimonio_total += valor_final

    performance.append({
        'Ticker':         t.replace('.SA', ''),
        'Peso (%)':       round(peso * 100, 2),
        'Vol 2025':       round(volatilidade[t], 4),
        'Vol Anual':      round(vol_anualizada[t], 4),
        'Retorno 2026 %': round(retorno * 100, 2),
        'Valor Final (R$)': round(valor_final, 2)
    })

df_final = pd.DataFrame(performance).sort_values(by='Peso (%)', ascending=False)

# =============================================================================
# 4. BENCHMARK
# =============================================================================

retorno_carteira = (patrimonio_total / CAPITAL_INICIAL) - 1
retorno_ibov     = (ibov.iloc[-1] / ibov.iloc[0] - 1).values[0]
alpha            = retorno_carteira - retorno_ibov

# =============================================================================
# 5. STOP LOSS POR VOLATILIDADE
# =============================================================================

stop_loss = -2 * vol_anualizada

stops = []
for t in TICKERS:
    retorno_atual = (precos_fim[t] / precos_ini[t]) - 1
    limite        = stop_loss[t]
    status        = "STOP ATINGIDO" if retorno_atual < limite else "OK"

    stops.append({
        'Ticker':       t.replace('.SA', ''),
        'Retorno (%)':  round(retorno_atual * 100, 2),
        'Stop (%)':     round(limite * 100, 2),
        'Status':       status
    })

df_stops = pd.DataFrame(stops).sort_values(by='Retorno (%)', ascending=True)

# =============================================================================
# 6. RELATÓRIO FINAL
# =============================================================================

print("\n" + "="*65)
print("  CARTEIRA TRUTH — PESOS POR VOLATILIDADE (REF: 2025)")
print("="*65)
print(df_final.to_string(index=False))

print("\n" + "-"*40)
print(f"  Patrimônio Inicial : R$ {CAPITAL_INICIAL:>12,.2f}")
print(f"  Patrimônio Atual   : R$ {patrimonio_total:>12,.2f}")
print(f"  Rentabilidade      :    {retorno_carteira*100:>10.2f}%")

print("\n" + "-"*40)
print("  BENCHMARK")
print("-"*40)
print(f"  IBOV 2026          :    {retorno_ibov*100:>10.2f}%")
print(f"  Carteira Truth     :    {retorno_carteira*100:>10.2f}%")
print(f"  Alpha              :    {alpha*100:>10.2f}%")

print("\n" + "-"*40)
print("  STOP LOSS (2x Vol Anualizada)")
print("-"*40)
print(df_stops.to_string(index=False))
print("="*65 + "\n")