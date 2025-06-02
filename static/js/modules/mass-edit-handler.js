// static/js/modules/mass-edit-handler.js

// Initialize material list button handlers
function initializeMaterialListHandlers() {
    console.log('Initializing material list button handlers...');
    
    // Handle mass edit buttons
    document.querySelectorAll('.mass-edit-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const formId = this.getAttribute('data-form-id');
            const form = document.getElementById('material-form-' + formId);
            const checkedBoxes = form.querySelectorAll('.material-checkbox:checked');

            if (checkedBoxes.length === 0) {
                alert('Bitte wählen Sie mindestens ein Material für die Massenbearbeitung aus.');
                return;
            }

            const materialIds = Array.from(checkedBoxes).map(cb => cb.value);
            
            // Determine the correct URL based on the current page
            let massUpdateUrl;
            if (window.location.pathname.includes('lba')) {
                massUpdateUrl = '/lba/materials/mass-update/';
            } else if (window.location.pathname.includes('il')) {
                massUpdateUrl = '/il/materials/mass-update/';
            } else {
                massUpdateUrl = '/il/materials/mass-update/';
            }
            
            const url = massUpdateUrl + '?' + materialIds.map(id => 'materials=' + id).join('&');
            window.location.href = url;
        });
    });

    // Handle tabular material edit buttons
    document.querySelectorAll('.tabular-material-edit-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const formId = this.getAttribute('data-form-id');
            const form = document.getElementById('material-form-' + formId);
            const checkedBoxes = form.querySelectorAll('.material-checkbox:checked');

            if (checkedBoxes.length === 0) {
                alert('Bitte wählen Sie mindestens ein Material für die Material-Tabellen-Bearbeitung aus.');
                return;
            }

            const materialIds = Array.from(checkedBoxes).map(cb => cb.value);
            
            // Determine the correct URL based on the current page
            let tabularUpdateUrl;
            if (window.location.pathname.includes('lba')) {
                tabularUpdateUrl = '/lba/materials/tabular-materials-mass-update/';
            } else if (window.location.pathname.includes('il')) {
                tabularUpdateUrl = '/il/materials/tabular-materials-mass-update/';
            } else {
                tabularUpdateUrl = '/il/materials/tabular-materials-mass-update/';
            }
            
            const url = tabularUpdateUrl + '?' + materialIds.map(id => 'materials=' + id).join('&');
            window.location.href = url;
        });
    });

    // Handle tabular fields edit buttons
    document.querySelectorAll('.tabular-fields-edit-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const formId = this.getAttribute('data-form-id');
            const form = document.getElementById('material-form-' + formId);
            const checkedBoxes = form.querySelectorAll('.material-checkbox:checked');

            if (checkedBoxes.length === 0) {
                alert('Bitte wählen Sie mindestens ein Material für die Felder-Tabellen-Bearbeitung aus.');
                return;
            }

            const materialIds = Array.from(checkedBoxes).map(cb => cb.value);
            
            // Determine the correct URL based on the current page
            let fieldsTabularUpdateUrl;
            if (window.location.pathname.includes('lba')) {
                fieldsTabularUpdateUrl = '/lba/materials/tabular-fields-mass-update/';
            } else if (window.location.pathname.includes('il')) {
                fieldsTabularUpdateUrl = '/il/materials/tabular-fields-mass-update/';
            } else {
                fieldsTabularUpdateUrl = '/il/materials/tabular-fields-mass-update/';
            }
            
            const url = fieldsTabularUpdateUrl + '?' + materialIds.map(id => 'materials=' + id).join('&');
            window.location.href = url;
        });
    });
    
    console.log('Material list button handlers initialized.');
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

// Export functions for module use
window.MassEditHandler = {
    initializeMaterialListHandlers,
    initializeMassEditHandlers
};
