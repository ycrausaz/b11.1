// File validation constants
const MAX_FILE_SIZE = 2.5 * 1024 * 1024; // 2.5MB in bytes
const MAX_ATTACHMENTS = 5;

// Global flag to prevent double initialization
let validationInitialized = false;

// Validate file size
function validateFileSize(file) {
    if (file.size > MAX_FILE_SIZE) {
        alert(`File ${file.name} is too large. Maximum size is 2.5MB.`);
        return false;
    }
    return true;
}

// Update the add attachment button state
function updateAddAttachmentButton() {
    // Wait for DOM to be fully loaded
    setTimeout(() => {
        const existingCount = $('.existing-attachment-row').length;
        const newCount = $('.attachment-row').not('.existing-attachment-row').length;
        const deletedCount = $('input[name="delete_attachments[]"]:checked').length;
        const totalCount = existingCount + newCount - deletedCount;

        const addButton = $('#add-attachment');
        if (totalCount >= MAX_ATTACHMENTS) {
            addButton.prop('disabled', true);
            addButton.addClass('btn-secondary-disabled');
            addButton.attr('title', `Maximum of ${MAX_ATTACHMENTS} attachments reached`);
        } else {
            addButton.prop('disabled', false);
            addButton.removeClass('btn-secondary-disabled');
            addButton.attr('title', '');
        }
        console.log('Button state updated. Total attachments:', totalCount);
    }, 100);
}

// Handle toggling of attachment deletion
function initializeAttachmentDeleteToggle() {
    $(document).on('click', '.toggle-delete-btn', function() {
        const btn = $(this);
        const attachmentRow = btn.closest('.attachment-row');
        const attachmentLink = attachmentRow.find('.attachment-link');
        const commentInput = attachmentRow.find('input[type="text"]');
        const checkbox = attachmentRow.find('.attachment-delete-checkbox');
        
        if (btn.hasClass('btn-danger')) {
            // Switch to "Keep" mode
            btn.removeClass('btn-danger').addClass('btn-success');
            btn.text('Keep');
            attachmentLink.css('text-decoration', 'line-through');
            commentInput.css('text-decoration', 'line-through');
            checkbox.prop('checked', true);
        } else {
            // Switch to "Delete" mode
            btn.removeClass('btn-success').addClass('btn-danger');
            btn.text('Delete');
            attachmentLink.css('text-decoration', 'none');
            commentInput.css('text-decoration', 'none');
            checkbox.prop('checked', false);
        }
        
        // Update attachment button state after toggling deletion
        updateAddAttachmentButton();
    });
}

// Initialize attachment handlers
function initializeAttachmentHandlers() {
    // Initialize button state on page load
    updateAddAttachmentButton();

    // Also initialize after a short delay to ensure all elements are loaded
    setTimeout(updateAddAttachmentButton, 500);

    // Initialize attachment delete toggle
    initializeAttachmentDeleteToggle();

    // Add attachment button handler
    $('#add-attachment').click(function() {
        const existingCount = $('.existing-attachment-row').length;
        const newCount = $('.attachment-row').not('.existing-attachment-row').length;
        const deletedCount = $('input[name="delete_attachments[]"]:checked').length;
        const totalCount = existingCount + newCount - deletedCount;

        if (totalCount >= MAX_ATTACHMENTS) {
            alert(`Cannot have more than ${MAX_ATTACHMENTS} attachments per material.`);
            return;
        }

        const newRow = $('.attachment-row').not('.existing-attachment-row').first().clone();
        newRow.find('input').val('');
        $('#attachments-container').append(newRow);

        updateAddAttachmentButton();
    });

    // Remove attachment handler
    $(document).on('click', '.remove-attachment', function() {
        if ($('.attachment-row').not('.existing-attachment-row').length > 1) {
            $(this).closest('.attachment-row').remove();
        } else {
            $('.attachment-row').not('.existing-attachment-row').first().find('input').val('');
        }
        updateAddAttachmentButton();
    });

    // Handle deletion of existing attachments
    $(document).on('change', 'input[name="delete_attachments[]"]', function() {
        updateAddAttachmentButton();
    });

    // File input change handler
    $(document).on('change', 'input[type="file"]', function() {
        const file = this.files[0];
        if (file && !validateFileSize(file)) {
            $(this).val(''); // Clear the file input
        }
    });

    // Form submit handler for attachments
    $('form').submit(function(e) {
        // Only apply this to forms with file inputs
        if ($(this).find('input[type="file"]').length === 0) {
            return true;
        }
        
        const files = $('input[type="file"]').get().filter(input => input.files.length > 0);

        // Validate all file sizes
        for (let input of files) {
            if (!validateFileSize(input.files[0])) {
                e.preventDefault();
                return false;
            }
        }

        // Count total attachments (existing + new - deleted)
        const existingCount = $('.existing-attachment-row').length;
        const deletedCount = $('input[name="delete_attachments[]"]:checked').length;
        const newCount = files.length;
        const totalCount = existingCount - deletedCount + newCount;

        if (totalCount > MAX_ATTACHMENTS) {
            alert(`Cannot have more than ${MAX_ATTACHMENTS} attachments per material.`);
            e.preventDefault();
            return false;
        }
    });
}

