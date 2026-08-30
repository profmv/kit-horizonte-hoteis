const root = document.body;
const menuButton = document.querySelector('#menuButton');
const nav = document.querySelector('#mainNav');
const themeButton = document.querySelector('#themeButton');
const readingBar = document.querySelector('#readingBar');
const toast = document.querySelector('#toast');

const savedTheme = localStorage.getItem('horizonte-theme');
if (savedTheme === 'dark') root.classList.add('dark');

themeButton?.addEventListener('click', () => {
  root.classList.toggle('dark');
  localStorage.setItem('horizonte-theme', root.classList.contains('dark') ? 'dark' : 'light');
});

menuButton?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

nav?.addEventListener('click', event => {
  if (event.target.matches('a')) {
    nav.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  }
});

window.addEventListener('scroll', () => {
  const max = document.documentElement.scrollHeight - innerHeight;
  readingBar.style.width = `${max > 0 ? (scrollY / max) * 100 : 0}%`;
}, { passive: true });

let toastTimer;
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      toast.textContent = 'Copiado para a área de transferência.';
    } catch {
      toast.textContent = 'Selecione o código e copie manualmente.';
    }
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
  });
});

const glossaryEntries = [
  { aliases: ['PMS'], slug: 'pms', tip: 'PMS (Property Management System): sistema de gestão hoteleira que registra reservas, hóspedes, quartos e estadias.' },
  { aliases: ['OTA', 'OTAs'], slug: 'ota', tip: 'OTA (Online Travel Agency): agência de viagem on-line; no projeto, é um canal de venda que cobra comissão.' },
  { aliases: ['Analytics'], slug: 'analytics', tip: 'Uso dos dados para encontrar padrões, explicar resultados e recomendar ações.' },
  { aliases: ['ADR'], slug: 'adr', tip: 'ADR (Average Daily Rate): diária média vendida, calculada pela receita de hospedagem dividida pelas diárias vendidas.' },
  { aliases: ['RevPAR'], slug: 'revpar', tip: 'RevPAR (Revenue per Available Room): receita por quarto disponível; combina preço e ocupação em um indicador.' },
  { aliases: ['diária vendida', 'diárias vendidas'], slug: 'diarias-vendidas', tip: 'Quantidade de noites efetivamente ocupadas por reservas válidas.' },
  { aliases: ['diária disponível', 'diárias disponíveis'], slug: 'diarias-disponiveis', tip: 'Capacidade de hospedagem oferecida: quartos disponíveis multiplicados pelos dias do período.' },
  { aliases: ['comissão', 'comissões'], slug: 'comissao', tip: 'Percentual pago ao canal de venda; reduz a receita líquida das OTAs e agências.' },
  { aliases: ['SLA'], slug: 'sla', tip: 'SLA (Service Level Agreement): acordo de nível de serviço; no projeto, é o prazo definido para resolver um chamado conforme sua prioridade.' },
  { aliases: ['no-show'], slug: 'no-show', tip: 'Reserva em que o hóspede não comparece e não realiza o check-in.' },
  { aliases: ['check-in'], slug: 'check-in', tip: 'Momento de entrada do hóspede; marca o início efetivo da estadia.' },
  { aliases: ['check-out'], slug: 'check-out', tip: 'Momento de saída do hóspede; encerra a estadia e define o total de noites.' },
  { aliases: ['lead time'], slug: 'lead-time', tip: 'Dias entre a criação da reserva e o check-in; ajuda a entender antecedência da demanda.' },
  { aliases: ['Power Query'], slug: 'power-query', tip: 'Área do Power BI usada para importar, limpar e transformar os CSVs.' },
  { aliases: ['modelo normalizado'], slug: 'modelo-normalizado', tip: 'Dados separados por assunto para reduzir repetição e manter chaves consistentes.' },
  { aliases: ['PK'], slug: 'pk', tip: 'PK (Primary Key / chave primária): coluna que identifica cada linha de uma tabela sem repetição.' },
  { aliases: ['FK', 'FKs'], slug: 'fk', tip: 'FK (Foreign Key / chave estrangeira): coluna que aponta para a chave primária de outra tabela.' },
  { aliases: ['1:N', 'relações 1:N', 'relacionamentos 1:N'], slug: 'relacao-1-n', tip: 'Relação um-para-muitos: uma linha no lado 1 pode se relacionar a várias no lado N.' },
  { aliases: ['dimensão', 'dimensões'], slug: 'dimensao', tip: 'Tabela descritiva usada para filtrar e agrupar, como Hotéis, Quartos e Hóspedes.' },
  { aliases: ['fato', 'fatos'], slug: 'fato', tip: 'Tabela de eventos mensuráveis, como Reservas, Consumos e Chamados.' },
  { aliases: ['grão'], slug: 'grao', tip: 'O que exatamente uma linha representa; por exemplo, uma reserva ou um consumo.' },
  { aliases: ['DAX'], slug: 'dax', tip: 'DAX (Data Analysis Expressions): linguagem de fórmulas usada para criar medidas e indicadores.' },
  { aliases: ['medida', 'medidas'], slug: 'medida', tip: 'Cálculo dinâmico em DAX que responde aos filtros aplicados ao relatório.' },
  { aliases: ['KPI', 'KPIs'], slug: 'kpi', tip: 'KPI (Key Performance Indicator): indicador-chave usado para acompanhar desempenho e apoiar decisões.' },
  { aliases: ['Revenue management'], slug: 'revenue-management', tip: 'Gestão conjunta de preço e disponibilidade para maximizar receita hoteleira.' },
  { aliases: ['semi-aditiva'], slug: 'semi-aditiva', tip: 'Métrica que não pode ser simplesmente somada em qualquer dimensão, especialmente no tempo.' },
  { aliases: ['ETL'], slug: 'etl', tip: 'ETL (Extract, Transform, Load): extrair, transformar e carregar dados; neste projeto, o processo acontece no Power Query.' },
  { aliases: ['esquema estrela'], slug: 'esquema-estrela', tip: 'Modelo analítico com tabelas fato no centro e dimensões ao redor.' },
  { aliases: ['cardinalidade'], slug: 'cardinalidade', tip: 'Regra que informa quantas linhas de uma tabela podem se relacionar com outra.' },
  { aliases: ['contexto de filtro', 'filtro', 'filtros'], slug: 'contexto-filtro', tip: 'Conjunto de seleções que determina quais linhas participam do cálculo de uma medida.' },
  { aliases: ['ocupação'], slug: 'ocupacao', tip: 'Percentual das diárias disponíveis que foram efetivamente vendidas.' },
  { aliases: ['taxa de cancelamento'], slug: 'taxa-cancelamento', tip: 'Percentual de reservas canceladas sobre o total de reservas analisadas.' },
  { aliases: ['receita bruta'], slug: 'receita-bruta', tip: 'Valor da venda antes de descontar comissões e outros custos do canal.' },
  { aliases: ['receita líquida'], slug: 'receita-liquida', tip: 'Valor que permanece após descontar a comissão do canal de venda.' },
  { aliases: ['sazonalidade'], slug: 'sazonalidade', tip: 'Padrão de alta e baixa demanda que se repete conforme mês, estação ou calendário.' },
  { aliases: ['segmentação', 'segmentações'], slug: 'segmentacao', tip: 'Controle visual usado para filtrar o relatório por período, hotel, canal ou outro atributo.' },
  { aliases: ['benchmark'], slug: 'benchmark', tip: 'Referência usada para comparar desempenho, como outro hotel, uma meta ou período anterior.' },
  { aliases: ['insight', 'insights'], slug: 'insight', tip: 'Descoberta relevante que explica um resultado e ajuda a decidir uma ação.' },
  { aliases: ['ambiguidade'], slug: 'ambiguidade', tip: 'Situação em que existem caminhos de filtro concorrentes entre tabelas, gerando resultados imprevisíveis.' }
];

