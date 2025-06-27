// Main JavaScript file for Starboi WebApp

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-info):not(.alert-secondary)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Date input validation
    var dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            validateDateLogic();
        });
    });

    // Real-time filter update
    var filterForm = document.querySelector('form[action*="index"]');
    if (filterForm) {
        var filterInputs = filterForm.querySelectorAll('input, select');
        filterInputs.forEach(function(input) {
            if (input.type !== 'submit') {
                input.addEventListener('change', function() {
                    // Auto-submit filter form on change
                    setTimeout(function() {
                        filterForm.submit();
                    }, 100);
                });
            }
        });
    }

    // Statistics auto-refresh (every 30 seconds)
    setInterval(refreshStatistics, 30000);
});

// Delete confirmation function
function confirmDelete(recordId) {
    var deleteModal = document.getElementById('deleteModal');
    var deleteForm = document.getElementById('deleteForm');
    
    if (deleteModal && deleteForm) {
        deleteForm.action = '/delete/' + recordId;
        var modal = new bootstrap.Modal(deleteModal);
        modal.show();
    } else {
        // Fallback if modal is not available
        if (confirm('Are you sure you want to delete this visa record? This action cannot be undone.')) {
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = '/delete/' + recordId;
            document.body.appendChild(form);
            form.submit();
        }
    }
}

// Validate date logic (ensure visa date is after submit date)
function validateDateLogic() {
    var submitDateInput = document.querySelector('input[name="file_submit_date"]');
    var visaDateInput = document.querySelector('input[name="visa_date"]');
    
    if (submitDateInput && visaDateInput && submitDateInput.value && visaDateInput.value) {
        var submitDate = new Date(submitDateInput.value);
        var visaDate = new Date(visaDateInput.value);
        
        if (visaDate < submitDate) {
            visaDateInput.setCustomValidity('Visa date cannot be before submit date');
            visaDateInput.classList.add('is-invalid');
            
            // Show custom error message
            var feedback = visaDateInput.parentElement.querySelector('.invalid-feedback');
            if (!feedback) {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                visaDateInput.parentElement.appendChild(feedback);
            }
            feedback.textContent = 'Visa date cannot be before submit date';
        } else {
            visaDateInput.setCustomValidity('');
            visaDateInput.classList.remove('is-invalid');
            var feedback = visaDateInput.parentElement.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.remove();
            }
        }
    }
}

// Refresh statistics via API
function refreshStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            // Update statistics cards
            var thisMonthEl = document.querySelector('.text-info');
            var thisYearEl = document.querySelector('.text-warning');
            var lifetimeEl = document.querySelector('.text-success');
            
            if (thisMonthEl) thisMonthEl.textContent = data.total_this_month;
            if (thisYearEl) thisYearEl.textContent = data.total_this_year;
            if (lifetimeEl) lifetimeEl.textContent = data.total_lifetime;
        })
        .catch(error => {
            console.log('Statistics refresh failed:', error);
        });
}

// Country-specific form enhancements
function enhanceCountrySelection() {
    var countrySelect = document.querySelector('select[name="country"]');
    if (countrySelect) {
        countrySelect.addEventListener('change', function() {
            var selectedCountry = this.value;
            
            // You could add country-specific form enhancements here
            // For example, show/hide certain fields based on country requirements
            
            console.log('Country selected:', selectedCountry);
        });
    }
}

// Payment amount formatting
function formatPaymentAmount() {
    var paymentInput = document.querySelector('input[name="payment_amount"]');
    if (paymentInput) {
        paymentInput.addEventListener('blur', function() {
            var value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    }
}

// Search functionality enhancement
function enhanceSearch() {
    var searchInput = document.querySelector('input[name="passport_no"]');
    if (searchInput) {
        var searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            var form = this.closest('form');
            
            // Debounce search to avoid too many requests
            searchTimeout = setTimeout(function() {
                if (searchInput.value.length >= 3 || searchInput.value.length === 0) {
                    form.submit();
                }
            }, 500);
        });
    }
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', function() {
    enhanceCountrySelection();
    formatPaymentAmount();
    enhanceSearch();
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N for new record
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/create';
    }
    
    // Escape key to close modals
    if (e.key === 'Escape') {
        var openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(function(modal) {
            var bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// Print functionality
function printRecord() {
    window.print();
}

// Export functionality (basic CSV export)
function exportToCSV() {
    // This would be implemented to export filtered results to CSV
    console.log('Export functionality would be implemented here');
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'Not set';
    var date = new Date(dateString);
    return date.toLocaleDateString();
}

function calculateDaysBetween(startDate, endDate) {
    if (!startDate || !endDate) return null;
    var start = new Date(startDate);
    var end = new Date(endDate);
    var diffTime = Math.abs(end - start);
    var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker would be registered here for offline functionality
        console.log('Service worker support detected');
    });
}
