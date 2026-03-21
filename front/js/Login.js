const form = document.getElementById('login-form');
//Funcion para mostrar error o exsito de inicio de sesion personalizado 
function showToast(message, type = "error") {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    document.body.appendChild(toast);
  }

  //Personalizamos el mensaje de inicio de sesion incorrecto
  toast.textContent = message;
  toast.style.position = "fixed";
  toast.style.bottom = "30px";
  toast.style.left = "50%";
  toast.style.transform = "translateX(-50%)";
  toast.style.padding = "14px 22px";
  toast.style.borderRadius = "12px";
  toast.style.fontWeight = "600";
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
    toast.style.border = "1px solid rgba(16, 16, 16, 0.25)";
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
//Hacemos fetch al navegador para verficar el token y si todo correcto el usuario accede a la pagin correctamente
(async () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const res = await fetch('http://sahlafix.es/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const me = await res.json();
        localStorage.setItem('user_id', me.user.id);
        localStorage.setItem('email', me.user.email); // opcional, Ãºtil
        localStorage.setItem('role', me.user.role);   // opcional
        window.location.href = 'http://sahlafix.es/front/auth/Home.html';
        return;
      } else {
        localStorage.removeItem('token');
      }
    } catch (_) {
      localStorage.removeItem('token');
    }
  }
})();
//Funcion para hacer peticion al servidor y verficar el login
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  //Seleccionamos los inputs de correo y contraseÃ±a
  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  //Hacemos un fetch al backend
  const resp = await fetch('http://sahlafix.es/api/v1/auth/login',{
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({email,password})
  });

  //Si responde el backend con codigo de estado 200 entonces es correcto
  if(resp.ok){
      const data = await resp.json();
      const token = data.token;
      const userID = data.user.id;
      localStorage.setItem("user_id",userID)
      localStorage.setItem('token', token);
      // Validar inmediatamente con /me y redirigir
      const resMe = await fetch('http://sahlafix.es/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (resMe.ok) {
        showToast("Inicio de sesiÃ³n correcto", "success");
        setTimeout(() => {
          window.location.href = 'http://sahlafix.es
/front/auth/Home.html';
        }, 1000);
      } else {
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        showToast("Token invÃ¡lido. Inicia sesiÃ³n de nuevo.");
      }
  }else{
      showToast("Inicio de sesiÃ³n incorrecto. Verifica tus credenciales.");
  }
});