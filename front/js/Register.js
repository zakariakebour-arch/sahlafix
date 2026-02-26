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

  // ===============================
  // Funciones de UI
  // ===============================
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

  roleCliente.addEventListener('click', () => setRole('cliente'));
  roleTecnico.addEventListener('click', () => setRole('tecnico'));
  updateThumb();

  // ===============================
  // Validación
  // ===============================
  function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  }

  function showError(el, msg) {
    const errEl = document.getElementById('err-' + el.id);
    if (errEl) errEl.textContent = msg || '';
    el.classList.toggle('invalid', Boolean(msg));
  }

  function clearError(el) { showError(el, ''); }
  // Envio al forumulario del formulario
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validacion final
    let ok = true;
    const requiredIds = ['name','email','password'].concat(role === 'tecnico' ? ['phone','wilaya','city'] : []);
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

    // Preparar datos
    const payload = {
      name: fields.name.value.trim(),
      email: fields.email.value.trim(),
      password: fields.password.value,
      role,
      tecnico: role === 'tecnico' ? {
        phone: fields.phone.value.trim(),
        wilaya: fields.wilaya.value.trim(),
        city: fields.city.value.trim(),
        desc: fields.desc.value.trim(),
        categorias: fields.categorias.value ? [fields.categorias.value] : []
      } : null
    };
    // Fetch al backend
    try {
      const res = await fetch('http://127.0.0.1:5000/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.status === 201) {
        alert('Usuario creado correctamente');
        form.reset();
        setRole('cliente');
      } else {
        alert('Error: ' + (data.error || 'No se pudo crear usuario'));
        console.error(data);
      }
    } catch (err) {
      console.error('Error al conectar con backend:', err);
      alert('Error de conexión. Intenta nuevamente.');
    }
  });
})();