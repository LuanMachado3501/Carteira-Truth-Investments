# Carteira Truth — Portfólio Hipotético com Pesos por Volatilidade

**Início:** Janeiro de 2026 | **Capital Simulado:** R$ 100.000,00 | **Benchmark:** IBOV

## Tese Central

> O Brasil só cresce de forma sustentável quando descentraliza — quando o Norte, o Nordeste e o Centro-Oeste param de depender do eixo SP-Rio para existir.

Cada ativo representa um pilar dessa tese. Não são apostas em gráficos — são apostas em estruturas que o país precisa construir independentemente do ciclo político.

## Os 5 Pilares

**1. Descentralização e Abastecimento — GMAT3**
O Grupo Mateus prova que o Brasil profundo é lucrativo. Domina Norte e Nordeste resolvendo distribuição onde o Estado é ausente. Ativo defensivo: mesmo em crise, as pessoas precisam comer.

**2. Eficiência Energética — WEGE3, EGIE3, NEOE3, ENEV3**
WEG é a racionalidade técnica aplicada à indústria. Engie e Neoenergia apostam na geração limpa como infraestrutura permanente. Eneva garante flexibilidade térmica em momentos de seca.

**3. Commodities e Soberania — VALE3, PETR4, KEPL3**
O mundo sempre precisará de ferro, petróleo e armazenagem de grãos. Kepler Weber é a peça menos óbvia: de nada adianta produzir mais grãos sem silos para guardá-los.

**4. Inteligência Financeira e Digital — BPAC11, TOTS3, ROXO34, INBR32**
Para o Brasil funcionar, dinheiro e dados precisam fluir com eficiência. BTG (capital), Totvs (gestão empresarial), Nu e Inter (eliminação da fricção bancária).

**5. Consumo — AZZA3**
Consumo discricionário de qualidade com escala e gestão comprovadas.

## Metodologia

**Inverse Volatility Weighting:** peso de cada ativo inversamente proporcional à sua volatilidade histórica de 2025. Ativos mais estáveis recebem maior alocação.

**Stop Loss:** saída quando retorno < -2x volatilidade anualizada do ativo.

## Resultados — v1 (Jan–Fev 2026)

| Métrica | Valor |
|---|---|
| Rentabilidade Carteira | +8,48% |
| IBOV no período | +17,60% |
| Alpha | -9,12% |

*Alpha negativo esperado em períodos de forte alta — inverse vol é estratégia defensiva.*

## Próximas Versões
- v2: Filtro de momentum para seleção de ativos
- v3: Rebalanceamento periódico automático
- v4: Backtest histórico

## Stack
Python | yfinance | pandas | numpy

*A analise feita para montar essa carteira foi feita no dia 28/12/2025 - desde então monitoro semanalmente as ações e o mercado.*

*Portfólio hipotético e educacional. Não constitui recomendação de investimento.*
