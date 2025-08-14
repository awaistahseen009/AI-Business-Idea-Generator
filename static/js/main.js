// AI Business Idea Generator - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize copy functionality
    initializeCopyFunctionality();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Copy single idea content (from idea cards)
    document.querySelectorAll('.copy-idea-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const content = btn.getAttribute('data-idea-content') || '';
            if (content) {
                copyToClipboard(content);
            } else {
                showToast('Nothing to copy', 'error');
            }
        });
    });

    // Copy all ideas in one go
    const copyAllBtn = document.getElementById('copyAllIdeas');
    if (copyAllBtn) {
        copyAllBtn.addEventListener('click', () => {
            const ideaButtons = document.querySelectorAll('.copy-idea-btn');
            const all = Array.from(ideaButtons).map(b => b.getAttribute('data-idea-content') || '').filter(Boolean);
            if (all.length) {
                const joined = all.join('\n\n---\n\n');
                copyToClipboard(joined);
            } else {
                showToast('No ideas to copy', 'error');
            }
        });
    }
}

/**
 * Initialize form validations
 */
function initializeFormValidations() {
    // Password confirmation validation
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (passwordField && confirmPasswordField) {
        function validatePassword() {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity("Passwords don't match");
                confirmPasswordField.classList.add('is-invalid');
            } else {
                confirmPasswordField.setCustomValidity('');
                confirmPasswordField.classList.remove('is-invalid');
                if (confirmPasswordField.value.length >= 6) {
                    confirmPasswordField.classList.add('is-valid');
                }
            }
        }
        
        passwordField.addEventListener('input', validatePassword);
        confirmPasswordField.addEventListener('input', validatePassword);
    }
    
    // Email validation
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('input', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailRegex.test(this.value)) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
    
    // Niche textarea validation
    const nicheField = document.getElementById('niche');
    if (nicheField) {
        nicheField.addEventListener('input', function() {
            const length = this.value.trim().length;
            if (length >= 3) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    }
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Fade in animation for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize copy functionality
 */
function initializeCopyFunctionality() {
    // Add copy buttons to code blocks if any
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-secondary copy-btn';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.style.position = 'absolute';
        button.style.top = '10px';
        button.style.right = '10px';
        
        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
        
        button.addEventListener('click', () => {
            copyToClipboard(block.textContent);
        });
    });
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Could not copy text: ', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback copy method for older browsers
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Copied to clipboard!', 'success');
        } else {
            showToast('Failed to copy to clipboard', 'error');
        }
    } catch (err) {
        console.error('Fallback: Could not copy text: ', err);
        showToast('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show toast-notification`;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';
    toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    
    toast.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentNode) {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 150);
        }
    }, duration);
}

/**
 * Form submission with loading state
 */
function handleFormSubmission(formElement, buttonElement, loadingText = 'Processing...') {
    const originalText = buttonElement.innerHTML;
    const originalDisabled = buttonElement.disabled;
    
    formElement.addEventListener('submit', function() {
        buttonElement.disabled = true;
        buttonElement.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
        
        // Reset button after 30 seconds as fallback
        setTimeout(() => {
            buttonElement.disabled = originalDisabled;
            buttonElement.innerHTML = originalText;
        }, 30000);
    });
}

/**
 * Initialize form submission handlers
 */
document.addEventListener('DOMContentLoaded', function() {
    // Handle idea generation form
    const generateForm = document.querySelector('#generate-form');
    const generateBtn = document.querySelector('#generateBtn');
    if (generateForm && generateBtn) {
        handleFormSubmission(generateForm, generateBtn, 'Generating Ideas...');
    }
    
    // Handle login form
    const loginForm = document.querySelector('form[action*="login"]');
    const loginBtn = loginForm?.querySelector('button[type="submit"]');
    if (loginForm && loginBtn) {
        handleFormSubmission(loginForm, loginBtn, 'Signing In...');
    }
    
    // Handle register form
    const registerForm = document.querySelector('form[action*="register"]');
    const registerBtn = registerForm?.querySelector('button[type="submit"]');
    if (registerForm && registerBtn) {
        handleFormSubmission(registerForm, registerBtn, 'Creating Account...');
    }
});

/**
 * Utility function to format dates
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Utility function to truncate text
 */
function truncateText(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

/**
 * Initialize search functionality (if needed in future)
 */
function initializeSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            searchTimeout = setTimeout(() => {
                if (query.length >= 2) {
                    performSearch(query);
                } else {
                    clearSearchResults();
                }
            }, 300);
        });
    }
}

/**
 * Perform search (placeholder for future implementation)
 */
function performSearch(query) {
    console.log('Searching for:', query);
    // Implementation for search functionality
}

/**
 * Clear search results
 */
function clearSearchResults() {
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
}

/**
 * Initialize dark mode toggle (if implemented)
 */
function initializeDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.setAttribute('data-theme', savedTheme);
            darkModeToggle.checked = savedTheme === 'dark';
        }
        
        darkModeToggle.addEventListener('change', function() {
            const theme = this.checked ? 'dark' : 'light';
            document.body.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        });
    }
}

/**
 * Handle responsive navigation
 */
function initializeResponsiveNav() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on links
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
    }
}

// Initialize responsive navigation
document.addEventListener('DOMContentLoaded', initializeResponsiveNav);
