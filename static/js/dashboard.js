/**
 * Dashboard JavaScript functionality
 * Handles form validation, calendar integration, and UI interactions
 */

// Global variables
let calendar = null;
let currentToasts = [];

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

/**
 * Initialize dashboard functionality
 */
function initializeDashboard() {
    initializeCalendar();
    initializeForms();
    initializeEventListeners();
    initializeAnimations();
    loadDashboardData();

    console.log('Dashboard initialized successfully');
}

/**
 * Initialize FullCalendar
 */
function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        console.warn('Calendar element not found');
        return;
    }

    try {
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            height: 'auto',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,listWeek'
            },
            buttonText: {
                today: 'Today',
                month: 'Month',
                week: 'Week',
                list: 'List'
            },
            events: function(fetchInfo, successCallback, failureCallback) {
                fetchCalendarEvents(fetchInfo, successCallback, failureCallback);
            },
            eventClick: function(info) {
                handleEventClick(info);
            },
            dateClick: function(info) {
                handleDateClick(info);
            },
            eventDidMount: function(info) {
                // Add custom styling based on event type
                const eventType = info.event.extendedProps.type;
                if (eventType) {
                    info.el.classList.add(`fc-event-${eventType}`);
                }

                // Add priority styling
                const priority = info.event.extendedProps.priority;
                if (priority) {
                    info.el.classList.add(`priority-${priority}`);
                }
            },
            loading: function(bool) {
                const loadingEl = document.getElementById('calendar-loading');
                if (loadingEl) {
                    loadingEl.style.display = bool ? 'block' : 'none';
                }
            }
        });

        calendar.render();
    } catch (error) {
        console.error('Failed to initialize calendar:', error);
        showCalendarFallback();
    }
}

/**
 * Fetch calendar events from the server
 */
function fetchCalendarEvents(fetchInfo, successCallback, failureCallback) {
    const startStr = fetchInfo.start.toISOString();
    const endStr = fetchInfo.end.toISOString();

    // This would typically fetch from your Django backend
    // For now, we'll use dummy data
    const events = getDummyEvents(fetchInfo.start, fetchInfo.end);
    successCallback(events);
}

/**
 * Get dummy events for testing
 */
function getDummyEvents(start, end) {
    return [
        {
            id: '1',
            title: 'Math Assignment Due',
            start: new Date().toISOString().split('T')[0],
            backgroundColor: '#ef4444',
            borderColor: '#dc2626',
            extendedProps: {
                type: 'assignment',
                priority: 'high',
                course: 'Mathematics'
            }
        },
        {
            id: '2',
            title: 'Physics Exam',
            start: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            backgroundColor: '#f59e0b',
            borderColor: '#d97706',
            extendedProps: {
                type: 'exam',
                priority: 'urgent',
                course: 'Physics'
            }
        }
    ];
}

/**
 * Handle calendar event click
 */
function handleEventClick(info) {
    const event = info.event;
    const eventDetails = `
        <strong>${event.title}</strong><br>
        Date: ${event.start.toLocaleDateString()}<br>
        Course: ${event.extendedProps.course || 'N/A'}<br>
        Priority: ${event.extendedProps.priority || 'Normal'}
    `;

    showToast(eventDetails, 'info', 5000);
}

/**
 * Handle calendar date click
 */
function handleDateClick(info) {
    const selectedDate = info.dateStr;
    console.log('Date clicked:', selectedDate);

    // You could open a modal to create new events here
    showToast(`Selected date: ${selectedDate}`, 'info');
}

/**
 * Show calendar fallback when FullCalendar fails
 */
