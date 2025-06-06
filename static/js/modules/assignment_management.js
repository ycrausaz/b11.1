// ===== MATERIAL-USER MANAGEMENT FUNCTIONS =====

// Initialize material-user management functionality
export function initializeMaterialUserManagement() {
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
export function initializeBulkAssignmentForm() {
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
export function initializeMaterialAssignmentDetailForm() {
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

// ===== LEGACY AND UTILITY FUNCTIONS =====

