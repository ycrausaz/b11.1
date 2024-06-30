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
    try:
        # Define your database views and their specific columns
        views = {
            'MVKE_Verkaufsdaten': ['SOURCE_ID', 'VKORG', 'VTWEG', 'MTPOS'],
            'MARA_Grunddaten': ['SOURCE_ID', 'MTART', 'MEINS', 'MFRPN', 'MFRNR', 'GROES', 'NTGEW', 'LAENG', 'BREIT', 'HOEHE', 'MEABM', 'GEWEI', 'PROFL', 'NSNID', 'EAN11', 'NUMTP', 'BEGRU', 'NORMT', 'MBRSH', 'MATKL', 'BISMT', 'BRGEW', 'BSTME', 'SPART', 'XCHPF', 'MSTAE', 'MTPOS_MARA', 'MCOND', 'ZZFUEHR_MAT', 'ZZLABEL', 'RETDELC', 'ADSPC_SPC', 'PRDHA', 'HNDLCODE', 'TEMPB', 'ZZCPVCODE', 'ZZSONDERABLAUF', '"MARA-MHDHB"'],
            # Add all your view names and their specific columns here
        }
    
        connection = connections['default']

        # Create a BytesIO buffer to hold the Excel data
        output = BytesIO()

        # Create a Pandas Excel writer using openpyxl as the engine, writing to the BytesIO buffer
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            sheet_added = False
            for view, columns in views.items():
                try:
                    query = f'SELECT {", ".join(columns)} FROM {view}'
                    df = pd.read_sql_query(query, connection)

                    df = make_timezone_naive(df)


                    df.to_excel(writer, sheet_name=view, index=False)
                    sheet_added = True
                except Exception as e:
                    print(f"Error fetching data for view '{view}': {e}")

            if not sheet_added:
                pd.DataFrame().to_excel(writer, sheet_name='EmptySheet')

            selected_df = pd.DataFrame(list(materials.values()))
            if not selected_df.empty:
                selected_df = make_timezone_naive(selected_df)
                selected_df.columns = [col.capitalize().replace('_', ' ') for col in selected_df.columns]
#                selected_df.to_excel(writer, sheet_name='Selected Materials', index=False)

        # Seek to the beginning of the stream
        output.seek(0)

        # Create the HttpResponse object with the appropriate Excel header
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=database_views.xlsx'

        return response
    except Exception as e:
        print(f"Error generating Excel file: {e}")
        return HttpResponse("An error occurred while generating the Excel file.", status=500)

