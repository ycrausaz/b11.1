import pandas as pd
import openpyxl
from pathlib import Path

def get_excel_column_letter(column_number):
    """
    Convert column number to Excel column letter (e.g., 1 -> A, 27 -> AA)
    """
    result = ""
    while column_number > 0:
        column_number -= 1
        remainder = column_number % 26
        result = chr(65 + remainder) + result
        column_number //= 26
    return result

def compare_excel_files(file1_path: str, file2_path: str, output_path: str = "comparison_results.xlsx"):
    """
    Compare two Excel files sheet by sheet, analyzing differences based on matching headers.
    
    Args:
        file1_path (str): Path to the first Excel file
        file2_path (str): Path to the second Excel file
        output_path (str): Path where to save the comparison results
    """
    # Load both Excel files
    excel1 = pd.ExcelFile(file1_path)
    excel2 = pd.ExcelFile(file2_path)
    
    # Get sheet names from both files
    sheets1 = set(excel1.sheet_names)
    sheets2 = set(excel2.sheet_names)
    
    # Find common sheets
    common_sheets = sheets1.intersection(sheets2)
    
    # Create Excel writer for output
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Compare each common sheet
        for sheet_name in common_sheets:
            # Read sheets into dataframes
            df1 = pd.read_excel(excel1, sheet_name=sheet_name)
            df2 = pd.read_excel(excel2, sheet_name=sheet_name)
            
            # Get common columns
            common_cols = set(df1.columns).intersection(set(df2.columns))
            
            # Initialize differences dictionary
            differences = {
                'Sheet': [],
                'Column': [],
                'Excel_Column': [],  # New column for Excel column letters
                'Row_Index': [],
                'File1_Value': [],
                'File2_Value': []
            }
            
            # Compare values in common columns
            for col_idx, col in enumerate(common_cols, 1):
                # Ensure both columns have the same length
                max_length = max(len(df1), len(df2))
                if len(df1) < max_length:
                    df1 = df1.reindex(range(max_length))
                if len(df2) < max_length:
                    df2 = df2.reindex(range(max_length))
                
                # Compare values
                for idx in range(max_length):
                    val1 = df1.iloc[idx][col] if idx < len(df1) else None
                    val2 = df2.iloc[idx][col] if idx < len(df2) else None
                    
                    # Skip if both values are NaN or equal
                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    if pd.notna(val1) and pd.notna(val2) and val1 == val2:
                        continue
                    
                    differences['Sheet'].append(sheet_name)
                    differences['Column'].append(col)
                    differences['Excel_Column'].append(get_excel_column_letter(df1.columns.get_loc(col) + 1))
                    differences['Row_Index'].append(idx + 2)  # +2 for Excel row number (1-based + header)
                    differences['File1_Value'].append(str(val1) if pd.notna(val1) else 'NA')
                    differences['File2_Value'].append(str(val2) if pd.notna(val2) else 'NA')
            
            # Create differences DataFrame and save to output
            diff_df = pd.DataFrame(differences)
            if not diff_df.empty:
                diff_df.to_excel(writer, sheet_name=f"{sheet_name}_diff", index=False)
        
        # Create summary sheet
        summary = {
            'Description': [
                'Total sheets in File 1',
                'Total sheets in File 2',
                'Common sheets',
                'Sheets only in File 1',
                'Sheets only in File 2'
            ],
            'Value': [
                len(sheets1),
                len(sheets2),
                len(common_sheets),
                ', '.join(sheets1 - sheets2) or 'None',
                ', '.join(sheets2 - sheets1) or 'None'
            ]
        }
        pd.DataFrame(summary).to_excel(writer, sheet_name='Summary', index=False)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python script.py <file1_path> <file2_path> [output_path]")
        sys.exit(1)
    
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "comparison_results.xlsx"
    
    compare_excel_files(file1_path, file2_path, output_path)
    print(f"Comparison completed. Results saved to {output_path}")
