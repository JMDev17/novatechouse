document.addEventListener('DOMContentLoaded', () => {

 if (typeof lucide !== 'undefined') lucide.createIcons();

 gsap.registerPlugin(ScrollTrigger);

 // ── Hero animations ───────────────────────────────────────────────────────
 const heroTitle = document.querySelector('.hero-title');
 const heroDesc = document.querySelector('.hero-desc');
 const heroCtas = document.querySelector('.hero-ctas');
 const heroImgs = document.querySelectorAll('.hero-content');

 if (heroTitle) gsap.fromTo(heroTitle, { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', delay: 0.2 });
 if (heroDesc) gsap.fromTo(heroDesc, { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out', delay: 0.42 });
 if (heroCtas) gsap.fromTo(heroCtas, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out', delay: 0.62 });
 if (heroImgs.length > 1) gsap.fromTo(heroImgs[1], { opacity: 0, scale: 0.97 }, { opacity: 1, scale: 1, duration: 1.1, ease: 'power3.out', delay: 0.28 });

 // ── Scroll reveals ────────────────────────────────────────────────────────
 gsap.utils.toArray('.gs-reveal').forEach(el => {
 gsap.fromTo(el, { opacity: 0, y: 44 }, {
 opacity: 1, y: 0, duration: 0.85, ease: 'power3.out',
 scrollTrigger: { trigger: el, start: 'top 87%', toggleActions: 'play none none none' }
 });
 });

 gsap.utils.toArray('.gs-reveal-card').forEach((el, i) => {
 gsap.fromTo(el, { opacity: 0, y: 36 }, {
 opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: i * 0.1,
 scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' }
 });
 });

 // ── Navbar scroll style ───────────────────────────────────────────────────
 const navbar = document.getElementById('navbar');
 if (navbar) {
 ScrollTrigger.create({
 start: 72,
 onEnter: () => navbar.classList.add('navbar-scrolled'),
 onLeaveBack: () => navbar.classList.remove('navbar-scrolled')
 });
 }

 // ── Services carousel (transform-based, 5 cards exact) ───────────────────
 initServicesCarousel();
  initReviewsCarousel();

 // ── Catalog carousel (drag + buttons) ────────────────────────────────────
 setupDragScroll('#catalog-carousel');
 setupCarouselButtons('catalog-prev', 'catalog-next', 'catalog-carousel', 230);

 // ── Magnetic buttons ─────────────────────────────────────────────────────
 document.querySelectorAll('.magnetic-btn').forEach(btn => {
 let rect = null;
 btn.addEventListener('mouseenter', () => { rect = btn.getBoundingClientRect(); });
 btn.addEventListener('mousemove', e => {
 if (!rect) return;
 gsap.to(btn, { x: (e.clientX - rect.left - rect.width / 2) * 0.14, y: (e.clientY - rect.top - rect.height / 2) * 0.14, duration: 0.4, ease: 'power2.out' });
 });
 btn.addEventListener('mouseleave', () => {
 rect = null;
 gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
 });
 });

});

// ── Services carousel: transform-based, responsive visible count ──────────────
function initServicesCarousel() {
 const track = document.getElementById('services-track');
 const outer = document.getElementById('services-outer');
 if (!track || !outer) return;

 const cards = Array.from(track.querySelectorAll('.services-card'));
 const GAP = 12;
 let current = 0;

 function getVisible() {
 const w = window.innerWidth;
 if (w >= 1024) return 5;
 if (w >= 768) return 3;
 if (w >= 480) return 2;
 return 1;
 }

 function outerInnerWidth() {
 const s = window.getComputedStyle(outer);
 return outer.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight);
 }

 function cardWidth() {
 const vis = getVisible();
 return (outerInnerWidth() - GAP * (vis - 1)) / vis;
 }

 function applyWidths() {
 const w = cardWidth();
 cards.forEach(c => { c.style.width = w + 'px'; });
 }

 function slideTo(index) {
 const max = Math.max(0, cards.length - getVisible());
 current = Math.max(0, Math.min(index, max));
 const offset = current * (cardWidth() + GAP);
 track.style.transform = `translateX(-${offset}px)`;
 syncButtons();
 }

 function syncButtons() {
 const prev = document.getElementById('services-prev');
 const next = document.getElementById('services-next');
 const max = Math.max(0, cards.length - getVisible());
 if (prev) prev.disabled = current <= 0;
 if (next) next.disabled = current >= max;
 }

 applyWidths();
 slideTo(0);

 const ro = new ResizeObserver(() => { applyWidths(); slideTo(current); });
 ro.observe(outer);

 document.getElementById('services-prev')?.addEventListener('click', () => slideTo(current - 1));
 document.getElementById('services-next')?.addEventListener('click', () => slideTo(current + 1));

 let tx = 0;
 track.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
 track.addEventListener('touchend', e => {
 const dx = tx - e.changedTouches[0].clientX;
 if (Math.abs(dx) > 40) slideTo(current + (dx > 0 ? 1 : -1));
 }, { passive: true });
}

// ── iPhones carousel: scroll-based with buttons ───────────────────────────────
function setupCarouselButtons(prevId, nextId, carouselId, scrollAmount) {
 const prev = document.getElementById(prevId);
 const next = document.getElementById(nextId);
 const carousel = document.getElementById(carouselId);
 if (!carousel || !prev || !next) return;

 next.addEventListener('click', () => carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' }));
 prev.addEventListener('click', () => carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' }));

 const update = () => {
 prev.disabled = carousel.scrollLeft <= 0;
 next.disabled = carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 2;
 };
 carousel.addEventListener('scroll', update, { passive: true });
 update();
}

// ── Drag-to-scroll (for iPhones carousel only) ────────────────────────────────
function setupDragScroll(selector) {
 const el = document.querySelector(selector);
 if (!el) return;

 let isDown = false, startX, scrollLeft, hasDragged = false;

 el.addEventListener('mousedown', e => {
 isDown = true; hasDragged = false;
 startX = e.pageX - el.offsetLeft;
 scrollLeft = el.scrollLeft;
 el.style.cursor = 'grabbing';
 });
 el.addEventListener('mouseleave', () => { isDown = false; el.style.cursor = 'grab'; });
 el.addEventListener('mouseup', () => { isDown = false; el.style.cursor = 'grab'; });
 el.addEventListener('mousemove', e => {
 if (!isDown) return;
 e.preventDefault();
 const walk = (e.pageX - el.offsetLeft - startX) * 1.3;
 if (Math.abs(walk) > 4) hasDragged = true;
 el.scrollLeft = scrollLeft - walk;
 });
 el.addEventListener('click', e => { if (hasDragged) e.preventDefault(); }, true);
}


// ── Reviews carousel: transform-based, responsive visible count ──────────────
function initReviewsCarousel() {
  const track = document.getElementById('rev-track');
  const outer = document.getElementById('rev-outer');
  if (!track || !outer) return;

  const cards = Array.from(track.querySelectorAll('.review-card'));
  const GAP = 20;
  let current = 0;

  function getVisible() {
    const w = window.innerWidth;
    if (w >= 1024) return 3;
    if (w >= 640) return 2;
    return 1;
  }

  function cardWidth() {
    const vis = getVisible();
    return (outer.clientWidth - GAP * (vis - 1)) / vis;
  }

  function applyWidths() {
    const w = cardWidth();
    cards.forEach(c => { c.style.width = w + 'px'; });
  }

  function slideTo(index) {
    const max = Math.max(0, cards.length - getVisible());
    current = Math.max(0, Math.min(index, max));
    const offset = current * (cardWidth() + GAP);
    track.style.transform = `translateX(-${offset}px)`;
    syncButtons();
  }

  function syncButtons() {
    const prev = document.getElementById('rev-prev');
    const next = document.getElementById('rev-next');
    const max = Math.max(0, cards.length - getVisible());
    if (prev) prev.disabled = current <= 0;
    if (next) next.disabled = current >= max;
  }

  applyWidths();
  slideTo(0);

  const ro = new ResizeObserver(() => { applyWidths(); slideTo(current); });
  ro.observe(outer);

  document.getElementById('rev-prev')?.addEventListener('click', () => slideTo(current - 1));
  document.getElementById('rev-next')?.addEventListener('click', () => slideTo(current + 1));

  let tx = 0;
  track.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend', e => {
    const dx = tx - e.changedTouches[0].clientX;
    if (Math.abs(dx) > 40) slideTo(current + (dx > 0 ? 1 : -1));
  }, { passive: true });
}
