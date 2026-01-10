# The script categorizes values based on a threshold and generates reports.
# It reads numbers from a CSV file, logs invalid rows, and outputs:
# - outputs/report.txt (human readable)
# - outputs/report_long.csv (Excel/pandas friendly)
# - outputs/invalid_rows.csv (invalid input log)

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
        "--threshold",
        type=int,
        default=25,
        help="Threshold for categorization (default: 25)",
    )

    parser.add_argument(
        "--delimiter",
        default=";",
        help="CSV delimiter (default: ;)",
    )

    parser.add_argument(
        "--outdir",
        default="outputs",
        help="Output directory (default: outputs)",
    )

    return parser.parse_args()


def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)

def read_numbers_with_invalids(filename, delimiter=";"):
    numbers = []
    invalid_rows = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)

        for line_no, row in enumerate(reader, start=2):
            raw = (row.get("value") or "").strip()
        reader = csv.reader(file, delimiter=delimiter)
        next(reader, None)  # skip header safely

        for line_no, row in enumerate(reader, start=2):  # start=2 because header is line 1
            if not row:
                invalid_rows.append((line_no, "", "empty row"))
                continue

            raw = row[0].strip()

            if raw == "":
                invalid_rows.append((line_no, raw, "empty value"))
                continue

            if not raw.isdigit():
                invalid_rows.append((line_no, raw, "not a positive integer"))
                continue

            number = int(raw)
            if not (1 <= number <= 100):
                invalid_rows.append((line_no, raw, "out of range 1-100"))
                continue

            numbers.append(number)

    return numbers, invalid_rows



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


def save_report_txt(numbers, low_numbers, high_numbers, invalid_rows, threshold, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("NUMBERS REPORT\n")
        file.write("----------------\n")
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
    # Excel/pandas friendly: one value per row + category
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
    threshold = args.threshold
    delimiter = args.delimiter
    outdir = args.outdir

    ensure_outdir(outdir)

    numbers, invalid_rows = read_numbers_with_invalids(input_file, delimiter=delimiter)
    low_numbers, high_numbers = categorize(numbers, threshold=threshold) if numbers else ([], [])

    if not numbers:
        print("Soubor neobsahuje žádná platná čísla (1–100).")
    else:
        print("Načtená a validní čísla:", numbers)
        print("Počet čísel:", len(numbers))
        print("Součet:", sum(numbers))
        print("Průměr:", round(average(numbers), 2))
        print("Minimum:", min(numbers))
        print("Maximum:", max(numbers))
        print(f"Načtená čísla ≤ {threshold}:", low_numbers)
        print(f"Počet čísel ≤ {threshold}:", len(low_numbers))
        print(f"Načtená čísla > {threshold}:", high_numbers)
        print(f"Počet čísel > {threshold}:", len(high_numbers))

    report_txt = os.path.join(outdir, "report.txt")
    report_long_csv = os.path.join(outdir, "report_long.csv")
    invalid_csv = os.path.join(outdir, "invalid_rows.csv")

    save_report_txt(numbers, low_numbers, high_numbers, invalid_rows, threshold, report_txt)
    save_report_long_csv(numbers, threshold, report_long_csv, delimiter=delimiter)
    save_invalids_csv(invalid_rows, invalid_csv, delimiter=delimiter)

    print("\nUloženo:")
    print(f"- {report_txt}")
    print(f"- {report_long_csv}")
    print(f"- {invalid_csv}")


if __name__ == "__main__":
    main()

