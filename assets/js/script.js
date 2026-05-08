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
  let popupShown = sessionStorage.getItem('newsletterShown') === 'true';

  if (gallerySection && newsletterPopup) {
    const popupObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !popupShown) {
          popupShown = true; // ensure it only pops up once
          sessionStorage.setItem('newsletterShown', 'true');
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

  /* ── Video Popup ────────────────────────────────────────── */
  const watchBtn = document.getElementById('watchJourneyBtn');
  const videoPopup = document.getElementById('videoPopup');
  const videoOverlay = document.getElementById('videoOverlay');
  const videoCloseBtn = document.getElementById('videoCloseBtn');
  const youtubePlayer = document.getElementById('youtubePlayer');
  const videoUrl = "https://www.youtube-nocookie.com/embed/51-gNYZkTYQ?autoplay=1";

  function openVideo() {
    if (!youtubePlayer) return;
    youtubePlayer.src = videoUrl;
    videoPopup.classList.remove('pointer-events-none', 'opacity-0');
    videoPopup.classList.add('opacity-100');
    document.getElementById('videoModalContent').classList.remove('scale-95');
    document.getElementById('videoModalContent').classList.add('scale-100');
    document.body.style.overflow = 'hidden';
  }

  function closeVideo() {
    if (!videoPopup) return;
    videoPopup.classList.add('pointer-events-none', 'opacity-0');
    videoPopup.classList.remove('opacity-100');
    document.getElementById('videoModalContent').classList.add('scale-95');
    document.getElementById('videoModalContent').classList.remove('scale-100');
    document.body.style.overflow = '';
    // Stop video playback
    setTimeout(() => {
      if (youtubePlayer) youtubePlayer.src = "";
    }, 500);
  }

  watchBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    openVideo();
  });
  videoOverlay?.addEventListener('click', closeVideo);
  videoCloseBtn?.addEventListener('click', closeVideo);

  /* ── Product Modal ─────────────────────────────────────── */
  const productCards = document.querySelectorAll('.product-card');
  const productPopup = document.getElementById('productPopup');
  const productOverlay = document.getElementById('productOverlay');
  const productModalContent = document.getElementById('productModalContent');
  const productCloseBtn = document.getElementById('productCloseBtn');
  
  const popupProductImage = document.getElementById('popupProductImage');
  const popupProductTitle = document.getElementById('popupProductTitle');
  const popupProductDesc = document.getElementById('popupProductDesc');
  const popupProductInput = document.getElementById('popupProductInput');
  const productWaitlistForm = document.getElementById('productWaitlistForm');

  const openProductModal = (card) => {
    if (!productPopup) return;
    
    // Set data
    const title = card.getAttribute('data-title');
    const desc = card.getAttribute('data-desc');
    const mainImage = card.getAttribute('data-image');
    const imagesStr = card.getAttribute('data-images');
    const images = imagesStr ? imagesStr.split(',') : (mainImage ? [mainImage] : []);
    
    popupProductTitle.textContent = title;
    popupProductDesc.textContent = desc;
    popupProductInput.value = title;
    
    // Set main image
    if (mainImage) {
      popupProductImage.src = mainImage;
      popupProductImage.style.display = 'block';
    } else {
      popupProductImage.style.display = 'none';
    }

    // Handle thumbnails
    const thumbsContainer = document.getElementById('popupProductThumbs');
    if (thumbsContainer) {
      thumbsContainer.innerHTML = '';
      if (images.length > 1) {
        images.forEach((imgSrc, index) => {
          const thumb = document.createElement('div');
          thumb.className = `w-12 h-12 rounded-lg overflow-hidden border-2 cursor-pointer transition-all ${index === 0 ? 'border-space-accent' : 'border-transparent opacity-60 hover:opacity-100'}`;
          thumb.innerHTML = `<img src="${imgSrc}" class="w-full h-full object-contain p-1" alt="Thumbnail ${index + 1}">`;
          
          thumb.addEventListener('click', () => {
            popupProductImage.src = imgSrc;
            // Update active state
            thumbsContainer.querySelectorAll('div').forEach(t => {
              t.classList.remove('border-space-accent');
              t.classList.add('border-transparent', 'opacity-60');
            });
            thumb.classList.add('border-space-accent');
            thumb.classList.remove('border-transparent', 'opacity-60');
          });
          
          thumbsContainer.appendChild(thumb);
        });
        thumbsContainer.style.display = 'flex';
      } else {
        thumbsContainer.style.display = 'none';
      }
    }
    
    // Reset form UI if previously submitted
    if (productWaitlistForm) {
      const btn = productWaitlistForm.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = 'Register';
        btn.className = 'btn-primary w-full text-white font-semibold px-4 py-3 rounded-xl text-sm flex items-center justify-center gap-2 mt-1';
      }
      productWaitlistForm.reset();
    }

    // Show modal
    productPopup.classList.remove('pointer-events-none');
    productPopup.classList.remove('opacity-0');
    setTimeout(() => {
      productModalContent.classList.remove('scale-95', 'translate-y-8');
    }, 50);
  };

  const closeProductModal = () => {
    if (!productPopup) return;
    productModalContent.classList.add('scale-95', 'translate-y-8');
    setTimeout(() => {
      productPopup.classList.add('opacity-0');
      productPopup.classList.add('pointer-events-none');
    }, 300);
  };

  productCards.forEach(card => {
    card.addEventListener('click', () => openProductModal(card));
  });

  productOverlay?.addEventListener('click', closeProductModal);
  productCloseBtn?.addEventListener('click', closeProductModal);

  /* ── Google Form Submission Handling ────────────────────── */
  const handleFormSubmit = async (formId) => {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;
      
      // Update UI to show loading
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Processing...
      `;

      try {
        const formData = new FormData(form);
        if (form.action && !form.action.endsWith('#')) {
          await fetch(form.action, {
            method: 'POST',
            body: formData,
            mode: 'no-cors'
          });
        } else {
          // Simulate network request for placeholder forms
          await new Promise(resolve => setTimeout(resolve, 1000));
        }

        // Customize success message
        let successMessage = "Welcome Explorer!";
        if (formId === 'productWaitlistForm') {
          successMessage = "You're on the list!";
        }

        // Show Success UI
        submitBtn.innerHTML = `
          <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          ${successMessage}
        `;
        submitBtn.classList.remove('btn-primary');
        submitBtn.classList.add('bg-green-500/20', 'border', 'border-green-500/50', 'text-green-400');

        // Reset form
        form.reset();

        // Specific actions for popups
        if (formId === 'newsletterForm') {
          setTimeout(() => {
            closeNewsletterPopup();
          }, 2000);
        } else if (formId === 'productWaitlistForm') {
          setTimeout(() => {
            closeProductModal();
          }, 2000);
        }

      } catch (error) {
        console.error('Submission error:', error);
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
        alert('There was an error submitting the form. Please try again.');
      }
    });
  };

  handleFormSubmit('productWaitlistForm');
  
  /* ── Legal Modals (Terms & Privacy) ─────────────────────── */
  const termsModal = document.getElementById('termsModal');
  const privacyModal = document.getElementById('privacyModal');
  const footerTerms = document.getElementById('footerTerms');
  const footerPrivacy = document.getElementById('footerPrivacy');
  
  function openModal(modal) {
    if (!modal) return;
    modal.classList.remove('pointer-events-none');
    modal.classList.add('opacity-100');
    const content = modal.querySelector('.glass');
    if (content) {
      content.classList.remove('scale-95', 'translate-y-8');
      content.classList.add('scale-100', 'translate-y-0');
    }
    document.body.style.overflow = 'hidden';
  }

  function closeModal(modal) {
    if (!modal) return;
    const content = modal.querySelector('.glass');
    if (content) {
      content.classList.add('scale-95', 'translate-y-8');
      content.classList.remove('scale-100', 'translate-y-0');
    }
    setTimeout(() => {
      modal.classList.remove('opacity-100');
      modal.classList.add('pointer-events-none');
      document.body.style.overflow = '';
    }, 300);
  }

  // Terms Triggers
  footerTerms?.addEventListener('click', () => openModal(termsModal));
  document.getElementById('termsClose')?.addEventListener('click', () => closeModal(termsModal));
  document.getElementById('termsAccept')?.addEventListener('click', () => closeModal(termsModal));
  document.getElementById('termsOverlay')?.addEventListener('click', () => closeModal(termsModal));

  // Privacy Triggers
  footerPrivacy?.addEventListener('click', () => openModal(privacyModal));
  document.getElementById('privacyClose')?.addEventListener('click', () => closeModal(privacyModal));
  document.getElementById('privacyAccept')?.addEventListener('click', () => closeModal(privacyModal));
  document.getElementById('privacyOverlay')?.addEventListener('click', () => closeModal(privacyModal));

});
