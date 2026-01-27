// ===== Navigation Scroll Effect =====
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ===== Smooth Scroll for Navigation Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Mobile Menu Toggle =====
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = mobileMenuBtn.querySelector('i');
        if (navLinks.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
}

// ===== Form Submission Handler =====
const enrollForm = document.getElementById('enrollForm');

if (enrollForm) {
    enrollForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        
        // Simple validation
        if (!data.name || !data.email || !data.plan) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            showNotification('Please enter a valid email address.', 'error');
            return;
        }
        
        // Simulate form submission
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitBtn.disabled = true;
        
        setTimeout(() => {
            showNotification('Thank you for enrolling! We\'ll contact you shortly.', 'success');
            this.reset();
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
}

// ===== Notification System =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles dynamically
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 24px;
        padding: 16px 20px;
        background: ${type === 'success' ? '#059669' : '#dc2626'};
        color: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    // Add animation keyframes
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .notification-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                padding: 4px;
                opacity: 0.7;
                transition: opacity 0.2s;
            }
            .notification-close:hover {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Close button handler
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// ===== Intersection Observer for Animations =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.tech-card, .curriculum-item, .feature-card, .testimonial-card, .pricing-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
});

// Add animation class styles
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(animationStyles);

// ===== Counter Animation for Stats =====
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            if (target >= 1000) {
                element.textContent = Math.floor(start / 1000) + 'K+';
            } else if (target < 10) {
                element.textContent = start.toFixed(1);
            } else {
                element.textContent = Math.floor(start) + '%';
            }
            requestAnimationFrame(updateCounter);
        } else {
            if (target >= 1000) {
                element.textContent = (target / 1000) + 'K+';
            } else if (target < 10) {
                element.textContent = target.toFixed(1);
            } else {
                element.textContent = target + '%';
            }
        }
    }
    
    updateCounter();
}

// Observe stats section
const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const text = stat.textContent;
                    if (text.includes('K+')) {
                        animateCounter(stat, 10000, 2000);
                    } else if (text.includes('%')) {
                        animateCounter(stat, 95, 2000);
                    } else {
                        animateCounter(stat, 4.9, 2000);
                    }
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statsObserver.observe(statsSection);
}

// ===== Typing Effect for Hero (Optional Enhancement) =====
const heroTitle = document.querySelector('.hero h1');
if (heroTitle) {
    // The title is already static, but we could add typing effect
    // Leaving this as a placeholder for future enhancement
}

// ===== Console Welcome Message =====
console.log('%c DevOps Mastery Program ', 'background: linear-gradient(135deg, #6366f1, #a855f7); color: white; font-size: 20px; padding: 10px 20px; border-radius: 8px;');
console.log('%c Welcome to the future of your career! ', 'color: #6366f1; font-size: 14px;');
