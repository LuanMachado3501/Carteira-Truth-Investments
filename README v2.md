# Carteira Truth — v2
**Início da v2:** Março de 2026 | **Benchmark:** IBOV

| | Carteira Truth | Carteira Momentum |
|---|---|---|
| **Capital de origem** | R$ 100.000,00  | R$ 100.000,00 (novo) |
| **Início** | Janeiro 2026 | Março 2026 |

> *"Não basta saber o que comprar. É preciso saber quando o mercado concorda com você."*

---

## O que mudou da v1 para a v2

A v1 provou o conceito: uma carteira construída sobre tese fundamentalista, com pesos calibrados por volatilidade histórica, entregou **+8,48%** em Jan-Fev 2026 contra **+17,60%** do IBOV. O alpha negativo era esperado — inverse volatility é uma estratégia defensiva que sacrifica upside em períodos de forte alta generalizada.

A v2 adiciona duas camadas:

**1. Filtro de Momentum 12-1 na Carteira Truth**
Ativos com retorno negativo nos últimos 12 meses (excluindo o mês mais recente) têm seu peso reduzido à metade. A carteira continua guiada pela tese, mas agora respeita o que o mercado está sinalizando sobre cada ativo.

**2. Carteira Momentum — fator puro e independente**
Uma segunda carteira paralela que varre o universo do IBOV (~70 ativos), seleciona os de maior momentum positivo por setor (máx. 2 por setor para evitar concentração) e aplica inverse volatility nos selecionados. Capital separado. Lógica separada. Serve como contraponto quantitativo à Carteira Truth, que é fundamentalista.

---

## Tese Central (mantida)

> O Brasil só cresce de forma sustentável quando descentraliza — quando o Norte, o Nordeste e o Centro-Oeste param de depender do eixo SP-Rio para existir.

Cada ativo da Carteira Truth representa um pilar dessa tese. A v2 não abandona essa convicção — ela adiciona disciplina quantitativa para não carregar posições que o mercado está punindo sem critério de saída.

---

## Carteira Truth v2 — Os 5 Pilares

### 1. Descentralização e Abastecimento
| Ticker | Decisão | Tese |
|--------|---------|------|
| GMAT3 | ✅ Mantido | Domina Norte e Nordeste onde o Estado é ausente. +27% em 2026 confirma recuperação após punição exagerada. |

### 2. Eficiência Energética
| Ticker | Decisão | Tese |
|--------|---------|------|
| WEGE3 | ✅ Mantido | Qualidade estrutural. Trimestre ruim não quebra empresa de 60 anos de excelência operacional. |
| ENEV3 | ⚠️ Mantido com atenção | Melhor fundamento do pilar. Risco regulatório ANEEL real, mas cenário geopolítico joga a favor. |
| EGIE3 | ⚠️ Em observação | Aguarda próximo trimestre e destino dos R$ 2bi em debêntures. Gatilho de saída definido. |
| EQTL3 | 🆕 Entrada | Substitui NEOE3. Distribuidora no Norte/Nordeste, alinhada com a tese geográfica, sem curtailment. |
| ~~NEOE3~~ | ❌ Saiu | OPA com teto definido. Sem upside. |

### 3. Commodities e Soberania
| Ticker | Decisão | Tese |
|--------|---------|------|
| VALE3 | ✅ Mantido | Reposicionamento em cobre é a jogada certa. Curto prazo beneficiado pelo cenário geopolítico. |
| PETR4 | ✅ Mantido | Máquina de caixa. P/L ~6x, dividend yield ~14%. Guerra é catalisador imediato. |
| KEPL3 | ✅ Transitório | Fusão com GPT a R$11 + prêmio. Captura +14% se aprovada. Substituta em avaliação: SLCE3 ou RANI3. |

### 4. Inteligência Financeira e Digital
| Ticker | Decisão | Tese |
|--------|---------|------|
| BPAC11 | ✅ Mantido | BTG em transição para banco múltiplo real — asset, IB, wealth (Julius Bär), ativos físicos. ROE histórico de 26,9% em 2025. |
| TOTS3 | ⚠️ Mantido com atenção | 91% de receita recorrente protege no longo prazo. Monitorar impacto real da IA nos próximos 2 trimestres. |
| ROXO34 | ✅ Mantido | Lucro +50% no 4T25. Tese de expansão LATAM e licença bancária nos EUA intacta. Queda em Jan/Fev foi ruído de correlação tech, não fundamento. |
| INBR32 | ⚠️ Mantido com atenção | Lucro recorde em 2025. Gatilho de saída: descontinuação dos BDRs sem estrutura clara ou ROE 2026 abaixo de 20%. |

### 5. Consumo
| Ticker | Decisão | Tese |
|--------|---------|------|
| AZZA3 | ✅ Mantido | P/L de 7x contra média histórica de 70x. Valuation absurdamente barato justifica paciência com reestruturação da Hering. |

---

## Metodologia v2

### Carteira Truth
**Inverse Volatility Weighting** com filtro de momentum:

```
1. Calibração de pesos
   → Vol histórica de 2025 por ativo
   → Peso base = (1/vol) / Σ(1/vol)

2. Filtro Momentum 12-1
   → Score = retorno entre t-12m e t-1m
   → Score < 0: peso reduzido à metade
   → Pesos renormalizados para somar 100%

3. Stop Loss
   → Saída quando retorno < -2x volatilidade anualizada
```

### Carteira Momentum
**Fator puro sobre universo IBOV:**

```
1. Universo
   → ~70 ativos do IBOV organizados por setor

2. Score Momentum 12-1
   → Retorno entre t-12m e t-1m para cada ativo
   → Apenas scores positivos são elegíveis

3. Seleção
   → Top 2 por setor (evita concentração setorial)
   → Resultado: 30+ ativos diversificados

4. Pesos
   → Inverse volatility nos ativos selecionados

5. Rebalanceamento
   → Mensal: recalcula scores e ajusta posições
```

---

## Resultados — v1 (Jan–Fev 2026, referência)

| Métrica | Valor |
|---------|-------|
| Rentabilidade Carteira Truth v1 | +8,48% |
| IBOV no período | +17,60% |
| Alpha | -9,12% |

*Alpha negativo esperado em período de forte alta — inverse vol é estratégia defensiva.*

---

## Arquivos do Repositório

| Arquivo | Descrição | Frequência de execução |
|---------|-----------|----------------------|
| `carteira_truth_v1.py` | Carteira Truth original | Referência histórica |
| `carteira_truth_v2.py` | Carteira Truth com filtro de momentum | Diária (monitoramento) / Mensal (recalibração) |
| `carteira_momentum_v2.py` | Carteira Momentum fator puro | Mensal (rebalanceamento) |

---

## Frequência de Execução Recomendada

**`carteira_truth_v2.py`**
- **Diária** → monitora retorno acumulado e alertas de stop loss
- **Mensal** → recalcula scores de momentum, ajusta pesos se necessário
- **Semestral** → recalibra pesos base com nova janela de volatilidade

**`carteira_momentum_v2.py`**
- **Mensal** → recalcula momentum de todo o universo IBOV, vende o que saiu do filtro, compra o que entrou

---

## Próximas Versões

- **v3:** Rebalanceamento periódico automático com log de operações
- **v4:** Backtest histórico completo (2020–2025)
- **v5:** Dashboard interativo com visualização de pesos e performance

---

## Stack

`Python` | `yfinance` | `pandas` | `numpy`

---

*Portfólio hipotético e educacional. Não constitui recomendação de investimento.*
