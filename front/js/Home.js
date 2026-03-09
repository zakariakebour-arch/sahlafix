const API_BASE = 'http://127.0.0.1:5000/api/v1';

//Hacemos una promesa para sacar las categorias disponibles en el servidor
(async () => {
    //Seleccionamos el contenedor de categorias
    const selectCategorias = document.querySelector('.filter-grid .select-wrap select');
    //Seleccionamos el contenedor de filtros rapidos segun categorias disponibles tambien
    const selectOptions = document.querySelector('.quick-filters');

    if (!selectCategorias) return;
    if (!selectOptions) return;

    // Mantener la opción placeholder inicial
    const placeholder = selectCategorias.querySelector('option[value=""]') || selectCategorias.querySelector('option:first-child');

    // Estado: "cargando"
    const originalText = placeholder ? placeholder.textContent : 'Categoría';
    if (placeholder) {
      placeholder.textContent = 'Cargando categorías...';
      placeholder.disabled = true;
      placeholder.selected = true;
      placeholder.value = '';
    }

    try {
      const res = await fetch(`${API_BASE}/categories`, { method: 'GET' });
      if (!res.ok) throw new Error('Error al obtener categorías');

      const categorias = await res.json(); // esperado la respuesta del servidor
      const keepFirst = placeholder ? 1 : 0;
      while (selectCategorias.options.length > keepFirst) {
        selectCategorias.remove(keepFirst);
      }

      categorias.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = String(cat.id);
        opt.textContent = cat.name;
        selectCategorias.appendChild(opt);
      });

      if (placeholder) {
        placeholder.textContent = originalText || 'Categoría';
        placeholder.disabled = false;
        placeholder.selected = true;
        placeholder.value = '';
      }
      selectOptions.innerHTML = '';

      // Botón "Todos"
      const btnTodos = document.createElement('button');
      btnTodos.className = 'pill active';
      btnTodos.type = 'button';
      btnTodos.textContent = 'Todos';
      btnTodos.dataset.categoryId = '';
      selectOptions.appendChild(btnTodos);

      // Resto de categorías
      categorias.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'pill';
        btn.type = 'button';
        btn.textContent = cat.name;
        btn.dataset.categoryId = String(cat.id);
        btn.dataset.slug = cat.slug || '';
        selectOptions.appendChild(btn);
      });

      // Manejador de clicks para activar/desactivar y (opcional) sincronizar el <select>
      selectOptions.addEventListener('click', (e) => {
        const target = e.target;
        if (!(target instanceof HTMLElement)) return;
        if (!target.classList.contains('pill')) return;

        // Activar visualmente
        selectOptions.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        target.classList.add('active');

        // Sincronizar el <select> (opcional)
        const catId = target.dataset.categoryId || '';
        selectCategorias.value = catId;
        selectCategorias.dispatchEvent(new Event('change')); // aquí puedes enganchar tu filtrado
      });

    } catch (_) {
      if (placeholder) {
        placeholder.textContent = 'No se pudieron cargar las categorías';
        placeholder.disabled = true;
        placeholder.selected = true;
        placeholder.value = '';
      }
      console.log("Algun error ha ocurrido");
    }
  })();


//Resolver URL de avatar del tecnico
function resolveAvatarUrl(imageUrl) {
  if (!imageUrl) return null;
  if (imageUrl.startsWith('http')) return imageUrl;
  if (imageUrl.includes('/uploads/avatars')) return `http://127.0.0.1:5000${imageUrl}`;
  return `${API_BASE}/uploads/avatars/${imageUrl}`;
}


