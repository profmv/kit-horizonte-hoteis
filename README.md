# Horizonte Hotéis & Resorts — kit educacional de Power BI

Projeto completo para conduzir alunos do dado bruto a um dashboard executivo de hotelaria no Power BI.

Este repositório reúne quatro produtos relacionados:

1. um gerador determinístico de dados sintéticos;
2. bases prontas em diferentes níveis de dificuldade;
3. materiais de condução e validação para o professor;
4. um site público, orientado ao aluno, publicado pelo GitHub Pages.

O README também funciona como memória de projeto. Ele registra decisões, preferências do usuário, erros ocorridos durante a criação e o padrão recomendado para produzir outro kit educacional de tema completamente diferente com a mesma qualidade.

## Links

- Site: <https://profmv.github.io/kit-horizonte-hoteis/>
- Glossário: <https://profmv.github.io/kit-horizonte-hoteis/glossario.html>
- Repositório: <https://github.com/profmv/kit-horizonte-hoteis>
- Publicação: branch `main`, pasta `/docs`

## 1. Resultado educacional esperado

O aluno recebe os dados prontos, trabalha exclusivamente no Power BI e entrega um arquivo `.pbix` funcional.

O dashboard final deve conter:

- quatro páginas: Visão Executiva, Receita e Canais, Ocupação e Demanda, Operação e Experiência;
- modelo de dados validado, com calendário e relacionamentos coerentes;
- medidas DAX organizadas;
- indicadores de hotelaria calculados corretamente;
- pelo menos três insights sustentados pelos dados;
- pelo menos três recomendações executivas;
- um breve registro das decisões, limitações e próximos passos.

O critério de sucesso é simples: uma pessoa da diretoria deve conseguir entender o problema, explorar os resultados e decidir o próximo passo em até cinco minutos.

## 2. Público e limites do projeto

### Aluno

O aluno já estudou Power BI. Ele não precisa aprender Python, linha de comando ou geração de dados para realizar a atividade.

O aluno precisa:

- baixar uma base pronta;
- importar os arquivos no Power BI;
- reconhecer e corrigir problemas de qualidade;
- modelar as tabelas;
- criar medidas;
- construir e defender o dashboard.

### Professor

O professor precisa de recursos adicionais que não devem ser expostos como parte da atividade pública:

- gerador do dataset;
- base limpa de validação;
- gabarito de contagens e KPIs;
- plano de aula;
- critérios de correção.

### Separação obrigatória

| Material | Aluno/site público | Professor/repositório |
|---|---:|---:|
| Base V1 iniciante | Sim | Sim |
| Base V2 desafio | Sim | Sim |
| Guia de apoio | Sim | Sim |
| Tema visual | Sim | Sim |
| Gerador Python | Não | Sim |
| Base V3 limpa | Não | Sim |
| Gabarito de KPIs | Não | Sim |
| Plano de aula | Não | Sim |

Regra central: a pasta `docs/` é a fronteira pública. Nenhum gabarito, base perfeita ou código necessário apenas ao professor deve ser copiado para ela.

## 3. Preferências confirmadas do usuário

Estas preferências devem ser tratadas como requisitos em futuros projetos semelhantes.

### Experiência do aluno

- O site deve explicar a atividade desde o início, sem pressupor que o aluno conhece o caso fictício.
- A missão, os dados, as etapas e a entrega devem ficar claros sem orientação externa.
- O aluno deve baixar dados já gerados. O gerador nunca deve ser a chamada principal do site.
- O aluno não deve precisar instalar nem executar Python.
- O produto final é um dashboard pronto, não um exercício parcial.
- Exemplos e sugestões devem orientar sem entregar toda a solução.
- O texto deve ser curto, escaneável e voltado à ação.
- Conceitos básicos já trabalhados no curso não devem receber explicações desnecessárias.

### Linguagem

- Usar português do Brasil.
- Preferir frases curtas e instruções concretas.
- Explicar o significado das siglas na primeira oportunidade.
- No balão de ajuda, escrever a sigla, a forma completa e sua relação com o projeto.
- Usar termos técnicos somente quando ajudam a executar ou interpretar a atividade.
- Não criar links de glossário para termos cotidianos da turma, como Power BI, dashboard, CSV, ZIP, JSON e PBIX.

