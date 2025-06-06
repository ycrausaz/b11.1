// ===== FIELDS TABULAR EDIT FUNCTIONALITY =====
import { selectedCells, clearAllSelections, selectionMode, toggleSelectionMode } from "./tabular.js";

// Fields tabular edit cell selection (adapted from material version)
export function initializeFieldsCellSelection() {
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
export function handleSingleFieldCellSelection(cell, fieldName, materialId) {
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

export function handleMultiFieldCellSelection(cell, fieldName, materialId) {
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

export function updateFieldsSelectionUI() {
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

export function performFieldsCopyOperation() {
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

