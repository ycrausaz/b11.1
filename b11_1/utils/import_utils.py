# import_utils.py

import pandas as pd
from django.contrib import messages
import logging
from openpyxl import load_workbook
from ..models import *
from ..utils.field_mapping_config import FIELD_MAPPING

logger = logging.getLogger(__name__)

# Define the mapping between Excel columns and model fields
field_mapping = FIELD_MAPPING

def column_letter_to_index(letter):
    """Convert Excel column letter to zero-based column index."""
    result = 0
    for char in letter:
        result = result * 26 + (ord(char.upper()) - ord('A') + 1)
    return result - 1  # Convert to 0-based index

def get_tab_data(excel_file):
    """
    Read all required tabs from the Excel file and return their DataFrames.
    Also reads cell B1 from the Input_Lieferant tab to get the system name.
    Skips rows where positions_nr (column B) or kurztext_de (column D) is empty.
    """
    unique_tabs = {mapping['tab'] for mapping in field_mapping.values()}
    tab_data = {}
    systemname = None  # Initialize the systemname variable

    try:
        # First, read the B1 cell from Input_Lieferant tab to get the systemname
        try:
            header_df = pd.read_excel(
                excel_file,
                sheet_name='Input_Lieferant',
                nrows=1,  # Read only the first row
                usecols='B',  # Read only column B
                header=None
            )
            if not header_df.empty and not pd.isna(header_df.iloc[0, 0]):
                systemname = str(header_df.iloc[0, 0]).strip()
                logger.info(f"Found system name in cell B1: {systemname}")
            else:
                logger.warning("Cell B1 in Input_Lieferant tab is empty or not found")
        except Exception as e:
            logger.error(f"Error reading system name from cell B1: {str(e)}")
            
        # Now read columns B and D from Input_Lieferant to determine valid rows
        initial_df = pd.read_excel(
            excel_file,
            sheet_name='Input_Lieferant',
            skiprows=8,  # Skip first 8 rows to start at row 9
            usecols='B,D',  # Read columns B (positions_nr) and D (kurztext_de)
            header=None
        )

        # Create masks for rows with non-empty required fields
        valid_positions_mask = initial_df[1].notna()  # Column B (positions_nr)
        valid_kurztext_mask = initial_df[3].notna()  # Column D (kurztext_de)

        # Combine masks to get rows where both fields are non-empty
        valid_rows_mask = valid_positions_mask & valid_kurztext_mask

        if not valid_rows_mask.any():
            raise ValueError("No valid data found with both positions_nr and kurztext_de in Input_Lieferant tab")

        # Get indices of valid rows
        valid_row_indices = valid_rows_mask[valid_rows_mask].index

        logger.info(f"Found {len(valid_row_indices)} valid rows with both positions_nr and kurztext_de in Input_Lieferant tab")

        # Track skipped rows for logging
        total_rows = len(initial_df)
        skipped_rows = total_rows - len(valid_row_indices)
        logger.info(f"Skipped {skipped_rows} rows due to missing positions_nr or kurztext_de")

        # Now read all required tabs, but only keep the valid rows
        for tab in unique_tabs:
            try:
                # Read the entire sheet
                df = pd.read_excel(
                    excel_file,
                    sheet_name=tab,
                    skiprows=8,  # Skip first 8 rows to start at row 9
                    header=None
                )

                # Filter to keep only rows with valid data
                df = df.iloc[valid_row_indices]

                # Create a dictionary to store column mappings
                col_mappings = {}
                for field, config in field_mapping.items():
                    if config['tab'] == tab:
                        col_idx = column_letter_to_index(config['column'])
                        col_mappings[col_idx] = config['column']

                # Rename columns to match Excel letters
                df.rename(columns={col_idx: letter for col_idx, letter in col_mappings.items()}, inplace=True)

                # Reset the index to start from 0 after filtering
                df.reset_index(drop=True, inplace=True)

                tab_data[tab] = df

                logger.info(f"Successfully read {len(df)} rows from tab '{tab}'")

            except Exception as e:
                logger.error(f"Error reading tab {tab}: {str(e)}")
                raise ValueError(f"Error reading tab {tab}: {str(e)}")

    except Exception as e:
        logger.error(f"Error determining valid rows from Input_Lieferant tab: {str(e)}")
        raise ValueError(f"Error determining valid rows from Input_Lieferant tab: {str(e)}")

    # Store the systemname in the tab_data dictionary
    tab_data['systemname'] = systemname
    
    return tab_data

# Define special field processors
def process_produkthierarchie(value):
    """
    Special processor for produkthierarchie field.
    Add your custom logic here.
    """
    if pd.isna(value):
        return None

    # Convert to string and strip whitespace
    value = str(int(value)).strip().zfill(4)

    return value

#    # Example processing:
#    # - Ensure correct format (e.g., XX.XX.XX)
#    # - Validate hierarchical structure
#    # - Convert legacy formats
#    parts = value.split('.')
#    if len(parts) == 3:
#        # Pad each part to 2 digits
#        formatted_parts = [part.zfill(2) for part in parts]
#        return '.'.join(formatted_parts)
#    else:
#        logger.warning(f"Invalid produkthierarchie format: {value}")
#        return value

# Map field names to their special processors
FIELD_PROCESSORS = {
    'produkthierarchie': process_produkthierarchie,
    # Add more special processors here:
    # 'another_field': process_another_field,
}