// Obtener y renderizar tecnicos dinamicamente haciendo una peticion al servidor
(async () => {
  try {
    const res = await fetch(`${API_BASE}/technicians/`, {
      method: "GET"
    });

    if (!res.ok) throw new Error("Error al cargar técnicos");

    const technicians = await res.json();

    const cardsContainer = document.querySelector('.cards');
    if (!cardsContainer) return;

    // Limpiamos contenedor
    cardsContainer.innerHTML = "";

    technicians.forEach(tech => {

      // Crear card
      const card = document.createElement('a');
      card.className = 'card';
      //Aqui creamos enlance que escoje el indice con la ruta dinamicamente,asi podremos consultar el servidor para la informacion del usuario
      card.href = `technician_info.html?id=${tech.id}`;

      // Avatar con foto si existe, si no primera letra del nombre
      const avatar = document.createElement('div');
      avatar.className = 'avatar';
      const avatarSrc = resolveAvatarUrl(tech.image_url);
      if (avatarSrc) {
        const img = document.createElement('img');
        img.src = avatarSrc;
        img.alt = tech.name.charAt(0).toUpperCase();
        img.onerror = () => { img.style.display = 'none'; avatar.textContent = tech.name.charAt(0).toUpperCase(); };
        avatar.appendChild(img);
      } else {
        avatar.textContent = tech.name.charAt(0).toUpperCase();
      }

      // Body
      const body = document.createElement('div');
      body.className = 'card-body';

      const name = document.createElement('div');
      name.className = 'card-name';
      name.textContent = tech.name;

      const meta = document.createElement('div');
      meta.className = 'card-meta';

      const dot1 = document.createElement('span');
      dot1.className = 'dot';

      const category = document.createElement('span');
      category.textContent = `${tech.category_name}`;

      const dot2 = document.createElement('span');
      dot2.className = 'dot';

      // Descripción
      const description = document.createElement('div');
      description.className = 'card-description';
      description.textContent = tech.description;

      // Estructura
      meta.appendChild(dot1);
      meta.appendChild(category);
      meta.appendChild(dot2);

      body.appendChild(name);
      body.appendChild(meta);
      body.appendChild(description);

      card.appendChild(avatar);
      card.appendChild(body);

      cardsContainer.appendChild(card);
    });

  } catch (error) {
    console.error("Error:", error);
  }
})();


(async () => {
  const cardsContainer = document.querySelector('.cards');
  let allTechnicians = [];

  async function fetchTechnicians() {
    const res = await fetch(`${API_BASE}/technicians/`, { method: "GET" });
    if (!res.ok) throw new Error("Error al cargar técnicos");
    return await res.json();
  }

  function renderTechnicians(technicians) {
    cardsContainer.innerHTML = "";
    technicians.forEach(tech => {
      const card = document.createElement('a');
      card.className = 'card';
      card.href = `technician_info.html?id=${tech.id}`;

      // Avatar con foto si existe, si no primera letra del nombre
      const avatar = document.createElement('div');
      avatar.className = 'avatar';
      const avatarSrc = resolveAvatarUrl(tech.image_url);
      if (avatarSrc) {
        const img = document.createElement('img');
        img.src = avatarSrc;
        img.alt = tech.name.charAt(0).toUpperCase();
        img.onerror = () => { img.style.display = 'none'; avatar.textContent = tech.name.charAt(0).toUpperCase(); };
        avatar.appendChild(img);
      } else {
        avatar.textContent = tech.name.charAt(0).toUpperCase();
      }

      const body = document.createElement('div');
      body.className = 'card-body';

      const name = document.createElement('div');
      name.className = 'card-name';
      name.textContent = tech.name;

      const meta = document.createElement('div');
      meta.className = 'card-meta';

      const dot1 = document.createElement('span');
      dot1.className = 'dot';

      const category = document.createElement('span');
      category.textContent = tech.category_name;

      const dot2 = document.createElement('span');
      dot2.className = 'dot';

      const description = document.createElement('div');
      description.className = 'card-description';
      description.textContent = tech.description;

      meta.appendChild(dot1);
      meta.appendChild(category);
      meta.appendChild(dot2);

      body.appendChild(name);
      body.appendChild(meta);
      body.appendChild(description);

      card.appendChild(avatar);
      card.appendChild(body);

      cardsContainer.appendChild(card);
    });
  }

  function filterAndRender(categoryId) {
    if (!categoryId) {
      renderTechnicians(allTechnicians);
    } else {
      const filtered = allTechnicians.filter(t => String(t.category_id) === String(categoryId));
      renderTechnicians(filtered);
    }
  }

  try {
    allTechnicians = await fetchTechnicians();
    renderTechnicians(allTechnicians);

    const selectCategorias = document.querySelector('.filter-grid .select-wrap select');
    const quickFilters = document.querySelector('.quick-filters');

    selectCategorias.addEventListener('change', () => {
      filterAndRender(selectCategorias.value);
      quickFilters.querySelectorAll('.pill').forEach(p => {
        p.classList.toggle('active', p.dataset.categoryId === selectCategorias.value);
      });
    });

    quickFilters.addEventListener('click', (e) => {
      const target = e.target;
      if (!target.classList.contains('pill')) return;
      filterAndRender(target.dataset.categoryId);
    });

  } catch (error) {
    console.error("Error:", error);
  }
})();

