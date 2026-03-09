
const track  = document.getElementById('categorias');
const slides = document.querySelectorAll('.categorias');
const total  = slides.length;
let current  = 0;
const dots = document.querySelectorAll('.carousel-dot');

function updateDots(index) {
    dots.forEach((dot, i) => dot.classList.toggle('active', i === index));
}

dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
        current = i;
        track.style.transform = `translateX(-${current * 100}%)`;
        updateDots(current);
    });
});

setInterval(() => {
    current = (current + 1) % total;
    track.style.transform = `translateX(-${current * 100}%)`;
    updateDots(current);
}, 2500);

const images = document.querySelectorAll('#servicios-fotos img');

const imgObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, index * 300);
        }
    });
}, { threshold: 0.3 });

images.forEach(img => imgObserver.observe(img));

const stepsObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, index * 200);
        }
    });
}, { threshold: 0.3 });

steps.forEach(step => stepsObserver.observe(step));
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
const menuToggle = document.getElementById('menu-toggle');
const navLinks   = document.getElementById('nav-links');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        menuToggle.classList.toggle('open', isOpen);
        menuToggle.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('open');
            menuToggle.classList.remove('open');
            menuToggle.setAttribute('aria-expanded', false);
        });
    });
}