// ============================================================
// SpacePoint Landing Page — script.js
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  
  /* ── Custom Star Cursor ─────────────────────────────────── */
  const cursor = document.getElementById('customCursor');
  document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';

    // Add sparkle trail
    for (let i = 0; i < 2; i++) {
      cursorSparkles.push({
        x: e.clientX,
        y: e.clientY,
        r: Math.random() * 1.5 + 0.5,
        alpha: 1,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        life: 1.0,
        decay: Math.random() * 0.03 + 0.02
      });
    }
  });

  document.addEventListener('mouseover', e => {
    if (e.target.closest('a, button, [role="button"], input, select, textarea')) {
      document.body.classList.add('cursor-hover');
    }
  });

  document.addEventListener('mouseout', e => {
    if (e.target.closest('a, button, [role="button"], input, select, textarea')) {
      document.body.classList.remove('cursor-hover');
    }
  });

  /* ── Stars ──────────────────────────────────────────────── */
  const canvas = document.getElementById('starCanvas');
  const ctx = canvas.getContext('2d');
  let W, H, stars = [], shooters = [], cursorSparkles = [];

  function resizeCanvas() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function makeStar() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.4 + 0.3,
      alpha: Math.random(),
      delta: (Math.random() * 0.005 + 0.002) * (Math.random() < .5 ? 1 : -1),
    };
  }

  function initStars(n = 220) {
    stars = Array.from({ length: n }, makeStar);
  }

  function makeShooter() {
    const angle = Math.PI / 6;
    const speed = Math.random() * 6 + 4;
    return {
      x: Math.random() * W * 0.7,
      y: Math.random() * H * 0.4,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      len: Math.random() * 120 + 60,
      alpha: 1,
      active: true,
    };
  }

  function drawStars() {
    ctx.clearRect(0, 0, W, H);
    stars.forEach(s => {
      s.alpha += s.delta;
      if (s.alpha >= 1 || s.alpha <= 0) s.delta *= -1;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${s.alpha})`;
      ctx.fill();
    });

    shooters = shooters.filter(sh => sh.active);
    shooters.forEach(sh => {
      ctx.beginPath();
      const grad = ctx.createLinearGradient(sh.x, sh.y, sh.x - sh.vx * 10, sh.y - sh.vy * 10);
      grad.addColorStop(0, `rgba(167,125,255,${sh.alpha})`);
      grad.addColorStop(1, 'rgba(167,125,255,0)');
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.5;
      ctx.moveTo(sh.x, sh.y);
      ctx.lineTo(sh.x - sh.vx * (sh.len / 10), sh.y - sh.vy * (sh.len / 10));
      ctx.stroke();
      sh.x += sh.vx;
      sh.y += sh.vy;
      sh.alpha -= 0.018;
      if (sh.alpha <= 0 || sh.x > W || sh.y > H) sh.active = false;
    });

    // Draw cursor sparkles
    cursorSparkles = cursorSparkles.filter(s => s.life > 0);
    cursorSparkles.forEach(s => {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r * s.life, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${s.life})`;
      ctx.shadowBlur = 4 * s.life;
      ctx.shadowColor = 'white';
      ctx.fill();
      ctx.shadowBlur = 0; // reset for other elements
      s.x += s.vx;
      s.y += s.vy;
      s.life -= s.decay;
    });

    requestAnimationFrame(drawStars);
  }

  // Fire a shooting star occasionally
  function scheduleShooter() {
    const delay = Math.random() * 5000 + 3000;
    setTimeout(() => {
      shooters.push(makeShooter());
      scheduleShooter();
    }, delay);
  }

  resizeCanvas();
  initStars();
  drawStars();
  scheduleShooter();
  window.addEventListener('resize', () => { resizeCanvas(); initStars(); });


  /* ── CubeSat mouse-follow ───────────────────────────────── */
  const cubesat = document.getElementById('cubesat');
  if (cubesat) {
    let targetX = 0, targetY = 0, currentX = 0, currentY = 0;
    document.addEventListener('mousemove', e => {
      const cx = window.innerWidth  / 2;
      const cy = window.innerHeight / 2;
      targetX = (e.clientX - cx) / cx * 18;
      targetY = (e.clientY - cy) / cy * 12;
    });
    (function animateCube() {
      currentX += (targetX - currentX) * 0.06;
      currentY += (targetY - currentY) * 0.06;
      cubesat.style.transform = `translate(${currentX}px, ${currentY}px)`;
      requestAnimationFrame(animateCube);
    })();
  }


  /* ── Navbar scroll glass ─────────────────────────────────── */
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('nav-scrolled');
    } else {
      navbar.classList.remove('nav-scrolled');
    }
  });


  /* ── Mobile menu ─────────────────────────────────────────── */
  const menuBtn  = document.getElementById('mobileMenuBtn');
  const closeBtn = document.getElementById('mobileMenuClose');
  const mobileMenu = document.getElementById('mobileMenu');

  menuBtn?.addEventListener('click', () => {
    mobileMenu.classList.remove('translate-x-full');
    mobileMenu.classList.add('translate-x-0');
    document.body.style.overflow = 'hidden';
  });
  closeBtn?.addEventListener('click', closeMobileMenu);
  function closeMobileMenu() {
    mobileMenu.classList.add('translate-x-full');
    mobileMenu.classList.remove('translate-x-0');
    document.body.style.overflow = '';
  }

  // Close mobile menu on link click
  mobileMenu?.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', closeMobileMenu);
  });


  /* ── Discover dropdown ───────────────────────────────────── */
  const discoverBtn  = document.getElementById('discoverBtn');
  const discoverMenu = document.getElementById('discoverMenu');
  let dropOpen = false;

  discoverBtn?.addEventListener('click', e => {
    e.stopPropagation();
    dropOpen = !dropOpen;
    discoverMenu.classList.toggle('opacity-0', !dropOpen);
    discoverMenu.classList.toggle('pointer-events-none', !dropOpen);
    discoverMenu.classList.toggle('translate-y-2', !dropOpen);
  });

  document.addEventListener('click', () => {
    if (dropOpen) {
      dropOpen = false;
      discoverMenu.classList.add('opacity-0', 'pointer-events-none', 'translate-y-2');
    }
  });


  /* ── Mobile accordion for Discover ──────────────────────── */
  const mobileDiscoverBtn  = document.getElementById('mobileDiscoverBtn');
  const mobileDiscoverList = document.getElementById('mobileDiscoverList');
  const mobileDiscoverIcon = document.getElementById('mobileDiscoverIcon');

  mobileDiscoverBtn?.addEventListener('click', () => {
    const open = !mobileDiscoverList.classList.contains('hidden');
    mobileDiscoverList.classList.toggle('hidden', open);
    mobileDiscoverIcon.style.transform = open ? 'rotate(0deg)' : 'rotate(180deg)';
  });


  /* ── Smooth scroll for CTA ───────────────────────────────── */
  document.querySelectorAll('[data-scroll]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(el.dataset.scroll);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });


  /* ── Intersection observer fade-in ──────────────────────── */
  const fadeEls = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  fadeEls.forEach(el => observer.observe(el));

  /* ── Number Counter Animation ───────────────────────────── */
  const counters = document.querySelectorAll('.counter');
  let animationStarted = false;

  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animationStarted) {
        animationStarted = true;
        const duration = 2500; // 2.5 seconds
        const startTime = performance.now();
        
        function updateCounters(currentTime) {
          const elapsedTime = currentTime - startTime;
          const progress = Math.min(elapsedTime / duration, 1);
          
          // Easing function (easeOutQuart) for smooth deceleration
          const easeProgress = 1 - Math.pow(1 - progress, 4);

          counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const current = Math.floor(easeProgress * target);
            counter.innerText = current;
          });

          if (progress < 1) {
            requestAnimationFrame(updateCounters);
          } else {
            counters.forEach(counter => {
              counter.innerText = counter.getAttribute('data-target');
            });
          }
        }
        
        requestAnimationFrame(updateCounters);
      }
    });
  }, { threshold: 0.5 });

  const impactSection = document.getElementById('impact');
  if (impactSection) {
    counterObserver.observe(impactSection);
  }

  /* ── Floating Rocket Navigation ─────────────────────────── */
  const rocketNav = document.getElementById('rocketNav');
  const rocketFlame = document.getElementById('rocketFlame');
  let isLaunching = false;

  window.addEventListener('scroll', () => {
    // Show rocket after scrolling past the hero section (~600px)
    if (window.scrollY > 600 && !isLaunching) {
      rocketNav.classList.add('rocket-visible');
      if (typeof Intercom === 'function') {
        Intercom('update', { "hide_default_launcher": false });
      }
    } else {
      rocketNav.classList.remove('rocket-visible');
      if (typeof Intercom === 'function') {
        Intercom('update', { "hide_default_launcher": true });
      }
    }
  });

  rocketNav?.addEventListener('click', () => {
    if (isLaunching) return;
    
    isLaunching = true;
    
    // Add launching animation class
    rocketNav.classList.add('launching');
    
    // Force flame to be fully visible during launch
    rocketFlame.classList.remove('opacity-0', 'group-hover:opacity-100');
    rocketFlame.classList.add('opacity-100');

    // Smooth scroll to top
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });

    // Reset after animation completes (1.8s)
    setTimeout(() => {
      isLaunching = false;
      rocketNav.classList.remove('launching', 'rocket-visible');
      
      // Reset flame visibility classes
      rocketFlame.classList.add('opacity-0', 'group-hover:opacity-100');
      rocketFlame.classList.remove('opacity-100');
    }, 1800);
  });

  /* ── Newsletter Popup ───────────────────────────────────── */
  const newsletterPopup = document.getElementById('newsletterPopup');
  const newsletterClose = document.getElementById('newsletterClose');
  const newsletterOverlay = document.getElementById('newsletterOverlay');
  const gallerySection = document.getElementById('gallery');
  let popupShown = false;

  if (gallerySection && newsletterPopup) {
    const popupObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !popupShown) {
          popupShown = true; // ensure it only pops up once
          // Slight delay so they can see the gallery moving before the popup appears
          setTimeout(() => {
            newsletterPopup.classList.add('popup-visible');
            document.body.style.overflow = 'hidden'; // freeze background scrolling
          }, 1200);
        }
      });
    }, { threshold: 0.3 }); // trigger when 30% of gallery is on screen

    popupObserver.observe(gallerySection);
  }

  function closeNewsletterPopup() {
    newsletterPopup.classList.remove('popup-visible');
    document.body.style.overflow = '';
  }

  newsletterClose?.addEventListener('click', closeNewsletterPopup);
  newsletterOverlay?.addEventListener('click', closeNewsletterPopup);

});
