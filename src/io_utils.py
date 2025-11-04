"""
Utility functions to read/write word-frequency pairs from CSV files.

Each line in the CSV should contain:
    word, score
(without a header row)
"""

import csv


def load_csv(path):
    """
    Read a CSV file and return a list of (word, freq) tuples.
    Frequencies are converted to float; invalid entries become 0.0.
    """
    items = []

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                # ignore blank / empty lines
                if not row:
                    continue

                w = row[0].strip().lower()

                # attempt to parse frequency
                freq = 0.0
                if len(row) > 1:
                    try:
                        freq = float(row[1])
                    except Exception:
                        freq = 0.0

                items.append((w, freq))

    except FileNotFoundError:
        print(f"[load_csv] File not found: {path}")
        return []
    except Exception as err:
        print(f"[load_csv] Error reading {path}: {err}")
        return []

    return items


def save_csv(path, pairs):
    """
    Write the given (word, freq) list to a CSV file, overwriting if needed.
    """
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for w, freq in pairs:
                writer.writerow((w, freq))

    except Exception as err:
        print(f"[save_csv] Could not write to {path}: {err}")
