python transfer.py import_B11-1.xlsx output.xlsx
open output.xlsx
[copy content of 'output.xlsx' into 'output.csv']
cat output.csv | sed -f command_file.txt > output_clean.csv
[import 'output_clean.csv' in PostgreSQP: \i /Users/yann/Prog/Python/LBA/symm/fields/output_clean.csv]
