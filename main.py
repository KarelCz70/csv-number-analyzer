# The script categorizes values based on a threshold,
# saves a human-readable TXT report and CSV outputs into /outputs.

import csv
import os


def read_numbers_with_invalids(filename="data.csv", delimiter=";"):
    numbers = []
    invalid_rows = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader, None)  # přeskočí hlavičku

        for line_no, row in enumerate(reader, start=2):  # start=2 kvůli hlavičce
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


def ensure_outputs_dir(path="outputs"):
    os.makedirs(path, exist_ok=True)


def save_report_txt(numbers, low_numbers, high_numbers, invalid_rows, threshold=25, filename="outputs/report.txt"):
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


def save_report_long_csv(numbers, threshold=25, filename="outputs/report_long.csv", delimiter=";"):
    # Excel/pandas friendly: value, category, threshold (jeden záznam = jeden řádek)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["value", "category", "threshold"])

        for n in numbers:
            category = "low" if n <= threshold else "high"
            writer.writerow([n, category, threshold])


def save_invalids_csv(invalid_rows, filename="outputs/invalid_rows.csv", delimiter=";"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["line_no", "raw_value", "reason"])

        for line_no, raw, reason in invalid_rows:
            writer.writerow([line_no, raw, reason])


def main():
    threshold = 25
    input_file = "data.csv"
    delimiter = ";"  # pro CZ Excel

    ensure_outputs_dir("outputs")

    numbers, invalid_rows = read_numbers_with_invalids(input_file, delimiter=delimiter)

    if not numbers:
        print("Soubor neobsahuje žádná platná čísla (1–100).")
    else:
        low_numbers, high_numbers = categorize(numbers, threshold=threshold)

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

    # když numbers je prázdné, potřebujeme mít low/high prázdné, aby TXT report fungoval
    if numbers:
        low_numbers, high_numbers = categorize(numbers, threshold=threshold)
    else:
        low_numbers, high_numbers = [], []

    save_report_txt(
        numbers,
        low_numbers,
        high_numbers,
        invalid_rows,
        threshold=threshold,
        filename="outputs/report.txt",
    )
    save_report_long_csv(numbers, threshold=threshold, filename="outputs/report_long.csv", delimiter=delimiter)
    save_invalids_csv(invalid_rows, filename="outputs/invalid_rows.csv", delimiter=delimiter)

    print("\nUloženo do složky outputs:")
    print("- outputs/report.txt")
    print("- outputs/report_long.csv")
    print("- outputs/invalid_rows.csv")


main()
