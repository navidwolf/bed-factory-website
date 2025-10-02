// Lightbox تصاویر محصولات
const lightbox = document.createElement('div');
lightbox.id = 'lightbox';
document.body.appendChild(lightbox);

const images = document.querySelectorAll('.product-card img');
images.forEach(img => {
    img.addEventListener('click', e => {
        lightbox.classList.add('active');
        const imgElement = document.createElement('img');
        imgElement.src = img.src;
        imgElement.alt = img.alt; // alt برای SEO
        while (lightbox.firstChild) lightbox.removeChild(lightbox.firstChild);
        lightbox.appendChild(imgElement);
    });
});

lightbox.addEventListener('click', e => {
    if (e.target !== e.currentTarget) return;
    lightbox.classList.remove('active');
});