### Visual

- Evitar vermelho como cor de destaque principal.
- Preferir verde-claro e amarelo/dourado, apoiados por verde-escuro para contraste.
- Preservar legibilidade: texto escuro sobre verde-claro e texto claro sobre superfícies escuras.
- Usar uma imagem principal coerente com o domínio do caso fictício.
- O segundo site pode ter tema visual completamente diferente; deve reutilizar o padrão de qualidade, não copiar a identidade de hotelaria.

### Publicação

- O site é estático e deve funcionar no GitHub Pages.
- A publicação vem da pasta `/docs` da branch `main`.
- Downloads estudantis devem estar dentro de `docs/` e usar caminhos relativos.

## 4. Erros cometidos pelo agente de IA e lições aprendidas

Esta seção é uma retrospectiva objetiva. Ela deve ser consultada antes de criar um novo kit.

### Erro 1 — oferecer o gerador ao aluno

Na primeira abordagem, o gerador foi tratado como parte do produto público. Isso transferia ao aluno uma responsabilidade técnica que não fazia parte do objetivo da disciplina.

Correção aplicada:

- o gerador permaneceu na raiz do repositório, para uso do professor;
- o site passou a oferecer bases ZIP já geradas;
- a pasta pública passou a conter apenas os materiais necessários ao aluno.

Lição reutilizável: diferenciar a ferramenta que produz o material daquilo que o aluno deve consumir.

### Erro 2 — excesso de texto

A versão inicial explicava demais e exigia muita leitura antes de o aluno entender o que fazer.

Correção aplicada:

- parágrafos foram condensados;
- instruções viraram cartões, etapas e perguntas;
- a sequência principal foi reduzida a reconhecer, limpar, modelar, calcular e apresentar;
- detalhes passaram para o glossário ou para materiais de apoio.

Lição reutilizável: o site é uma interface de condução da atividade, não uma apostila completa.

### Erro 3 — diagrama de modelo pouco informativo

O primeiro modelo sugerido parecia quebrado e não comunicava relações úteis. Um diagrama decorativo não ajuda o aluno a modelar.

Correção aplicada:

- cada nó passou a indicar o papel da tabela;
- fatos e dimensões passaram a ser visualmente distintos;
- PKs, FKs e cardinalidades foram explicitadas;
- o grão das tabelas fato passou a aparecer;
- o diagrama passou a alertar sobre duplicação de receita ao juntar reservas e consumos.

Lição reutilizável: todo diagrama precisa responder “o que esta tabela representa?”, “como ela se relaciona?” e “qual erro evita?”.

### Erro 4 — siglas e termos sem apoio contextual

PMS, OTA, ADR, RevPAR, SLA e outros termos apareciam sem suporte suficiente para quem conhece Power BI, mas não necessariamente hotelaria.

Correção aplicada:

- termos relevantes ganharam sublinhado discreto;
- passar o mouse ou focar pelo teclado abre um resumo;
- clicar leva à definição detalhada no glossário;
- siglas passaram a ser escritas por extenso no balão.

Exemplo correto:

> SLA (Service Level Agreement): acordo de nível de serviço; no projeto, é o prazo definido para resolver um chamado conforme sua prioridade.

Lição reutilizável: definição, expansão da sigla e aplicação no caso devem aparecer juntas.

### Erro 5 — glossário abrangente demais

Termos básicos do curso, como Power BI, dashboard e formatos de arquivo, também receberam links. Isso poluiu a leitura e diminuiu a importância dos conceitos realmente novos.

Correção aplicada:

- foram removidos Power BI, dashboard, CSV, ZIP, JSON e PBIX;
- permaneceram conceitos de domínio, modelagem e análise que afetam a solução;
- o glossário atual possui 39 termos, todos com destino detalhado correspondente.

Lição reutilizável: o glossário deve cobrir lacunas da atividade, não repetir o curso inteiro.

### Erro 6 — cor de destaque rejeitada

O vermelho/coral usado inicialmente não correspondia à preferência do usuário.

