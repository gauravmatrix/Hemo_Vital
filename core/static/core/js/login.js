/**
 * HemoVital - Login Page JavaScript
 * Handles form validation, password toggle, and interactions
 */

(function() {
    'use strict';

    // ==========================================
    // DOM Elements
    // ==========================================
    const loginForm = document.querySelector('.auth-form');
    const passwordToggleBtn = document.querySelector('.password-toggle-btn');
    const passwordInput = document.querySelector('input[type="password"]');
    const emailInput = document.querySelector('input[type="email"], input[type="text"]');
    const roleOptions = document.querySelectorAll('.role-option input[type="radio"]');
    const submitButton = document.querySelector('.submit-button');

    // ==========================================
    // Password Toggle Functionality
    // ==========================================
    function initPasswordToggle() {
        if (passwordToggleBtn && passwordInput) {
            passwordToggleBtn.addEventListener('click', function() {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                
                // Toggle icon
                const icon = this.querySelector('i');
                if (type === 'text') {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            });
        }
    }

    // ==========================================
    // Form Validation
    // ==========================================
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    function showError(input, message) {
        input.classList.add('error');
        
        // Check if error message already exists
        let errorMsg = input.parentElement.nextElementSibling;
        if (!errorMsg || !errorMsg.classList.contains('input-error-message')) {
            errorMsg = document.createElement('p');
            errorMsg.classList.add('input-error-message');
            input.parentElement.after(errorMsg);
        }
        errorMsg.textContent = message;
        
        // Shake animation
        input.style.animation = 'shake 0.5s ease';
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    }

    function clearError(input) {
        input.classList.remove('error');
        const errorMsg = input.parentElement.nextElementSibling;
        if (errorMsg && errorMsg.classList.contains('input-error-message')) {
            errorMsg.remove();
        }
    }

    function validateForm() {
        let isValid = true;

        // Clear previous errors
        const inputs = loginForm.querySelectorAll('input[type="email"], input[type="text"], input[type="password"]');
        inputs.forEach(input => clearError(input));

        // Validate email
        if (emailInput) {
            const emailValue = emailInput.value.trim();
            if (emailValue === '') {
                showError(emailInput, 'Email address is required');
                isValid = false;
            } else if (!validateEmail(emailValue)) {
                showError(emailInput, 'Please enter a valid email address');
                isValid = false;
            }
        }

        // Validate password
        if (passwordInput) {
            const passwordValue = passwordInput.value;
            if (passwordValue === '') {
                showError(passwordInput, 'Password is required');
                isValid = false;
            } else if (passwordValue.length < 6) {
                showError(passwordInput, 'Password must be at least 6 characters');
                isValid = false;
            }
        }

        return isValid;
    }

    // ==========================================
    // Form Submit Handler
    // ==========================================
    function handleFormSubmit(e) {
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }

        // Show loading state
        if (submitButton) {
            const originalText = submitButton.querySelector('.btn-text') || submitButton.childNodes[0];
            submitButton.disabled = true;
            submitButton.style.opacity = '0.7';
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        }
    }

    // ==========================================
    // Real-time Validation
    // ==========================================
    function initRealtimeValidation() {
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                const value = this.value.trim();
                if (value !== '') {
                    if (!validateEmail(value)) {
                        showError(this, 'Please enter a valid email address');
                    } else {
                        clearError(this);
                    }
                }
            });

            emailInput.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    clearError(this);
                }
            });
        }

        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    clearError(this);
                }
            });
        }
    }

    // ==========================================
    // Role Selection Enhancement
    // ==========================================
    function initRoleSelection() {
        roleOptions.forEach(radio => {
            radio.addEventListener('change', function() {
                // Add smooth transition effect
                const label = this.nextElementSibling;
                label.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    label.style.transform = 'scale(1)';
                }, 100);
            });
        });
    }

    // ==========================================
    // Input Focus Effects
    // ==========================================
    function initInputEffects() {
        const inputs = document.querySelectorAll('.auth-form input[type="email"], .auth-form input[type="text"], .auth-form input[type="password"]');
        
        inputs.forEach(input => {
            // Focus effect
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
            });

            // Blur effect
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });

            // Typing effect
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.style.borderColor = 'var(--primary-red)';
                } else {
                    this.style.borderColor = '';
                }
            });
        });
    }

    // ==========================================
    // Submit Button Ripple Effect
    // ==========================================
    function addRippleEffect(e) {
        const button = e.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple-effect');

        button.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Add ripple CSS
    function addRippleStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .submit-button {
                position: relative;
                overflow: hidden;
            }
            
            .ripple-effect {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            }
            
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // ==========================================
    // Auto-fill Detection
    // ==========================================
    function detectAutofill() {
        const inputs = document.querySelectorAll('.auth-form input');
        
        inputs.forEach(input => {
            // Check for autofill on load
            setTimeout(() => {
                if (input.matches(':-webkit-autofill')) {
                    input.parentElement.classList.add('autofilled');
                }
            }, 100);

            // Monitor for autofill changes
            input.addEventListener('animationstart', (e) => {
                if (e.animationName === 'onAutoFillStart') {
                    input.parentElement.classList.add('autofilled');
                }
            });
        });
    }

    // ==========================================
    // Keyboard Navigation Enhancement
    // ==========================================
    function enhanceKeyboardNav() {
        const inputs = loginForm.querySelectorAll('input');
        
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && index < inputs.length - 1) {
                    e.preventDefault();
                    inputs[index + 1].focus();
                }
            });
        });
    }

    // ==========================================
    // Remember Me Functionality
    // ==========================================
    function initRememberMe() {
        const rememberCheckbox = document.getElementById('remember');
        const emailInput = document.querySelector('input[type="email"], input[type="text"]');
        
        if (rememberCheckbox && emailInput) {
            // Load saved email
            const savedEmail = localStorage.getItem('hemovital_remembered_email');
            if (savedEmail) {
                emailInput.value = savedEmail;
                rememberCheckbox.checked = true;
            }

            // Save email on form submit
            loginForm.addEventListener('submit', function() {
                if (rememberCheckbox.checked) {
                    localStorage.setItem('hemovital_remembered_email', emailInput.value);
                } else {
                    localStorage.removeItem('hemovital_remembered_email');
                }
            }
            );
        }
    }
    
    // ==========================================
    // Initialization
    // ==========================================
    function init() {
        if (loginForm) {
            loginForm.addEventListener('submit', handleFormSubmit);
        }
        if (submitButton) {
            submitButton.addEventListener('click', addRippleEffect);
        }
        initPasswordToggle();
        initRealtimeValidation();
        initRoleSelection();
        initInputEffects();
        addRippleStyles();
        detectAutofill();
        enhanceKeyboardNav();
        initRememberMe();
    }
    
    // Initialize when DOM is fully loaded
    document.addEventListener('DOMContentLoaded', init);
}
)();
