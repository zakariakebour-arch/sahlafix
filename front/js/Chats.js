const API_BASE = 'http://127.0.0.1:5000/api/v1';

// ── ID del usuario actual (cambiar dinámicamente según login) ──
async function getOrFetchUserId() {
  let uid = localStorage.getItem('user_id');
  if (uid) return uid;
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return null;
    const me = await res.json();
    uid = me?.user?.id ?? null;
    if (uid) localStorage.setItem('user_id', uid);
    return uid;
  } catch {
    return null;
  }
}

console.log(localStorage.getItem('user_id'))

//Referencias DOM
const listEl       = document.getElementById('chats-list');
const stateLoading = document.getElementById('state-loading');
const stateEmpty   = document.getElementById('state-empty');
const stateError   = document.getElementById('state-error');
const retryBtn     = document.getElementById('retry-btn');

retryBtn.addEventListener('click', loadConversations);

//Mostramos estado
function showState(name) {
  stateLoading.style.display = name === 'loading' ? 'flex' : 'none';
  stateEmpty.style.display   = name === 'empty'   ? 'flex' : 'none';
  stateError.style.display   = name === 'error'   ? 'flex' : 'none';
  listEl.style.display       = name === null      ? 'flex' : 'none';
}

//Formateamos fecha y hora
function formatTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now  = new Date();
  const diff = now - date;
  const days = Math.floor(diff / 86400000);

  if (days === 0) {
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
  } else if (days === 1) {
    return 'Ayer';
  } else if (days < 7) {
    return date.toLocaleDateString('es-ES', { weekday: 'short' });
  } else {
    return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' });
  }
}

//Iniciales de nombre
function getInitials(name) {
  if (!name) return '?';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return parts[0][0].toUpperCase();
}

//Resolver URL de avatar (añadido para que cargue la imagen correctamente)
function resolveAvatarUrl(imageUrl) {

  if (!imageUrl) return null;

  if (imageUrl.startsWith('http')) {
    return imageUrl;
  }

  if (imageUrl.includes('/uploads/avatars')) {
    return `http://127.0.0.1:5000${imageUrl}`;
  }

  return `http://127.0.0.1:5000/uploads/avatars/${imageUrl}`;  // 
}

//Construimos conversacion
function buildCard(conv) {
  const name        = conv.other_user_name || conv.name || 'Usuario';
  const lastMsg     = conv.last_message    || 'Sin mensajes aún';
  const time        = formatTime(conv.last_message_time || conv.updated_at);
  const unread      = conv.unread_count    || 0;
  const imageUrl    = conv.other_user_image || conv.image_url || null;
  const convId      = conv.conversation_id  || conv.id || '';

  const isUnread = unread > 0;

  const avatarSrc = resolveAvatarUrl(imageUrl);

  const avatarInner = avatarSrc
    ? `<img src="${avatarSrc}" alt="${getInitials(name)}" onerror="this.style.display='none'">`
    : getInitials(name);

  const unreadDot   = isUnread ? `<span class="unread-dot"></span>` : '';
  const unreadBadge = isUnread ? `<span class="unread-badge">${unread > 99 ? '99+' : unread}</span>` : '';
  const timeClass   = isUnread ? 'chat-time unread' : 'chat-time';
  const nameClass   = isUnread ? 'chat-name unread' : 'chat-name';
  const previewClass= isUnread ? 'chat-preview unread' : 'chat-preview';

  const card = document.createElement('a');
  card.className = 'chat-card';
  card.href = `chat_detail.html?id=${convId}`;

  card.innerHTML = `
    <div class="chat-avatar">
      ${avatarInner}
      ${unreadDot}
    </div>
    <div class="chat-body">
      <div class="chat-top">
        <span class="${nameClass}">${name}</span>
        <span class="${timeClass}">${time}</span>
      </div>
      <div class="${previewClass}">
        <span>${lastMsg}</span>
        ${unreadBadge}
      </div>
    </div>
  `;

  return card;
}

//Para cargar las conversaciones
async function loadConversations() {
  showState('loading');
  listEl.innerHTML = '';

  //Verficar el token
  const token = localStorage.getItem("token"); 
  if (!token) {
    showState('error');
    return;
  }

  const currentUserId = await getOrFetchUserId();
  if (!currentUserId) {
    showState('error');
    return;
  }

  fetch(`${API_BASE}/message/conversations/user/${currentUserId}`, {
    headers: {
      "Authorization": "Bearer " + token
    }
  })
    .then(res => {
      if (!res.ok) throw new Error('Error del servidor');
      return res.json();
    })
    .then(data => {
      if (!data || data.length === 0) {
        showState('empty');
        return;
      }

      // Ordenar por último mensaje mas reciente
      data.sort((a, b) => {
        const ta = new Date(a.last_message_time || a.updated_at || 0);
        const tb = new Date(b.last_message_time || b.updated_at || 0);
        return tb - ta;
      });

      data.forEach(conv => {
        listEl.appendChild(buildCard(conv));
      });

      showState(null);
    })
    .catch(err => {
      console.error('[SahlaFix Chats]', err);
      showState('error');
    });
}

