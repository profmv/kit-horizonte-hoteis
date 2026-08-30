# Gabarito de validação — uso do professor

Valores calculados a partir de `v3_normalizada_perfeita`, com `SEED=42`.
Use-os para conferir se a limpeza e o modelo do aluno preservaram o negócio.

## Contagens

| Item | Valor esperado |
|---|---:|
| Hotéis | 10 |
| Quartos | 426 |
| Hóspedes | 4.000 |
| Funcionários | 180 |
| Reservas limpas | 49.472 |
| Consumos limpos | 148.879 |
| Chamados | 5.000 |
| V1 bruta (60 duplicatas) | 49.532 |
| Reservas V2 brutas (40 duplicatas) | 49.512 |
| Consumos V2 brutos (55 duplicatas) | 148.934 |

## KPIs de referência

Status válidos para hospedagem: `Check-out Realizado` e `Hospedado`.

| KPI | Valor esperado | Regra |
|---|---:|---|
| Receita de hospedagem | R$ 96.180.944,00 | noites × diária, somente hospedagens válidas |
| Diárias vendidas | 129.549 | soma das noites das hospedagens válidas |
| ADR | R$ 742,43 | receita / diárias vendidas |
| Receita de extras | R$ 28.356.350,21 | quantidade × valor unitário |
| Taxa de cancelamento | 7,36% | canceladas / todas as reservas |
| No-show | 1,77% | no-show / todas as reservas |
| Ocupação histórica | 41,56% | diárias no intervalo / quartos disponíveis |
| RevPAR de referência | R$ 308,86 | receita / diárias disponíveis no período histórico |
| SLA cumprido | 78,76% | resolução ≤ 2h/8h/24h conforme prioridade |
| Avaliação média dos chamados | 3,96 | média simples de `Avaliacao_Atendimento` |

## Cuidados ao comparar

- A base contém reservas futuras até setembro de 2026. Defina e mostre o período analisado.
- Para ocupação, intercepte cada estadia com o período filtrado; não conte apenas o check-in.
- Pequenas diferenças de RevPAR podem ocorrer se o aluno limitar também a receita das reservas hospedadas que atravessam a data de referência. A regra deve ser documentada.
- Receita líquida exige a tabela de comissões por canal e, portanto, depende da implementação do aluno.
- A versão V2 só deve coincidir com este gabarito depois de corrigidas chaves, datas invertidas, categorias e duplicatas.
