import * as Attachments from './modules/attachments.js';
import * as MassEdit from './modules/mass_edit.js';
import * as FieldTabular from './modules/field_tabular.js';
import * as Tabular from './modules/tabular.js';
import * as Assignment from './modules/assignment_management.js';

let validationInitialized = false;

export function initializeValidations() {
    if (validationInitialized) {
        console.log('Validation already initialized, skipping...');
        return;
    }

    console.log('Initializing validation functionality...');

    if (document.getElementById('add-attachment')) {
        Attachments.initializeAttachmentHandlers();
    }

    MassEdit.initializeConditionalRequirements();
    Assignment.initializeMaterialUserManagement();

    if (document.querySelector('[id^="material-form-"]')) {
        MassEdit.initializeMaterialListHandlers();
    }

    if (document.querySelector('.mass-edit-table') || document.getElementById('select-all-fields')) {
        MassEdit.initializeMassEditHandlers();
    }

    Tabular.initializeTabularMassEdit();

    validationInitialized = true;
    console.log('Validation functionality initialized.');
}

window.ValidationUtils = {
    ...Attachments,
    ...MassEdit,
    ...Tabular,
    ...FieldTabular,
    ...Assignment,
    initializeValidations,
    initialized: false
};

$(document).ready(function() {
    initializeValidations();
    window.ValidationUtils.initialized = true;
});

document.addEventListener('DOMContentLoaded', function() {
    if (typeof $ === 'undefined' && !validationInitialized) {
        initializeValidations();
        window.ValidationUtils.initialized = true;
    }
});

