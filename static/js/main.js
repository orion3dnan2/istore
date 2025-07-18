// Main JavaScript file for Electronics Store

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(function() {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Add loading state
            this.classList.add('loading');
            
            // Remove loading state after a short delay
            setTimeout(() => {
                this.classList.remove('loading');
            }, 300);
        });
    }

    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.getAttribute('min')) || 1;
            const max = parseInt(this.getAttribute('max')) || 999;
            const value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('a[href*="add_to_cart"]');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add visual feedback
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            this.classList.add('disabled');
            
            // Reset button after redirect (this won't actually run due to redirect)
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-cart-plus"></i> Add to Cart';
                this.classList.remove('disabled');
            }, 1000);
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check if form is valid
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Add loading state to submit button
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitButton.disabled = true;
            }
            
            this.classList.add('was-validated');
        });
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Mobile menu improvements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarToggler.contains(e.target) && !navbarCollapse.contains(e.target)) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    }

    // Price formatting
    const priceElements = document.querySelectorAll('.price, .price-tag');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent.replace('$', ''));
        if (!isNaN(price)) {
            element.textContent = '$' + price.toFixed(2);
        }
    });

    // Admin table enhancements
    const adminTables = document.querySelectorAll('.table');
    adminTables.forEach(table => {
        // Add hover effect to rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f8f9fa';
            });
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });

    // Confirmation dialogs
    const deleteButtons = document.querySelectorAll('a[href*="delete"], button[onclick*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Auto-save form data in localStorage
    const autoSaveForms = document.querySelectorAll('form[data-auto-save]');
    autoSaveForms.forEach(form => {
        const formId = form.getAttribute('data-auto-save');
        
        // Load saved data
        const savedData = localStorage.getItem(`form_${formId}`);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = data[key];
                    }
                });
            } catch (e) {
                console.error('Error loading saved form data:', e);
            }
        }
        
        // Save data on input
        form.addEventListener('input', function() {
            const formData = new FormData(this);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem(`form_${formId}`, JSON.stringify(data));
        });
        
        // Clear saved data on submit
        form.addEventListener('submit', function() {
            localStorage.removeItem(`form_${formId}`);
        });
    });
});

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

function formatPrice(price) {
    return '$' + parseFloat(price).toFixed(2);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Export functions for use in other scripts
window.ElectronicsStore = {
    showNotification,
    formatPrice,
    formatDate
};
