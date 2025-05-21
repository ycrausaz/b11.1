# log_export_utils.py
import io
import xlsxwriter
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db import connection

def export_logs_to_excel(start_date=None, end_date=None):
    """
    Export log entries to Excel with optional date filtering

    Parameters:
    start_date (datetime.date): The start date for filtering
    end_date (datetime.date): The end date for filtering

    Returns:
    HttpResponse: Excel file as a downloadable response
    """
    # Create a file-like buffer to receive Excel data
    buffer = io.BytesIO()

    # Create the Excel workbook with timezone handling
    workbook = xlsxwriter.Workbook(buffer, {'remove_timezone': True})
    worksheet = workbook.add_worksheet('Log Entries')

    # Add styles
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#CCCCCC',
        'border': 1
    })
    date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
    time_format = workbook.add_format({'num_format': 'hh:mm:ss'})

    # Set column widths
    worksheet.set_column('A:A', 10)  # ID
    worksheet.set_column('B:B', 15)  # Date
    worksheet.set_column('C:C', 10)  # Time
    worksheet.set_column('D:D', 15)  # Level
    worksheet.set_column('E:E', 100)  # Message

    # Write headers
    headers = ['ID', 'Date', 'Time', 'Level', 'Message']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Build parameterized query
    query = "SELECT id, timestamp, level, message FROM b11_1_log_entries"
    where_clauses = []
    params = []

    # Handle date filtering
    if start_date:
        # Convert start_date to ISO format string for SQL
        start_date_str = start_date.strftime('%Y-%m-%d')
        where_clauses.append("timestamp >= %s")
        params.append(start_date_str)

    if end_date:
        # Convert end_date to ISO format string and add 1 day to include the entire end date
        next_day = end_date + timedelta(days=1)
        end_date_str = next_day.strftime('%Y-%m-%d')
        where_clauses.append("timestamp < %s")
        params.append(end_date_str)

    # Add WHERE clause if we have conditions
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    # Add ORDER BY
    query += " ORDER BY timestamp DESC"

    # Execute query
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        log_entries = cursor.fetchall()

        # Write data rows
        for row_num, log_entry in enumerate(log_entries, 1):
            id_val, timestamp, level, message = log_entry

            # Write ID in column A
            worksheet.write(row_num, 0, id_val)

            # Write Date in column B
            worksheet.write_datetime(row_num, 1, timestamp, date_format)

            # Write Time in column C
            worksheet.write_datetime(row_num, 2, timestamp, time_format)

            # Write Level in column D
            worksheet.write(row_num, 3, level)

            # Write Message in column E
            worksheet.write(row_num, 4, message)

    # Close the workbook
    workbook.close()

    # Set up the response
    buffer.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"log_entries_{timestamp}.xlsx"

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
