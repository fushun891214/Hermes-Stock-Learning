document.documentElement.classList.add('js-ready');

const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');

if (navToggle && siteNav) {
  navToggle.addEventListener('click', () => {
    const isOpen = siteNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  siteNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      siteNav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const navLinks = Array.from(document.querySelectorAll('.site-nav a'));
const normalizePath = (value) => value.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
const currentPath = normalizePath(window.location.pathname);
const currentHash = window.location.hash;
const isLessonPage = currentPath.includes('/lessons/day-');

navLinks.forEach((link) => link.classList.remove('is-current'));

if (currentHash) {
  const hashMatch = navLinks.find((link) => new URL(link.href, window.location.origin).hash === currentHash);
  if (hashMatch) {
    hashMatch.classList.add('is-current');
  }
} else if (isLessonPage) {
  const startLink = navLinks.find((link) => link.textContent.trim() === '開始學習');
  if (startLink) {
    startLink.classList.add('is-current');
  }
} else {
  const homeLink = navLinks.find((link) => normalizePath(new URL(link.href, window.location.origin).pathname) === currentPath && !new URL(link.href, window.location.origin).hash);
  if (homeLink) {
    homeLink.classList.add('is-current');
  }
}