Correção aplicada:

- o destaque principal mudou para verde-claro;
- amarelo/dourado permaneceu como apoio;
- componentes sobre verde-claro passaram a usar texto escuro;
- o tema JSON do Power BI foi atualizado junto com o site.

Lição reutilizável: cor não é detalhe isolado. Ao trocar a paleta, atualizar site, estados, diagramas, código destacado e tema baixável, sempre verificando contraste.

## 5. Arquitetura do repositório

```text
Gerador_Hotelaria/
├── README.md
├── gerador_hotelaria_horizonte.py
├── nomes_data.py
├── requirements.txt
├── PLANO_DE_AULA.md
├── GABARITO_VALIDACAO.md
├── dataset_horizonte_hoteis/
│   ├── v1_desnormalizada_com_erros/
│   ├── v2_normalizada_com_erros/
│   ├── v3_normalizada_perfeita/
│   └── DICAS_POWERBI.md
├── downloads/
│   ├── base-v1-iniciante.zip
│   ├── base-v2-desafio.zip
│   ├── gabarito-v3-professor.zip
│   └── DICAS_POWERBI.md
├── assets/
│   ├── horizonte-hero.png
│   └── tema-horizonte.json
└── docs/
    ├── .nojekyll
    ├── index.html
    ├── glossario.html
    ├── styles.css
    ├── script.js
    ├── assets/
    │   ├── horizonte-hero.png
    │   └── tema-horizonte.json
    └── downloads/
        ├── base-v1-iniciante.zip
        ├── base-v2-desafio.zip
        └── DICAS_POWERBI.md
```

### Responsabilidade dos arquivos principais

| Arquivo | Responsabilidade |
|---|---|
| `gerador_hotelaria_horizonte.py` | Fonte da verdade do dataset sintético |
| `nomes_data.py` | Listas auxiliares de nomes usadas pelo gerador |
| `GABARITO_VALIDACAO.md` | Contagens, KPIs e regras esperadas |
| `PLANO_DE_AULA.md` | Roteiro de condução do professor |
| `docs/index.html` | Jornada principal do aluno |
| `docs/glossario.html` | Explicações detalhadas dos conceitos selecionados |
| `docs/styles.css` | Identidade visual, responsividade e estados |
| `docs/script.js` | Tema, menu, progresso, cópia de DAX, glossário e busca |

Os arquivos de `assets/` e `downloads/` fora de `docs/` são cópias de trabalho ou distribuição. As cópias dentro de `docs/` são as que chegam ao GitHub Pages. Sempre verificar sincronização quando um material público mudar.

## 6. Contrato do dataset

### Reprodutibilidade

- `SEED=42` para Python e NumPy;
- data de referência: `30/06/2026`;
- início histórico: 24 meses antes da data de referência;
- reservas futuras: até 90 dias após a data de referência;
- CSV separado por `;`;
- codificação UTF-8 com BOM, adequada ao ambiente brasileiro.

### Três níveis

| Versão | Formato | Uso |
|---|---|---|
| V1 | uma tabela desnormalizada com erros | turma iniciante; limpeza e discussão de perda de grão |
| V2 | sete tabelas normalizadas com erros | desafio recomendado; limpeza, chaves, grãos e relacionamentos |
| V3 | sete tabelas limpas | gabarito exclusivo do professor |

### Contagens de referência

| Item | Valor esperado |
|---|---:|
| Hotéis | 10 |
| Quartos | 426 |
| Hóspedes | 4.000 |
| Funcionários | 180 |
| Reservas limpas | 49.472 |
| Consumos limpos | 148.879 |
| Chamados | 5.000 |
| V1 bruta | 49.532 |
| Reservas V2 brutas | 49.512 |
| Consumos V2 brutos | 148.934 |

### KPIs de referência

| KPI | Valor esperado |
|---|---:|
| Receita de hospedagem | R$ 96.180.944,00 |
| Diárias vendidas | 129.549 |
| ADR | R$ 742,43 |
| Receita de extras | R$ 28.356.350,21 |
| Taxa de cancelamento | 7,36% |
| No-show | 1,77% |
| Ocupação histórica | 41,56% |
| RevPAR de referência | R$ 308,86 |
| SLA cumprido | 78,76% |
| Avaliação média dos chamados | 3,96 |

