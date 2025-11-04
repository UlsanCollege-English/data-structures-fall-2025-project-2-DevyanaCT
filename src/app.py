#!/usr/bin/env python3
"""
Command-line interface for trie-based autocomplete.

Accepted commands (line-based):
  load <file>
  save <file>
  insert <word> <freq>
  remove <word>
  contains <word>
  complete <prefix> <k>
  stats
  quit
"""

import sys
import os
from pathlib import Path
from typing import Tuple

# add project root to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.trie import Trie
from src.io_utils import load_csv, save_csv


def do_load(path: str) -> Trie:
    """Load a new trie from a CSV file."""
    p = Path(path)
    data = load_csv(p)
    t = Trie()
    for w, s in data:
        t.insert(w, s)
    return t


def do_save(t: Trie, path: str) -> None:
    """Write the trie items (word,freq) to disk."""
    save_csv(Path(path), t.items())


def do_insert(t: Trie, w: str, f: str) -> None:
    t.insert(w.lower(), float(f))


def do_remove(t: Trie, w: str) -> None:
    print("OK" if t.remove(w.lower()) else "MISS")


def do_contains(t: Trie, w: str) -> None:
    print("YES" if t.contains(w.lower()) else "NO")


def do_complete(t: Trie, pref: str, k: str) -> None:
    k_int = int(k)
    results = t.complete(pref.lower(), k_int)
    print(",".join(results))


def do_stats(t: Trie) -> None:
    count, height, nodes = t.stats()
    print(f"words={count} height={height} nodes={nodes}")


def handle_command(line: str, t: Trie) -> Tuple[bool, Trie]:
    line = line.strip()
    if not line:
        return True, t

    parts = line.split()
    cmd = parts[0].lower()

    try:
        if cmd == "quit":
            return False, t

        elif cmd == "load" and len(parts) >= 2:
            file_path = " ".join(parts[1:])
            t = do_load(file_path)
            return True, t

        elif cmd == "save" and len(parts) >= 2:
            file_path = " ".join(parts[1:])
            do_save(t, file_path)
            return True, t

        elif cmd == "insert" and len(parts) == 3:
            do_insert(t, parts[1], parts[2])

        elif cmd == "remove" and len(parts) == 2:
            do_remove(t, parts[1])

        elif cmd == "contains" and len(parts) == 2:
            do_contains(t, parts[1])

        elif cmd == "complete" and len(parts) == 3:
            do_complete(t, parts[1], parts[2])

        elif cmd == "stats" and len(parts) == 1:
            do_stats(t)

    except FileNotFoundError:
        print(f"ERROR: cannot find file '{parts[1]}'", file=sys.stderr)
    except (IOError, OSError) as e:
        print(f"ERROR: file access issue: {e}", file=sys.stderr)
    except Exception:
        pass  # ignore malformed input silently

    return True, t


def main():
    trie = Trie()
    for line in sys.stdin:
        keep_running, trie = handle_command(line, trie)
        if not keep_running:
            break


if __name__ == "__main__":
    main()