// Arrancar
loadConversations();



(function() {

  const form = document.getElementById('user-form');
  const roleCliente = document.getElementById('role-cliente');
  const roleTecnico = document.getElementById('role-tecnico');
  const thumb = document.querySelector('.segmented .thumb');
  const tecnicoSection = document.getElementById('tecnico-section');

  const fields = {
    name: document.getElementById('name'),
    email: document.getElementById('email'),
    password: document.getElementById('password'),
    phone: document.getElementById('phone'),
    wilaya: document.getElementById('wilaya'),
    city: document.getElementById('city'),
    desc: document.getElementById('desc'),
    categorias: document.getElementById('categorias')
  };

  let role = 'cliente';

  function updateThumb() {
    const index = role === 'cliente' ? 0 : 1;
    thumb.style.translate = `${index * 100}% 0`;
  }

  function setRole(nextRole) {
    role = nextRole;
    const isTecnico = role === 'tecnico';

    roleCliente.setAttribute('aria-pressed', String(!isTecnico));
    roleCliente.setAttribute('aria-selected', String(!isTecnico));

    roleTecnico.setAttribute('aria-pressed', String(isTecnico));
    roleTecnico.setAttribute('aria-selected', String(isTecnico));

    tecnicoSection.classList.toggle('open', isTecnico);
    tecnicoSection.setAttribute('aria-hidden', String(!isTecnico));

    ['phone', 'wilaya', 'city'].forEach(id => {
      fields[id].required = isTecnico;
    });

    updateThumb();
  }

  updateThumb();

  function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  }

  function showError(el, msg) {
    const errEl = document.getElementById('err-' + el.id);
    if (errEl) errEl.textContent = msg || '';
    el.classList.toggle('invalid', Boolean(msg));
  }

  function clearError(el) { showError(el, ''); }

  const toast = document.getElementById("toast");

  function showToast(message, type = "error") {

    toast.textContent = message;

    toast.style.position = "fixed";
    toast.style.bottom = "30px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.padding = "14px 22px";
    toast.style.borderRadius = "12px";
    toast.style.fontWeight = "600";
    toast.style.boxShadow = "0 10px 30px rgba(0,0,0,0.08)";
    toast.style.zIndex = "9999";
    toast.style.opacity = "0";
    toast.style.transition = "all .3s ease";

    if (type === "success") {
      toast.style.background = "#2BA5A5";
      toast.style.color = "#fff";
      toast.style.border = "none";
    } else {
      toast.style.background = "#fff";
      toast.style.color = "#E03A49";
      toast.style.border = "1px solid rgba(224,58,73,0.25)";
    }

    requestAnimationFrame(() => {
      toast.style.opacity = "1";
      toast.style.bottom = "40px";
    });

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.bottom = "30px";
    }, 3500);
  }

  form.addEventListener('submit', async (e) => {

    e.preventDefault();

    let ok = true;

    const requiredIds = ['name','email','password']
      .concat(role === 'tecnico' ? ['phone','wilaya','city'] : []);

    requiredIds.forEach(id => {

      const el = fields[id];

      if (!el.value.trim()) {
        showError(el, 'Este campo es obligatorio.');
        ok = false;
      }

    });

    if (fields.email.value && !validateEmail(fields.email.value)) {
      showError(fields.email, 'Introduce un email válido.');
      ok = false;
    }

    if (fields.password.value && fields.password.value.length < 8) {
      showError(fields.password, 'Mínimo 8 caracteres.');
      ok = false;
    }

    if (!ok) return;

    let payload;
    let url;

    if (role === 'tecnico') {

      url = 'http://127.0.0.1:5000/api/v1/auth/register-technician';

      if (!navigator.geolocation) {
        showToast("Tu navegador no permite geolocalización.");
        return;
      }

      navigator.geolocation.getCurrentPosition(async function(pos){

        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        payload = {
          email: fields.email.value.trim(),
          password: fields.password.value,
          role: "technician",
          full_name: fields.name.value.trim(),
          phone: fields.phone.value.trim(),
          wilaya: fields.wilaya.value.trim(),
          city: fields.city.value.trim(),
          description: fields.desc.value.trim(),
          category_id: Number(fields.categorias.value),
          latitude: lat,
          longitude: lng
        };

        sendRegister(url,payload);

      }, function(){
        showToast("Debes permitir ubicación para registrarte como técnico.");
      });

    }

    else {

      url = 'http://127.0.0.1:5000/api/v1/auth/register';

      payload = {
        email: fields.email.value.trim(),
        password: fields.password.value,
        role: "user",
        full_name: fields.name.value.trim()
      };

      sendRegister(url,payload);

    }

  });

})();