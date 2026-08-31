# Horizonte Hotéis & Resorts — Guia de estudo Power BI

## Ponto de partida obrigatório

Comece pela **V1 desnormalizada**. A tarefa inclui identificar os assuntos
repetidos e separar hotéis, quartos, hóspedes, reservas e demais entidades. A V2
é somente um checkpoint opcional para comparação depois que seu modelo estiver
proposto; não deve ser usada como ponto de partida.

Dataset sintético de hotelaria: **49,472 reservas**,
148,879 consumos extras e 5,000 chamados de
manutenção em 10 hotéis (426 quartos),
06/2024 a 09/2026. Data de referência dos status:
**30/06/2026**. SEED=42 — reproduzível. Sem campos vazios:
estados são expressos em `Status_Reserva`.

## As três versões

| Pasta | Conteúdo | Objetivo |
|---|---|---|
| `v1_desnormalizada_com_erros/` | 1 CSV (grão = reserva; consumos agregados) | Limpar e normalizar no Power Query. Bônus: discutir a **perda de grão** dos consumos agregados |
| `v2_normalizada_com_erros/` | 7 CSVs sujos | Limpeza tabela a tabela + relacionamentos |
| `v3_normalizada_perfeita/` | 7 CSVs limpos | Gabarito validado (sem overlap de reservas, FKs íntegras) |

Modelo: `hoteis 1─N quartos 1─N reservas N─1 hospedes`;
`reservas 1─N consumos_extras`; `quartos 1─N chamados N─1 funcionarios`.
Duas tabelas fato com grãos diferentes (reserva × lançamento de consumo) —
exercício clássico de modelo com múltiplas fatos.

## Regras de negócio reais embutidas (explorem nas análises!)

* **Tarifa dinâmica**: a diária sobe com a demanda (verão na praia, inverno
  na serra, Réveillon, Carnaval, julho), com reserva de última hora (<7 dias)
  e no balcão; cai com antecedência >60 dias e agência. Ocupação e ADR são
  correlacionados — o RevPAR revela isso.
* **Perfis de destino**: hotéis urbanos lotam **terça a quinta** (corporativo);
  praia/serra lotam **sexta e sábado**. Compare os heatmaps!
* **Fidelidade por frequência**: Diamante/Ouro têm desconto (10%/6%) e são
  os hóspedes que mais repetem — analise receita por tier.
* **Comissão de OTA** (crie a tabela de-para): OTA BookNow 18%, OTA ViajaMais
  15%, Agência 10%, demais 0% → medida de **Receita Líquida de Canal**.
* **SLA de manutenção**: Alta 2 h, Média 8 h, Baixa 24 h (~78% cumprido);
  a avaliação do hóspede cai quando o SLA estoura.

## Erros plantados (incidência baixa e irregular)

1. Espaços perdidos, CAIXA alta/baixa e acentos removidos em nomes, cidades,
   tipos de quarto (`STD`/`Standard `/`LUXO`) e categorias de consumo.
2. Datas como texto em formatos mistos (`DD/MM/AAAA`, `AAAA-MM-DD`,
   `DD-MM-AAAA`, `DD.MM.AA`) em várias colunas.
3. Valores como texto com vírgula e alguns `R$ 1.234,56` (diárias, tarifas,
   consumos, nota de avaliação `8,7`).
4. `Categoria_Estrelas` ora número, ora `"4 estrelas"`, ora `"★★★★"`.
5. Canais ambíguos: `BookNow`/`OTA - BookNow`/`booknow`; `Walk-in`/`BALCAO`;
   prioridades `P1`/`ALTA`/`alta`.
6. Telefones com e sem máscara.
7. **Duplicatas** em reservas (integração da OTA lançou duas vezes — dor
   real de hotelaria), consumos e no tabelão.
8. **~1% dos `Quarto_ID` em reservas com espaço à direita** → o
   relacionamento com `quartos` perde linhas até aplicar `Text.Trim` na chave.
9. **~0,4% das reservas com check-in/checkout invertidos** — crie uma coluna
   de validação (`Data_Checkout > Data_Checkin?`) e decida o tratamento.

## Roteiro Power Query (estado ótimo)

1. Importar com `;`, desligar detecção automática de tipos.
2. `Text.Trim`/`Text.Clean` em textos **e nas chaves** (`Quarto_ID`!).
3. `Text.Proper` em nomes; de-para (Replace/coluna condicional) para canal,
   tipo de quarto, prioridade e nível de fidelidade.
4. Datas: tipo "Usando localidade → pt-BR"; tratar `DD.MM.AA` antes com
   Replace/coluna personalizada.
5. Valores: remover `R$ `, vírgula→ponto (ou localidade), tipar decimal;
   `Categoria_Estrelas` → extrair só o dígito (`Text.Select`).
6. Remover duplicatas por chave (`Reserva_ID`; `Consumo_ID`).
7. Coluna `Noites = Duration.Days([Data_Checkout] - [Data_Checkin])` e
   `Valor_Hospedagem = [Noites] * [Diaria_Media_Cobrada]` (deixado de fora
   de propósito!). Corrigir antes as datas invertidas (noites negativas).
8. Coluna `Lead_Time_Dias` (checkin − data da reserva) e faixas
   (`Última hora` <7, `Normal` 7-30, `Antecipada` 30-60, `Early bird` >60).
