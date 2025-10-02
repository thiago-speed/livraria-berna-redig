let API_BASE = localStorage.getItem('API_BASE') || 'http://localhost:5000';

const q = (sel) => document.querySelector(sel);
const qa = (sel) => Array.from(document.querySelectorAll(sel));

function showMsgAbove(targetEl, texto, tipo = 'ok') {
  if (!targetEl) return;
  const container = targetEl.closest('td, .linha, .alinhar-direita') || targetEl.parentElement;
  if (!container) return;
  let span = container.querySelector('.mensagens-inline');
  if (!span) {
    span = document.createElement('span');
    span.className = 'mensagens-inline';
    container.insertBefore(span, container.firstChild);
  }
  span.textContent = texto || '';
  span.dataset.tipo = tipo;
}

async function fetchJson(url, options = {}) {
  const resp = await fetch(url, options);
  let data = null;
  try { data = await resp.json(); } catch (_) { /* ignore */ }
  if (!resp.ok) {
    const msg = data && data.mensagem ? data.mensagem : `Erro HTTP ${resp.status}`;
    throw new Error(msg);
  }
  return data;
}

function renderTabela(livros) {
  const tbody = q('#tabela-livros tbody');
  tbody.innerHTML = '';
  const vazio = q('#estado-vazio');
  if (!livros || livros.length === 0) {
    vazio.hidden = false;
    return;
  }
  vazio.hidden = true;
  livros.forEach((l) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${l.id}</td>
      <td>${l.titulo}</td>
      <td>${l.autor}</td>
      <td>${l.ano_publicacao}</td>
      <td>R$ ${Number(l.preco).toFixed(2)}</td>
      <td>
        <input type="number" step="0.01" min="0" value="${Number(l.preco).toFixed(2)}" id="novo-preco-${l.id}" class="preco-input"/>
        <button data-acao="atualizar" data-id="${l.id}">Atualizar</button>
      </td>
      <td>
        <button class="perigo" data-acao="remover" data-id="${l.id}">Remover</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function carregarLivros() {
  q('#carregando').hidden = false;
  const data = await fetchJson(`${API_BASE}/livros`);
  renderTabela(data.dados || []);
  q('#carregando').hidden = true;
}

async function buscarPorAutor() {
  const autor = q('#busca-autor').value.trim();
  if (!autor) { await carregarLivros(); return; }
  const data = await fetchJson(`${API_BASE}/livros/buscar?autor=${encodeURIComponent(autor)}`);
  renderTabela(data.dados || []);
}

async function adicionarLivro(ev) {
  ev.preventDefault();
  const titulo = q('#titulo').value.trim();
  const autor = q('#autor').value.trim();
  const ano = q('#ano').value.trim();
  const preco = q('#preco').value.trim();
  try {
    await fetchJson(`${API_BASE}/livros`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ titulo, autor, ano_publicacao: ano, preco })
    });
    showMsgAbove(ev.submitter, 'Livro adicionado com sucesso', 'ok');
    q('#form-adicionar').reset();
    await carregarLivros();
  } catch (e) {
    showMsgAbove(ev.submitter, e.message, 'erro');
  }
}

async function atualizarPreco(id, btn) {
  const input = q(`#novo-preco-${id}`);
  const preco = input.value;
  try {
    await fetchJson(`${API_BASE}/livros/${id}/preco`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preco })
    });
    showMsgAbove(btn, 'Preço atualizado', 'ok');
    await carregarLivros();
  } catch (e) {
    showMsgAbove(btn, e.message, 'erro');
  }
}

async function removerLivro(id, btn) {
  if (!confirm('Tem certeza que deseja remover este livro?')) return;
  try {
    await fetchJson(`${API_BASE}/livros/${id}`, { method: 'DELETE' });
    showMsgAbove(btn, 'Livro removido', 'ok');
    await carregarLivros();
  } catch (e) {
    showMsgAbove(btn, e.message, 'erro');
  }
}

function exportarCSV(ev) {
  showMsgAbove(ev.currentTarget, 'Exportando CSV...', 'ok');
  window.location.href = `${API_BASE}/exportar`;
}

async function importarCSV(ev) {
  const input = q('#arquivo-csv');
  if (!input.files || !input.files[0]) { setMensagem('Selecione um arquivo CSV', 'erro'); return; }
  const formData = new FormData();
  formData.append('arquivo', input.files[0]);
  try {
    await fetchJson(`${API_BASE}/importar`, { method: 'POST', body: formData });
    showMsgAbove(ev.currentTarget, 'Importação concluída', 'ok');
    input.value = '';
    await carregarLivros();
  } catch (e) {
    showMsgAbove(ev.currentTarget, e.message, 'erro');
  }
}

async function criarBackup(ev) {
  try {
    await fetchJson(`${API_BASE}/backup`);
    showMsgAbove(ev.currentTarget, 'Backup criado', 'ok');
  } catch (e) {
    showMsgAbove(ev.currentTarget, e.message, 'erro');
  }
}

async function limparBackups(ev) {
  const max = Number(q('#max-backups').value || 5);
  try {
    await fetchJson(`${API_BASE}/backups/limpar?max=${max}`, { method: 'POST' });
    showMsgAbove(ev.currentTarget, 'Backups antigos limpos', 'ok');
  } catch (e) {
    showMsgAbove(ev.currentTarget, e.message, 'erro');
  }
}

function delegarTabela() {
  q('#tabela-livros').addEventListener('click', async (ev) => {
    const btn = ev.target.closest('button');
    if (!btn) return;
    const acao = btn.dataset.acao;
    const id = btn.dataset.id;
    if (acao === 'atualizar') await atualizarPreco(id, btn);
    if (acao === 'remover') await removerLivro(id, btn);
  });
}

function registrarEventos() {
  q('#form-adicionar').addEventListener('submit', adicionarLivro);
  q('#btn-buscar').addEventListener('click', async (ev) => {
    try {
      await buscarPorAutor();
      showMsgAbove(ev.currentTarget, 'Busca concluída', 'ok');
    } catch (e) {
      showMsgAbove(ev.currentTarget, e.message, 'erro');
    }
  });
  q('#btn-carregar-todos').addEventListener('click', carregarLivros);
  q('#btn-exportar').addEventListener('click', exportarCSV);
  q('#btn-importar').addEventListener('click', importarCSV);
  q('#btn-backup').addEventListener('click', criarBackup);
  q('#btn-limpar-backups').addEventListener('click', limparBackups);
  delegarTabela();
  const inputApi = q('#api-url');
  const btnSalvarApi = q('#btn-salvar-api');
  if (inputApi && btnSalvarApi) {
    inputApi.value = API_BASE;
    btnSalvarApi.addEventListener('click', (ev) => {
      const url = inputApi.value.trim();
      if (!url) return;
      API_BASE = url;
      localStorage.setItem('API_BASE', API_BASE);
      showMsgAbove(ev.currentTarget, 'URL da API salva', 'ok');
    });
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  registrarEventos();
  await carregarLivros();
});