O arquivo `GABARITO_VALIDACAO.md` contém as regras completas de comparação. Se qualquer regra do gerador mudar, atualizar o gabarito, os exemplos do site, as bases ZIP e os materiais do professor na mesma alteração.

## 7. Arquitetura pedagógica do site

O site usa uma superfície narrativa porque sua função é ensinar e conduzir uma atividade. A ordem das seções acompanha o trabalho do aluno.

### Primeiro viewport

O primeiro viewport precisa responder imediatamente:

- qual é o domínio do caso;
- qual problema será resolvido;
- qual ferramenta será usada;
- qual é o produto final;
- onde começar ou baixar a base.

No projeto atual, o hero apresenta o caso da rede Horizonte, a promessa de transformar operação em decisões, uma chamada para iniciar e outra para baixar a V2.

### Sequência da página principal

| Ordem | Seção | Pergunta respondida |
|---:|---|---|
| 1 | Missão | Qual problema de negócio devo resolver? |
| 2 | Dados | O que recebo e qual nível devo usar? |
| 3 | Modelo rápido | Como as tabelas se relacionam e qual erro devo evitar? |
| 4 | Jornada | Em que ordem devo trabalhar? |
| 5 | Limpeza | Como registrar uma transformação? |
| 6 | Medidas | Quais cálculos mínimos orientam a solução? |
| 7 | Dashboard | Que páginas e perguntas devem compor a entrega? |
| 8 | Investigação | Que análises devo fazer além do primeiro número? |
| 9 | Entrega | O que será avaliado e como saber se terminei? |

### Jornada de cinco etapas

1. Reconhecer o grão e os problemas da base.
2. Limpar e documentar regras no Power Query.
3. Modelar com relações coerentes.
4. Calcular KPIs com medidas DAX.
5. Apresentar quatro páginas e recomendações executivas.

Esta sequência é reutilizável. Em outro domínio, mudar tabelas, métricas e perguntas, mas preservar a progressão cognitiva.

## 8. Padrão de redação

### Princípios

- Uma seção deve ter uma mensagem central.
- Um cartão deve comunicar uma única ideia.
- Títulos devem expressar decisão ou ação, não apenas nomear assuntos.
- Parágrafos devem ser curtos e dispensáveis quando um exemplo visual comunica melhor.
- Instruções operacionais devem usar verbos no infinitivo ou imperativo.
- Toda métrica apresentada deve estar ligada a uma pergunta de negócio.
- Toda recomendação deve indicar ação e impacto esperado.

### Fórmula recomendada para cada seção

```text
Rótulo curto
Título que comunica a ideia principal
Uma ou duas frases de contexto
Exemplo, ação ou artefato esperado
```

### O que deve ir para outro lugar

- explicação longa de conceito: glossário;
- instrução detalhada de Power Query ou DAX: guia de apoio;
- valores corretos e solução completa: gabarito do professor;
- instalação e regeneração de dados: README;
- condução em sala e intervenções: plano de aula.

### Teste de densidade

Antes de publicar, verificar:

- o aluno consegue identificar o próximo passo olhando títulos e cartões?
- há algum parágrafo que repete o título?
- há definições básicas que a turma já conhece?
- um detalhe poderia ser movido para o glossário?
- a página inicial funciona como roteiro mesmo sem o professor falar?

## 9. Padrão de glossário e balões

### Critério para incluir um termo

Incluir quando pelo menos uma destas condições for verdadeira:

- pertence ao domínio de negócio e pode ser novo para a turma;
- muda a forma correta de modelar ou calcular;
- representa uma armadilha relevante do dataset;
- é uma sigla necessária para interpretar o caso;
- aparece repetidamente em mais de uma seção.

Não incluir apenas porque o termo existe no texto.

### Estrutura da entrada curta

Cada termo interativo em `docs/script.js` possui:

```javascript
{
  aliases: ['SLA'],
  slug: 'sla',
  tip: 'SLA (Service Level Agreement): acordo de nível de serviço; no projeto, é o prazo definido para resolver um chamado conforme sua prioridade.'
}
```

