const root = document.body;
const menuButton = document.querySelector('#menuButton');
const nav = document.querySelector('#mainNav');
const themeButton = document.querySelector('#themeButton');
const readingBar = document.querySelector('#readingBar');
const toast = document.querySelector('#toast');

const savedTheme = localStorage.getItem('horizonte-theme');
if (savedTheme === 'dark') root.classList.add('dark');

themeButton.addEventListener('click', () => {
  root.classList.toggle('dark');
  localStorage.setItem('horizonte-theme', root.classList.contains('dark') ? 'dark' : 'light');
});

menuButton.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

nav.addEventListener('click', event => {
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

const tasks = [...document.querySelectorAll('#checklist input')];
const progressValue = document.querySelector('#progressValue');
const taskProgress = document.querySelector('#taskProgress');
const progressMessage = document.querySelector('#progressMessage');

function updateProgress() {
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
updateProgress();
