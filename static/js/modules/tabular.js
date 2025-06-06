import { initializeFieldsCellSelection, updateFieldsSelectionUI } from "./field_tabular.js";

// ===== TABULAR MASS EDIT FUNCTIONALITY =====

// Track changes in form fields for tabular editing
export function initializeTabularChangeTracking() {
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
export let selectedCells = new Map(); // Map of column/field -> {cell, value, input}
export let selectionMode = 'single'; // 'single' or 'multiple'

// Initialize cell selection functionality
export function initializeCellSelection() {
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
export function toggleSelectionMode() {
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
export function handleSingleCellSelection(cell, column, rowIndex) {
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
export function handleMultiCellSelection(cell, column, rowIndex) {
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
export function updateSelectionUI() {
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
export function performCopyOperation() {
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
export function clearAllSelections() {
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
export function showMultiCopySuccessMessage(results, totalCopied) {
    let message;

    if (results.length === 1) {
        const result = results[0];
        message = `<strong>Erfolg!</strong> Der Wert "${result.value}" wurde in ${result.count} Zellen der Spalte "${result.columnName}" kopiert.`;
    } else {
        const summaries = results.map(res => `${res.count} × ${res.columnName}`).join(', ');
        message = `<strong>Erfolg!</strong> ${totalCopied} Zellen aktualisiert (${summaries}).`;
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success copy-success-alert';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = message;

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.classList.add('show');
    }, 10);

    setTimeout(() => {
        alertDiv.classList.remove('show');
        alertDiv.addEventListener('transitionend', () => alertDiv.remove());
    }, 3000);
}

// Legacy functions for backward compatibility
export function clearSelection() {
    clearAllSelections();
}

export function showCopySuccessMessage(value, columnName, count) {
    showMultiCopySuccessMessage([{
        columnName: columnName,
        value: value,
        count: count
    }], count);
}

// Column copy functionality for tabular editing (legacy support)
export function initializeColumnCopyFunctionality() {
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
export function initializeTabularFormReset(originalValues) {
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
export function initializeTabularKeyboardNavigation() {
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
export function getNextField(currentField, direction) {
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
export function initializeTabularAutoSave() {
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
export function initializeTabularMassEdit() {
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