Regras:

- `aliases`: grafias que devem ser encontradas automaticamente;
- `slug`: deve ser idêntico ao `id` do cartão em `glossario.html`;
- `tip`: resumo curto, forma completa da sigla e relação com o projeto.

### Estrutura da entrada detalhada

Cada cartão do glossário deve conter:

- termo e categoria;
- definição em linguagem simples;
- aplicação específica no projeto;
- exemplo, validação, risco ou boa prática.

### Comportamento

- passar o mouse mostra o balão;
- foco pelo teclado também mostra o balão;
- clicar abre `glossario.html#slug`;
- a busca filtra cartões e categorias;
- o destino indicado no hash é aberto automaticamente;
- termos dentro de links, botões, código e campos não são transformados.

### Auditoria obrigatória

O número de `slug` em `script.js` deve corresponder ao número de cartões com `id` em `glossario.html`, e nenhum `slug` pode ficar sem definição.

## 10. Padrão para diagramas de dados

O diagrama deve ser funcional, não ornamental.

Cada tabela exibida deve informar:

- nome;
- papel: fato ou dimensão;
- grão, quando for fato;
- chave primária ou chave de ligação relevante;
- cardinalidade;
- direção conceitual do relacionamento.

O diagrama também deve comunicar pelo menos um risco real. Neste projeto, o risco é juntar reservas e consumos em uma única tabela e duplicar a receita de hospedagem.

Checklist do diagrama:

- [ ] as linhas realmente conectam as tabelas relacionadas;
- [ ] os lados `1` e `N` estão legíveis;
- [ ] nenhuma relação contradiz o dataset;
- [ ] fatos e dimensões têm distinção visual;
- [ ] o grão é explícito;
- [ ] PK e FK estão explicadas no glossário;
- [ ] o diagrama continua compreensível em telas menores;
- [ ] existe uma frase que explica por que o modelo importa.

Se o diagrama não puder responder a essas questões, é melhor usar uma tabela de relacionamentos do que uma ilustração genérica.

## 11. Sistema visual atual

### Paleta

| Token | Cor | Uso |
|---|---|---|
| `--navy` | `#082F38` | fundos escuros e contraste principal |
| `--navy-2` | `#0D4650` | superfícies escuras secundárias |
| `--teal` | `#19756F` | textos de destaque e estados interativos |
| `--mint` | `#8FD6B7` | destaque verde-claro e chamadas principais |
| `--sand` | `#D9B978` | apoio amarelo/dourado |
| `--paper` | `#F5F1E8` | fundo claro |
| `--ink` | `#132C32` | texto principal |

Regras de contraste:

- usar `--navy` ou `--ink` sobre `--mint`;
- usar branco ou tons claros sobre `--navy`;
- usar `--teal` para texto sobre fundos claros;
- não usar verde-claro como texto pequeno sobre branco;
- não reintroduzir vermelho como cor dominante sem nova orientação do usuário.

### Tipografia

- títulos: Manrope, peso forte;
- texto e controles: DM Sans;
- hierarquia marcada por tamanho, peso e espaço, não por excesso de cores.

### Forma e espaçamento

- largura máxima de conteúdo: `1180px`;
- cantos principais: `22px`;
- superfícies com borda discreta e sombra leve;
- botões principais arredondados;
- seções com bastante separação vertical;
- movimento curto e funcional.

### Outro tema

Para criar um site de assunto diferente, não copiar automaticamente hotel, piscina, letra H, verde ou dourado.

Preservar:

- hierarquia visual;
- contraste;
- consistência dos tokens;
- densidade controlada;
- clareza das chamadas;
- coerência entre site e tema do Power BI.

Substituir:

- nome e marca fictícios;
- imagem principal;
- paleta;
- tipografia, quando fizer sentido;
- ícones e vocabulário;
- perguntas de negócio;
- tabelas, medidas e exemplos.

Qualidade equivalente significa mesma clareza e acabamento, não aparência idêntica.

## 12. Interações, acessibilidade e responsividade

### Interações existentes

