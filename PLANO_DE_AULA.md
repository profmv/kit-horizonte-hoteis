# Plano de aula — Horizonte Hotéis & Resorts

## Objetivo

Ao final, o aluno entrega um dashboard Power BI com quatro páginas, modelo de dados consistente, medidas de hotelaria e recomendações executivas sustentadas por dados.

## Formato sugerido

Carga total: **8 a 10 horas**, em cinco encontros de 2 horas ou dois encontros de 4–5 horas.

| Encontro | Tema | Entrega intermediária |
|---|---|---|
| 1 | Caso de negócio e diagnóstico | inventário das tabelas, grãos e cinco problemas de qualidade |
| 2 | Power Query | consultas limpas, tipadas e documentadas |
| 3 | Modelagem | calendário, comissão por canal e relacionamentos validados |
| 4 | DAX | tabela `_Medidas` com KPIs de receita, demanda e operação |
| 5 | Storytelling | dashboard de quatro páginas e apresentação de cinco minutos |

## Antes da aula

1. Execute `python gerador_hotelaria_horizonte.py`.
2. Confirme a criação das três pastas dentro de `dataset_horizonte_hoteis`.
3. Para iniciantes, distribua a V1; para uma turma intermediária, distribua a V2.
4. Guarde a V3 como gabarito. Não a entregue antes da validação final.
5. Abra o site e apresente somente as seções **O caso**, **O que você recebe** e **Sua jornada**.

## Condução por etapa

### 1. Reconhecer

Pergunte antes de explicar:

- Qual é o grão de `reservas`?
- Uma reserva pode ter vários consumos?
- O que acontece com a receita se as tabelas forem unidas sem cuidado?
- Quais campos parecem dimensão e quais parecem medida?

Não revele todos os erros plantados. Peça que os alunos criem um diagnóstico com exemplos, quantidade de linhas afetadas e proposta de tratamento.

### 2. Limpar

Demonstre um exemplo de cada classe de problema e deixe o restante para a dupla:

- `Text.Trim`/`Text.Clean` nas chaves e textos;
- datas com localidade `pt-BR`;
- remoção de `R$` e conversão decimal;
- de-para para canais, tipos de quarto e prioridades;
- remoção de duplicatas pela chave de negócio;
- regra explícita para check-in posterior ao checkout.
- `Horas_Resolucao` pela diferença entre fechamento e abertura;
- `SLA_Horas` por prioridade: Alta = 2, Média = 8, Baixa = 24.

Peça que renomeiem etapas do Power Query. Etapas como `Tipo Alterado 7` não explicam a lógica.

### 3. Modelar

O aluno deve justificar:

- por que `reservas` e `consumos_extras` permanecem fatos separadas;
- por que a direção de filtro deve ser simples sempre que possível;
- como a dimensão calendário filtra análises por período;
- por que uma tabela manual de comissão por canal pertence ao modelo.

Validação rápida: ao selecionar um hotel, reservas, consumos e chamados relacionados devem responder sem caminhos ambíguos.

### 4. Calcular

Ordem sugerida:

1. quantidade de reservas;
2. diárias vendidas e disponíveis;
3. receita de hospedagem e extras;
4. ADR, ocupação e RevPAR;
5. cancelamento e no-show;
6. receita líquida após comissão;
7. SLA cumprido e avaliação média;
8. inteligência temporal e ranking.

Faça o aluno validar cada medida em uma matriz antes de criar cartões. Um número bonito ainda pode estar errado.

### 5. Comunicar

Use a regra **contexto → evidência → ação**:

> A ocupação do hotel X caiu 9 p.p. no trimestre (contexto). A queda está concentrada em dias úteis e no canal direto (evidência). Recomenda-se testar tarifa corporativa e campanha de recompra (ação).

Cada grupo apresenta em cinco minutos. A banca faz duas perguntas: “como você validou?” e “qual decisão tomaria amanhã?”.

## Rubrica — 100 pontos

| Critério | Pontos | Evidência |
|---|---:|---|
| ETL e qualidade | 25 | tipos, padronização, duplicatas, regras documentadas |
| Modelagem | 20 | grãos, cardinalidade, calendário, ausência de ambiguidade |
| DAX e validação | 25 | KPIs corretos, medidas legíveis, conferência contra gabarito |
| Design e usabilidade | 15 | hierarquia, contraste, filtros claros, navegação |
| Insights e defesa | 15 | três achados e três recomendações acionáveis |

## Erros comuns para observar

- Somar diárias ou receitas duplicadas depois de unir reservas e consumos.
- Calcular ocupação como `reservas / quartos` sem considerar noites e período.
- Criar relações muitos-para-muitos para “fazer funcionar”.
- Usar coluna calculada quando a pergunta depende do filtro do relatório.
- Misturar receita bruta e líquida sem informar a comissão.
- Criar um gráfico por campo, sem pergunta de negócio.
- Entregar prints sem o `.pbix` navegável.
