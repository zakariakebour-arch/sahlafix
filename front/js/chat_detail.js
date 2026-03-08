const API_BASE = "http://127.0.0.1:5000/api/v1";

const params         = new URLSearchParams(window.location.search);
const conversationId = params.get("id");

const token  = localStorage.getItem("token");
const userId = Number(localStorage.getItem("user_id"));

const chatBox = document.getElementById("chat-messages");
const sendBtn = document.getElementById("send-btn");
const input   = document.getElementById("message-input");

let lastMessageId  = 0;
let lastDateLabel  = '';  // para separadores de fecha
/* ══════════════════════════════════════
   CARGAR INFO DE LA CONVERSACIÓN
   ══════════════════════════════════════ */
async function loadConversationInfo() {
  try {
    const res = await fetch(
      `${API_BASE}/message/conversations/user/${userId}`,
      { headers: { "Authorization": "Bearer " + token } }
    );
    if (!res.ok) return;

    const convs = await res.json();
    const conv = convs.find(c => String(c.conversation_id || c.id) === String(conversationId));
    if (!conv) return;

    const name     = conv.other_user_name || conv.name || 'Usuario';
    const imageUrl = conv.other_user_image || conv.image_url || null;
    const initial  = name.charAt(0).toUpperCase();

    // Nombre en header
    document.getElementById('header-name').textContent = name;

    // Avatar: foto o inicial
    const avatarEl = document.getElementById('header-avatar');

    // limpiar avatar antes de renderizar
    avatarEl.innerHTML = "";

    if (imageUrl && imageUrl.trim() !== "") {

      const img = document.createElement('img');

      img.src = `${API_BASE}/uploads/avatars/${imageUrl}`;

      img.alt = initial;

      img.style.width = "100%";
      img.style.height = "100%";
      img.style.objectFit = "cover";

      img.onerror = () => {
        avatarEl.innerHTML = "";
        avatarEl.textContent = initial;
      };

      avatarEl.appendChild(img);

    } else {

      avatarEl.textContent = initial;

    }

  } catch (err) {
    console.error('[Chat info]', err);
  }
}
//Formatear hora
function formatHour(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleTimeString('es-ES', {
    hour: '2-digit', minute: '2-digit'
  });
}

function formatDateLabel(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now  = new Date();
  const diff = Math.floor((now - date) / 86400000);
  if (diff === 0) return 'Hoy';
  if (diff === 1) return 'Ayer';
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long' });
}
//Construimos la burbuja
function buildBubble(msg) {
  const isMine = msg.sender_id === userId;

  // Separador de fecha
  const dateLabel = formatDateLabel(msg.created_at || msg.timestamp);
  if (dateLabel && dateLabel !== lastDateLabel) {
    const sep = document.createElement('div');
    sep.className = 'date-separator';
    sep.textContent = dateLabel;
    chatBox.appendChild(sep);
    lastDateLabel = dateLabel;
  }

  const bubble = document.createElement('div');
  bubble.className = `msg-bubble ${isMine ? 'mine' : 'other'}`;
  bubble.innerHTML = `
    ${msg.content}
    <span class="msg-time">${formatHour(msg.created_at || msg.timestamp)}</span>
  `;

  return bubble;
}
//Cargar mensajes
async function loadMessages() {
  try {
    const res = await fetch(
      `${API_BASE}/message/conversations/${conversationId}/messages`,
      { headers: { "Authorization": "Bearer " + token } }
    );

    if (!res.ok) throw new Error("Error cargando mensajes");

    const messages = await res.json();
    let scrollDown = false;

    messages.forEach(msg => {
      if (msg.id <= lastMessageId) return;
      chatBox.appendChild(buildBubble(msg));
      lastMessageId = msg.id;
      scrollDown = true;
    });

    if (scrollDown) {
      chatBox.scrollTop = chatBox.scrollHeight;
    }

  } catch (err) {
    console.error(err);
  }
}
//Enviar el mensaje
async function sendMessage() {
  const content = input.value.trim();
  if (!content) return;

  try {
    const res = await fetch(`${API_BASE}/message/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        sender_id: userId,
        content: content
      })
    });

    if (!res.ok) throw new Error("Error enviando mensaje");

    input.value = "";
    loadMessages();

  } catch (err) {
    console.error(err);
  }
}

sendBtn.addEventListener("click", sendMessage);

// Enter para enviar
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
//Cargar los mensajes cada 1.5 segudos para refrescar
loadMessages();
setInterval(loadMessages, 1500);
loadConversationInfo();