/**
 * CV & Portfölj - Interaktiv funktionalitet
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initProjectFilters();
  initCopyButtons();
  initPrintButtons();
  initScrollAnimations();
  initCurrentYear();
  initVisitorStats();
});

/**
 * Hantera tema (Ljust / Mörkt läge)
 */
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  // Ljust läge är alltid standard för alla besökare om man inte aktivt växlat
  const savedTheme = localStorage.getItem('theme');
  const initialTheme = savedTheme === 'dark' ? 'dark' : 'light';

  html.setAttribute('data-theme', initialTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      
      showToast(`Bytte till ${newTheme === 'dark' ? 'mörkt' : 'ljust'} läge`);
    });
  }
}

/**
 * Hantera mobilmeny och aktiv länk vid skrollning
 */
function initNavigation() {
  const menuToggle = document.getElementById('menu-toggle');
  const mainNav = document.getElementById('main-nav');
  const navLinks = document.querySelectorAll('.nav-link');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mainNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', isOpen.toString());
    });

    // Stäng menyn vid klick på nav-länk
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (mainNav.classList.contains('open')) {
          mainNav.classList.remove('open');
          menuToggle.setAttribute('aria-expanded', 'false');
        }
      });
    });

    // Stäng menyn om man klickar utanför
    document.addEventListener('click', (e) => {
      if (!mainNav.contains(e.target) && !menuToggle.contains(e.target) && mainNav.classList.contains('open')) {
        mainNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Markera aktiv länk med IntersectionObserver
  const sections = document.querySelectorAll('section[id]');
  if ('IntersectionObserver' in window && sections.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }, {
      rootMargin: '-20% 0px -70% 0px'
    });

    sections.forEach(section => observer.observe(section));
  }
}

/**
 * Filtrera portföljprojekt efter kategori
 */
function initProjectFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  if (filterBtns.length === 0 || projectCards.length === 0) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Uppdatera aktiv knapp
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          card.style.animation = 'fadeIn 0.3s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/**
 * Snabbkopiera e-postadress med klick & visa toast
 */
function initCopyButtons() {
  const copyBtns = document.querySelectorAll('.copy-email-btn');

  copyBtns.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const email = btn.getAttribute('data-email') || 'maxandersen041023@gmail.com';
      
      try {
        await navigator.clipboard.writeText(email);
        showToast('E-postadressen kopierades till urklipp! 📋');
      } catch (err) {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = email;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('E-postadressen kopierades till urklipp! 📋');
      }
    });
  });
}

/**
 * Skriv ut / Spara som PDF
 */
function initPrintButtons() {
  const printBtn = document.getElementById('print-btn');
  const heroDownloadBtn = document.getElementById('hero-download-btn');

  const triggerPrint = () => {
    window.print();
  };

  if (printBtn) printBtn.addEventListener('click', triggerPrint);
  if (heroDownloadBtn) heroDownloadBtn.addEventListener('click', triggerPrint);
}

/**
 * Mjuka intoningseffekter vid skrollning (valfritt)
 */
function initScrollAnimations() {
  if (!('IntersectionObserver' in window)) return;

  const elementsToAnimate = document.querySelectorAll('.edu-entry, .exp-card, .project-item, .skills-group, .trait-box, .contact-card');
  if (!elementsToAnimate.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.05
  });

  elementsToAnimate.forEach(el => observer.observe(el));
}

/**
 * Automatiskt aktuellt år i footer
 */
function initCurrentYear() {
  const yearSpan = document.getElementById('current-year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
}

/**
 * Toast-meddelande
 */
let toastTimeout;
function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;

  clearTimeout(toastTimeout);
  toast.textContent = message;
  toast.removeAttribute('hidden');
  toast.classList.add('show');

  toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      toast.setAttribute('hidden', '');
    }, 400);
  }, 2800);
}

/**
 * Besöksstatistik & Sidvisningsmätare
 */
async function initVisitorStats() {
  const countEl = document.getElementById('visitor-count');
  const pillEl = document.getElementById('visitor-pill');
  if (!countEl) return;

  // 1. Lokal session-räknare som fallback
  let localViews = parseInt(localStorage.getItem('ma_cv_views') || '14', 10) + 1;
  localStorage.setItem('ma_cv_views', localViews.toString());

  // 2. Försök anropa offentlig gratis Counter API (fungerar när sidan är online)
  let displayCount = localViews;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2500);

    const res = await fetch('https://api.counterapi.dev/v1/max-andersen-frisk-cv/views/up', {
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      if (data && typeof data.count === 'number') {
        displayCount = data.count;
      }
    }
  } catch (err) {
    // Vid offline eller CORS-blockering lokalt används lokal session
    displayCount = localViews;
  }

  // Formatera snyggt med tusentalsavgränsare
  countEl.textContent = Number(displayCount).toLocaleString('sv-SE');

  // Logga besöksmetrik för utvecklaren i konsolen
  const visitInfo = {
    tidpunkt: new Date().toLocaleString('sv-SE'),
    skärm: `${window.innerWidth}x${window.innerHeight}`,
    enhet: /Mobi|Android|iPhone/i.test(navigator.userAgent) ? 'Mobil' : 'Dator',
    källa: document.referrer ? document.referrer : 'Direktbesök / Bokmärke'
  };

  console.log(
    '%c📊 Besöksanalys aktiv: Max Andersen Frisk CV',
    'color: #0284c7; font-weight: bold; font-size: 13px;'
  );
  console.log('Besökardetaljer:', visitInfo);

  if (pillEl) {
    pillEl.style.cursor = 'pointer';
    pillEl.addEventListener('click', () => {
      showToast(`📊 Totalt ${countEl.textContent} visningar registrerade.`);
    });
  }
}
