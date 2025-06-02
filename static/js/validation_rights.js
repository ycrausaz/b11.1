// File validation constants
const MAX_FILE_SIZE = 2.5 * 1024 * 1024; // 2.5MB in bytes
const MAX_ATTACHMENTS = 5;

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

// ===== MATERIAL-USER MANAGEMENT FUNCTIONS =====

// Toggle all materials in bulk assignment form
function toggleAllMaterials() {
    const checkboxes = document.querySelectorAll('.material-checkbox input[type="checkbox"]');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => cb.checked = !allChecked);
}

// Toggle all users in bulk assignment form
function toggleAllUsers() {
    const checkboxes = document.querySelectorAll('.user-checkbox input[type="checkbox"]');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => cb.checked = !allChecked);
}

// Initialize material-user management functionality
function initializeMaterialUserManagement() {
    // Check if we're on the material-user management page
    if ($('#bulk-assignment-form').length === 0) {
        return;
    }

    // Toggle all materials button
    $('#toggle-all-materials').click(function() {
        toggleAllMaterials();
    });

    // Toggle all users button
    $('#toggle-all-users').click(function() {
        toggleAllUsers();
    });

    // Add confirmation for bulk operations
    $('#bulk-assignment-form').submit(function(e) {
        const selectedMaterials = document.querySelectorAll('.material-checkbox input:checked').length;
        const selectedUsers = document.querySelectorAll('.user-checkbox input:checked').length;
        const action = document.querySelector('input[name="action"]:checked');
        
        if (selectedMaterials === 0 || selectedUsers === 0) {
            e.preventDefault();
            alert('Please select at least one material and one user.');
            return;
        }
        
        if (!action) {
            e.preventDefault();
            alert('Please select an action.');
            return;
        }
        
        const actionValue = action.value;
        const actionText = {
            'assign': 'assign',
            'remove': 'remove',
            'replace': 'replace all assignments for'
        };
        
        if (!confirm(`Are you sure you want to ${actionText[actionValue]} ${selectedUsers} user(s) to/from ${selectedMaterials} material(s)?`)) {
            e.preventDefault();
        }
    });
}

// Main initialization function
function initializeValidations() {
    if ($('#add-attachment').length > 0) {
        initializeAttachmentHandlers();
    }
    
    initializeConditionalRequirements();
    initializeMaterialUserManagement();
}

// Make functions available globally
window.ValidationUtils = {
    validateFileSize,
    updateAddAttachmentButton,
    updateRequiredStatus,
    initializeValidations,
    toggleAllMaterials,
    toggleAllUsers,
    initializeMaterialUserManagement
};

// Initialize when DOM is ready
$(document).ready(function() {
    initializeValidations();
});