// Mass Edit functionality
function initializeMassEditHandlers() {
    const selectAllBtn = document.getElementById('select-all-fields');
    const deselectAllBtn = document.getElementById('deselect-all-fields');
    const updateCheckboxes = document.querySelectorAll('.update-checkbox:not([disabled])');

    // Select all fields button
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            updateCheckboxes.forEach(function(checkbox) {
                checkbox.checked = true;
            });
        });
    }

    // Deselect all fields button
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', function() {
            updateCheckboxes.forEach(function(checkbox) {
                checkbox.checked = false;
            });
        });
    }

    // Form submission confirmation for mass edit
    const massEditForm = document.querySelector('form[action*="mass-update"]') || 
                        (document.querySelector('.mass-edit-table') ? document.querySelector('form') : null);
    
    if (massEditForm) {
        massEditForm.addEventListener('submit', function(e) {
            const checkedBoxes = document.querySelectorAll('.update-checkbox:checked:not([disabled])');
            
            if (checkedBoxes.length === 0) {
                e.preventDefault();
                alert('Bitte wählen Sie mindestens ein Feld zum Aktualisieren aus.');
                return false;
            }
            
            // Get material count from hidden inputs
            const materialCount = document.querySelectorAll('input[name="material_ids"]').length;
            const fieldCount = checkedBoxes.length;
            
            const materialText = materialCount > 1 ? 'ien' : '';
            const fieldText = fieldCount > 1 ? 'er' : '';
            
            if (!confirm(`Sie werden ${fieldCount} Feld${fieldText} in ${materialCount} Material${materialText} aktualisieren. Sind Sie sicher?`)) {
                e.preventDefault();
                return false;
            }
        });
    }
}

// Conditional requirement handling for manufacturer fields
function updateRequiredStatus() {
    var cageCode = $('#id_cage_code').val();
    var herstellerName = $('#id_hersteller_name').val();
    var herstellerAdresse = $('#id_hersteller_adresse').val();
    var herstellerPlz = $('#id_hersteller_plz').val();
    var herstellerOrt = $('#id_hersteller_ort').val();
    
    // If cage_code is empty, hersteller fields are required
    if (!cageCode) {
        $('#hersteller_name_required, #hersteller_adresse_required, #hersteller_plz_required, #hersteller_ort_required').show();
    } else {
        $('#hersteller_name_required, #hersteller_adresse_required, #hersteller_plz_required, #hersteller_ort_required').hide();
    }
    
    // If any hersteller field is empty, cage_code is required
    if (!herstellerName || !herstellerAdresse || !herstellerPlz || !herstellerOrt) {
        $('#cage_code_required').show();
    } else {
        $('#cage_code_required').hide();
    }
}

// Initialize conditional requirement handling
function initializeConditionalRequirements() {
    if ($('#id_cage_code').length > 0) {
        // Initial state
        updateRequiredStatus();
        
        // Bind to input events
        $('#id_cage_code, #id_hersteller_name, #id_hersteller_adresse, #id_hersteller_plz, #id_hersteller_ort').on('input change', function() {
            updateRequiredStatus();
        });
    }
}

// ===== TABULAR MASS EDIT FUNCTIONALITY =====

