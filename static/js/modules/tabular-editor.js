// static/js/modules/tabular-editor.js

// Global variables for cell selection
let selectedCells = new Map(); // Map of column/field -> {cell, value, input}
let selectionMode = 'single'; // 'single' or 'multiple'

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

// Initialize tabular mass edit functionality
function initializeTabularMassEdit() {
    // Initialize material-based tabular edit
    if (document.getElementById('tabular-form')) {
        console.log('Initializing material-based tabular mass edit functionality...');
        const originalValues = initializeTabularChangeTracking();
        initializeCellSelection();
        console.log('Material-based tabular mass edit functionality initialized.');
    }
    
    // Initialize fields-based tabular edit
    if (document.getElementById('tabular-fields-form')) {
        console.log('Initializing fields-based tabular mass edit functionality...');
        const originalValues = initializeTabularChangeTracking();
        console.log('Fields-based tabular mass edit functionality initialized.');
    }
}

// Export functions for module use
window.TabularEditor = {
    initializeTabularChangeTracking,
    initializeCellSelection,
    initializeTabularMassEdit,
    clearAllSelections,
    showMultiCopySuccessMessage: showMultiCopySuccessMessage
};
