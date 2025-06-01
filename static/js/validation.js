// File validation constants
const MAX_FILE_SIZE = 2.5 * 1024 * 1024; // 2.5MB in bytes
const MAX_ATTACHMENTS = 5;

// Global flag to prevent double initialization
let validationInitialized = false;

// Validate file size
function validateFileSize(file) {
    console.log('validateFileSize');
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

// ===== MATERIAL LIST BUTTON HANDLERS =====

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
    
    // Store original values for both material and fields forms
    const selectors = ['#tabular-form input, #tabular-form select, #tabular-form textarea',
                      '#tabular-fields-form input, #tabular-fields-form select, #tabular-fields-form textarea'];
    
    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(function(field) {
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
    });
    
    return originalValues;
}

// ===== ENHANCED MULTI-CELL SELECTION FUNCTIONALITY =====

// Global variables for cell selection
let selectedCells = new Map(); // Map of column/field -> {cell, value, input}
let selectionMode = 'single'; // 'single' or 'multiple'

// Initialize cell selection functionality
function initializeCellSelection() {
    const copyBtn = document.getElementById('copy-value-btn');
    const selectedInfo = document.getElementById('selected-cell-info');
    const clearSelectionBtn = document.getElementById('clear-selection-btn');
    const modeToggleBtn = document.getElementById('mode-toggle-btn');
    
    if (!copyBtn || !selectedInfo) {
        console.log('Cell selection elements not found, skipping initialization');
        return;
    }
    
    console.log('Initializing enhanced multi-cell selection functionality...');
    
    // Initialize mode toggle button functionality
    if (modeToggleBtn) {
        modeToggleBtn.addEventListener('click', toggleSelectionMode);
        console.log('Mode toggle button initialized');
    } else {
        console.log('Mode toggle button not found');
    }
    
    // Handle cell selection for material-based tabular editing
    document.querySelectorAll('.editable-cell').forEach(function(cell) {
        cell.addEventListener('click', function(e) {
            // Don't interfere with form controls
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            const column = this.getAttribute('data-column');
            const rowIndex = this.getAttribute('data-row');
            
            if (selectionMode === 'single') {
                handleSingleCellSelection(this, column, rowIndex);
            } else {
                handleMultiCellSelection(this, column, rowIndex);
            }
            
            updateSelectionUI();
        });
    });
    
    // Handle copy button click
    copyBtn.addEventListener('click', function() {
        if (selectedCells.size === 0) {
            alert('Bitte wählen Sie zuerst mindestens eine Zelle aus.');
            return;
        }
        
        performCopyOperation();
    });
    
    // Handle clear selection
    if (clearSelectionBtn) {
        clearSelectionBtn.addEventListener('click', function() {
            clearAllSelections();
        });
    }
    
    // Clear selection when clicking outside table
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#materials-table') && 
            !e.target.closest('#fields-table') &&
            !e.target.closest('#copy-value-btn') && 
            !e.target.closest('#clear-selection-btn') &&
            !e.target.closest('#mode-toggle-btn')) {
            clearAllSelections();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+C or Cmd+C to copy
        if ((e.ctrlKey || e.metaKey) && e.key === 'c' && selectedCells.size > 0) {
            e.preventDefault();
            copyBtn.click();
        }
        
        // Escape to clear selection
        if (e.key === 'Escape') {
            clearAllSelections();
        }
        
        // Ctrl+M or Cmd+M to toggle mode
        if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
            e.preventDefault();
            toggleSelectionMode();
        }
    });
    
    console.log('Enhanced multi-cell selection functionality initialized');
}

