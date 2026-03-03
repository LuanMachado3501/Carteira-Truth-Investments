"""
Carteira Truth v2 — Inverse Volatility + Filtro de Momentum 12-1
=================================================================
Frequência recomendada de execução:
    - Diária    → monitorar retorno atual e alertas de stop loss
    - Mensal    → recalibrar filtro de momentum (recalcula scores)
    - Semestral → rebalancear pesos (recalcula inverse vol)

Metodologia:
    - Pesos base: inverso da volatilidade histórica (calibração 2025)
    - Filtro momentum 12-1: ativo com retorno negativo nos últimos
      12 meses (excluindo último mês) tem peso reduzido à metade
    - Stop loss: saída quando retorno < -2x volatilidade anualizada

Autor: Luan Machado
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

CAPITAL_INICIAL  = 100_000

CALIBRACAO_START = '2025-01-01'
CALIBRACAO_END   = '2025-12-31'

AVALIACAO_START  = '2026-01-02'
AVALIACAO_END    = date.today().strftime('%Y-%m-%d')

# Janela momentum: últimos 12 meses excluindo o último mês
MOMENTUM_END     = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
MOMENTUM_START   = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')

# Ativos v2: NEOE3 removida, EQTL3 entra
TICKERS = [
    'BPAC11.SA', 'ROXO34.SA', 'INBR32.SA', 'VALE3.SA',  'PETR4.SA',
    'ENEV3.SA',  'EQTL3.SA',  'EGIE3.SA',  'AZZA3.SA',  'KEPL3.SA',
    'TOTS3.SA',  'WEGE3.SA',  'GMAT3.SA'
]

# =============================================================================
# 1. COLETA DE DADOS
# =============================================================================

print("\nBaixando dados da Carteira Truth...")

data_cal  = yf.download(TICKERS, start=CALIBRACAO_START, end=CALIBRACAO_END, auto_adjust=True)['Close']
data_aval = yf.download(TICKERS, start=AVALIACAO_START,  end=AVALIACAO_END,  auto_adjust=True)['Close']
data_mom  = yf.download(TICKERS, start=MOMENTUM_START,   end=MOMENTUM_END,   auto_adjust=True)['Close']
ibov      = yf.download('^BVSP', start=AVALIACAO_START,  end=AVALIACAO_END,  auto_adjust=True)['Close']

for df in [data_aval, data_mom, ibov]:
    df.ffill(inplace=True)
    df.bfill(inplace=True)

# =============================================================================
# 2. VOLATILIDADE E PESOS BASE (calibração 2025)
# =============================================================================

retornos_cal = data_cal.pct_change().dropna()
vol          = retornos_cal.std()
vol_anual    = vol * np.sqrt(252)

inv_vol    = 1 / vol
pesos_base = inv_vol / inv_vol.sum()

# =============================================================================
# 3. FILTRO DE MOMENTUM 12-1
# =============================================================================

momentum_scores = {}
for t in TICKERS:
    if t in data_mom.columns:
        serie = data_mom[t].dropna()
        if len(serie) >= 2:
            momentum_scores[t] = (serie.iloc[-1] / serie.iloc[0]) - 1
        else:
            momentum_scores[t] = np.nan
    else:
        momentum_scores[t] = np.nan

# Peso pela metade se momentum negativo, renormaliza
pesos_ajustados = {}
for t in TICKERS:
    score = momentum_scores.get(t, np.nan)
    pesos_ajustados[t] = pesos_base[t] if (pd.isna(score) or score >= 0) else pesos_base[t] * 0.5

total_peso      = sum(pesos_ajustados.values())
pesos_ajustados = {t: p / total_peso for t, p in pesos_ajustados.items()}

# =============================================================================
# 4. PERFORMANCE
# =============================================================================

precos_ini  = data_aval.iloc[0]
precos_fim  = data_aval.iloc[-1]
stop_loss   = -2 * vol_anual
patrimonio  = 0
performance = []

for t in TICKERS:
    peso          = pesos_ajustados[t]
    peso_original = pesos_base[t]
    valor_alocado = CAPITAL_INICIAL * peso
    retorno       = (precos_fim[t] / precos_ini[t]) - 1
    valor_final   = valor_alocado * (1 + retorno)
    patrimonio   += valor_final

    score      = momentum_scores.get(t, np.nan)
    mom_status = "OK" if pd.isna(score) or score >= 0 else "HALF (mom<0)"
    stop_st    = "STOP" if retorno < stop_loss[t] else "OK"

    performance.append({
        'Ticker':           t.replace('.SA', ''),
        'Peso Base (%)':    round(peso_original * 100, 2),
        'Momentum':         mom_status,
        'Score Mom (%)':    round(score * 100, 2) if not pd.isna(score) else 'N/A',
        'Peso Final (%)':   round(peso * 100, 2),
        'Vol Anual':        round(vol_anual[t], 4),
        'Retorno 2026 (%)': round(retorno * 100, 2),
        'Valor Final (R$)': round(valor_final, 2),
        'Stop (%)':         round(stop_loss[t] * 100, 2),
        'Stop Status':      stop_st,
    })

df_perf          = pd.DataFrame(performance).sort_values('Peso Final (%)', ascending=False)
retorno_carteira = (patrimonio / CAPITAL_INICIAL) - 1
retorno_ibov     = (ibov.iloc[-1] / ibov.iloc[0] - 1).values[0]
alpha            = retorno_carteira - retorno_ibov
retorno_v1       = 0.0848
alpha_v1         = retorno_v1 - 0.1760

# =============================================================================
# 5. RELATÓRIO
# =============================================================================

sep  = "=" * 70
sep2 = "-" * 70

print(f"\n{sep}")
print("  CARTEIRA TRUTH v2 — INVERSE VOL + FILTRO MOMENTUM 12-1")
print(f"  Período: {AVALIACAO_START} → {AVALIACAO_END}")
print(f"{sep}")
print(df_perf[['Ticker','Peso Base (%)','Momentum','Score Mom (%)','Peso Final (%)','Retorno 2026 (%)','Stop Status']].to_string(index=False))

print(f"\n{sep2}")
print(f"  Patrimônio Inicial : R$ {CAPITAL_INICIAL:>12,.2f}")
print(f"  Patrimônio Atual   : R$ {patrimonio:>12,.2f}")
print(f"  Rentabilidade      :    {retorno_carteira*100:>10.2f}%")
print(f"{sep2}")
print(f"  IBOV               :    {retorno_ibov*100:>10.2f}%")
print(f"  Alpha v2           :    {alpha*100:>10.2f}%")
print(f"{sep2}")
print(f"  Referência v1      :    {retorno_v1*100:>10.2f}%   Alpha v1: {alpha_v1*100:.2f}%")

stops_atingidos = df_perf[df_perf['Stop Status'] == 'STOP']
if not stops_atingidos.empty:
    print(f"\n  ⚠️  ALERTAS DE STOP LOSS:")
    print(stops_atingidos[['Ticker','Retorno 2026 (%)','Stop (%)']].to_string(index=False))

print(f"\n{sep}")
print("  DETALHAMENTO DE PESOS E VALORES")
print(f"{sep}")
print(df_perf[['Ticker','Peso Base (%)','Peso Final (%)','Vol Anual','Valor Final (R$)']].to_string(index=False))
print(f"{sep}\n")