- menu adaptado para telas menores;
- alternância entre tema claro e escuro;
- tema escolhido salvo em `localStorage`;
- barra de progresso da leitura;
- botões para copiar exemplos DAX;
- checklist da entrega com progresso persistente;
- balões contextuais e links para o glossário;
- pesquisa no glossário;
- abertura automática do termo indicado na URL.

### Acessibilidade

- documento em `pt-BR`;
- link “Pular para o conteúdo”;
- landmarks semânticos;
- rótulos acessíveis em menu e botões;
- foco visível nos termos;
- balão disponível por mouse e teclado;
- `aria-live` para a confirmação de cópia;
- imagem principal com texto alternativo;
- redução de movimento respeitando `prefers-reduced-motion`.

### Breakpoints

- até `980px`: navegação móvel e reorganização das grades;
- até `720px`: layout compacto, cartões em uma coluna e glossário simplificado;
- evitar larguras fixas que provoquem rolagem horizontal.

Em um novo site, testar no mínimo uma largura ampla, uma intermediária e uma de celular.

## 13. Metadados e identidade pública

Cada site deve possuir:

- `lang="pt-BR"`;
- `charset` UTF-8;
- viewport responsivo;
- título próprio;
- descrição específica;
- `theme-color` coerente com a marca;
- URL canônica;
- Open Graph com título, descrição, URL e imagem;
- imagem social em formato paisagem e com texto legível, quando houver texto;
- aviso de que empresa e dados são fictícios.

Ao duplicar este projeto, substituir todas as ocorrências da marca e das URLs. Não publicar um novo site com metadados da Horizonte.

## 14. Gerar e atualizar os dados

### Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

### Executar o gerador

```powershell
python gerador_hotelaria_horizonte.py
```

O gerador recria as três versões dentro de `dataset_horizonte_hoteis/`.

### Depois de regenerar

1. Conferir contagens e KPIs do gabarito.
2. Inspecionar se as sujeiras intencionais continuam presentes na V1 e V2.
3. Confirmar integridade da V3.
4. Recriar os ZIPs de aluno.
5. Manter o ZIP V3 apenas fora de `docs/`.
6. Copiar V1, V2 e o guia atualizado para `docs/downloads/`.
7. Atualizar exemplos, números e textos do site quando necessário.
8. Verificar se o tema JSON em `assets/` e `docs/assets/` é o mesmo.

Para comparar cópias públicas e de trabalho:

```powershell
Get-FileHash assets\tema-horizonte.json
Get-FileHash docs\assets\tema-horizonte.json
Get-FileHash downloads\base-v2-desafio.zip
Get-FileHash docs\downloads\base-v2-desafio.zip
```

## 15. Executar o site localmente

O site é estático e não precisa de build.

```powershell
python -m http.server --directory docs 8000
```

Acesse <http://localhost:8000/>.

Não usar apenas abertura direta por `file://` como teste final, porque downloads, URLs relativas e alguns comportamentos devem ser verificados por HTTP.

## 16. Publicar no GitHub Pages

1. Enviar as alterações para a branch `main`.
2. Abrir **Settings → Pages** no repositório.
3. Selecionar **Deploy from a branch**.
4. Escolher branch `main` e pasta `/docs`.
5. Manter `docs/.nojekyll`.
6. Aguardar o build indicar sucesso.
7. Conferir a página principal, o glossário, o CSS, o JavaScript, o tema e os downloads pela URL pública.

O site publicado deve ser verificado, não apenas o commit local. Cache do navegador pode ser evitado temporariamente com uma query string, por exemplo `?v=<commit>`.

## 17. Validação antes de publicar

### Conteúdo

- [ ] o primeiro viewport explica o caso e a entrega;
- [ ] os dados podem ser baixados sem Python;
- [ ] a versão recomendada está evidente;
- [ ] nenhuma resposta completa ou gabarito está em `docs/`;
- [ ] textos são curtos e orientados à ação;
- [ ] siglas estão expandidas no balão;
- [ ] termos básicos do curso não foram linkados;
- [ ] toda métrica está ligada a uma pergunta de negócio;
- [ ] a entrega final exige um dashboard pronto.

