const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('.nav-links');
if (menuButton && menu) {
  menuButton.addEventListener('click', () => {
    const opened = menu.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(opened));
    menuButton.textContent = opened ? '✕' : '☰';
  });
}
