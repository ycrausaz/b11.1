import pandas as pd
from io import BytesIO  # Import BytesIO
from django.http import HttpResponse
from django.db import connections
from django.utils.timezone import is_aware


def export_to_excel(materials):
    export_to_excel_type_1(materials)

def make_timezone_naive(df):
    for col in df.select_dtypes(include=['datetime64[ns]']).columns:
        df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) and is_aware(x) else x)
    return df

def export_to_excel(materials):
    """
    Exports the provided materials to an Excel file with multiple sheets,
    each corresponding to a database view.

    Parameters:
    materials (QuerySet): A queryset of Material objects to export.

    Returns:
    HttpResponse: An HttpResponse with the Excel file for download.
    """
#    try:
    # List of your database view names
    views = ['MAKT_Beschreibung', 'MARA_KSSK_Klassenzuordnung', 'MARA_AUSP_Merkmale', 'MARA_STXH_Grunddaten', 'MARA_STXL_Grunddaten', 'MARC_Werkdaten', 'MBEW_Buchhaltung', 'MLAN_Steuer', 'MVKE_Verkaufsdaten', 'MARA_Grunddaten']

    # Open a connection to the database
    connection = connections['default']

    # Create a BytesIO buffer to hold the Excel data
    output = BytesIO()

    # Create a Pandas Excel writer using openpyxl as the engine, writing to the BytesIO buffer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sheet_added = False
        for view in views:
            try:
                # Query all data from the view
                query = f'SELECT * FROM {view}'
                df = pd.read_sql_query(query, connection)

                # Write the DataFrame to a specific sheet, including headers
                df.to_excel(writer, sheet_name=view, index=False)
                sheet_added = True
            except Exception as e:
                print(f"Error fetching data for view '{view}': {e}")

        if not sheet_added:
            # Add an empty sheet if no data was added
            pd.DataFrame().to_excel(writer, sheet_name='EmptySheet')

        # Also write the selected materials to a new sheet
        selected_df = pd.DataFrame(list(materials.values()))
        if not selected_df.empty:
            selected_df.to_excel(writer, sheet_name='Selected Materials', index=False)

    # Seek to the beginning of the stream
    output.seek(0)

    # Create the HttpResponse object with the appropriate Excel header
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=database_views.xlsx'

    return response
#    except Exception as e:
#        print(f"Error generating Excel file: {e}")
#        return HttpResponse("An error occurred while generating the Excel file.", status=500)
