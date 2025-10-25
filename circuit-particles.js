/**
 * Circuit OS Particle System
 * Subtle, professional particle animation with gold accents
 * Optimized for 60fps performance
 */

(function() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationFrameId;
    let mouse = { x: null, y: null };

    // Configuration
    const config = {
        particleCount: 50,
        maxDistance: 150,
        particleSize: 2,
        baseSpeed: 0.3,
        mouseRadius: 200,
        colors: {
            gold: 'rgba(212, 175, 55, 0.6)',
            goldLight: 'rgba(229, 193, 88, 0.4)',
            white: 'rgba(255, 255, 255, 0.3)'
        }
    };

    // Particle class
    class Particle {
        constructor() {
            this.reset();
            this.y = Math.random() * canvas.height;
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * config.baseSpeed;
            this.vy = (Math.random() - 0.5) * config.baseSpeed;
            this.size = Math.random() * config.particleSize + 1;
            this.opacity = Math.random() * 0.5 + 0.2;

            // Randomly assign color (mostly gold, some white)
            this.color = Math.random() > 0.7 ? config.colors.white :
                        Math.random() > 0.5 ? config.colors.gold : config.colors.goldLight;
        }

        update() {
            // Mouse interaction - subtle attraction
            if (mouse.x !== null && mouse.y !== null) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < config.mouseRadius) {
                    const force = (config.mouseRadius - distance) / config.mouseRadius;
                    this.vx += (dx / distance) * force * 0.01;
                    this.vy += (dy / distance) * force * 0.01;
                }
            }

            // Update position
            this.x += this.vx;
            this.y += this.vy;

            // Boundary check - wrap around
            if (this.x < 0) this.x = canvas.width;
            if (this.x > canvas.width) this.x = 0;
            if (this.y < 0) this.y = canvas.height;
            if (this.y > canvas.height) this.y = 0;

            // Dampen velocity (friction)
            this.vx *= 0.99;
            this.vy *= 0.99;

            // Ensure minimum movement
            if (Math.abs(this.vx) < 0.1) this.vx += (Math.random() - 0.5) * 0.05;
            if (Math.abs(this.vy) < 0.1) this.vy += (Math.random() - 0.5) * 0.05;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();

            // Add subtle glow for larger particles
            if (this.size > 1.5) {
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.fill();
                ctx.shadowBlur = 0;
            }
        }
    }

    // Initialize canvas size
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // Create particles
    function initParticles() {
        particles = [];
        for (let i = 0; i < config.particleCount; i++) {
            particles.push(new Particle());
        }
    }

    // Draw connections between nearby particles
    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < config.maxDistance) {
                    const opacity = (1 - distance / config.maxDistance) * 0.15;
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(212, 175, 55, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update and draw all particles
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        // Draw connections
        drawConnections();

        animationFrameId = requestAnimationFrame(animate);
    }

    // Mouse move event
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // Mouse leave event
    window.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });

    // Window resize event
    window.addEventListener('resize', () => {
        resizeCanvas();
        initParticles();
    });

    // Initialize
    resizeCanvas();
    initParticles();
    animate();

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
    });
})();