// Toggle between single and multiple selection modes
function toggleSelectionMode() {
    selectionMode = selectionMode === 'single' ? 'multiple' : 'single';
    
    const modeToggleBtn = document.getElementById('mode-toggle-btn');
    if (modeToggleBtn) {
        if (selectionMode === 'single') {
            modeToggleBtn.innerHTML = '<i class="fas fa-mouse-pointer"></i> Einzelauswahl';
            modeToggleBtn.className = 'btn btn-outline-secondary btn-sm me-2';
        } else {
            modeToggleBtn.innerHTML = '<i class="fas fa-check-double"></i> Mehrfachauswahl';
            modeToggleBtn.className = 'btn btn-outline-success btn-sm me-2';
        }
    }
    
    // Clear current selections when switching modes
    clearAllSelections();
    
    console.log(`Selection mode changed to: ${selectionMode}`);
}

// Handle single cell selection
function handleSingleCellSelection(cell, column, rowIndex) {
    // Clear all previous selections
    clearAllSelections();
    
    // Get the input element and its value
    const input = cell.querySelector('input, select, textarea');
    if (!input) return;
    
    // Store the selection
    selectedCells.set(column, {
        cell: cell,
        value: input.type === 'checkbox' ? input.checked : input.value,
        input: input,
        rowIndex: rowIndex
    });
    
    // Apply visual highlighting
    cell.classList.add('selected');
    
    // Highlight same column cells
    document.querySelectorAll(`[data-column="${column}"]`).forEach(function(sameColumnCell) {
        if (sameColumnCell !== cell) {
            sameColumnCell.classList.add('same-column-highlight');
        }
    });
}

// Handle multiple cell selection
function handleMultiCellSelection(cell, column, rowIndex) {
    // Get the input element and its value
    const input = cell.querySelector('input, select, textarea');
    if (!input) return;
    
    // Check if this column is already selected
    if (selectedCells.has(column)) {
        // Remove selection from this column
        const existingSelection = selectedCells.get(column);
        existingSelection.cell.classList.remove('multi-selected');
        selectedCells.delete(column);
        
        // Clear column highlighting for this column
        document.querySelectorAll(`[data-column="${column}"]`).forEach(function(columnCell) {
            columnCell.classList.remove('multi-column-highlight');
        });
    } else {
        // Add new selection
        selectedCells.set(column, {
            cell: cell,
            value: input.type === 'checkbox' ? input.checked : input.value,
            input: input,
            rowIndex: rowIndex
        });
        
        // Apply visual highlighting
        cell.classList.add('multi-selected');
        
        // Highlight same column cells
        document.querySelectorAll(`[data-column="${column}"]`).forEach(function(sameColumnCell) {
            if (sameColumnCell !== cell) {
                sameColumnCell.classList.add('multi-column-highlight');
            }
        });
    }
}

// Update UI elements based on current selection
function updateSelectionUI() {
    const copyBtn = document.getElementById('copy-value-btn');
    const selectedInfo = document.getElementById('selected-cell-info');
    
    if (selectedCells.size === 0) {
        // No selection
        copyBtn.disabled = true;
        selectedInfo.style.display = 'none';
        selectedInfo.textContent = '';
    } else if (selectedCells.size === 1) {
        // Single selection
        copyBtn.disabled = false;
        selectedInfo.style.display = 'inline';
        
        const [column, selection] = selectedCells.entries().next().value;
        const columnHeader = document.querySelector(`th[data-column="${column}"]`);
        const columnName = columnHeader ? columnHeader.textContent.trim() : column;
        selectedInfo.textContent = `${columnName} - Zeile ${parseInt(selection.rowIndex) + 1}`;
    } else {
        // Multiple selection
        copyBtn.disabled = false;
        selectedInfo.style.display = 'inline';
        
        const columnNames = Array.from(selectedCells.keys()).map(column => {
            const columnHeader = document.querySelector(`th[data-column="${column}"]`);
            return columnHeader ? columnHeader.textContent.trim() : column;
        });
        
        selectedInfo.innerHTML = `${selectedCells.size} Spalten: ${columnNames.join(', ')} <span style="font-size: 0.75em;">(${selectedCells.size})</span>`;
    }
}