function showCalendarFallback() {
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        calendarEl.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-times"></i>
                <p>Calendar could not be loaded. Please refresh the page.</p>
                <button class="btn btn-primary" onclick="initializeCalendar()">
                    <i class="fas fa-redo"></i> Retry
                </button>
            </div>
        `;
    }
}

/**
 * Initialize all forms
 */
function initializeForms() {
    const forms = document.querySelectorAll('form[data-validate="true"]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit(this);
        });
    });
}

/**
 * Handle form submission
 */
function handleFormSubmit(form) {
    const formType = form.dataset.formType;
    let isValid = false;

    // Clear previous validation states
    clearFormValidation(form);

    // Validate based on form type
    switch (formType) {
        case 'course':
            isValid = validateCourseForm(form);
            break;
        case 'assignment':
            isValid = validateAssignmentForm(form);
            break;
        case 'exam':
            isValid = validateExamForm(form);
            break;
        case 'event':
            isValid = validateEventForm(form);
            break;
        default:
            isValid = validateGenericForm(form);
    }

    if (isValid) {
        submitForm(form);
    }
}

/**
 * Validate course form
 */
function validateCourseForm(form) {
    const requiredFields = ['course-name', 'course-code', 'instructor'];
    return validateRequiredFields(form, requiredFields);
}

/**
 * Validate assignment form
 */
function validateAssignmentForm(form) {
    const requiredFields = ['assignment-title', 'assignment-course', 'assignment-due_date'];
    let isValid = validateRequiredFields(form, requiredFields);

    // Additional validation for due date
    const dueDateField = form.querySelector('[name="assignment-due_date"]');
    if (dueDateField && dueDateField.value) {
        const dueDate = new Date(dueDateField.value);
        const today = new Date();

        if (dueDate < today) {
            showFieldError(dueDateField, 'Due date cannot be in the past');
            isValid = false;
        }
    }

    return isValid;
}

/**
 * Validate exam form
 */
function validateExamForm(form) {
    const requiredFields = ['exam-title', 'exam-course', 'exam-date', 'exam-time'];
    let isValid = validateRequiredFields(form, requiredFields);

    // Additional validation for exam date
    const examDateField = form.querySelector('[name="exam-date"]');
    if (examDateField && examDateField.value) {
        const examDate = new Date(examDateField.value);
        const today = new Date();

        if (examDate < today) {
            showFieldError(examDateField, 'Exam date cannot be in the past');
            isValid = false;
        }
    }

    return isValid;
}

/**
 * Validate event form
 */
function validateEventForm(form) {
    const requiredFields = ['event-title', 'event-date', 'event-time'];
    return validateRequiredFields(form, requiredFields);
}

/**
 * Validate generic form
 */
function validateGenericForm(form) {
    const requiredFields = Array.from(form.querySelectorAll('[required]')).map(field => field.name);
    return validateRequiredFields(form, requiredFields);
}

/**
 * Validate required fields
 */
function validateRequiredFields(form, fieldNames) {
    let isValid = true;

    fieldNames.forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (!field) return;

        const value = field.value.trim();

        if (!value) {
            showFieldError(field, `${getFieldLabel(fieldName)} is required`);
            isValid = false;
        } else {
            showFieldSuccess(field);
        }
    });

    return isValid;
}

/**
 * Get field label from field name
 */
function getFieldLabel(fieldName) {
    return fieldName
        .replace(/^.*-/, '') // Remove prefix
        .replace(/_/g, ' ') // Replace underscores with spaces
        .replace(/\b\w/g, l => l.toUpperCase()); // Capitalize
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    field.classList.remove('form-success');
    field.classList.add('form-error');

    // Remove existing error message
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

/**
 * Show field success
 */
function showFieldSuccess(field) {
    field.classList.remove('form-error');
    field.classList.add('form-success');

    // Remove error message
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Clear form validation
 */
function clearFormValidation(form) {
    const fields = form.querySelectorAll('.form-error, .form-success');
    fields.forEach(field => {
        field.classList.remove('form-error', 'form-success');
    });

    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach(msg => msg.remove());
}

/**
 * Submit form via AJAX
 */
function submitForm(form) {
    setFormLoading(form, true);

    const formData = new FormData(form);
    const url = form.action || window.location.href;

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        setFormLoading(form, false);

        if (data.success) {
            showToast(data.message || 'Successfully saved!', 'success');
            form.reset();
            clearFormValidation(form);

            // Refresh calendar if it exists
            if (calendar) {
                calendar.refetchEvents();
            }

            // Refresh page data
            loadDashboardData();
        } else {
            showToast(data.message || 'An error occurred', 'error');
        }
    })
    .catch(error => {
        setFormLoading(form, false);
        console.error('Form submission error:', error);
        showToast('An error occurred while saving', 'error');
    });
}

/**
 * Get CSRF token
 */
function getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

/**
 * Set form loading state
 */
function setFormLoading(form, isLoading) {
    const submitBtn = form.querySelector('button[type="submit"]');

    if (submitBtn) {
        submitBtn.disabled = isLoading;

        if (isLoading) {
            submitBtn.classList.add('btn-loading');
            submitBtn.dataset.originalText = submitBtn.innerHTML;
        } else {
            submitBtn.classList.remove('btn-loading');
            if (submitBtn.dataset.originalText) {
                submitBtn.innerHTML = submitBtn.dataset.originalText;
            }
        }
    }

    form.style.opacity = isLoading ? '0.7' : '1';
    form.style.pointerEvents = isLoading ? 'none' : 'auto';
}

/**
 * Initialize event listeners
 */
function initializeEventListeners() {
    // Toggle assignment completion
    document.addEventListener('click', function(e) {
        if (e.target.matches('.toggle-assignment')) {
            toggleAssignment(e.target);
        }

        // Handle delete buttons
        if (e.target.matches('.delete-item')) {
            handleDeleteItem(e.target);
        }

        // Handle edit buttons
        if (e.target.matches('.edit-item')) {
            handleEditItem(e.target);
        }
    });

    // Real-time form validation
    document.addEventListener('input', function(e) {
        if (e.target.matches('input, select, textarea')) {
            debounce(function() {
                validateFieldRealTime(e.target);
            }, 500)();
        }
    });

    // Handle form resets
    document.addEventListener('reset', function(e) {
        if (e.target.matches('form')) {
            clearFormValidation(e.target);
        }
    });
}

/**
 * Toggle assignment completion
 */
function toggleAssignment(element) {
    const assignmentId = element.dataset.assignmentId;
    const isCompleted = element.checked;

    fetch('/toggle-assignment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            assignment_id: assignmentId,
            completed: isCompleted
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const listItem = element.closest('.list-item');
            if (listItem) {
                if (isCompleted) {
                    listItem.classList.add('completed-item');
                } else {
                    listItem.classList.remove('completed-item');
                }
            }

            showToast(data.message, 'success');

            // Update stats
            updateStats();
        } else {
            element.checked = !isCompleted; // Revert checkbox
            showToast(data.message || 'Failed to update assignment', 'error');
        }
    })
    .catch(error => {
        element.checked = !isCompleted; // Revert checkbox
        console.error('Toggle assignment error:', error);
        showToast('An error occurred', 'error');
    });
}

/**
 * Handle delete item
 */
function handleDeleteItem(element) {
    const itemId = element.dataset.itemId;
    const itemType = element.dataset.itemType;

    if (confirm(`Are you sure you want to delete this ${itemType}?`)) {
        fetch(`/delete-${itemType}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ id: itemId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const listItem = element.closest('.list-item');
                if (listItem) {
                    listItem.remove();
                }

                showToast(`${itemType} deleted successfully`, 'success');
                updateStats();

                if (calendar) {
                    calendar.refetchEvents();
                }
            } else {
                showToast(data.message || 'Failed to delete item', 'error');
            }
        })
        .catch(error => {
            console.error('Delete error:', error);
            showToast('An error occurred while deleting', 'error');
        });
    }
}

