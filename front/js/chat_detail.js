const API_BASE = "http://127.0.0.1:5000/api/v1";

const params = new URLSearchParams(window.location.search);
const conversationId = params.get("id");

const token = localStorage.getItem("token");
const userId = Number(localStorage.getItem("user_id"));

const chatBox = document.getElementById("chat-messages");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("message-input");

let lastMessageId = 0;


// CARGAR MENSAJES
async function loadMessages() {

  try {

    const res = await fetch(`${API_BASE}/message/conversations/${conversationId}/messages`, {
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    if (!res.ok) throw new Error("Error cargando mensajes");

    const messages = await res.json();

    messages.forEach(msg => {

      if (msg.id <= lastMessageId) return;

      const div = document.createElement("div");

      div.textContent = msg.content;

      if (msg.sender_id === userId) {
        div.style.textAlign = "right";
      } else {
        div.style.textAlign = "left";
      }

      chatBox.appendChild(div);

      lastMessageId = msg.id;

    });

    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (err) {

    console.error(err);

  }

}


// ENVIAR MENSAJE
sendBtn.addEventListener("click", async () => {

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

    if (!res.ok) {
      throw new Error("Error enviando mensaje");
    }

    input.value = "";

    loadMessages();

  } catch (err) {

    console.error(err);

  }

});


// CARGA INICIAL
loadMessages();


// AUTO ACTUALIZACIÓN
setInterval(loadMessages, 5000);