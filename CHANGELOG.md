# CHANGELOG — Carteira Truth

Histórico de versões e decisões do portfólio.

---

## [v2] — Março 2026

### Adicionado
- **Filtro de Momentum 12-1** na Carteira Truth
  - Ativos com retorno negativo nos últimos 12 meses (excluindo o mês mais recente) têm peso reduzido à metade
  - Pesos renormalizados após o ajuste
- **Carteira Momentum v2** — nova carteira independente
  - Universo: ~70 ativos do IBOV organizados por setor
  - Seleção: top 2 por setor com maior momentum positivo
  - Pesos: inverse volatility nos selecionados
  - Capital: R$ 100.000,00 independente da Carteira Truth
  - Rebalanceamento mensal
- **Score de Momentum** exibido no relatório de cada ativo
- **Coluna Stop Status** com alerta explícito quando stop loss é atingido

### Alterações na carteira
- `NEOE3` → **removida** (OPA com teto definido, sem upside)
- `EQTL3` → **entrada** (substitui NEOE3, distribuidora Norte/Nordeste sem curtailment)
- `KEPL3` → **transitória** (aguarda conclusão da fusão com GPT; substituta em avaliação: SLCE3 ou RANI3)

### Ativos em observação
- `EGIE3` — aguarda próximo trimestre e destino dos R$ 2bi em debêntures
- `TOTS3` — monitorar impacto real da IA nos próximos 2 trimestres
- `INBR32` — monitorar descontinuação dos BDRs e convergência do ROE

### Resultados da v1 (referência)
| Período | Carteira Truth | IBOV | Alpha |
|---------|---------------|------|-------|
| Jan–Fev 2026 | +8,48% | +17,60% | -9,12% |

*Alpha negativo esperado — inverse vol é estratégia defensiva em períodos de forte alta.*

---

## [v1] — Janeiro 2026

### Lançamento
- Carteira Truth com **13 ativos** organizados em 5 pilares temáticos
- Metodologia: **Inverse Volatility Weighting** calibrado em 2025
- Stop loss: -2x volatilidade anualizada por ativo
- Benchmark: IBOV

### Composição inicial
| Pilar | Ativos |
|-------|--------|
| Descentralização e Abastecimento | GMAT3 |
| Eficiência Energética | WEGE3, EGIE3, NEOE3, ENEV3 |
| Commodities e Soberania | VALE3, PETR4, KEPL3 |
| Inteligência Financeira e Digital | BPAC11, TOTS3, ROXO34, INBR32 |
| Consumo | AZZA3 |

### Tese
> O Brasil só cresce de forma sustentável quando descentraliza — quando o Norte, o Nordeste e o Centro-Oeste param de depender do eixo SP-Rio para existir.

---

*Carteira hipotética e educacional. Não constitui recomendação de investimento.*
