/**
 * HemoVital - Base JavaScript
 * Main functionality for navbar, mobile menu, scroll effects, and alerts
 */

(function() {
    'use strict';

    // ==========================================
    // DOM Elements
    // ==========================================
    const navbar = document.getElementById('navbar');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');
    const scrollToTopBtn = document.getElementById('scrollToTop');
    const dropdowns = document.querySelectorAll('.dropdown');
    const alertCloseButtons = document.querySelectorAll('.close-alert');

    // ==========================================
    // Navbar Scroll Effect
    // ==========================================
    function handleNavbarScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // ==========================================
    // Mobile Menu Toggle
    // ==========================================
    function toggleMobileMenu() {
        mobileMenuToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    }

    // Close mobile menu when clicking outside
    function handleClickOutside(event) {
        if (navMenu.classList.contains('active') && 
            !navMenu.contains(event.target) && 
            !mobileMenuToggle.contains(event.target)) {
            toggleMobileMenu();
        }
    }

    // Close mobile menu when clicking on a link
    function closeMobileMenuOnLinkClick() {
        const navLinks = navMenu.querySelectorAll('.nav-link:not(.dropdown-toggle)');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navMenu.classList.contains('active')) {
                    toggleMobileMenu();
                }
            });
        });
    }

    // ==========================================
    // Mobile Dropdown Toggle
    // ==========================================
    function handleMobileDropdown() {
        if (window.innerWidth <= 768) {
            dropdowns.forEach(dropdown => {
                const toggle = dropdown.querySelector('.dropdown-toggle');
                if (toggle) {
                    toggle.addEventListener('click', (e) => {
                        e.preventDefault();
                        dropdown.classList.toggle('active');
                        
                        // Close other dropdowns
                        dropdowns.forEach(other => {
                            if (other !== dropdown) {
                                other.classList.remove('active');
                            }
                        });
                    });
                }
            });
        }
    }

    // ==========================================
    // Scroll to Top Button
    // ==========================================
    function handleScrollToTop() {
        if (window.scrollY > 300) {
            scrollToTopBtn.classList.add('show');
        } else {
            scrollToTopBtn.classList.remove('show');
        }
    }

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // ==========================================
    // Alert Messages
    // ==========================================
    function handleAlertClose() {
        alertCloseButtons.forEach(button => {
            button.addEventListener('click', () => {
                const alert = button.closest('.alert');
                alert.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        });
    }

    // Auto-dismiss alerts after 5 seconds
    function autoDismissAlerts() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach((alert, index) => {
            setTimeout(() => {
                const closeBtn = alert.querySelector('.close-alert');
                if (closeBtn) {
                    closeBtn.click();
                }
            }, 5000 + (index * 500)); // Stagger dismissal
        });
    }

    // ==========================================
    // Smooth Scroll for Anchor Links
    // ==========================================
    function handleSmoothScroll() {
        const anchorLinks = document.querySelectorAll('a[href^="#"]');
        anchorLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href !== '#' && href !== '#!') {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }

    // ==========================================
    // Active Link Highlighting
    // ==========================================
    function updateActiveLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');

        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }

    // ==========================================
    // Lazy Loading Images
    // ==========================================
    function lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ==========================================
    // Scroll Animations
    // ==========================================
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('.fade-in-up, .fade-in-down, .slide-in-left, .slide-in-right, .zoom-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translate(0, 0) scale(1)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(el => {
            el.style.opacity = '0';
            observer.observe(el);
        });
    }

    // ==========================================
    // Form Validation Helper
    // ==========================================
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePhone(phone) {
        const re = /^[0-9]{10}$/;
        return re.test(phone.replace(/\s/g, ''));
    }

    // ==========================================
    // Loading Spinner
    // ==========================================
    function showLoading() {
        const loader = document.createElement('div');
        loader.id = 'page-loader';
        loader.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            ">
                <div style="
                    width: 50px;
                    height: 50px;
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #DC143C;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                "></div>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        document.body.appendChild(loader);
    }

    function hideLoading() {
        const loader = document.getElementById('page-loader');
        if (loader) {
            loader.remove();
        }
    }

    // ==========================================
    // Local Storage Helper
    // ==========================================
    const Storage = {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.error('Error saving to localStorage', e);
            }
        },
        
        get: function(key) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.error('Error reading from localStorage', e);
                return null;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
            } catch (e) {
                console.error('Error removing from localStorage', e);
            }
        },
        
        clear: function() {
            try {
                localStorage.clear();
            } catch (e) {
                console.error('Error clearing localStorage', e);
            }
        }
    };

    // ==========================================
    // Notification System
    // ==========================================
    function showNotification(message, type = 'info') {
        const container = document.querySelector('.messages-container') || createNotificationContainer();
        
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible`;
        notification.innerHTML = `
            <i class="fas fa-${getIconForType(type)}"></i>
            <span>${message}</span>
            <button type="button" class="close-alert" aria-label="Close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(notification);
        
        // Add close functionality
        const closeBtn = notification.querySelector('.close-alert');
        closeBtn.addEventListener('click', () => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        });
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                closeBtn.click();
            }
        }, 5000);
    }

    function createNotificationContainer() {
        const container = document.createElement('div');
        container.className = 'messages-container';
        document.body.appendChild(container);
        return container;
    }

    function getIconForType(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // ==========================================
    // Debounce Function
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
    // Initialize Everything
    // ==========================================
    function init() {
        // Navbar functionality
        window.addEventListener('scroll', debounce(handleNavbarScroll, 10));
        window.addEventListener('scroll', debounce(handleScrollToTop, 10));
        
        // Mobile menu
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', toggleMobileMenu);
        }
        document.addEventListener('click', handleClickOutside);
        closeMobileMenuOnLinkClick();
        handleMobileDropdown();
        
        // Scroll to top
        if (scrollToTopBtn) {
            scrollToTopBtn.addEventListener('click', scrollToTop);
        }
        
        // Alerts
        handleAlertClose();
        autoDismissAlerts();
        
        // Other features
        handleSmoothScroll();
        updateActiveLink();
        lazyLoadImages();
        initScrollAnimations();
        
        // Initial calls
        handleNavbarScroll();
        handleScrollToTop();
        
        // Handle window resize
        window.addEventListener('resize', debounce(() => {
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                toggleMobileMenu();
            }
        }, 250));
    }

    // ==========================================
    // Export Functions (for use in other scripts)
    // ==========================================
    window.HemoVital = {
        showLoading,
        hideLoading,
        showNotification,
        validateEmail,
        validatePhone,
        Storage
    };

    // ==========================================
    // Start when DOM is ready
    // ==========================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();