/**
 * Handle edit item
 */
function handleEditItem(element) {
    const itemId = element.dataset.itemId;
    const itemType = element.dataset.itemType;

    // This would typically open a modal or navigate to edit page
    console.log(`Edit ${itemType} with ID: ${itemId}`);
    showToast(`Edit functionality not implemented yet`, 'warning');
}

/**
 * Validate field in real-time
 */
function validateFieldRealTime(field) {
    if (!field.value.trim()) {
        field.classList.remove('form-success', 'form-error');
        return;
    }

    // Basic validation
    let isValid = true;
    let errorMessage = '';

    // Email validation
    if (field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }

    // Date validation
    if (field.type === 'date') {
        const date = new Date(field.value);
        const today = new Date();

        if (date < today && field.name.includes('due_date')) {
            isValid = false;
            errorMessage = 'Date cannot be in the past';
        }
    }

    if (isValid) {
        showFieldSuccess(field);
    } else {
        showFieldError(field, errorMessage);
    }
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.stats-card, .section-card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in-up');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Intersection Observer for scroll animations
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });

        document.querySelectorAll('.section-card').forEach(card => {
            observer.observe(card);
        });
    }
}

/**
 * Load dashboard data
 */
function loadDashboardData() {
    updateStats();
    updateRecentItems();
    updateUpcomingItems();
}

