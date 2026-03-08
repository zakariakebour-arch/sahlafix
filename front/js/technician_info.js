    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    async function loadTechnician() {
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/technicians/${id}`);
        if (!res.ok) throw new Error("Error al cargar técnico");
        const tech = await res.json();

        // AVATAR
        const avatar = document.getElementById("avatar");
        if (tech.image_url && tech.image_url.trim() !== "") {
          const img = document.createElement("img");
          img.src = tech.image_url;
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

const API_BASE = "http://127.0.0.1:5000/api/v1";

const contactBtn = document.getElementById("contact-btn");

contactBtn.addEventListener("click", async () => {

  const token = localStorage.getItem("token");

  if (!token) {
    alert("Debes iniciar sesión");
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

    if (!res.ok) {
      throw new Error("Error creando conversación");
    }

    const data = await res.json();

    const conversationId = data.id || data.conversation_id;

    window.location.href = `chat_detail.html?id=${conversationId}`;

  } catch (err) {

    console.error(err);
    alert("No se pudo iniciar el chat");

  }

});