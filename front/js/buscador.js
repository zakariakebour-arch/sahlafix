const API_BASE = 'http://127.0.0.1:5000/api/v1';

const searchInput   = document.getElementById('search-input');
const globalSearch  = document.getElementById('global-search');
const searchBtn     = document.getElementById('search-btn');
const searchClear   = document.getElementById('search-clear');
const resultsGrid   = document.getElementById('results-grid');
const resultsHeader = document.getElementById('results-header');
const resultsCount  = document.getElementById('results-count');
const resultsClear  = document.getElementById('results-clear');
const retryBtn      = document.getElementById('retry-btn');

const stateInitial  = document.getElementById('state-initial');
const stateLoading  = document.getElementById('state-loading');
const stateEmpty    = document.getElementById('state-empty');
const stateError    = document.getElementById('state-error');

/* ── State ── */
let lastQuery = '';
let debounceTimer = null;

/* ══════════════════════════════════════
   SHOW / HIDE STATES
   ══════════════════════════════════════ */
function showState(name) {
  [stateInitial, stateLoading, stateEmpty, stateError].forEach(el => el.style.display = 'none');
  resultsHeader.style.display = 'none';
  resultsGrid.innerHTML = '';

  const map = {
    initial: stateInitial,
    loading: stateLoading,
    empty:   stateEmpty,
    error:   stateError,
  };

  if (map[name]) map[name].style.display = 'flex';
}

/* ══════════════════════════════════════
   HIGHLIGHT MATCH
   ══════════════════════════════════════ */
function highlight(text, query) {
  if (!query) return escapeHtml(text);
  const escaped = escapeHtml(text);
  const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
  return escaped.replace(regex, '<mark class="highlight">$1</mark>');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
//Creamos card
function buildCard(tech, query, index) {
  const name     = tech.full_name  ?? '—';
  const wilaya   = tech.wilaya     ?? '';
  const city     = tech.city       ?? '';
  const location = [city, wilaya].filter(Boolean).join(', ') || '—';
  const avail    = tech.availability ?? 'Disponible';

  /* Avatar */
  let avatarHtml;
  if (tech.image_url && tech.image_url.trim() !== '') {
    avatarHtml = `<img src="${escapeHtml(`${API_BASE}/uploads/avatars/${tech.image_url}`)}" alt="${escapeHtml(name)}" loading="lazy">`;
  } else {
    avatarHtml = `<span>${name.charAt(0).toUpperCase()}</span>`;
  }

  /* Category label — fetch from categories map if available */
  const categoryLabel = tech.category_name ?? `Cat. ${tech.category_id ?? ''}`;

  const card = document.createElement('a');
  card.className = 'card';

  /* Detectamos si es técnico o cliente */
  const isTechnician = tech.role === "technician";

  /* Si es técnico va a su ficha, si es cliente a perfil */
  card.href = isTechnician
    ? `technician_info.html?id=${tech.technician_id}`
    : `technician_info.html?id=${tech.user_id}`;

  card.style.animationDelay = `${index * 60}ms`;

  card.innerHTML = `
    <div class="avatar">${avatarHtml}</div>
    <div class="card-body">
      <div class="card-name">${highlight(name, query)}</div>
      <div class="card-meta">
        <span class="badge-category">${tech.role === "technician" ? escapeHtml(categoryLabel) : "Cliente"}</span>
        <span class="dot"></span>
        <svg style="width:11px;height:11px;stroke:var(--muted);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
          <circle cx="12" cy="9" r="2.5"/>
        </svg>
        <span>${escapeHtml(location)}</span>
      </div>
    </div>
    <div class="card-right">
      <span class="badge-avail">${escapeHtml(avail)}</span>
    </div>
    <div class="card-arrow">
      <svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
    </div>
  `;

  return card;
}
//Renderizar resultados
function renderResults(technicians, query) {
  if (!technicians || technicians.length === 0) {
    showState('empty');
    return;
  }

  showState(null); // hide all states
  resultsGrid.innerHTML = '';

  technicians.forEach((tech, i) => {
    resultsGrid.appendChild(buildCard(tech, query, i));
  });

  /* Results count header */
  const n = technicians.length;
  resultsCount.innerHTML = `<strong>${n}</strong> resultado${n !== 1 ? 's' : ''} encontrado${n !== 1 ? 's' : ''}`;
  resultsHeader.style.display = 'flex';
}

//fetch a tecnicos
async function searchTechnicians(query) {
  query = query.trim();
  if (!query) { showState('initial'); return; }

  lastQuery = query;
  showState('loading');

  try {
    /* Search by name — adjust endpoint to your API */
    const url = `${API_BASE}/technicians/search?name=${encodeURIComponent(query)}`;
    const res = await fetch(url);

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();

    /* API may return array directly or wrapped */
    const list = Array.isArray(data) ? data : (data.technicians ?? data.data ?? []);

    renderResults(list, query);

  } catch (err) {
    console.error('[SahlaFix Search]', err);
    showState('error');
  }
}
//Borramos busqueda
function clearSearch() {
  searchInput.value = '';
  searchClear.classList.remove('visible');
  showState('initial');
  lastQuery = '';
  searchInput.focus();
}

//El evento para buscar en tiempo real
searchInput.addEventListener('input', () => {
  const val = searchInput.value;

  /* Sync header search */
  if (globalSearch) globalSearch.value = val;

  /* Show/hide clear button */
  if (val.trim()) {
    searchClear.classList.add('visible');
  } else {
    searchClear.classList.remove('visible');
    showState('initial');
    clearTimeout(debounceTimer);
    return;
  }

  /* Debounced live search — 420ms */
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    searchTechnicians(val);
  }, 420);
});

/* Enter key */
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    clearTimeout(debounceTimer);
    searchTechnicians(searchInput.value);
  }
});

/* Sync typing from header search bar */
if (globalSearch) {
  globalSearch.addEventListener('input', () => {
    searchInput.value = globalSearch.value;
    searchInput.dispatchEvent(new Event('input'));
  });
  globalSearch.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      clearTimeout(debounceTimer);
      searchTechnicians(globalSearch.value);
    }
  });
}

//Para limpiar el input
searchClear.addEventListener('click', clearSearch);

/* Results clear */
if (resultsClear) {
  resultsClear.addEventListener('click', clearSearch);
}

/* Retry */
if (retryBtn) {
  retryBtn.addEventListener('click', () => {
    if (lastQuery) searchTechnicians(lastQuery);
  });
}

/* ── Init ── */
showState('initial');
searchInput.focus();