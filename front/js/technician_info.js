const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const API_BASE = "http://127.0.0.1:5000/api/v1";

    async function loadTechnician() {
      try {
        const res = await fetch(`${API_BASE}/technicians/${id}`);
        if (!res.ok) throw new Error("Error al cargar técnico");
        const tech = await res.json();

        // AVATAR
        const avatar = document.getElementById("avatar");
        if (tech.image_url && tech.image_url.trim() !== "") {
          const img = document.createElement("img");
          img.src = `${API_BASE}/uploads/avatars/${tech.image_url}`;
          img.alt = tech.name;
          avatar.appendChild(img);
        } else {
          avatar.textContent = tech.name.charAt(0).toUpperCase();
        }

        // header
        document.getElementById("profile-name").textContent = tech.name;
        document.getElementById("profile-category").textContent = tech.category_name;
        //Nombre del usuario 
        document.querySelector("title").textContent = tech.name;

        // Descripcion
        document.getElementById("profile-desc").textContent = tech.description ?? "Sin descripción disponible.";

        // Informacion del tecnico
        document.getElementById("info-zone").textContent = tech.wilaya ?? "—";
        document.getElementById("info-category").textContent = tech.category_name ?? "—";

      } catch (error) {
        document.querySelector(".technician-profile").innerHTML = `
          <div style="text-align:center;padding:60px 20px;color:var(--muted)">
            <p style="font-size:15px;font-weight:600">No se pudo cargar el perfil</p>
          </div>`;
      }
    }

loadTechnician();

function showToast(message, type = "error") {
  const existing = document.getElementById("toast-msg");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.id = "toast-msg";
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: ${type === "error" ? "#ff4d4f" : "#52c41a"};
    color: white;
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.3s ease;
  `;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.style.opacity = "1");
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

const contactBtn = document.getElementById("contact-btn");

contactBtn.addEventListener("click", async () => {

  const token = localStorage.getItem("token");

  if (!token) {
    showToast("Debes iniciar sesión para contactar");
    return;
  }

  const userId = localStorage.getItem("user_id");
  try {

    const res = await fetch(`${API_BASE}/message/conversations`, {

      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },

      body: JSON.stringify({
        user_id: userId,
        technician_id: id
      })

    });

    if (res.status === 403) {
      const data = await res.json();
      showToast(data.error || "Este técnico no está disponible para ser contactado");
      return;
    }

    if (!res.ok) {
      throw new Error("Error creando conversación");
    }

    const data = await res.json();

    const conversationId = data.id || data.conversation_id;

    window.location.href = `chat_detail.html?id=${conversationId}`;

  } catch (err) {

    console.error(err);
    showToast("No se pudo iniciar el chat");

  }

});