categoria_id = document.querySelector("#categorias").value;
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

  roleCliente.addEventListener('click', () => setRole('cliente'));
  roleTecnico.addEventListener('click', () => setRole('tecnico'));
  updateThumb();

  // Validación básica
  function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  }

  function showError(el, msg) {
    const errEl = document.getElementById('err-' + el.id);
    if (errEl) errEl.textContent = msg || '';
    el.classList.toggle('invalid', Boolean(msg));
  }

  function clearError(el) { showError(el, ''); }

  // Toast
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

  // Envío del formulario
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validación local
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

    let payload;
    let url;

    if (role === 'tecnico') {
      url = 'http://127.0.0.1:5000/api/v1/auth/register-technician';
      payload = {
        email: fields.email.value.trim(),
        password: fields.password.value,
        role: "technician",
        full_name: fields.name.value.trim(),
        phone: fields.phone.value.trim(),
        wilaya: fields.wilaya.value.trim(),
        city: fields.city.value.trim(),
        description: fields.desc.value.trim(),
        category_id: Number(fields.categorias.value)
      };
    } else {
      url = 'http://127.0.0.1:5000/api/v1/auth/register';
      payload = {
        email: fields.email.value.trim(),
        password: fields.password.value,
        role: "user",
        name: fields.name.value.trim()
      };
    }

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.status === 201) {
        showToast("Cuenta creada correctamente", "success");
        setTimeout(() => {
          window.location.href = "file:///C:/Users/Usuario/Desktop/sahlafix/front/auth/Login.html";
        }, 1200);

      } else if (res.status === 409) {
        showError(fields.email, "Este email ya está registrado.");
        showToast("El usuario ya existe.");

      } else if (res.status === 400) {
        // Mostrar mensaje de error profesional del backend
        if (data.error) {
          // Intentar detectar el campo específico
          if (data.error.includes('Número de teléfono inválido')) {
            showError(fields.phone, "Número de teléfono inválido. Usa formato +34XXXXXXXXX o +213XXXXXXXXX");
            showToast("Número de teléfono inválido.");
          } else {
            showToast(data.error);
          }
        } else {
          showToast("Datos inválidos. Revisa los campos.");
        }

      } else {
        console.error(data);
      }
    } catch (err) {
      console.error('Error al conectar con backend:', err);
      showToast("Error de conexión. Intenta nuevamente.");
    }
  });
})();