function addGlossaryLinks() {
  if (root.classList.contains('glossary-page')) return;
  const main = document.querySelector('main');
  if (!main) return;
  const aliasMap = new Map();
  glossaryEntries.forEach(entry => entry.aliases.forEach(alias => aliasMap.set(alias.toLocaleLowerCase('pt-BR'), entry)));
  const aliases = [...aliasMap.keys()].sort((a, b) => b.length - a.length);
  const escaped = aliases.map(alias => alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const matcher = new RegExp(`(?<![\\p{L}\\p{N}_])(${escaped.join('|')})(?![\\p{L}\\p{N}_])`, 'giu');
  const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent || parent.closest('a, code, pre, script, style, button, input, summary, [data-no-glossary]')) return NodeFilter.FILTER_REJECT;
      matcher.lastIndex = 0;
      const hasTerm = matcher.test(node.nodeValue);
      matcher.lastIndex = 0;
      return hasTerm ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(node => {
    matcher.lastIndex = 0;
    const fragment = document.createDocumentFragment();
    node.nodeValue.split(matcher).forEach(part => {
      const entry = aliasMap.get(part.toLocaleLowerCase('pt-BR'));
      if (!entry) return fragment.append(part);
      const link = document.createElement('a');
      link.className = 'term-link';
      link.href = `glossario.html#${entry.slug}`;
      link.dataset.tip = entry.tip;
      link.textContent = part;
      fragment.append(link);
    });
    node.replaceWith(fragment);
  });
}

