import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.db import connections
from django.utils.timezone import is_aware
import random
import string
from datetime import datetime
from sqlalchemy import create_engine

def make_timezone_naive(df):
    for col in df.select_dtypes(include=['datetime64[ns]']).columns:
        df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) and is_aware(x) else x)
    return df

def generate_random_string(length=16):
    """
    Generates a random string of the specified length with letters only.

    Parameters:
    length (int): The length of the random string.

    Returns:
    str: The generated random string.
    """
    letters = string.ascii_uppercase  # Use uppercase letters only
    return ''.join(random.choice(letters) for i in range(length))

def update_df(df, view, sheet_name, export_type):
    # Drop the 'tmp_id' column if it exists
    if 'TMP_ID' in df.columns:
        df = df.drop(columns=['TMP_ID'])
    
    # Pad 'SOURCE_ID' column values to 3 digits with leading zeros and sort by 'SOURCE_ID'
    if 'SOURCE_ID' in df.columns: # makeLastUpdate_2
        df['SOURCE_ID'] = df['SOURCE_ID'].astype(str).str.zfill(3)
        df = df.sort_values(by='SOURCE_ID')
    
    # Transform MFRPN column if it exists
    if 'ZZFUEHR_MAT' in df.columns:
        # Apply transformation to convert NNNN.NNNN to 0000000000NNNNNNNN
        df['ZZFUEHR_MAT'] = df['ZZFUEHR_MAT'].apply(
            lambda x: '0000000000' + x.replace('.', '') 
            if isinstance(x, str) and '.' in x 
            else x
        )
    
    # Format dimension columns (LAENG, BREIT, HOEHE) to have 3 decimal places
    for dimension_col in ['LAENG', 'BREIT', 'HOEHE']:
        if dimension_col in df.columns:
            # First ensure values are converted to float
            df[dimension_col] = pd.to_numeric(df[dimension_col], errors='coerce')
            # Format to display exactly 3 decimal places
            df[dimension_col] = df[dimension_col].apply(
                lambda x: f"{x:.3f}" if pd.notnull(x) else x
            )
    
    # Filter out records with null values in specified columns for specific views
    if view == 'MARC_Werksdaten' and 'WERKS' in df.columns: # makeLastUpdate_3
        df = df.dropna(subset=['WERKS'])
    elif view == 'MBEW_Buchhaltung' and 'BWKEY' in df.columns: # makeLastUpdate_4
        df = df.dropna(subset=['BWKEY'])
    elif view == 'CKMLCR_material_ledger_preise' and 'BWKEY' in df.columns: # makeLastUpdate_7
        df = df.dropna(subset=['BWKEY'])
    elif view == 'MARA_MARA' and 'V_LAGERFAEHIGKEIT' in df.columns:
        df = df.dropna(subset=['V_LAGERFAEHIGKEIT']) # makeLastUpdate_1
    elif view == 'MARA_AUSP_Merkmale' and 'V_CHEOPS' in df.columns:
        df = df.dropna(subset=['V_CHEOPS']) # makeLastUpdate_10

    # Add handling for MARA_AUSP_Merkmale view to convert V_NACHSCHUBKLASSE from float to int
    if view == 'MARA_AUSP_Merkmale' and 'ATNAM' in df.columns and 'ATWRT' in df.columns:
        # Create a mask to identify rows where ATNAM is 'V_NACHSCHUBKLASSE'
        nachschubklasse_mask = df['ATNAM'] == 'V_NACHSCHUBKLASSE'

        # For those rows, convert ATWRT to float first (to handle potential strings)
        # then to int, but only if the value can be converted
        df.loc[nachschubklasse_mask, 'ATWRT'] = df.loc[nachschubklasse_mask, 'ATWRT'].apply(
            lambda x: str(int(float(x))) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x
        )

    if export_type == "RUAG":
        if view == 'MARA_MARA' and 'BEGRU' in df.columns: # makeLastUpdate_RUAG_3
            df['BEGRU'] = "3000"
        if view == 'MARA_MARA' and 'SPART' in df.columns: # makeLastUpdate_RUAG_3
            df['SPART'] = "V0"
        if view == 'MARA_MARA' and 'MTART' in df.columns: # makeLastUpdate_RUAG_3
            df['MTART'] = "V099"
        if view == 'MARA_AUSP_Merkmale' and 'V_ZERTFLUG' in df.columns: # makeLastUpdate_RUAG_4
            df['V_ZERTFLUG'] = "J"

    return df