// Track changes in form fields for tabular editing
function initializeTabularChangeTracking() {
    const originalValues = new Map();
    
    // Store original values
    document.querySelectorAll('#tabular-form input, #tabular-form select, #tabular-form textarea').forEach(function(field) {
        originalValues.set(field.name, field.value);
        
        // Add change listener
        field.addEventListener('change', function() {
            const cell = this.closest('td');
            if (cell) {
                if (this.value !== originalValues.get(this.name)) {
                    cell.classList.add('changed-cell');
                } else {
                    cell.classList.remove('changed-cell');
                }
            }
        });
    });
    
    return originalValues;
}

// Column copy functionality for tabular editing
function initializeColumnCopyFunctionality() {
    const copyColumnBtn = document.getElementById('copy-column-btn');
    const confirmCopyBtn = document.getElementById('confirm-copy-btn');
    
    if (!copyColumnBtn || !confirmCopyBtn) return;
    
    // Remove any existing event listeners to prevent duplicates
    copyColumnBtn.removeEventListener('click', copyColumnBtn._clickHandler);
    confirmCopyBtn.removeEventListener('click', confirmCopyBtn._clickHandler);
    
    // Define click handlers
    copyColumnBtn._clickHandler = function() {
        const modal = new bootstrap.Modal(document.getElementById('copyColumnModal'));
        modal.show();
    };

    confirmCopyBtn._clickHandler = function() {
        const selectedColumn = document.getElementById('column-select').value;
        if (!selectedColumn) {
            alert('Bitte wählen Sie eine Spalte aus.');
            return;
        }

        // Find all fields with this column name
        const fields = document.querySelectorAll(`[name*="${selectedColumn}"]`);
        if (fields.length === 0) {
            alert('Keine Felder für diese Spalte gefunden.');
            return;
        }

        // Get the value from the first field
        const firstFieldValue = fields[0].value;
        const firstFieldType = fields[0].type;

        // Copy to all other fields
        for (let i = 1; i < fields.length; i++) {
            if (firstFieldType === 'checkbox') {
                fields[i].checked = fields[0].checked;
            } else {
                fields[i].value = firstFieldValue;
            }
            
            // Trigger change event to update styling
            fields[i].dispatchEvent(new Event('change'));
        }

        const modal = bootstrap.Modal.getInstance(document.getElementById('copyColumnModal'));
        modal.hide();
        
        alert(`Wert wurde in alle Zeilen der Spalte "${selectedColumn}" kopiert.`);
    };
    
    // Add event listeners
    copyColumnBtn.addEventListener('click', copyColumnBtn._clickHandler);
    confirmCopyBtn.addEventListener('click', confirmCopyBtn._clickHandler);
}

// Form reset functionality for tabular editing
function initializeTabularFormReset(originalValues) {
    const resetFormBtn = document.getElementById('reset-form-btn');
    
    if (!resetFormBtn) return;
    
    // Remove any existing event listener to prevent duplicates
    if (resetFormBtn._clickHandler) {
        resetFormBtn.removeEventListener('click', resetFormBtn._clickHandler);
    }
    
    // Define the click handler
    resetFormBtn._clickHandler = function() {
        if (confirm('Sind Sie sicher, dass Sie alle Änderungen zurücksetzen möchten?')) {
            document.querySelectorAll('#tabular-form input, #tabular-form select, #tabular-form textarea').forEach(function(field) {
                const originalValue = originalValues.get(field.name);
                if (field.type === 'checkbox') {
                    field.checked = originalValue === 'on' || originalValue === true;
                } else {
                    field.value = originalValue || '';
                }
                
                // Remove change highlighting
                const cell = field.closest('td');
                if (cell) {
                    cell.classList.remove('changed-cell');
                }
            });
        }
    };
    
    // Add event listener
    resetFormBtn.addEventListener('click', resetFormBtn._clickHandler);
}

// Keyboard navigation for tabular editing
function initializeTabularKeyboardNavigation() {
    // Remove existing event listener if it exists
    if (document._tabularKeydownHandler) {
        document.removeEventListener('keydown', document._tabularKeydownHandler);
    }
    
    // Define the keydown handler
    document._tabularKeydownHandler = function(e) {
        // Only apply to tabular form fields
        if (!document.getElementById('tabular-form')) return;
        
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
            let nextField = null;
            
            switch(e.key) {
                case 'ArrowRight':
                    nextField = getNextField(e.target, 'right');
                    break;
                case 'ArrowLeft':
                    nextField = getNextField(e.target, 'left');
                    break;
                case 'ArrowDown':
                    nextField = getNextField(e.target, 'down');
                    break;
                case 'ArrowUp':
                    nextField = getNextField(e.target, 'up');
                    break;
            }
            
            if (nextField) {
                e.preventDefault();
                nextField.focus();
            }
        }
    };
    
    // Add event listener
    document.addEventListener('keydown', document._tabularKeydownHandler);
}

