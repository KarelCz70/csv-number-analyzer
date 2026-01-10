# CSV Number Analyzer

This project is a Python command-line tool that reads numeric values from a CSV file,
filters invalid rows, categorizes valid numbers based on a configurable threshold,
and generates multiple reports in TXT and CSV formats.

---

## Features

- Reads numbers from a CSV file (with header)
- Validates values (only integers in range 1–100)
- Logs invalid rows with line number and reason
- Categorizes numbers based on a threshold
- Generates the following outputs:
  - Human-readable TXT report
  - Excel / pandas friendly CSV report
  - CSV file with invalid input rows

---

## Project Structure

csv-number-analyzer/
│
├── main.py
├── data.csv
├── outputs/
│ ├── report.txt
│ ├── report_long.csv
│ └── invalid_rows.csv


---

## Input Format

The input CSV file must contain a header row.
Numeric values are expected in the first column.

Example `data.csv`:

```csv
value
10
25
50
abc
150
How to Run

Make sure you have Python 3.9+ installed

Prepare your input CSV file (e.g. data.csv)

Run the script from the command line:

python main.py --input data.csv --threshold 25 --delimiter ";" --outdir outputs

Command-line Arguments

--input
Path to the input CSV file (default: data.csv)

--threshold
Threshold used for categorization (default: 25)

--delimiter
CSV delimiter character (default: ;)

--outdir
Output directory for generated reports (default: outputs)

Output

After execution, the following files are created in the output directory:

report.txt
Human-readable summary report

report_long.csv
One row per value with category (low / high), suitable for Excel or pandas

invalid_rows.csv
Log of invalid rows with line number and reason

Example Use Case

This tool can be used for:

Cleaning numeric CSV data

Generating summary reports for business or analysis tasks

Validating and categorizing input data before further processing

Notes

The script is intentionally written without external dependencies

Designed as a small, reusable automation tool


---

