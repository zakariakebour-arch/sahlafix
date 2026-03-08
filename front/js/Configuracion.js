/* ═══════════════════════════════════════
   Configuracion.js — SahlaFix
   ═══════════════════════════════════════ */

const API_BASE = 'http://127.0.0.1:5000/api/v1';
const token    = localStorage.getItem('token');
console.log( localStorage.getItem('token'));
// ── Referencias DOM ──
const saveBtn       = document.getElementById('save-btn');
const toastEl       = document.getElementById('toast');
const avatarEl      = document.getElementById('config-avatar');
const nameDisplay   = document.getElementById('config-name-display');

const fields = {
  full_name:   document.getElementById('field-name'),
  phone:       document.getElementById('field-phone'),
  city:        document.getElementById('field-city'),
  wilaya:      document.getElementById('field-wilaya'),
  description: document.getElementById('field-desc'),
  photo:       document.getElementById('field-photo'),
};

/* ══════════════════════════════════════
   TOAST
   ══════════════════════════════════════ */
let toastTimer;
function showToast(msg, type = 'success') {
  clearTimeout(toastTimer);
  toastEl.textContent = msg;
  toastEl.className   = `config-toast ${type} show`;
  toastTimer = setTimeout(() => {
    toastEl.className = 'config-toast';
  }, 3000);
}

/* ══════════════════════════════════════
   AVATAR — foto o inicial
   ══════════════════════════════════════ */
function renderAvatar(name, imageUrl) {
  const initial = (name || '?').charAt(0).toUpperCase();
  avatarEl.innerHTML = '';

  if (imageUrl) {
    const img = document.createElement('img');
    img.src   = imageUrl;
    img.alt   = initial;
    img.onerror = () => {
      avatarEl.innerHTML = '';
      avatarEl.textContent = initial;
    };
    avatarEl.appendChild(img);
  } else {
    avatarEl.textContent = initial;
  }
}

/* ══════════════════════════════════════
   CARGAR DATOS ACTUALES DEL TÉCNICO
   ══════════════════════════════════════ */
async function loadProfile() {
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/technicians/me`, {
      headers: { 'Authorization': 'Bearer ' + token }
    });

    if (!res.ok) return;

    const data = await res.json();

    // Rellenar campos
    fields.full_name.value   = data.full_name   || '';
    fields.phone.value       = data.phone        || '';
    fields.city.value        = data.city         || '';
    fields.description.value = data.description  || '';
    fields.photo.value       = data.photo_profile || '';

    // Wilaya — seleccionar opción correcta
    if (data.wilaya) {
      const opt = [...fields.wilaya.options].find(o => o.value === data.wilaya);
      if (opt) fields.wilaya.value = data.wilaya;
    }

    // Nombre en header y avatar
    nameDisplay.textContent = data.full_name || 'Tu perfil';
    renderAvatar(data.full_name, data.photo_profile);

  } catch (err) {
    console.error('[Configuracion] loadProfile:', err);
  }
}

/* ══════════════════════════════════════
   ACTUALIZAR FOTO AL CAMBIAR URL
   ══════════════════════════════════════ */
fields.photo.addEventListener('input', () => {
  renderAvatar(fields.full_name.value, fields.photo.value.trim());
});

fields.full_name.addEventListener('input', () => {
  nameDisplay.textContent = fields.full_name.value || 'Tu perfil';
  renderAvatar(fields.full_name.value, fields.photo.value.trim());
});

/* ══════════════════════════════════════
   GUARDAR CAMBIOS — PUT /technicians/me
   ══════════════════════════════════════ */
saveBtn.addEventListener('click', async () => {
  if (!token) {
    showToast('No hay sesión activa', 'error');
    return;
  }

  // Construir payload solo con campos rellenados
  const payload = {};
  if (fields.full_name.value.trim())   payload.full_name   = fields.full_name.value.trim();
  if (fields.phone.value.trim())        payload.phone       = fields.phone.value.trim();
  if (fields.city.value.trim())         payload.city        = fields.city.value.trim();
  if (fields.wilaya.value)              payload.wilaya      = fields.wilaya.value;
  if (fields.description.value.trim())  payload.description = fields.description.value.trim();
  if (fields.photo.value.trim())        payload.photo       = fields.photo.value.trim();

  if (Object.keys(payload).length === 0) {
    showToast('No hay cambios que guardar', 'error');
    return;
  }

  saveBtn.disabled    = true;
  saveBtn.textContent = 'Guardando…';

  try {
    const res = await fetch(`${API_BASE}/technicians/me`, {
      method:  'PUT',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok) {
      showToast('Cambios guardados correctamente', 'success');
      nameDisplay.textContent = data.full_name || nameDisplay.textContent;
      renderAvatar(data.full_name, data.photo_profile);
    } else {
      showToast(data.error || 'Error al guardar', 'error');
    }

  } catch (err) {
    console.error('[Configuracion] save:', err);
    showToast('Error de conexión', 'error');
  } finally {
    saveBtn.disabled    = false;
    saveBtn.textContent = 'Guardar cambios';
  }
});

/* ══════════════════════════════════════
   ARRANCAR
   ══════════════════════════════════════ */
loadProfile();