### Dados

- [ ] o gerador é determinístico;
- [ ] formatos, separador e codificação são adequados;
- [ ] V1, V2 e V3 têm papéis distintos;
- [ ] contagens e KPIs conferem com o gabarito;
- [ ] ZIPs públicos correspondem às bases validadas;
- [ ] V3 permanece restrita ao professor.

### Site

- [ ] HTML das duas páginas é válido;
- [ ] JavaScript não possui erro de sintaxe;
- [ ] todos os `slug` possuem cartão correspondente;
- [ ] menu, tema, cópia, checklist, busca e links funcionam;
- [ ] diagrama tem relações e grãos legíveis;
- [ ] não existe rolagem horizontal no celular;
- [ ] contraste é suficiente;
- [ ] foco por teclado é visível;
- [ ] imagens e downloads não retornam 404;
- [ ] metadados usam a marca e a URL corretas;

### Repositório e publicação

```powershell
node --check docs\script.js
git diff --check
git status --short
```

Depois do push:

- conferir se o build do GitHub Pages usa o commit esperado;
- testar respostas HTTP públicas;
- confirmar que a cor, os balões e o glossário publicados são os mais recentes.

## 18. Roteiro para criar um segundo kit de tema diferente

### Etapa 1 — definir o contrato educacional

Preencher antes de gerar qualquer código:

| Decisão | Preenchimento do novo projeto |
|---|---|
| Disciplina/ferramenta | `[ex.: Power BI]` |
| Nível da turma | `[iniciante, intermediário ou avançado]` |
| Empresa fictícia | `[nome e segmento]` |
| Decisão central | `[pergunta de negócio]` |
| Período dos dados | `[intervalo]` |
| Tabelas | `[lista e grão]` |
| Problemas intencionais | `[duplicatas, datas, textos, FKs etc.]` |
| KPIs | `[lista e regra]` |
| Páginas do dashboard | `[nomes e perguntas]` |
| Entrega final | `[arquivos e critérios]` |
| Materiais do professor | `[gabarito, plano, base limpa]` |
| Identidade visual | `[paleta, imagem, tom]` |

### Etapa 2 — projetar o dataset antes do site

1. Definir tabelas e grãos.
2. Definir PKs, FKs e cardinalidades.
3. Definir regras de negócio e KPIs esperados.
4. Criar uma versão limpa validável.
5. Derivar versões com erros pedagógicos intencionais.
6. Garantir reprodutibilidade com semente fixa.
7. Gerar o gabarito do professor.
8. Empacotar bases estudantis prontas.

Nunca criar a narrativa do site antes de saber exatamente o que os dados permitem analisar.

### Etapa 3 — construir a narrativa

Usar esta estrutura como ponto de partida:

```text
Hero: caso + promessa + chamada
Missão: problema decisório
Dados: versões e downloads
Modelo: tabelas, grãos e risco
Jornada: reconhecer → limpar → modelar → calcular → apresentar
Exemplo: antes/depois de transformação
Medidas: exemplos mínimos
Dashboard: páginas e perguntas
Investigação: perguntas abertas
Entrega: checklist + rubrica + critério de sucesso
Glossário: somente lacunas relevantes
```

### Etapa 4 — criar identidade própria

- escolher referências visuais do novo domínio;
- definir tokens antes de estilizar componentes individuais;
- escolher imagem principal pertinente;
- criar contraste para claro e escuro;
- refletir a mesma paleta no tema do Power BI;
- remover toda ocorrência da marca anterior;
- evitar um “clone recolorido” da Horizonte.

### Etapa 5 — aplicar o padrão de ajuda contextual

- listar termos realmente novos;
- eliminar termos básicos da ferramenta;
- escrever forma completa das siglas;
- explicar a relação com o projeto;
- criar um cartão detalhado para cada slug;
- testar mouse, teclado, clique e busca.

### Etapa 6 — validar e publicar

- validar dados antes dos visuais;
- validar conteúdo antes da decoração;
- testar localmente por HTTP;
- conferir desktop, tablet e celular;
- publicar somente materiais estudantis;
- verificar a versão pública depois do build.

