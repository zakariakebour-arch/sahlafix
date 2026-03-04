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

        // DESCRIPCIÓN
        document.getElementById("profile-desc").textContent = tech.description ?? "Sin descripción disponible.";

        // INFO
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