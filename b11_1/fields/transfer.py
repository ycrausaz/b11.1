import pandas as pd
import argparse

def concatenate_columns(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Initialize an empty list to store the concatenated data
    concatenated_data = []

    # Start from the third column (index 2, which corresponds to column 'C')
    for col in df.columns[2:]:
        # Add the column data to the concatenated list
        concatenated_data.extend(df[col].dropna().tolist())

    # Create a new DataFrame from the concatenated data
    result_df = pd.DataFrame(concatenated_data, columns=['Concatenated Data'])

    # Write the resulting DataFrame to a new Excel file
    result_df.to_excel(output_file, index=False)

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Concatenate columns from an Excel file starting from column 'C' and save to an Excel file.")
    parser.add_argument('input_file', type=str, help="Path to the input Excel file")
    parser.add_argument('output_file', type=str, help="Path to the output Excel file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    concatenate_columns(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