def process_field_value(field_config, value, row_data):
    """
    Process a single field value based on its configuration.
    Returns the processed value ready for the Material model.
    Raises ValueError if a foreign key value doesn't exist.
    """
    if pd.isna(value):
        return None

    # Check if field has a special processor
    field_name = next(name for name, config in FIELD_MAPPING.items()
                     if config == field_config)
    if field_name in FIELD_PROCESSORS:
        return FIELD_PROCESSORS[field_name](value)

    # Handle different field types
    if field_config['type'] == 'simple':
        return value

    elif field_config['type'] == 'boolean':
        if isinstance(value, str):
            value = value.strip().upper()
            if value == 'X' or value == 'J':
                return True
            else:
                return False
        else:
            logger.warning(f"Unexpected boolean value type: {type(value)}")
            return None

    elif field_config['type'] in ['fk', 'padded_fk']:
        model_class = field_config['model']
        lookup_field = field_config['lookup_field']

        try:
            if pd.isna(value):
                return None

            # Handle the value conversion first
            if isinstance(value, (int, float)):
                # Convert to integer first to remove decimal point if it's a float
                value = str(int(value))
            else:
                value = str(value).strip()

            # Apply padding for padded_fk type
            if field_config['type'] == 'padded_fk':
                padding_length = field_config.get('length', 1)
                value = value.zfill(padding_length)

            # Try to get the existing object
            lookup_kwargs = {lookup_field: value}
            try:
                obj = model_class.objects.get(**lookup_kwargs)
                return obj
            except model_class.DoesNotExist:
                error_msg = f"{model_class.__name__} with {lookup_field}='{value}' does not exist in the database"
                logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            error_msg = f"Error processing foreign key {model_class.__name__}: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    else:
        error_msg = f"Unknown field type: {field_config['type']}"
        logger.error(error_msg)
        raise ValueError(error_msg)

# import_utils.py

def process_additional_fields(material, row_data):
    """
    Process and update fields that are not part of the Excel import.
    Args:
        material: The Material model instance
        row_data: Dictionary containing the row data from Excel
    """
    try:
        material.is_transferred = True
        material.save()

    except Exception as e:
        logger.error(f"Error processing additional fields for material {material.positions_nr}: {str(e)}")
        raise

def import_from_excel(excel_file, request, il_user):
    """
    Process the uploaded Excel file and create new Material objects.
    Requires il_user parameter to set as hersteller.
    Returns a tuple of (success_status, message, created_count, updated_count)
    """
    try:
        tab_data = get_tab_data(excel_file)
        
        # Get the system name from tab_data
        systemname = tab_data.pop('systemname', None)

        materials_created = 0
        materials_updated = 0
        errors = []

        # Get the number of rows from the first tab
        first_tab = next(iter(tab_data.values()))
        num_rows = len(first_tab)

        # Process each row
        for row_idx in range(num_rows):
            material_data = {}
            row_has_error = False

            # Calculate actual Excel row number (add 9 because we started at row 9)
            excel_row = row_idx + 9

            # Process each field according to its mapping
            for field_name, field_config in field_mapping.items():
                tab = field_config['tab']
                column = field_config['column']

                try:
                    value = tab_data[tab].loc[row_idx, column]
                    processed_value = process_field_value(field_config, value, tab_data[tab].iloc[row_idx])

                    if processed_value is not None:
                        material_data[field_name] = processed_value

                except ValueError as e:
                    error_msg = f"Row {excel_row} in tab '{tab}': {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    row_has_error = True
                    if request:
                        messages.error(request, error_msg)
                except Exception as e:
                    error_msg = f"Error processing field '{field_name}' at row {excel_row} in tab '{tab}': {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    row_has_error = True
                    if request:
                        messages.error(request, error_msg)

            # Only process the row if there were no errors
            if not row_has_error and material_data:
                try:
                    # Check if material with this positions_nr already exists
                    positions_nr = material_data.get('positions_nr')
                    material = None
                    
                    if positions_nr:
                        material = Material.objects.filter(positions_nr=positions_nr).first()
                    
                    material = Material(**material_data)
                    materials_created += 1
                    logger.info(f"Created new material from row {excel_row}")
                    
                    # Set hersteller to the IL user's email
                    material.hersteller = il_user.email
                    
                    # Set the Systemname from cell B1
                    if systemname:
                        material.systemname = systemname
                    
                    # Set additional fields
                    material.is_transferred = True
                    
                    # Save the material
                    material.save()

                except Exception as e:
                    error_msg = f"Error saving material at row {excel_row}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    if request:
                        messages.error(request, error_msg)

        if errors:
            error_message = "Import completed with errors. Please check the error messages above."
            logger.error(f"Excel import completed with {len(errors)} errors")
            return False, error_message, materials_created, materials_updated
        else:
            success_message = f'Successfully processed Excel file. Created: {materials_created}, Updated: {materials_updated} materials.'
            logger.info(f'Excel import completed. Created: {materials_created}, Updated: {materials_updated} materials.')
            return True, success_message, materials_created, materials_updated

    except Exception as e:
        error_message = f'Error processing Excel file: {str(e)}'
        logger.error(f'Excel import failed: {str(e)}')
        return False, error_message, 0, 0
