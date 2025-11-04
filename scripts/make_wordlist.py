"""
Utility script to produce a snapshot CSV of common English words
with approximate usage scores.

Requires:
    pip install wordfreq

Note: This is a setup tool, not part of the main application runtime.
"""

from pathlib import Path
import csv
import sys

# This import happens once up front; checked again in __main__.
import wordfreq


# Output file location
TARGET = Path(__file__).resolve().parents[1] / "data" / "words.csv"
LIMIT = 50_000


def build_list():
    """
    Retrieve top English words and write them to a CSV file.
    """
    print(f"Preparing word list (~{LIMIT} entries)...")

    words = wordfreq.top_n_list("en", n=LIMIT, wordlist="best")

    # Make sure data folder exists
    TARGET.parent.mkdir(exist_ok=True)

    try:
        with TARGET.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for w in words:
                score = wordfreq.zipf_frequency(w, "en")
                writer.writerow([w, score])

        print(f"Done → {TARGET}")
        print(f"Wrote {len(words)} words.")

    except OSError as err:
        print(f"Could not write to {TARGET}: {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")


if __name__ == "__main__":
    # Double-check dependency is present when run directly
    try:
        import wordfreq as _check
    except ImportError:
        print("Missing dependency 'wordfreq'. Install with:")
        print("    pip install wordfreq")
        sys.exit(1)

    build_list()
