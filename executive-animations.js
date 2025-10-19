/**
 * Executive Animations
 * Orchestrated page load sequence for luxury experience
 * Total duration: ~2.5 seconds
 */

(function() {
    'use strict';

    // Animation sequence configuration
    const sequence = {
        logo: { delay: 200, duration: 800 },
        header: { delay: 400, duration: 1000 },
        cards: { delay: 1000, stagger: 200 },
        stats: { delay: 1600, countDuration: 1500 }
    };

    /**
     * Number counter animation
     * Animates numbers from 0 to target value
     */
    function animateNumber(element, target, duration, formatter = null) {
        const start = 0;
        const startTime = performance.now();
        const isPercentage = target.toString().includes('%');
        const numericTarget = parseFloat(target);

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out cubic)
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = start + (numericTarget - start) * eased;

            // Format the number
            let displayValue;
            if (formatter) {
                displayValue = formatter(current);
            } else if (isPercentage) {
                displayValue = Math.round(current) + '%';
            } else if (target.toString().includes('$')) {
                displayValue = '$' + formatCurrency(current);
            } else if (target.toString().includes('K')) {
                displayValue = (current / 1000).toFixed(1) + 'K';
            } else if (target.toString().includes('M')) {
                displayValue = (current / 1000000).toFixed(1) + 'M';
            } else {
                displayValue = Math.round(current).toLocaleString();
            }

            element.textContent = displayValue;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    /**
     * Format currency values
     */
    function formatCurrency(value) {
        if (value >= 1000000) {
            return (value / 1000000).toFixed(1) + 'M';
        } else if (value >= 1000) {
            return (value / 1000).toFixed(1) + 'K';
        } else {
            return Math.round(value).toLocaleString();
        }
    }

    /**
     * Animate progress bars
     */
    function animateProgressBar(bar, targetWidth, duration) {
        const startWidth = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out cubic)
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = startWidth + (targetWidth - startWidth) * eased;

            bar.style.width = current + '%';

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    /**
     * Stagger animation for card elements
     */
    function staggerCards(cards, baseDelay, stagger) {
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate-in');
            }, baseDelay + (index * stagger));
        });
    }

    /**
     * Initialize stat counters
     */
    function initStatCounters() {
        const statElements = document.querySelectorAll('.stat-value[data-value]');

        statElements.forEach((element, index) => {
            const targetValue = element.getAttribute('data-value');
            const delay = sequence.stats.delay + (index * 100);

            setTimeout(() => {
                animateNumber(element, targetValue, sequence.stats.countDuration);
            }, delay);
        });
    }

    /**
     * Initialize progress bars
     */
    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill[data-width]');

        progressBars.forEach((bar, index) => {
            const targetWidth = parseFloat(bar.getAttribute('data-width'));
            const delay = sequence.stats.delay + (index * 150);

            setTimeout(() => {
                animateProgressBar(bar, targetWidth, 1500);
            }, delay);
        });
    }

    /**
     * Confidence bar animations
     */
    function initConfidenceBars() {
        const confidenceBars = document.querySelectorAll('.confidence-fill');

        confidenceBars.forEach((bar, index) => {
            const targetWidth = parseFloat(bar.style.width || bar.getAttribute('data-width') || 0);
            const delay = 1800 + (index * 100);

            // Reset width to 0
            bar.style.width = '0%';

            setTimeout(() => {
                animateProgressBar(bar, targetWidth, 1200);
            }, delay);
        });
    }

    /**
     * Add entrance animations to table rows
     */
    function initTableAnimations() {
        const tableRows = document.querySelectorAll('.table-row-hover, tbody tr');

        tableRows.forEach((row, index) => {
            const delay = 2000 + (index * 80);

            setTimeout(() => {
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                row.style.transition = 'all 0.5s ease-out';

                requestAnimationFrame(() => {
                    row.style.opacity = '1';
                    row.style.transform = 'translateX(0)';
                });
            }, delay);
        });
    }

    /**
     * Ripple effect for buttons
     */
    function initButtonRipples() {
        const buttons = document.querySelectorAll('.btn-executive, .cta, button');

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
                ripple.classList.add('ripple-effect');

                this.appendChild(ripple);

                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    /**
     * Add hover parallax effect to cards
     */
    function initCardParallax() {
        const cards = document.querySelectorAll('.executive-card, .dashboard-card');

        cards.forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;

                this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }

    /**
     * Smooth scroll for anchor links
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    /**
     * Initialize all animations on page load
     */
    function init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Initialize animations in sequence
        initStatCounters();
        initProgressBars();
        initConfidenceBars();
        initTableAnimations();
        initButtonRipples();
        initCardParallax();
        initSmoothScroll();

        // Add CSS for ripple effect if not present
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                .ripple-effect {
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.3);
                    transform: scale(0);
                    animation: ripple-animation 0.6s ease-out;
                    pointer-events: none;
                }

                @keyframes ripple-animation {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }

                .animate-in {
                    animation: slideInUp 0.6s ease-out forwards;
                }

                @keyframes slideInUp {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }

        console.log('Executive animations initialized');
    }

    // Auto-initialize
    init();

    // Expose utilities globally for manual use
    window.CircuitAnimations = {
        animateNumber,
        animateProgressBar,
        formatCurrency
    };
})();
