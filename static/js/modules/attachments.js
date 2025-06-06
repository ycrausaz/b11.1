// File validation constants
export const MAX_FILE_SIZE = 2.5 * 1024 * 1024; // 2.5MB in bytes
export const MAX_ATTACHMENTS = 5;

// Define allowed file types with their MIME types and extensions
export const ALLOWED_TYPES = {
    // Documents
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
    
    // Excel files
    'application/vnd.ms-excel': ['.xls'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    
    // Images
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/gif': ['.gif']
};

// Get all allowed MIME types and extensions for easy checking
export const ALLOWED_MIME_TYPES = Object.keys(ALLOWED_TYPES);
export const ALLOWED_EXTENSIONS = Object.values(ALLOWED_TYPES).flat();

// File signatures (magic numbers) for header validation
export const FILE_SIGNATURES = {
    '.pdf': ['255044462D'], // %PDF-
    '.png': ['89504E470D0A1A0A'], // PNG signature
    '.jpg': ['FFD8FF'], // JPEG signature
    '.jpeg': ['FFD8FF'], // JPEG signature
    '.gif': ['474946383761', '474946383961'], // GIF87a, GIF89a
    '.doc': ['D0CF11E0A1B11AE1'], // MS Office compound document
    '.docx': ['504B0304'], // ZIP signature (DOCX is ZIP-based)
    '.xls': ['D0CF11E0A1B11AE1'], // MS Office compound document (same as .doc)
    '.xlsx': ['504B0304'], // ZIP signature (XLSX is ZIP-based, same as .docx)
};

// Basic file validation (size, extension, MIME type)
export function validateFile(file) {
    const fileName = file.name.toLowerCase();
    const fileType = file.type;
    const fileExtension = '.' + fileName.split('.').pop();

    console.log(`Validating file: ${fileName}, MIME: ${fileType}, Extension: ${fileExtension}`);

    // Check file size first
    if (file.size > MAX_FILE_SIZE) {
        return {
            valid: false,
            message: `File "${file.name}" is too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is ${(MAX_FILE_SIZE / 1024 / 1024).toFixed(1)}MB.`
        };
    }

    // Check if extension is allowed
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
        return {
            valid: false,
            message: `File extension "${fileExtension}" is not allowed. Please upload: PDF, DOC, DOCX, XLS, XLSX, TXT, JPG, PNG, or GIF files.`
        };
    }

    // Check if MIME type is allowed
    if (!ALLOWED_MIME_TYPES.includes(fileType)) {
        return {
            valid: false,
            message: `File type "${fileType}" is not allowed. Please upload: PDF, DOC, DOCX, XLS, XLSX, TXT, JPG, PNG, or GIF files.`
        };
    }

    // Check if extension matches the MIME type
    const expectedExtensions = ALLOWED_TYPES[fileType];
    if (!expectedExtensions.includes(fileExtension)) {
        return {
            valid: false,
            message: `File extension "${fileExtension}" doesn't match the detected file type. Expected extensions for ${fileType}: ${expectedExtensions.join(', ')}`
        };
    }

    return { valid: true, message: 'File is valid' };
}

// Advanced validation using FileReader to check file headers
export function validateFileHeader(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const arrayBuffer = e.target.result;
            const uint8Array = new Uint8Array(arrayBuffer.slice(0, 20)); // Read first 20 bytes
            
            // Convert to hex string for easier comparison
            const hex = Array.from(uint8Array)
                .map(byte => byte.toString(16).padStart(2, '0'))
                .join('')
                .toUpperCase();
            
            console.log(`File header (hex): ${hex}`);
            
            const fileName = file.name.toLowerCase();
            const fileExtension = '.' + fileName.split('.').pop();
            
            // For TXT files, we can't reliably check headers, so skip this validation
            if (fileExtension === '.txt') {
                resolve({ valid: true, detectedType: 'TEXT', expectedType: 'TEXT' });
                return;
            }
            
            // Check if file has expected signature
            const expectedSignatures = FILE_SIGNATURES[fileExtension];
            if (!expectedSignatures) {
                resolve({ valid: true, message: 'No header validation available for this file type' });
                return;
            }
            
            let headerMatch = false;
            let detectedType = null;
            
            for (const signature of expectedSignatures) {
                if (hex.startsWith(signature)) {
                    headerMatch = true;
                    detectedType = fileExtension.substring(1).toUpperCase();
                    break;
                }
            }
            
            if (!headerMatch) {
                resolve({ 
                    valid: false, 
                    message: `File header does not match expected signature for ${fileExtension} files. This might be a renamed file with incorrect extension.`
                });
            } else {
                console.log(`File header validation successful: ${file.name}`);
                resolve({ valid: true, detectedType, expectedType: fileExtension.substring(1).toUpperCase() });
            }
        };
        
        reader.onerror = () => reject(new Error('Failed to read file'));
        reader.readAsArrayBuffer(file.slice(0, 20)); // Read first 20 bytes
    });
}

// Function to show validation error
export function showValidationError(input, message) {
    // Remove any existing error message
    const existingError = input.parentNode.querySelector('.file-validation-error');
    if (existingError) {
        existingError.remove();
    }

    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'file-validation-error alert alert-danger mt-2';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.textContent = message;
    
    // Insert after the input
    input.parentNode.appendChild(errorDiv);
    
    // Clear the input
    input.value = '';
}

