//Carrusel automatico,seleccionamos las etiquetas necesarias
const track = document.getElementById('categorias');
const slides = document.querySelectorAll('.categorias');
const total = slides.length;
//Variable contador de el indice actual de la imagen
let current = 0;

//Funcion para cada 2,5 segundos sume indice para mover y hacer un translate a cada imagen
setInterval(() => {
    current = (current + 1) % total;
    track.style.transform = `translateX(-${current * 100}%)`;
}, 2500);

//Animacion suave con js para contenedro de servicios
const images = document.querySelectorAll("#servicios-fotos img");

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if(entry.isIntersecting){
            setTimeout(() => {
                entry.target.classList.add("visible");
            }, index * 300); // aparecen una tras otra
        }
    });
}, {
    threshold: 0.3
});

images.forEach(img => observer.observe(img));
const steps = document.querySelectorAll(".step");

const stepsObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add("visible");
      }, index * 200);
    }
  });
}, {
  threshold: 0.3
});

steps.forEach(step => stepsObserver.observe(step));
