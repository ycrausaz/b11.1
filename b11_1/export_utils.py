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

def export_to_excel(materials, export_type):
    """
    Exports the provided materials to an Excel file with multiple sheets,
    each corresponding to a database view.

    Parameters:
    materials (QuerySet): A queryset of Material objects to export.

    Returns:
    HttpResponse: An HttpResponse with the Excel file for download.
    """
    # List of your database view names
    views = [
        'MARA_Grunddaten', 'MARA_AUSP_Merkmale', 'MARA_KSSK_Klassenzuordnung',
        'MARA_STXH_Grunddaten', 'MARA_STXL_Grunddaten', 'MARC_Werksdaten',
        'MBEW_Buchhaltung', 'MLAN_Steuer', 'MVKE_Verkaufsdaten', 'MAKT_Beschreibung',
        'CKMLCR_material_ledger_preise'
    ]

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

                # Drop the 'tmp_id' column if it exists
                if 'TMP_ID' in df.columns:
                    df = df.drop(columns=['TMP_ID'])

                # Pad 'SOURCE_ID' column values to 3 digits with leading zeros and sort by 'SOURCE_ID'
                if 'SOURCE_ID' in df.columns:
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
                if view == 'MARC_Werksdaten' and 'WERKS' in df.columns:
                    df = df.dropna(subset=['WERKS'])
                elif view == 'MBEW_Buchhaltung' and 'BWKEY' in df.columns:
                    df = df.dropna(subset=['BWKEY'])
                elif view == 'CKMLCR_material_ledger_preise' and 'BWKEY' in df.columns:
                    df = df.dropna(subset=['BWKEY'])

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
    response['Content-Disposition'] = 'attachment; filename=MDG_UPLOAD_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '.xlsx'

    return response

