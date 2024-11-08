# import_utils.py

import pandas as pd
from django.contrib import messages
import logging
from .models import *

logger = logging.getLogger(__name__)

# Define the mapping between Excel columns and model fields
FIELD_MAPPING = {
    # Simple fields
    'positions_nr': {
        'tab': 'T1', 
        'column': 'A', 
        'type': 'simple'
    },
    'kurztext_de': {
        'tab': 'T1', 
        'column': 'R', 
        'type': 'simple'
    },
    'hersteller': {
        'tab': 'T1', 
        'column': 'B', 
        'type': 'simple'
    },
    
    # Foreign key fields
    'basismengeneinheit': {
        'tab': 'T1',
        'column': 'C',
        'type': 'fk',
        'model': Basismengeneinheit,
        'lookup_field': 'text'
    },
    'begru': {
        'tab': 'T1',
        'column': 'D',
        'type': 'fk',
        'model': BEGRU,
        'lookup_field': 'text'
    },
    'materialart_grunddaten': {
        'tab': 'T1',
        'column': 'E',
        'type': 'fk',
        'model': Materialart,
        'lookup_field': 'text'
    },
    'sparte': {
        'tab': 'T1',
        'column': 'F',
        'type': 'fk',
        'model': Sparte,
        'lookup_field': 'text'
    },
    # Add more mappings as needed...
}

def get_tab_data(excel_file):
    """
    Read all required tabs from the Excel file and return their DataFrames.
    """
    unique_tabs = {mapping['tab'] for mapping in FIELD_MAPPING.values()}
    tab_data = {}
    
    for tab in unique_tabs:
        try:
            tab_data[tab] = pd.read_excel(excel_file, sheet_name=tab, skiprows=8)
        except Exception as e:
            logger.error(f"Error reading tab {tab}: {str(e)}")
            raise ValueError(f"Error reading tab {tab}: {str(e)}")
            
    return tab_data

def process_field_value(field_config, value, row_data):
    """
    Process a single field value based on its configuration.
    Returns the processed value ready for the Material model.
    """
    if pd.isna(value):
        return None

    if field_config['type'] == 'simple':
        return value
    
    elif field_config['type'] == 'fk':
        model_class = field_config['model']
        lookup_field = field_config['lookup_field']
        
        try:
            # Try to get existing object
            lookup_kwargs = {lookup_field: value}
            obj, created = model_class.objects.get_or_create(**lookup_kwargs)
            
            if created:
                logger.info(f"Created new {model_class.__name__} with {lookup_field}={value}")
            
            return obj
        
        except Exception as e:
            logger.error(f"Error processing foreign key {model_class.__name__}: {str(e)}")
            return None

def import_from_excel(excel_file, request=None):
    """
    Process the uploaded Excel file and create/update Material objects.
    Returns a tuple of (success_status, message, created_count, updated_count)
    """
    try:
        tab_data = get_tab_data(excel_file)
        
        materials_created = 0
        materials_updated = 0
        
        # Get the number of rows from the first tab
        first_tab = next(iter(tab_data.values()))
        num_rows = len(first_tab)
        
        # Process each row
        for row_idx in range(num_rows):
            material_data = {}
            
            # Process each field according to its mapping
            for field_name, field_config in FIELD_MAPPING.items():
                tab = field_config['tab']
                column = field_config['column']
                
                try:
                    value = tab_data[tab].iloc[row_idx][column]
                    processed_value = process_field_value(field_config, value, tab_data[tab].iloc[row_idx])
                    
                    if processed_value is not None:
                        material_data[field_name] = processed_value
                        
                except Exception as e:
                    logger.error(f"Error processing field {field_name} at row {row_idx + 9}: {str(e)}")
                    if request:
                        messages.warning(
                            request,
                            f"Warning: Could not process {field_name} at row {row_idx + 9}"
                        )
            
            try:
                # Create or update Material object
                if 'positions_nr' in material_data:
                    material, created = Material.objects.update_or_create(
                        positions_nr=material_data['positions_nr'],
                        defaults=material_data
                    )
                    
                    if created:
                        materials_created += 1
                    else:
                        materials_updated += 1
                        
            except Exception as e:
                logger.error(f"Error saving material at row {row_idx + 9}: {str(e)}")
                if request:
                    messages.error(
                        request,
                        f"Error: Could not save material at row {row_idx + 9}"
                    )
        
        success_message = f'Successfully processed Excel file. Created: {materials_created}, Updated: {materials_updated} materials.'
        logger.info(f'Excel import completed. Created: {materials_created}, Updated: {materials_updated}')
        return True, success_message, materials_created, materials_updated

    except Exception as e:
        error_message = f'Error processing Excel file: {str(e)}'
        logger.error(f'Excel import failed: {str(e)}')
        return False, error_message, 0, 0