// Helper function to get next field for keyboard navigation
function getNextField(currentField, direction) {
    const currentCell = currentField.closest('td');
    const currentRow = currentCell.closest('tr');
    
    let targetCell = null;
    
    switch(direction) {
        case 'right':
            targetCell = currentCell.nextElementSibling;
            break;
        case 'left':
            targetCell = currentCell.previousElementSibling;
            if (targetCell && targetCell.classList.contains('sticky-column')) {
                targetCell = null; // Skip the material name column
            }
            break;
        case 'down':
            const nextRow = currentRow.nextElementSibling;
            if (nextRow) {
                const cellIndex = Array.from(currentRow.children).indexOf(currentCell);
                targetCell = nextRow.children[cellIndex];
            }
            break;
        case 'up':
            const prevRow = currentRow.previousElementSibling;
            if (prevRow && !prevRow.querySelector('th')) { // Skip header row
                const cellIndex = Array.from(currentRow.children).indexOf(currentCell);
                targetCell = prevRow.children[cellIndex];
            }
            break;
    }
    
    if (targetCell) {
        const field = targetCell.querySelector('input, select, textarea');
        if (field && !field.disabled) {
            return field;
        }
    }
    
    return null;
}

// Auto-save functionality (optional)
function initializeTabularAutoSave() {
    let autoSaveTimeout;
    document.querySelectorAll('#tabular-form input, #tabular-form select, #tabular-form textarea').forEach(function(field) {
        field.addEventListener('input', function() {
            clearTimeout(autoSaveTimeout);
            autoSaveTimeout = setTimeout(function() {
                // You could implement auto-save here if needed
                console.log('Auto-save triggered');
            }, 2000);
        });
    });
}

// Initialize tabular mass edit functionality
function initializeTabularMassEdit() {
    // Only initialize if we're on a tabular mass edit page
    if (!document.getElementById('tabular-form')) return;
    
    console.log('Initializing tabular mass edit functionality...');
    
    // Initialize change tracking and get original values
    const originalValues = initializeTabularChangeTracking();
    
    // Initialize other tabular functionalities
    initializeColumnCopyFunctionality();
    initializeTabularFormReset(originalValues);
    initializeTabularKeyboardNavigation();
    initializeTabularAutoSave();
    
    console.log('Tabular mass edit functionality initialized.');
}

// Main initialization function
function initializeValidations() {
    // Prevent double initialization
    if (validationInitialized) {
        console.log('Validation already initialized, skipping...');
        return;
    }
    
    console.log('Initializing validation functionality...');
    
    // Initialize attachment handlers if attachment elements exist
    if ($('#add-attachment').length > 0) {
        initializeAttachmentHandlers();
    }
    
    // Initialize conditional requirements
    initializeConditionalRequirements();
    
    // Initialize mass edit handlers if mass edit elements exist
    if (document.querySelector('.mass-edit-table') || document.getElementById('select-all-fields')) {
        initializeMassEditHandlers();
    }
    
    // Initialize tabular mass edit functionality
    initializeTabularMassEdit();
    
    // Mark as initialized
    validationInitialized = true;
    console.log('Validation functionality initialized.');
}

// Make functions available globally
window.ValidationUtils = {
    validateFileSize,
    updateAddAttachmentButton,
    updateRequiredStatus,
    initializeValidations,
    initializeMassEditHandlers,
    initializeTabularMassEdit,
    initializeTabularChangeTracking,
    initializeColumnCopyFunctionality,
    initializeTabularKeyboardNavigation,
    initialized: false
};

// Initialize when DOM is ready
$(document).ready(function() {
    initializeValidations();
    window.ValidationUtils.initialized = true;
});

// Also initialize when content is loaded (for compatibility)
document.addEventListener('DOMContentLoaded', function() {
    // Only run if jQuery is not available or hasn't run yet
    if (typeof $ === 'undefined' && !validationInitialized) {
        initializeValidations();
        window.ValidationUtils.initialized = true;
    }
});
