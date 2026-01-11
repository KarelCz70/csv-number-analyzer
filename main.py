# CSV Number Analyzer
# Reads numbers from a CSV file, validates and categorizes them,
# logs invalid rows, and generates reports into an output folder.

import csv
import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze numbers from a CSV file and generate TXT/CSV reports."
    )

    parser.add_argument(
        "--input",
        default="data.csv",
        help="Input CSV file (default: data.csv)",
    )

    parser.add_argument(
        "--delimiter",
        default=";",
        help="CSV delimiter (default: ;)",
    )

    parser.add_argument(
        "--column",
        default="value",
        help="Name of the column containing numeric values (default: value)",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=25,
        help="Threshold for categorization (default: 25)",
    )

    parser.add_argument(
        "--min",
        dest="min_value",
        type=int,
        default=1,
        help="Minimum allowed value (default: 1)",
    )

    parser.add_argument(
        "--max",
        dest="max_value",
        type=int,
        default=100,
        help="Maximum allowed value (default: 100)",
    )

    parser.add_argument(
        "--outdir",
        default="outputs",
        help="Output directory (default: outputs)",
    )

    return parser.parse_args()


def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)


def categorize(numbers, threshold=25):
    low_numbers = []
    high_numbers = []

    for n in numbers:
        if n <= threshold:
            low_numbers.append(n)
        else:
            high_numbers.append(n)

    return low_numbers, high_numbers


def average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0


def read_numbers_with_invalids(
    filename,
    delimiter=";",
    column="value",
    min_value=1,
    max_value=100,
):
    numbers = []
    invalid_rows = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)

        # Kontrola, že existuje hlavička a požadovaný sloupec
        fieldnames = reader.fieldnames or []
        if not fieldnames:
            invalid_rows.append((1, "", "missing header row"))
            return numbers, invalid_rows

        if column not in fieldnames:
            invalid_rows.append((1, "", f"missing column '{column}'"))
            return numbers, invalid_rows

        # start=2 protože hlavička je řádek 1
        for line_no, row in enumerate(reader, start=2):
            raw = (row.get(column) or "").strip()

            if raw == "":
                invalid_rows.append((line_no, raw, "empty value"))
                continue

            if not raw.isdigit():
                invalid_rows.append((line_no, raw, "not a positive integer"))
                continue

            number = int(raw)
            if not (min_value <= number <= max_value):
                invalid_rows.append((line_no, raw, f"out of range {min_value}-{max_value}"))
                continue

            numbers.append(number)

    return numbers, invalid_rows


def save_report_txt(
    numbers,
    low_numbers,
    high_numbers,
    invalid_rows,
    threshold,
    min_value,
    max_value,
    column,
    filename,
):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("NUMBERS REPORT\n")
        file.write("----------------\n")
        file.write(f"Column: {column}\n")
        file.write(f"Valid range: {min_value}-{max_value}\n")
        file.write(f"Threshold: {threshold}\n\n")

        if not numbers:
            file.write("No valid numbers found.\n\n")
        else:
            file.write(f"Count: {len(numbers)}\n")
            file.write(f"Total: {sum(numbers)}\n")
            file.write(f"Average: {round(average(numbers), 2)}\n")
            file.write(f"Minimum: {min(numbers)}\n")
            file.write(f"Maximum: {max(numbers)}\n\n")

            file.write(f"Numbers <= {threshold}:\n")
            file.write(", ".join(map(str, low_numbers)) + "\n")
            file.write(f"Count <= {threshold}: {len(low_numbers)}\n\n")

            file.write(f"Numbers > {threshold}:\n")
            file.write(", ".join(map(str, high_numbers)) + "\n")
            file.write(f"Count > {threshold}: {len(high_numbers)}\n\n")

        file.write("INVALID ROWS\n")
        file.write("----------------\n")
        if not invalid_rows:
            file.write("None\n")
        else:
            for line_no, raw, reason in invalid_rows:
                file.write(f"Line {line_no}: '{raw}' -> {reason}\n")


def save_report_long_csv(numbers, threshold, filename, delimiter=";"):
    # Excel/pandas friendly: value, category, threshold (one value per row)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["value", "category", "threshold"])

        for n in numbers:
            category = "low" if n <= threshold else "high"
            writer.writerow([n, category, threshold])


def save_invalids_csv(invalid_rows, filename, delimiter=";"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["line_no", "raw_value", "reason"])

        for line_no, raw, reason in invalid_rows:
            writer.writerow([line_no, raw, reason])


def main():
    args = parse_arguments()

    input_file = args.input
    delimiter = args.delimiter
    outdir = args.outdir
    threshold = args.threshold
    column = args.column
    min_value = args.min_value
    max_value = args.max_value

    ensure_outdir(outdir)

    numbers, invalid_rows = read_numbers_with_invalids(
        input_file,
        delimiter=delimiter,
        column=column,
        min_value=min_value,
        max_value=max_value,
    )

    low_numbers, high_numbers = categorize(numbers, threshold=threshold) if numbers else ([], [])

    # Terminal summary
    if not numbers:
        print("No valid numbers found.")
        if invalid_rows:
            # vypiš první důvod, ať uživatel hned ví co je špatně
            print(f"First issue: Line {invalid_rows[0][0]} -> {invalid_rows[0][2]}")
    else:
        print("Valid numbers:", numbers)
        print("Count:", len(numbers))
        print("Total:", sum(numbers))
        print("Average:", round(average(numbers), 2))
        print("Minimum:", min(numbers))
        print("Maximum:", max(numbers))
        print(f"Low (<= {threshold}):", low_numbers)
        print(f"Low count:", len(low_numbers))
        print(f"High (> {threshold}):", high_numbers)
        print(f"High count:", len(high_numbers))

    report_txt = os.path.join(outdir, "report.txt")
    report_long_csv = os.path.join(outdir, "report_long.csv")
    invalid_csv = os.path.join(outdir, "invalid_rows.csv")

    save_report_txt(
        numbers,
        low_numbers,
        high_numbers,
        invalid_rows,
        threshold=threshold,
        min_value=min_value,
        max_value=max_value,
        column=column,
        filename=report_txt,
    )
    save_report_long_csv(numbers, threshold=threshold, filename=report_long_csv, delimiter=delimiter)
    save_invalids_csv(invalid_rows, filename=invalid_csv, delimiter=delimiter)

    print("\nSaved:")
    print(f"- {report_txt}")
    print(f"- {report_long_csv}")
    print(f"- {invalid_csv}")


if __name__ == "__main__":
    main()