## 19. Briefing pronto para um próximo agente de IA

O texto abaixo pode ser copiado e preenchido para iniciar outro projeto.

```text
Crie um kit educacional completo de Power BI sobre [TEMA], para alunos de nível [NÍVEL].

A empresa deve ser fictícia e se chamar [EMPRESA]. O problema central é [PERGUNTA DE NEGÓCIO]. O aluno deve receber dados prontos, trabalhar somente no Power BI e entregar um dashboard final com [PÁGINAS/ENTREGÁVEIS]. Não exponha o gerador, a base limpa nem o gabarito no site público.

Crie:
1. um gerador determinístico com semente fixa;
2. uma base iniciante, uma base desafio e uma base limpa do professor;
3. gabarito com contagens, KPIs e regras;
4. plano de aula;
5. guia de apoio ao aluno;
6. site estático em /docs, pronto para GitHub Pages;
7. arquivos ZIP estudantis prontos para download;
8. tema JSON coerente com a identidade visual.

O site deve explicar, com pouco texto, a missão, os dados, a jornada, o modelo, as medidas sugeridas, as páginas do dashboard, as perguntas para investigar e a entrega final. Use cartões, exemplos e checklists. Não transforme o site em apostila.

Inclua glossário apenas para conceitos de domínio, modelagem e métricas que possam ser novos. Ao passar o mouse ou focar uma sigla, mostre a forma completa, a definição curta e sua relação com o projeto. O clique deve abrir a explicação detalhada. Não crie links para Power BI, dashboard, CSV, ZIP, JSON ou PBIX.

Crie um diagrama útil: nome das tabelas, fatos/dimensões, grão, PK/FK, cardinalidade e um risco de modelagem. Não use um diagrama meramente decorativo.

A identidade deve ser própria do tema [REFERÊNCIAS VISUAIS]. Use [PALETA], verifique contraste e mantenha coerência entre site e tema do Power BI. Evite vermelho como destaque principal, salvo nova orientação.

Valide sintaxe, HTML, correspondência entre termos e glossário, downloads, responsividade, acessibilidade, dados, gabarito e publicação pública. A entrega só termina quando o site publicado e os downloads responderem corretamente.
```

## 20. Critérios de qualidade para equivalência entre projetos

Um novo kit tem qualidade equivalente quando atende a todos estes critérios:

| Dimensão | Critério |
|---|---|
| Clareza | missão, dados e entrega compreensíveis no primeiro contato |
| Autonomia | aluno consegue começar sem Python ou suporte técnico |
| Pedagogia | dificuldade intencional, exemplos e rubrica coerentes |
| Dados | reprodutibilidade, grãos e gabarito validados |
| Modelagem | diagrama correto e útil |
| Conteúdo | texto curto, específico e orientado à decisão |
| Glossário | ajuda contextual seletiva e acessível |
| Visual | identidade própria, contraste e consistência |
| Responsividade | navegação e leitura funcionam em telas menores |
| Acessibilidade | semântica, teclado, foco e movimento reduzido |
| Segurança pedagógica | gabarito e base perfeita fora do site público |
| Publicação | Pages e downloads verificados na URL final |

## 21. Definição de pronto

O projeto está pronto somente quando:

1. o gerador reproduz as bases;
2. o gabarito confere com a base limpa;
3. as versões estudantis possuem os erros pedagógicos esperados;
4. os ZIPs públicos estão atualizados;
5. a página inicial explica toda a jornada sem excesso de leitura;
6. o modelo sugerido comunica tabelas, grãos e relações;
7. os balões expandem siglas e contextualizam os conceitos;
8. o glossário contém apenas termos relevantes e não possui links quebrados;
9. o dashboard final e seus critérios estão explícitos;
10. a identidade visual foi aplicada também ao tema do Power BI;
11. o site funciona em desktop e celular, com teclado;
12. nenhum material exclusivo do professor está em `docs/`;
13. o GitHub Pages publicou o commit correto;
14. página, glossário, recursos e downloads foram verificados na URL pública.

---

Empresa, pessoas e dados deste projeto são fictícios. O material foi criado exclusivamente para fins educacionais.
