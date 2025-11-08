/* ===================================================================
   HemoVital - Donor Dashboard JavaScript (donor_dashboard.js)
   Handles live countdown timers for blood requests.
   =================================================================== */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        const countdownElements = document.querySelectorAll('.countdown-timer');

        if (countdownElements.length === 0) {
            return; // No timers on the page, do nothing.
        }

        /**
         * Updates all countdown timers on the page every second.
         */
        function updateAllTimers() {
            countdownElements.forEach(timerEl => {
                const expiresOnString = timerEl.getAttribute('data-expires');
                if (!expiresOnString) return;

                const expiryDate = new Date(expiresOnString);
                const now = new Date();

                const remainingTime = expiryDate - now;

                const timerStrongTag = timerEl.querySelector('strong');

                if (remainingTime <= 0) {
                    timerStrongTag.textContent = 'Expired';
                    timerEl.closest('.request-card')?.classList.add('expired'); // Optional: style expired cards
                } else {
                    const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
                    
                    let formattedTime = '';

                    if (days > 0) {
                        formattedTime = `${days}d ${hours}h`;
                    } else if (hours > 0) {
                        formattedTime = `${hours}h ${minutes}m`;
                    } else if (minutes > 0) {
                        formattedTime = `${minutes}m ${seconds}s`;
                    } else {
                        formattedTime = `${seconds}s`;
                    }
                    
                    timerStrongTag.textContent = formattedTime;
                }
            });
        }

        // Run the timer update function immediately on page load
        updateAllTimers();

        // Then, update it every second
        setInterval(updateAllTimers, 1000);
    });

})();

