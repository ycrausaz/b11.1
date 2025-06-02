// static/js/modules/validation-core.js

// Global flag to prevent double initialization
let validationInitialized = false;

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

// Initialize material-user management functionality
function initializeMaterialUserManagement() {
    console.log("Initializing material-user management...");
    
    // Initialize bulk assignment form if it exists
    if (document.getElementById('bulk-assignment-form')) {
        initializeBulkAssignmentForm();
    }
    
    // Initialize material assignment detail form if it exists
    if (document.getElementById('assignment-form')) {
        initializeMaterialAssignmentDetailForm();
    }
}

// Initialize bulk assignment form functionality
function initializeBulkAssignmentForm() {
    // Toggle all materials button
    const toggleMaterialsBtn = document.getElementById('toggle-all-materials');
    if (toggleMaterialsBtn) {
        toggleMaterialsBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.material-checkbox input[type="checkbox"]');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            checkboxes.forEach(cb => cb.checked = !allChecked);
        });
    }

    // Toggle all users button
    const toggleUsersBtn = document.getElementById('toggle-all-users');
    if (toggleUsersBtn) {
        toggleUsersBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.user-checkbox input[type="checkbox"]');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            checkboxes.forEach(cb => cb.checked = !allChecked);
        });
    }

    // Add confirmation for bulk operations
    const bulkForm = document.getElementById('bulk-assignment-form');
    if (bulkForm) {
        bulkForm.addEventListener('submit', function(e) {
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
}

// Initialize material assignment detail form functionality
function initializeMaterialAssignmentDetailForm() {
    console.log("Initializing material assignment detail form...");
    
    const assignedUsersCheckboxes = document.querySelectorAll('#id_assigned_users input[type="checkbox"]');
    const primaryUserSelect = document.getElementById('id_primary_user');
    
    if (!assignedUsersCheckboxes.length || !primaryUserSelect) {
        console.log("Required elements not found for material assignment detail form");
        return;
    }
    
    // Enhanced form validation and interaction
    const form = document.getElementById('assignment-form');
    
    if (form) {
        // Form submission confirmation
        form.addEventListener('submit', function(e) {
            const assignedCount = Array.from(assignedUsersCheckboxes).filter(cb => cb.checked).length;
            const primaryUser = primaryUserSelect.value;
            
            if (assignedCount === 0 && primaryUser) {
                if (!confirm('You have selected a primary user but no assigned users. The primary user will be automatically assigned. Continue?')) {
                    e.preventDefault();
                    return;
                }
            }
            
            if (assignedCount === 0 && !primaryUser) {
                if (!confirm('You are about to remove all user assignments from this material. Continue?')) {
                    e.preventDefault();
                    return;
                }
            }
        });
    }
    
    console.log("Material assignment detail form initialized.");
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
    if ($('#add-attachment').length > 0 && window.AttachmentHandler) {
        window.AttachmentHandler.initializeAttachmentHandlers();
    }
    
    // Initialize conditional requirements
    initializeConditionalRequirements();
    
    // Initialize material-user management
    initializeMaterialUserManagement();
    
    // Initialize material list handlers (for list pages)
    if (document.querySelector('[id^="material-form-"]') && window.MassEditHandler) {
        window.MassEditHandler.initializeMaterialListHandlers();
    }
    
    // Initialize mass edit handlers if mass edit elements exist
    if ((document.querySelector('.mass-edit-table') || document.getElementById('select-all-fields')) && window.MassEditHandler) {
        window.MassEditHandler.initializeMassEditHandlers();
    }
    
    // Initialize tabular mass edit functionality
    if (window.TabularEditor) {
        window.TabularEditor.initializeTabularMassEdit();
    }
    
    // Mark as initialized
    validationInitialized = true;
    console.log('Validation functionality initialized.');
}

// Legacy function aliases for backwards compatibility
function clearSelection() {
    if (window.TabularEditor) {
        window.TabularEditor.clearAllSelections();
    }
}

function showCopySuccessMessage(value, columnName, count) {
    if (window.TabularEditor) {
        window.TabularEditor.showMultiCopySuccessMessage([{
            columnName: columnName,
            value: value,
            count: count
        }], count);
    }
}

// Make functions available globally
window.ValidationUtils = {
    validateFileSize: window.AttachmentHandler?.validateFileSize,
    updateAddAttachmentButton: window.AttachmentHandler?.updateAddAttachmentButton,
    updateRequiredStatus,
    initializeValidations,
    initializeMassEditHandlers: window.MassEditHandler?.initializeMassEditHandlers,
    initializeTabularMassEdit: window.TabularEditor?.initializeTabularMassEdit,
    initializeTabularChangeTracking: window.TabularEditor?.initializeTabularChangeTracking,
    initializeCellSelection: window.TabularEditor?.initializeCellSelection,
    initializeMaterialListHandlers: window.MassEditHandler?.initializeMaterialListHandlers,
    initializeMaterialUserManagement,
    clearSelection,
    showCopySuccessMessage,
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