9. Coluna `Faixa_Etaria` do hóspede; `Fim_de_Semana?` do check-in.
10. Criar tabela **Comissao_Canal** manualmente (Inserir Dados) e mesclar.
11. Em `chamados_manutencao`, criar `Horas_Resolucao` com a diferença entre
    fechamento e abertura; criar `SLA_Horas` por prioridade (Alta=2,
    Média=8, Baixa=24). Essas colunas alimentam o KPI de SLA.
12. `Dim_Calendario` com `CALENDAR(DATE(2024,7,1), DATE(2026,9,30))`,
    marcar como tabela de datas.
13. Na v1: normalizar por referência (hoteis, quartos, hospedes) e discutir
    por que os consumos agregados impedem análise por categoria.

## Medidas DAX (das básicas às semi-aditivas de hotelaria)

```dax
Receita Hospedagem = SUMX(FILTER(reservas,
    reservas[Status_Reserva] IN {"Check-out Realizado", "Hospedado"}),
    reservas[Noites] * reservas[Diaria_Media_Cobrada])

Diárias Vendidas = SUMX(FILTER(reservas,
    reservas[Status_Reserva] IN {"Check-out Realizado", "Hospedado"}),
    reservas[Noites])

ADR = DIVIDE([Receita Hospedagem], [Diárias Vendidas])   -- diária média

Diárias Disponíveis =                                     -- semi-aditiva!
    DISTINCTCOUNT(quartos[Quarto_ID]) * COUNTROWS(Dim_Calendario)

Taxa de Ocupação = DIVIDE([Diárias Vendidas no Período], [Diárias Disponíveis])
-- versão por intervalo (quartos ocupados num dia qualquer do filtro):
Diárias Vendidas no Período =
VAR dMin = MIN(Dim_Calendario[Data])
VAR dMax = MAX(Dim_Calendario[Data]) + 1
RETURN SUMX(FILTER(reservas,
        reservas[Data_Checkin] < dMax && reservas[Data_Checkout] > dMin
        && reservas[Status_Reserva] IN {"Check-out Realizado","Hospedado"}),
    DATEDIFF(MAX(reservas[Data_Checkin], dMin),
             MIN(reservas[Data_Checkout], dMax), DAY))

RevPAR = DIVIDE([Receita Hospedagem], [Diárias Disponíveis])
Receita Extras = SUMX(consumos_extras,
    consumos_extras[Quantidade] * consumos_extras[Valor_Unitario])
Extras por Reserva = DIVIDE([Receita Extras],
    DISTINCTCOUNT(consumos_extras[Reserva_ID]))
Taxa de Cancelamento = DIVIDE(
    CALCULATE(COUNTROWS(reservas), reservas[Status_Reserva] = "Cancelada"),
    COUNTROWS(reservas))
% No-Show = DIVIDE(CALCULATE(COUNTROWS(reservas),
    reservas[Status_Reserva] = "No-Show"), COUNTROWS(reservas))
Receita Líquida = SUMX(reservas, reservas[Valor_Hospedagem]
    * (1 - RELATED(Comissao_Canal[Percentual])))
% SLA Cumprido = DIVIDE(CALCULATE(COUNTROWS(chamados_manutencao),
    chamados_manutencao[Horas_Resolucao] <= chamados_manutencao[SLA_Horas]),
    COUNTROWS(chamados_manutencao))
Lead Time Médio = AVERAGE(reservas[Lead_Time_Dias])
Receita YTD = TOTALYTD([Receita Hospedagem], Dim_Calendario[Data])
Var % YoY = VAR aa = CALCULATE([Receita Hospedagem],
    SAMEPERIODLASTYEAR(Dim_Calendario[Data]))
    RETURN DIVIDE([Receita Hospedagem] - aa, aa)
Ranking Hotéis = RANKX(ALL(hoteis[Hotel_Nome]), [RevPAR],, DESC, DENSE)
```

## Sugestões de visuais

* **Cartões**: Ocupação %, ADR, RevPAR, Taxa de Cancelamento, % SLA.
* **Linha com 2 eixos**: Ocupação % × ADR por mês — a essência do revenue
  management num único gráfico.
* **Heatmap (matriz)**: dia da semana × hotel com ocupação — compare o
  padrão urbano (ter-qui) com o de lazer (sex-sáb).
* **Dispersão**: ADR × Ocupação por hotel, tamanho = RevPAR (quadrantes de
  performance).
* **Colunas empilhadas**: receita por canal × bandeira; funil de status
  (Confirmada → Hospedado → Check-out / Cancelada / No-Show).
* **Barra**: Ranking de hotéis por RevPAR; top categorias de consumo.
* **Decomposition Tree**: Receita → Bandeira → Hotel → Tipo de Quarto.
* **Mapa**: RevPAR por cidade/UF.
* **Segmentações**: período, bandeira, canal, nível de fidelidade, perfil
  de destino.

## Checagens contra a v3

* Nenhum quarto com reservas sobrepostas (após remover duplicatas!).
* `Data_Checkout > Data_Checkin` em 100% das linhas (após corrigir invertidas).
* Após `Text.Trim`, 100% das reservas casam com `quartos`.
* Dezembro/janeiro nos hotéis de praia e junho/julho nos de serra devem
  liderar ocupação e ADR — se não liderarem, algo se perdeu na limpeza.