// Perform copy operation for selected cells
function performCopyOperation() {
    if (selectedCells.size === 0) return;
    
    const operations = Array.from(selectedCells.entries()).map(([column, selection]) => {
        const columnHeader = document.querySelector(`th[data-column="${column}"]`);
        const columnName = columnHeader ? columnHeader.textContent.trim() : column;
        return {
            column: column,
            columnName: columnName,
            value: selection.value,
            sourceCell: selection.cell
        };
    });
    
    // Create confirmation message
    let confirmMessage;
    if (operations.length === 1) {
        const op = operations[0];
        const cellCount = document.querySelectorAll(`[data-column="${op.column}"]`).length;
        confirmMessage = `Möchten Sie den Wert "${op.value}" in alle ${cellCount} Zellen der Spalte "${op.columnName}" kopieren?`;
    } else {
        const columnNames = operations.map(op => op.columnName).join(', ');
        confirmMessage = `Möchten Sie die Werte aus ${operations.length} Spalten (${columnNames}) in alle entsprechenden Zeilen kopieren?`;
    }
    
    if (!confirm(confirmMessage)) {
        return;
    }
    
    // Perform copy operations
    let totalCopied = 0;
    const results = [];
    
    operations.forEach(operation => {
        let copiedCount = 0;
        const targetCells = document.querySelectorAll(`[data-column="${operation.column}"]`);
        
        targetCells.forEach(function(cell) {
            const targetInput = cell.querySelector('input, select, textarea');
            if (targetInput && cell !== operation.sourceCell) {
                // Handle different input types
                if (targetInput.type === 'checkbox') {
                    targetInput.checked = operation.value;
                } else {
                    targetInput.value = operation.value;
                }
                
                // Trigger change event to update any dependencies
                targetInput.dispatchEvent(new Event('change', { bubbles: true }));
                copiedCount++;
            }
        });
        
        totalCopied += copiedCount;
        results.push({
            columnName: operation.columnName,
            value: operation.value,
            count: copiedCount
        });
    });
    
    // Show success message
    showMultiCopySuccessMessage(results, totalCopied);
    
    console.log(`Multi-copy operation completed: ${totalCopied} total cells updated across ${operations.length} columns`);
}

// Clear all selections
function clearAllSelections() {
    // Remove all visual highlights for both material and fields views
    const selectors = [
        '.selected', '.multi-selected', '.same-column-highlight', '.multi-column-highlight',
        '.same-row-highlight', '.multi-row-highlight'
    ];
    
    document.querySelectorAll(selectors.join(', ')).forEach(function(cell) {
        cell.classList.remove(...selectors.map(s => s.replace('.', '')));
    });
    
    // Clear selection data
    selectedCells.clear();
    
    // Update UI
    updateSelectionUI();
    updateFieldsSelectionUI();
}

// Show success message for multi-copy operations
function showMultiCopySuccessMessage(results, totalCopied) {
    let message;
    
    if (results.length === 1) {
        const result = results[0];
        message = `<strong>Erfolg!</strong> Der Wert "${result.value}" wurde in ${result.count} Zellen der Spalte "${result.columnName}" kopiert.`;
    } else {
        message = `<strong>Erfolg!</strong> Werte wurden in ${totalCopied} Zellen über ${results.length} Spalten kopiert:<br/>`;
        results.forEach(result => {
            message += `• ${result.columnName}: "${result.value}" (${result.count} Zellen)<br/>`;
        });
    }
    
    // Create success alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show copy-success-alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to page
    document.body.appendChild(alertDiv);
    
    // Auto-hide after 7 seconds (longer for multi-copy messages)
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 7000);
}

// ===== FIELDS TABULAR EDIT FUNCTIONALITY =====