/**
 * Update statistics
 */
function updateStats() {
    fetch('/api/stats/')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateStatCard('total-assignments', data.stats.total_assignments);
            updateStatCard('pending-assignments', data.stats.pending_assignments);
            updateStatCard('upcoming-exams', data.stats.upcoming_exams);
            updateStatCard('total-courses', data.stats.total_courses);
        }
    })
    .catch(error => {
        console.error('Failed to update stats:', error);
    });
}

/**
 * Update stat card
 */
function updateStatCard(statName, value) {
    const statElement = document.querySelector(`.stats-card[data-stat="${statName}"] .stats-number`);
    if (statElement) {
        // Animate number change
        animateNumber(statElement, parseInt(statElement.textContent) || 0, value);
    }
}

/**
 * Animate number change
 */
function animateNumber(element, start, end) {
    const duration = 1000;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const current = Math.round(start + (end - start) * progress);
        element.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Update recent items
 */
function updateRecentItems() {
    // This would fetch recent assignments, exams, etc.
    // Implementation depends on your backend API
    console.log('Updating recent items...');
}

/**
 * Update upcoming items
 */
function updateUpcomingItems() {
    // This would fetch upcoming assignments, exams, etc.
    // Implementation depends on your backend API
    console.log('Updating upcoming items...');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 4000) {
    const toastId = Date.now();
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    toast.dataset.toastId = toastId;

    const icon = getToastIcon(type);
    const color = getToastColor(type);

    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="${icon}" style="color: ${color}; font-size: 1.1rem;"></i>
            <div style="flex: 1; font-weight: 500;">${message}</div>
            <button type="button" onclick="removeToast(${toastId})"
                    style="background: none; border: none; font-size: 1.2rem; cursor: pointer; opacity: 0.7;">
                &times;
            </button>
        </div>
    `;

    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    container.appendChild(toast);
    currentToasts.push(toastId);

    // Auto-remove
    setTimeout(() => {
        removeToast(toastId);
    }, duration);

    return toastId;
}

/**
 * Remove toast notification
 */
function removeToast(toastId) {
    const toast = document.querySelector(`[data-toast-id="${toastId}"]`);
    if (toast) {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    }

    currentToasts = currentToasts.filter(id => id !== toastId);
}

/**
 * Get toast icon based on type
 */
function getToastIcon(type) {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    return icons[type] || icons.info;
}

/**
 * Get toast color based on type
 */
function getToastColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#06b6d4'
    };
    return colors[type] || colors.info;
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility function to debug log
 */
function debugLog(message, data = null) {
    if (console && console.log) {
        console.log(`[Dashboard Debug] ${message}`, data);
    }
}

// Add CSS animation for slide out
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
`;
document.head.appendChild(style);

// Make functions globally available
window.removeToast = removeToast;
window.debugLog = debugLog;