// Function to clear validation error
export function clearValidationError(input) {
    const existingError = input.parentNode.querySelector('.file-validation-error');
    if (existingError) {
        existingError.remove();
    }
}

// Add image preview for additional verification
export function addImagePreview(input, file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.createElement('img');
            preview.src = e.target.result;
            preview.style.maxWidth = '100px';
            preview.style.maxHeight = '100px';
            preview.style.marginTop = '10px';
            preview.className = 'file-preview';
            
            // Remove existing preview
            const existingPreview = input.parentNode.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            input.parentNode.appendChild(preview);
        };
        reader.readAsDataURL(file);
    } else {
        // Remove any existing preview for non-image files
        const existingPreview = input.parentNode.querySelector('.file-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
    }
}

// Comprehensive file validation function
export async function handleFileValidation(input, file) {
    console.log(`Validating file: ${file.name}`);
    
    // Basic validation first
    const basicValidation = validateFile(file);
    if (!basicValidation.valid) {
        showValidationError(input, basicValidation.message);
        return false;
    }

    // Advanced header validation
    try {
        const headerValidation = await validateFileHeader(file);
        if (!headerValidation.valid) {
            showValidationError(input, headerValidation.message);
            return false;
        }
        
        console.log(`File validation successful: ${file.name}`);
        clearValidationError(input);
        
        // Add image preview if it's an image
        addImagePreview(input, file);
        
        return true;
    } catch (error) {
        console.error('Error during file validation:', error);
        showValidationError(input, 'Error validating file. Please try again.');
        return false;
    }
}

// Legacy function for backward compatibility - now enhanced
export function validateFileSize(file) {
    console.log('validateFileSize (legacy function called)');
    const validation = validateFile(file);
    if (!validation.valid) {
        alert(validation.message);
        return false;
    }
    return true;
}

// Attach validation to a file input
export function attachValidationToInput(input) {
    input.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (file) {
            const isValid = await handleFileValidation(input, file);
            if (isValid) {
                // Update button state only if validation passes
                updateAddAttachmentButton();
            }
        } else {
            clearValidationError(input);
            // Remove any existing preview
            const existingPreview = input.parentNode.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            updateAddAttachmentButton();
        }
    });
}

// Update the add attachment button state
export function updateAddAttachmentButton() {
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
export function initializeAttachmentDeleteToggle() {
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
export function initializeAttachmentHandlers() {
    // Initialize button state on page load
    updateAddAttachmentButton();

    // Also initialize after a short delay to ensure all elements are loaded
    setTimeout(updateAddAttachmentButton, 500);

    // Initialize attachment delete toggle
    initializeAttachmentDeleteToggle();

    // Attach validation to existing file inputs
    document.querySelectorAll('input[type="file"][name="attachment_files[]"]').forEach(attachValidationToInput);

    // Handle dynamically added file inputs (for the "Add Another Attachment" functionality)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const fileInputs = node.querySelectorAll('input[type="file"][name="attachment_files[]"]');
                    fileInputs.forEach(attachValidationToInput);
                }
            });
        });
    });

    // Start observing the attachments container
    const attachmentsContainer = document.getElementById('attachments-container');
    if (attachmentsContainer) {
        observer.observe(attachmentsContainer, { childList: true, subtree: true });
    }

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
        
        // Clear any validation errors and previews from cloned row
        newRow.find('.file-validation-error').remove();
        newRow.find('.file-preview').remove();
        
        $('#attachments-container').append(newRow);

        // Attach validation to the new file input
        const newFileInput = newRow.find('input[type="file"]')[0];
        if (newFileInput) {
            attachValidationToInput(newFileInput);
        }

        updateAddAttachmentButton();
    });

    // Remove attachment handler
    $(document).on('click', '.remove-attachment', function() {
        if ($('.attachment-row').not('.existing-attachment-row').length > 1) {
            $(this).closest('.attachment-row').remove();
        } else {
            const row = $('.attachment-row').not('.existing-attachment-row').first();
            row.find('input').val('');
            row.find('.file-validation-error').remove();
            row.find('.file-preview').remove();
        }
        updateAddAttachmentButton();
    });

    // Handle deletion of existing attachments
    $(document).on('change', 'input[name="delete_attachments[]"]', function() {
        updateAddAttachmentButton();
    });

    // Enhanced form submit handler for attachments
    $('form').submit(function(e) {
        // Only apply this to forms with file inputs
        if ($(this).find('input[type="file"]').length === 0) {
            return true;
        }

        // Check for validation errors
        const validationErrors = document.querySelectorAll('.file-validation-error');
        if (validationErrors.length > 0) {
            e.preventDefault();
            alert('Please fix file validation errors before submitting.');
            return false;
        }

        const files = $('input[type="file"]').get().filter(input => input.files.length > 0);

        // Validate all file sizes (additional check)
        for (let input of files) {
            const validation = validateFile(input.files[0]);
            if (!validation.valid) {
                alert(validation.message);
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

        return true;
    });
}