// Fields tabular edit cell selection (adapted from material version)
function initializeFieldsCellSelection() {
    // Only initialize if we're on a fields tabular edit page
    if (!document.getElementById('tabular-fields-form')) return;
    
    console.log('Initializing fields cell selection...');
    
    // Reuse the existing cell selection logic but with fields-specific selectors
    const copyBtn = document.getElementById('copy-value-btn');
    const selectedInfo = document.getElementById('selected-cell-info');
    const clearSelectionBtn = document.getElementById('clear-selection-btn');
    const modeToggleBtn = document.getElementById('mode-toggle-btn');
    
    if (!copyBtn || !selectedInfo) return;
    
    // Initialize mode toggle if not already done
    if (modeToggleBtn && !modeToggleBtn._fieldsInitialized) {
        modeToggleBtn.addEventListener('click', toggleSelectionMode);
        modeToggleBtn._fieldsInitialized = true;
    }
    
    // Use the same selection logic but for rows instead of columns
    document.querySelectorAll('.fields-editable-cell').forEach(function(cell) {
        cell.addEventListener('click', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            const fieldName = this.getAttribute('data-field');
            const materialId = this.getAttribute('data-material');
            
            if (selectionMode === 'single') {
                handleSingleFieldCellSelection(this, fieldName, materialId);
            } else {
                handleMultiFieldCellSelection(this, fieldName, materialId);
            }
            
            updateFieldsSelectionUI();
        });
    });
    
    // Initialize button handlers if not already done
    if (!copyBtn._fieldsHandlerAdded) {
        copyBtn.addEventListener('click', performFieldsCopyOperation);
        copyBtn._fieldsHandlerAdded = true;
    }
    
    if (clearSelectionBtn && !clearSelectionBtn._fieldsHandlerAdded) {
        clearSelectionBtn.addEventListener('click', clearAllSelections);
        clearSelectionBtn._fieldsHandlerAdded = true;
    }
}

// Helper functions for fields selection
function handleSingleFieldCellSelection(cell, fieldName, materialId) {
    clearAllSelections();
    const input = cell.querySelector('input, select, textarea');
    if (!input) return;
    
    selectedCells.set(fieldName, {
        cell: cell,
        value: input.type === 'checkbox' ? input.checked : input.value,
        input: input,
        materialId: materialId
    });
    
    cell.classList.add('selected');
    document.querySelectorAll(`[data-field="${fieldName}"]`).forEach(function(sameRowCell) {
        if (sameRowCell !== cell) {
            sameRowCell.classList.add('same-row-highlight');
        }
    });
}

function handleMultiFieldCellSelection(cell, fieldName, materialId) {
    const input = cell.querySelector('input, select, textarea');
    if (!input) return;
    
    if (selectedCells.has(fieldName)) {
        const existingSelection = selectedCells.get(fieldName);
        existingSelection.cell.classList.remove('multi-selected');
        selectedCells.delete(fieldName);
        document.querySelectorAll(`[data-field="${fieldName}"]`).forEach(function(rowCell) {
            rowCell.classList.remove('multi-row-highlight');
        });
    } else {
        selectedCells.set(fieldName, {
            cell: cell,
            value: input.type === 'checkbox' ? input.checked : input.value,
            input: input,
            materialId: materialId
        });
        
        cell.classList.add('multi-selected');
        document.querySelectorAll(`[data-field="${fieldName}"]`).forEach(function(sameRowCell) {
            if (sameRowCell !== cell) {
                sameRowCell.classList.add('multi-row-highlight');
            }
        });
    }
}

function updateFieldsSelectionUI() {
    const copyBtn = document.getElementById('copy-value-btn');
    const selectedInfo = document.getElementById('selected-cell-info');
    
    if (!copyBtn || !selectedInfo) return;
    
    if (selectedCells.size === 0) {
        copyBtn.disabled = true;
        selectedInfo.style.display = 'none';
    } else if (selectedCells.size === 1) {
        copyBtn.disabled = false;
        selectedInfo.style.display = 'inline';
        const [fieldName] = selectedCells.keys();
        selectedInfo.textContent = `${fieldName} (Zeile)`;
    } else {
        copyBtn.disabled = false;
        selectedInfo.style.display = 'inline';
        selectedInfo.textContent = `${selectedCells.size} Felder ausgewählt`;
    }
}

