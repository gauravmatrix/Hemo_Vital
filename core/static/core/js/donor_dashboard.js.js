/* ===================================================================
   HemoVital - Donor Dashboard JavaScript
   Handles countdown timers for active requests.
   =================================================================== */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        const countdownTimers = document.querySelectorAll('.countdown-timer');

        if (countdownTimers.length > 0) {
            countdownTimers.forEach(timerElement => {
                const expiresISO = timerElement.getAttribute('data-expires');
                if (!expiresISO) return;

                const expiryDate = new Date(expiresISO);
                const timerDisplay = timerElement.querySelector('strong');

                const intervalId = setInterval(() => {
                    const now = new Date();
                    const distance = expiryDate - now;

                    if (distance < 0) {
                        clearInterval(intervalId);
                        timerDisplay.textContent = 'Expired';
                        timerElement.closest('.request-card').classList.add('expired');
                        return;
                    }

                    // Time calculations for days, hours, minutes and seconds
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                    // Build the display string
                    let displayString = '';
                    if (days > 0) {
                        displayString += `${days}d `;
                    }
                    if (hours > 0 || days > 0) {
                        displayString += `${hours}h `;
                    }
                    displayString += `${minutes}m ${seconds}s`;

                    timerDisplay.textContent = displayString.trim();

                }, 1000);
            });
        }
    });
})();
