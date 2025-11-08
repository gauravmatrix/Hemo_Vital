/* ===================================================================
   HemoVital - Simple Registration JavaScript (register_simple.js)
   Handles tab-based switching between user and hospital forms.
   =================================================================== */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // ==========================================
        //  DOM ELEMENTS
        // ==========================================
        const roleTabs = document.querySelectorAll('.role-tab');
        const userForm = document.getElementById('user-form');
        const hospitalForm = document.getElementById('hospital-form');

        // ==========================================
        //  EVENT LISTENER FOR TABS
        // ==========================================
        
        if (roleTabs.length > 0 && userForm && hospitalForm) {
            
            roleTabs.forEach(tab => {
                tab.addEventListener('click', function () {
                    
                    // 1. Update Tab Styles
                    // Remove 'active' class from all tabs
                    roleTabs.forEach(t => t.classList.remove('active'));
                    // Add 'active' class to the clicked tab
                    this.classList.add('active');

                    // 2. Get the target form's ID from the data-form attribute
                    const targetFormId = this.getAttribute('data-form');

                    // 3. Switch Forms with a fade effect for better UX
                    if (targetFormId === 'user-form') {
                        // Show user form, hide hospital form
                        fadeOut(hospitalForm, () => {
                            fadeIn(userForm);
                        });
                    } else if (targetFormId === 'hospital-form') {
                        // Show hospital form, hide user form
                        fadeOut(userForm, () => {
                            fadeIn(hospitalForm);
                        });
                    }
                });
            });
        }

        // ==========================================
        //  UTILITY FUNCTIONS FOR ANIMATIONS
        // ==========================================

        function fadeIn(element) {
            element.style.opacity = 0;
            element.style.display = 'block';

            let opacity = 0;
            const timer = setInterval(function () {
                if (opacity >= 1) {
                    clearInterval(timer);
                }
                element.style.opacity = opacity;
                opacity += 0.1;
            }, 20); // Adjust timing for faster/slower fade
        }

        function fadeOut(element, callback) {
            let opacity = 1;
            const timer = setInterval(function () {
                if (opacity <= 0) {
                    clearInterval(timer);
                    element.style.display = 'none';
                    if (callback) {
                        callback();
                    }
                }
                element.style.opacity = opacity;
                opacity -= 0.1;
            }, 20); // Adjust timing for faster/slower fade
        }
    });

})();

