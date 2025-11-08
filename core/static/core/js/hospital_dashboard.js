/* ===================================================================
   HemoVital - Reusable Countdown Timer JavaScript
   Handles live countdown timers for blood requests on any page.
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

                if (remainingTime <= 0) {
                    timerEl.textContent = 'Expired';
                    timerEl.closest('.data-table tr, .request-card')?.classList.add('expired');
                } else {
                    const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                    
                    let formattedTime = '';

                    if (days > 0) {
                        formattedTime = `${days}d ${hours}h left`;
                    } else if (hours > 0) {
                        formattedTime = `${hours}h ${minutes}m left`;
                    } else {
                        formattedTime = `${minutes}m left`;
                    }
                    
                    timerEl.textContent = formattedTime;
                }
            });
        }

        // Run the timer update function immediately on page load
        updateAllTimers();

        // Then, update it every second
        setInterval(updateAllTimers, 1000);
    });

})();

document.querySelectorAll('.btn-confirm, .btn-reject').forEach(button => {
    button.addEventListener('click', e => {
        const donationId = button.dataset.id;
        const action = button.classList.contains('btn-confirm') ? 'confirm' : 'reject';

        fetch(`/hospital/donation/${donationId}/update/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `action=${action}`
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success'){
                alert(data.message);
                // Optionally remove the row
                button.closest('tr').remove();
            } else {
                alert(data.message);
            }
        });
    });
});