def export_to_excel(materials, export_type):
    """
    Exports the provided materials to an Excel file with multiple sheets,
    each corresponding to a database view.

    Parameters:
    materials (QuerySet): A queryset of Material objects to export.

    Returns:
    HttpResponse: An HttpResponse with the Excel file for download.
    """

    view_to_sheet = {
        'MARA_MARA': 'MARA - MARA',
        'MAKT_Beschreibung': 'MAKT - Beschreibung',
        'MARA_STXH_Grunddaten': 'MARA_STXH - Grunddaten. Text Al',
        'MARA_STXL_Grunddaten': 'MARA_STXL - Grunddaten. Text',
        'MARA_KSSK_Klassenzuordnung': 'MARA_KSSK - Klassenzuordnung',
        'MARA_AUSP_Merkmale': 'MARA_AUSP - Merkmale',
        'MVKE_Verkaufsdaten': 'MVKE - Verkaufsdaten',
        'MLAN_Steuer': 'MLAN - Steuer',
        'MARC_Werksdaten': 'MARC - Werksdaten',
        'MBEW_Buchhaltung': 'MBEW - Buchhaltung',
        'CKMLCR_material_ledger_preise': 'CKMLCR - Material-Ledger-Preise',
    }

    # Conditionally remove sheets based on the 'export_type' value
    if export_type == 'RUAG':
        # Remove specified sheets for 'RUAG'
        sheets_to_remove = ['MVKE_Verkaufsdaten', 'MBEW_Buchhaltung', 'MLAN_Steuer', 'MARC_Werksdaten', 'CKMLCR_material_ledger_preise']
        for sheet in sheets_to_remove:
            view_to_sheet.pop(sheet, None)  # Remove the sheet if it exists

    # Get the database connection settings from Django
    db_settings = connections.databases['default']
    db_url = f"postgresql+psycopg://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"

    # Create a SQLAlchemy engine
    engine = create_engine(db_url)

    # Create a BytesIO buffer to hold the Excel data
    output = BytesIO()

    # Extract the IDs (or other relevant values) from the 'materials' parameter
    material_ids = list(materials.values_list('id', flat=True))

    # Create a Pandas Excel writer using xlsxwriter as the engine, writing to the BytesIO buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sheet_added = False
        for view, sheet_name in view_to_sheet.items():
            try:

                # Dynamically construct the query based on the 'material_ids'
                if material_ids:
                    id_conditions = ' OR '.join([f"tmp_id = {material_id}" for material_id in material_ids])
                    query = f"SELECT * FROM {view} WHERE {id_conditions}"
                else:
                    query = f"SELECT * FROM {view}"

                df = pd.read_sql_query(query, engine)

                # Convert headers to capital letters
                df.columns = [col.upper() for col in df.columns]

                # Applay a the modifications and business rules to the dataframe
                df = update_df(df, view, sheet_name, export_type)

                # Write the DataFrame to a specific sheet, including headers
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                sheet_added = True
            except Exception as e:
                print(f"Error fetching data for view '{view}': {e}")

        if not sheet_added:
            # Add an empty sheet if no data was added
            pd.DataFrame().to_excel(writer, sheet_name='EmptySheet')

    # Seek to the beginning of the stream
    output.seek(0)

    # Create the HttpResponse object with the appropriate Excel header
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=MDG_UPLOAD_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '_' + export_type + '.xlsx'

    return response

