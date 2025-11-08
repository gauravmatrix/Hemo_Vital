/* ==========================================
   HemoVital - Dashboard Base JavaScript
   Handles sidebar toggle for mobile.
   ========================================== */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.getElementById('sidebar');
        const toggleBtn = document.getElementById('sidebar-toggle-btn');
        const closeBtn = document.getElementById('sidebar-close-btn');

        function toggleSidebar() {
            if (sidebar) {
                sidebar.classList.toggle('active');
            }
        }

        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleSidebar);
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', toggleSidebar);
        }
        
        // Optional: Close sidebar if user clicks outside of it on mobile
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 992 && sidebar && sidebar.classList.contains('active')) {
                const isClickInsideSidebar = sidebar.contains(event.target);
                const isClickOnToggleBtn = toggleBtn ? toggleBtn.contains(event.target) : false;

                if (!isClickInsideSidebar && !isClickOnToggleBtn) {
                    sidebar.classList.remove('active');
                }
            }
        });
    });

})();

