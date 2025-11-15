/**
 * CIRCUIT OS - NEON + STEEL ANIMATION SYSTEM
 * Premium animation controls for world-class aesthetics
 * Version: 1.0.0
 */

(function() {
    'use strict';

    // Animation performance monitoring
    let animationFrameId = null;
    let performanceMode = 'high'; // high, medium, low

    /**
     * NEON PULSE CONTROLLER
     * Controls pulsing effects on logos and status indicators
     */
    class NeonPulseController {
        constructor() {
            this.elements = [];
            this.running = false;
        }

        init() {
            this.elements = document.querySelectorAll('.logo-neon-pulse, .neon-pulse');
            if (this.elements.length > 0) {
                this.start();
            }
        }

        start() {
            this.running = true;
            this.elements.forEach((el, index) => {
                // Stagger animation starts for visual interest
                setTimeout(() => {
                    el.style.animation = 'neonPulse 3s ease-in-out infinite';
                }, index * 200);
            });
        }

        stop() {
            this.running = false;
            this.elements.forEach(el => {
                el.style.animation = 'none';
            });
        }
    }

    /**
     * STEEL SHIMMER CONTROLLER
     * Controls metallic border shimmer effects
     */
    class SteelShimmerController {
        constructor() {
            this.elements = [];
            this.running = false;
        }

        init() {
            this.elements = document.querySelectorAll('.steel-border, .steel-shimmer');
            if (this.elements.length > 0) {
                this.start();
            }
        }

        start() {
            this.running = true;
            this.elements.forEach((el, index) => {
                // Stagger shimmer animations
                setTimeout(() => {
                    el.style.animation = 'steelShimmer 3s linear infinite';
                }, index * 300);
            });
        }

        stop() {
            this.running = false;
            this.elements.forEach(el => {
                el.style.animation = 'none';
            });
        }
    }

    /**
     * CIRCUIT FLOW ANIMATOR
     * Animates circuit board lines with flowing effect
     */
    class CircuitFlowAnimator {
        constructor() {
            this.lines = [];
            this.running = false;
        }

        init() {
            this.lines = document.querySelectorAll('.circuit-line');
            if (this.lines.length > 0) {
                this.start();
            }
        }

        start() {
            this.running = true;
            this.lines.forEach((line, index) => {
                setTimeout(() => {
                    line.style.animation = 'circuitFlow 20s linear infinite';
                    line.style.animationDelay = `${index * 0.5}s`;
                }, index * 100);
            });
        }

        stop() {
            this.running = false;
            this.lines.forEach(line => {
                line.style.animation = 'none';
            });
        }
    }

    /**
     * NEON TEXT GLOW CONTROLLER
     * Manages glowing text effects
     */
    class NeonTextGlowController {
        constructor() {
            this.elements = [];
        }

        init() {
            this.elements = document.querySelectorAll('.neon-text');
            this.elements.forEach((el, index) => {
                setTimeout(() => {
                    el.style.animation = 'neonTextGlow 2s ease-in-out infinite';
                }, index * 150);
            });
        }
    }

    /**
     * INTERACTIVE CARD EFFECTS
     * Handles steel-to-neon transitions on hover
     */
    class InteractiveCardController {
        constructor() {
            this.cards = [];
        }

        init() {
            this.cards = document.querySelectorAll('.card-interactive');
            this.attachListeners();
        }

        attachListeners() {
            this.cards.forEach(card => {
                // Smooth hover transitions handled by CSS
                // Add ripple effect on click
                card.addEventListener('click', (e) => {
                    this.createRipple(e, card);
                });

                // Track mouse movement for subtle parallax
                card.addEventListener('mousemove', (e) => {
                    this.handleParallax(e, card);
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'translateY(-4px) rotateX(0deg) rotateY(0deg)';
                });
            });
        }

        createRipple(event, card) {
            const ripple = document.createElement('span');
            const rect = card.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = event.clientX - rect.left - size / 2;
            const y = event.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: radial-gradient(circle, rgba(56, 255, 106, 0.4) 0%, transparent 70%);
                border-radius: 50%;
                transform: scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
                z-index: 10;
            `;

            card.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        }

        handleParallax(event, card) {
            if (performanceMode === 'low') return;

            const rect = card.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `translateY(-4px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        }
    }

    /**
     * NEON PROGRESS BAR
     * Animated loading progress with neon glow
     */
    class NeonProgressController {
        constructor() {
            this.bars = [];
        }

        init() {
            this.bars = document.querySelectorAll('.progress-neon');
        }

        animate(bar, targetWidth = 100, duration = 1500) {
            bar.style.animation = `neonProgress ${duration}ms ease-out forwards`;
            bar.style.width = `${targetWidth}%`;
        }

        animateAll(targetWidth = 100, duration = 1500) {
            this.bars.forEach((bar, index) => {
                setTimeout(() => {
                    this.animate(bar, targetWidth, duration);
                }, index * 200);
            });
        }
    }

    /**
     * STATUS DOT PULSE
     * Animated status indicators
     */
    class StatusDotController {
        constructor() {
            this.dots = [];
        }

        init() {
            this.dots = document.querySelectorAll('.status-dot-neon');
            this.dots.forEach((dot, index) => {
                setTimeout(() => {
                    dot.style.animation = 'neonDotPulse 2s ease-in-out infinite';
                }, index * 100);
            });
        }
    }

    /**
     * CIRCUIT BOARD BACKGROUND
     * Manages animated circuit board patterns
     */
    class CircuitBackgroundController {
        constructor() {
            this.canvas = null;
            this.ctx = null;
            this.nodes = [];
            this.running = false;
        }

        init() {
            this.canvas = document.getElementById('circuit-background-canvas');
            if (!this.canvas) return;

            this.ctx = this.canvas.getContext('2d');
            this.resize();
            this.createNodes();
            this.start();

            window.addEventListener('resize', () => this.resize());
        }

        resize() {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        }

        createNodes() {
            const nodeCount = Math.floor((window.innerWidth * window.innerHeight) / 20000);
            this.nodes = [];

            for (let i = 0; i < nodeCount; i++) {
                this.nodes.push({
                    x: Math.random() * this.canvas.width,
                    y: Math.random() * this.canvas.height,
                    size: Math.random() * 3 + 2,
                    pulseOffset: Math.random() * Math.PI * 2,
                    pulseSpeed: Math.random() * 0.02 + 0.01
                });
            }
        }

        start() {
            this.running = true;
            this.animate();
        }

        animate() {
            if (!this.running) return;

            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            // Draw nodes with pulse
            const time = Date.now() * 0.001;
            this.nodes.forEach(node => {
                const pulse = Math.sin(time * node.pulseSpeed + node.pulseOffset) * 0.5 + 0.5;
                const alpha = 0.3 + pulse * 0.4;

                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(56, 255, 106, ${alpha})`;
                this.ctx.fill();

                // Glow effect
                this.ctx.shadowBlur = 10 + pulse * 10;
                this.ctx.shadowColor = 'rgba(56, 255, 106, 0.8)';
            });

            this.ctx.shadowBlur = 0;

            animationFrameId = requestAnimationFrame(() => this.animate());
        }

        stop() {
            this.running = false;
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        }
    }

    /**
     * PERFORMANCE MONITOR
     * Adjusts animation quality based on performance
     */
    class PerformanceMonitor {
        constructor() {
            this.fps = 60;
            this.frameCount = 0;
            this.lastTime = performance.now();
        }

        init() {
            this.monitor();
        }

        monitor() {
            const currentTime = performance.now();
            this.frameCount++;

            if (currentTime - this.lastTime >= 1000) {
                this.fps = this.frameCount;
                this.frameCount = 0;
                this.lastTime = currentTime;

                // Adjust performance mode
                if (this.fps < 30) {
                    performanceMode = 'low';
                    console.log('Circuit OS: Performance mode set to LOW');
                } else if (this.fps < 50) {
                    performanceMode = 'medium';
                } else {
                    performanceMode = 'high';
                }
            }

            requestAnimationFrame(() => this.monitor());
        }
    }

    /**
     * MASTER ANIMATION CONTROLLER
     * Coordinates all animation systems
     */
    class CircuitAnimationMaster {
        constructor() {
            this.controllers = {
                neonPulse: new NeonPulseController(),
                steelShimmer: new SteelShimmerController(),
                circuitFlow: new CircuitFlowAnimator(),
                neonText: new NeonTextGlowController(),
                interactiveCards: new InteractiveCardController(),
                neonProgress: new NeonProgressController(),
                statusDots: new StatusDotController(),
                circuitBackground: new CircuitBackgroundController(),
                performance: new PerformanceMonitor()
            };
        }

        init() {
            console.log('Circuit OS: Initializing Neon + Steel Animation System...');

            // Initialize all controllers
            Object.values(this.controllers).forEach(controller => {
                controller.init();
            });

            console.log('Circuit OS: Animation system ready. Performance mode: ' + performanceMode);

            // Add ripple effect keyframe if not present
            this.injectAnimationStyles();
        }

        injectAnimationStyles() {
            const style = document.createElement('style');
            style.textContent = `
                @keyframes rippleEffect {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        pauseAll() {
            this.controllers.neonPulse.stop();
            this.controllers.steelShimmer.stop();
            this.controllers.circuitFlow.stop();
            this.controllers.circuitBackground.stop();
        }

        resumeAll() {
            this.controllers.neonPulse.start();
            this.controllers.steelShimmer.start();
            this.controllers.circuitFlow.start();
            this.controllers.circuitBackground.start();
        }

        getController(name) {
            return this.controllers[name];
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.CircuitAnimations = new CircuitAnimationMaster();
            window.CircuitAnimations.init();
        });
    } else {
        window.CircuitAnimations = new CircuitAnimationMaster();
        window.CircuitAnimations.init();
    }

    // Expose global API
    window.CircuitAnimations = window.CircuitAnimations || {};

})();