function performFieldsCopyOperation() {
    if (selectedCells.size === 0) return;
    
    const operations = Array.from(selectedCells.entries()).map(([fieldName, selection]) => ({
        fieldName: fieldName,
        value: selection.value,
        sourceCell: selection.cell
    }));
    
    if (!confirm(`Möchten Sie die Werte in alle entsprechenden Zeilen kopieren?`)) {
        return;
    }
    
    operations.forEach(operation => {
        const targetCells = document.querySelectorAll(`[data-field="${operation.fieldName}"]`);
        targetCells.forEach(function(cell) {
            const targetInput = cell.querySelector('input, select, textarea');
            if (targetInput && cell !== operation.sourceCell) {
                if (targetInput.type === 'checkbox') {
                    targetInput.checked = operation.value;
                } else {
                    targetInput.value = operation.value;
                }
                targetInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    });
    
    alert('Werte wurden erfolgreich kopiert!');
}

// ===== MATERIAL-USER MANAGEMENT FUNCTIONS =====

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

// ===== LEGACY AND UTILITY FUNCTIONS =====

// Legacy functions for backward compatibility
function clearSelection() {
    clearAllSelections();
}

function showCopySuccessMessage(value, columnName, count) {
    showMultiCopySuccessMessage([{
        columnName: columnName,
        value: value,
        count: count
    }], count);
}

// Column copy functionality for tabular editing (legacy support)
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
            const formSelectors = ['#tabular-form', '#tabular-fields-form'];
            
            formSelectors.forEach(formSelector => {
                document.querySelectorAll(`${formSelector} input, ${formSelector} select, ${formSelector} textarea`).forEach(function(field) {
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
            });
            
            // Clear cell selection
            clearSelection();
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
        if (!document.getElementById('tabular-form') && !document.getElementById('tabular-fields-form')) return;
        
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
            if (targetCell && (targetCell.classList.contains('sticky-column') || targetCell.classList.contains('fields-sticky-column'))) {
                targetCell = null; // Skip the sticky columns
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
    const formSelectors = ['#tabular-form', '#tabular-fields-form'];
    
    formSelectors.forEach(formSelector => {
        document.querySelectorAll(`${formSelector} input, ${formSelector} select, ${formSelector} textarea`).forEach(function(field) {
            field.addEventListener('input', function() {
                clearTimeout(autoSaveTimeout);
                autoSaveTimeout = setTimeout(function() {
                    // You could implement auto-save here if needed
                    console.log('Auto-save triggered');
                }, 2000);
            });
        });
    });
}

// Initialize tabular mass edit functionality
function initializeTabularMassEdit() {
    // Initialize material-based tabular edit
    if (document.getElementById('tabular-form')) {
        console.log('Initializing material-based tabular mass edit functionality...');
        const originalValues = initializeTabularChangeTracking();
        initializeCellSelection();
        initializeColumnCopyFunctionality();
        initializeTabularFormReset(originalValues);
        initializeTabularKeyboardNavigation();
        initializeTabularAutoSave();
        console.log('Material-based tabular mass edit functionality initialized.');
    }
    
    // Initialize fields-based tabular edit
    if (document.getElementById('tabular-fields-form')) {
        console.log('Initializing fields-based tabular mass edit functionality...');
        const originalValues = initializeTabularChangeTracking();
        initializeFieldsCellSelection();
        initializeTabularFormReset(originalValues);
        initializeTabularKeyboardNavigation();
        initializeTabularAutoSave();
        console.log('Fields-based tabular mass edit functionality initialized.');
    }
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
    
    // Initialize material-user management
    initializeMaterialUserManagement();
    
    // Initialize material list handlers (for list pages)
    if (document.querySelector('[id^="material-form-"]')) {
        initializeMaterialListHandlers();
    }
    
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
    initializeCellSelection,
    initializeFieldsCellSelection,
    initializeMaterialListHandlers,
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
