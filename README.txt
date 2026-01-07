# CSV Number Analyzer

This project is a simple Python script that reads numbers from a CSV file,
categorizes them using a configurable threshold, and generates reports in
both TXT and CSV formats.

## Features

- Reads numbers from a CSV file
- Validates values (1–100)
- Categorizes numbers based on a threshold
- Generates:
  - Human-readable TXT report
  - Excel-friendly CSV report
  - CSV file with invalid rows

## Project Structure

csv-number-analyzer/
│
├── main.py
├── data.csv
├── outputs/
│ ├── report.txt
│ ├── report_long.csv
│ └── invalid_rows.csv


## Input Format

The input file `data.csv` must contain a single column with numbers.

Example:

value
10
25
50
abc
150


## How to Run

1. Make sure you have Python 3 installed
2. Place your input data in `data.csv`
3. Run the script:

```bash
python main.py

Configuration

You can change the categorization threshold directly in main.py:

threshold = 25