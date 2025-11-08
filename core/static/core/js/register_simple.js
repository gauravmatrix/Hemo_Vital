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

            // We use a short delay to ensure the display property is applied before starting the transition
            setTimeout(() => {
                element.style.transition = 'opacity 0.3s ease';
                element.style.opacity = 1;
            }, 10);
        }

        function fadeOut(element, callback) {
            element.style.opacity = 1;
            element.style.transition = 'opacity 0.3s ease';
            element.style.opacity = 0;

            // Wait for the transition to finish before hiding the element and calling the callback
            setTimeout(() => {
                element.style.display = 'none';
                if (callback) {
                    callback();
                }
            }, 300); // This duration must match the transition duration
        }
    });

})();