function enableTermTooltips() {
  const tooltip = document.createElement('div');
  tooltip.className = 'term-tooltip';
  tooltip.id = 'termTooltip';
  tooltip.setAttribute('role', 'tooltip');
  document.body.append(tooltip);
  let activeLink;
  const show = link => {
    activeLink = link;
    tooltip.textContent = link.dataset.tip;
    tooltip.classList.add('visible');
    link.setAttribute('aria-describedby', tooltip.id);
    const rect = link.getBoundingClientRect();
    const maxLeft = Math.max(12, innerWidth - 312);
    const left = Math.min(Math.max(12, rect.left + rect.width / 2 - 150), maxLeft);
    const above = rect.top > 150;
    tooltip.style.left = `${left}px`;
    tooltip.style.top = above ? `${rect.top - tooltip.offsetHeight - 12}px` : `${rect.bottom + 12}px`;
  };
  const hide = link => {
    if (activeLink !== link) return;
    tooltip.classList.remove('visible');
    link.removeAttribute('aria-describedby');
    activeLink = undefined;
  };
  document.addEventListener('pointerover', event => { const link = event.target.closest('.term-link'); if (link) show(link); });
  document.addEventListener('pointerout', event => { const link = event.target.closest('.term-link'); if (link) hide(link); });
  document.addEventListener('focusin', event => { const link = event.target.closest('.term-link'); if (link) show(link); });
  document.addEventListener('focusout', event => { const link = event.target.closest('.term-link'); if (link) hide(link); });
}

addGlossaryLinks();
enableTermTooltips();

if (root.classList.contains('glossary-page')) {
  const openTarget = () => {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target?.tagName === 'DETAILS') target.open = true;
  };
  openTarget();
  window.addEventListener('hashchange', openTarget);
  const search = document.querySelector('#glossarySearch');
  const cards = [...document.querySelectorAll('.glossary-card')];
  const empty = document.querySelector('#glossaryEmpty');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR');
  search?.addEventListener('input', () => {
    const query = normalize(search.value.trim());
    let visible = 0;
    cards.forEach(card => {
      const match = !query || normalize(card.textContent).includes(query);
      card.hidden = !match;
      if (match) visible += 1;
    });
    document.querySelectorAll('.glossary-group').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.glossary-card')].some(card => !card.hidden);
    });
    if (empty) empty.hidden = visible > 0;
  });
}

const tasks = [...document.querySelectorAll('#checklist input')];
const progressValue = document.querySelector('#progressValue');
const taskProgress = document.querySelector('#taskProgress');
const progressMessage = document.querySelector('#progressMessage');

function updateProgress() {
  if (!tasks.length || !progressValue || !taskProgress || !progressMessage) return;
  const done = tasks.filter(task => task.checked).length;
  const value = Math.round(done / tasks.length * 100);
  progressValue.textContent = `${value}%`;
  taskProgress.style.width = `${value}%`;
  progressMessage.textContent = value === 100
    ? 'Entrega completa. Agora ensaie sua defesa.'
    : value >= 50 ? 'Você passou da metade. Valide os números.'
    : value > 0 ? 'Bom começo. Continue na ordem da jornada.'
    : 'Comece pelo diagnóstico da base.';
}

tasks.forEach(task => {
  task.checked = localStorage.getItem(`horizonte-task-${task.dataset.task}`) === 'true';
  task.addEventListener('change', () => {
    localStorage.setItem(`horizonte-task-${task.dataset.task}`, String(task.checked));
    updateProgress();
  });
});
if (tasks.length) updateProgress();
