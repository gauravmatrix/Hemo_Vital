/**
 * HemoVital - Home Page JavaScript
 * Handles animations, counter, and interactive elements
 */

(function() {
    'use strict';

    // ==========================================
    // Counter Animation
    // ==========================================
    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16); // 60 FPS
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = formatNumber(target);
                clearInterval(timer);
            } else {
                element.textContent = formatNumber(Math.floor(current));
            }
        }, 16);
    }

    function formatNumber(num) {
        if (num >= 1000) {
            return (num / 1000).toFixed(1).replace('.0', '') + 'K+';
        }
        return num.toString() + '+';
    }

    function initCounters() {
        const counters = document.querySelectorAll('.stat-number, .stat-value');
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    const target = parseInt(entry.target.getAttribute('data-target'));
                    animateCounter(entry.target, target);
                    entry.target.classList.add('counted');
                }
            });
        }, observerOptions);

        counters.forEach(counter => observer.observe(counter));
    }

    // ==========================================
    // Scroll Reveal Animations
    // ==========================================
    function initScrollReveal() {
        const revealElements = document.querySelectorAll(
            '.fade-in-up, .fade-in-down, .slide-in-left, .slide-in-right, .zoom-in'
        );

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    entry.target.classList.add('revealed');
                }
            });
        }, observerOptions);

        revealElements.forEach(element => {
            element.style.opacity = '0';
            element.style.animationPlayState = 'paused';
            observer.observe(element);
        });
    }

    // ==========================================
    // Feature Cards Hover Effect
    // ==========================================
    function initFeatureCards() {
        const featureCards = document.querySelectorAll('.feature-card');
        
        featureCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.setProperty('--hover-scale', '1.05');
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.setProperty('--hover-scale', '1');
            });
        });
    }

    // ==========================================
    // Role Cards Animation
    // ==========================================
    function initRoleCards() {
        const roleCards = document.querySelectorAll('.role-card');
        
        roleCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.2}s`;
        });
    }

    // ==========================================
    // Smooth Scroll Enhancement
    // ==========================================
    function enhanceSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                if (href === '#' || href === '#!') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // ==========================================
    // Hero Background Animation
    // ==========================================
    function animateHeroBackground() {
        const shapes = document.querySelectorAll('.shape');
        
        shapes.forEach((shape, index) => {
            shape.style.animationDelay = `${index * 0.5}s`;
        });
    }

    // ==========================================
    // Floating Cards Animation
    // ==========================================
    function initFloatingCards() {
        const floatingCards = document.querySelectorAll('.floating-card');
        
        floatingCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.5}s`;
            
            // Add subtle parallax effect on mouse move
            document.addEventListener('mousemove', (e) => {
                const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
                const moveY = (e.clientY - window.innerHeight / 2) * 0.01;
                
                card.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        });
    }

    // ==========================================
    // CTA Section Animation
    // ==========================================
    function initCTAAnimation() {
        const ctaIcon = document.querySelector('.cta-icon');
        
        if (ctaIcon) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        ctaIcon.style.animation = 'pulse 2s ease-in-out infinite';
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(ctaIcon);
        }
    }

    // ==========================================
    // Stats Section Background Animation
    // ==========================================
    function animateStatsBackground() {
        const statsSection = document.querySelector('.statistics');
        
        if (statsSection) {
            let scrollPosition = 0;
            
            window.addEventListener('scroll', () => {
                scrollPosition = window.pageYOffset;
                const sectionTop = statsSection.offsetTop;
                const sectionHeight = statsSection.offsetHeight;
                
                if (scrollPosition > sectionTop - window.innerHeight && 
                    scrollPosition < sectionTop + sectionHeight) {
                    const offset = (scrollPosition - sectionTop) * 0.5;
                    statsSection.style.backgroundPosition = `center ${offset}px`;
                }
            });
        }
    }

    // ==========================================
    // Button Ripple Effect
    // ==========================================
    function addButtonRippleEffect() {
        const buttons = document.querySelectorAll('.btn, .role-btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // Add ripple CSS dynamically
    function addRippleStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .btn, .role-btn {
                position: relative;
                overflow: hidden;
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
            }
            
            @keyframes rippleEffect {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // ==========================================
    // Lazy Load Images
    // ==========================================
    function lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        }, { rootMargin: '50px' });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // ==========================================
    // Typed Text Effect (Optional)
    // ==========================================
    function initTypedEffect() {
        const typedElement = document.querySelector('.typed-text');
        
        if (typedElement) {
            const texts = typedElement.dataset.texts.split(',');
            let textIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            
            function type() {
                const currentText = texts[textIndex];
                
                if (isDeleting) {
                    typedElement.textContent = currentText.substring(0, charIndex - 1);
                    charIndex--;
                } else {
                    typedElement.textContent = currentText.substring(0, charIndex + 1);
                    charIndex++;
                }
                
                let typeSpeed = isDeleting ? 50 : 100;
                
                if (!isDeleting && charIndex === currentText.length) {
                    typeSpeed = 2000;
                    isDeleting = true;
                } else if (isDeleting && charIndex === 0) {
                    isDeleting = false;
                    textIndex = (textIndex + 1) % texts.length;
                    typeSpeed = 500;
                }
                
                setTimeout(type, typeSpeed);
            }
            
            type();
        }
    }

    // ==========================================
    // Performance Optimization
    // ==========================================
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ==========================================
    // Page Loading Animation
    // ==========================================
    function handlePageLoad() {
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
            
            // Trigger hero animations
            const heroElements = document.querySelectorAll('.hero .fade-in-up');
            heroElements.forEach((el, index) => {
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    }

    // ==========================================
    // Initialize All Functions
    // ==========================================
    function init() {
        // Core animations
        initCounters();
        initScrollReveal();
        animateHeroBackground();
        
        // Interactive elements
        initFeatureCards();
        initRoleCards();
        initFloatingCards();
        initCTAAnimation();
        
        // Enhancements
        enhanceSmoothScroll();
        animateStatsBackground();
        addRippleStyles();
        addButtonRippleEffect();
        lazyLoadImages();
        
        // Optional effects
        // initTypedEffect(); // Uncomment if you add typed-text element
        
        // Page load
        handlePageLoad();
        
        // Performance optimizations
        window.addEventListener('resize', debounce(() => {
            // Handle responsive changes if needed
        }, 250));
        
        console.log('🩸 HemoVital Home Page Initialized Successfully!');
    }

    // ==========================================
    // Start when DOM is ready
    // ==========================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();