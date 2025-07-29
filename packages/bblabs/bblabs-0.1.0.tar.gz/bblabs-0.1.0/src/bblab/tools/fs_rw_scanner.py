#!/usr/bin/env python
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict
from collections.abc import Callable

# Dict to store results found in all modules to ensure uniqueness
RESULTS = {}
_UNIQUE = True
EXCLUDED_DIRS = {"venv", "__pycache__"}


# Regex patterns to detect file write/modify operations
WRITE_PATTERNS = [
    r"\bopen\s*\(.*,\s*['\"]w[bt]?['\"]",
    r"\bopen\s*\(.*,\s*['\"]a[bt]?['\"]",
    r"\bos\.(remove|unlink|rename|replace|rmdir|mkdir)\s*\(",
    r"\bshutil\.(move|copyfile|copy|rmtree|copy2|copytree)\s*\(",
    r"\bPath\s*\(.*\)\.write_(text|bytes)\s*\(",
    r"\bPath\s*\(.*\)\.(mkdir|unlink|rename)\s*\(",
    r"\bto_csv\s*\(",
    r"\bto_excel\s*\(",
    r"\bto_json\s*\(",
    r"\bto_pickle\s*\(",
    r"\bpickle\.dump\s*\(",
    r"\bpickle\.dumps\s*\(",
    r"\bjson\.dump\s*\(",
    r"\bnumpy\.save\s*\(",
    r"\bnumpy\.savez\s*\(",
    r"\bnumpy\.savez_compressed\s*\(",
    r"\b(torch\.save|save_model)\s*\(",
]

# Pattern list: path usage, file/folder-like variables or strings, slashes, file extensions
PATH_RELATED_PATTERNS = [
    r"\bos\.path\.",  # os.path
    r"\bpathlib\.|(?<!\w)Path\s*\(",  # pathlib usage
    r"\bPath\s*\([^\)]*\)\s*/",  # Path(...) / "file"
    r"[\"'].*[\\/].*[\"']",  # strings with / or \
    r"[\"'].*\.(csv|json|xlsx?|txt|pkl|pickle|zip)[\"']",  # common file extensions
    r"\b(file(name)?|folder(name)?|directory|dir|path(s)?|_path_?|path_)\b",  # variable/attr names
]


def parse_args():
    """Argparse for filesystem read-write operation scanner module."""
    parser = argparse.ArgumentParser(description="Scan Python files for FS operations.")
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Target directory to scan (default: current directory)",
    )
    parser.add_argument("--exclude", "-e", nargs="*", default=[], help="Directory names to exclude")
    return parser.parse_args()


def find_write_ops_in_file(filepath, unique_results=_UNIQUE):
    """
    Returns a list of (line number, line) for lines that performs filesystem write activity.

    based on:
      - fs ops usage from a wide range of write patters regex
    """
    global RESULTS  # noqa: PLW0602
    matches = []
    try:
        lines = Path(filepath).read_text(encoding="utf-8").split("\n")
    except (UnicodeDecodeError, OSError):
        return matches  # Skip unreadable files

    for lineno, line in enumerate(lines, start=1):
        for pattern in WRITE_PATTERNS:
            if re.search(pattern, line):
                match = (lineno, line.strip())
                if unique_results:
                    if match in RESULTS:
                        break
                    RESULTS[match] = True
                matches.append(match)
                break  # avoid duplicate hits on same line
    return matches


def find_possible_fs_ops_in_file(filepath, unique_results=_UNIQUE):
    """
    Returns a list of (line number, line) for lines that may involve filesystem activity.

    based on:
      - usage of os.path, pathlib.Path, or Path /
      - variables and strings resembling paths or filenames
    """
    global RESULTS  # noqa: PLW0602
    matches = []
    try:
        lines = Path(filepath).read_text(encoding="utf-8").split("\n")
    except (UnicodeDecodeError, OSError):
        return matches

    for lineno, line in enumerate(lines, start=1):
        for pattern in PATH_RELATED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                match = (lineno, line.strip())
                if unique_results:
                    if match in RESULTS:
                        break
                    RESULTS[match] = True
                matches.append(match)
                break
    return matches


def scan_directory(
    root_path: str, fn: Callable, excluded_dirs: list | None = None
) -> tuple[int, int, int]:
    """
    Scans the given directory recursively and executes fs ops finding methods.

    :param root_path: (str): directory to scan
    :param fn: (Callable): function to apply to each Python file
    :param excluded_dirs: (set[str]): additional directories to exclude
    :returns : total_matches, total_files, total_dirs
    """
    root_path = Path(root_path)
    excluded_dirs = EXCLUDED_DIRS.union(excluded_dirs or set())

    results_by_file = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories in-place
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in excluded_dirs]

        for filename in filenames:
            if filename in excluded_dirs:
                print(f"[-] Skipping: 📜 {dirpath}/{filename}")
                continue
            if not filename.endswith(".py"):
                continue

            file_path = Path(dirpath) / filename

            if self_file_name in str(file_path):
                continue  # Skip this script itself

            matches = fn(file_path)
            if matches:
                results_by_file[file_path] = matches

    # With rglob exclusion logic works, but it iterates through all files in excluded dirs
    # for file_path in root_path.rglob('*.py'):
    #     # Skip this script
    #     if self_file_name in str(file_path):
    #         continue

    #     # Skip dot directories and excluded directories
    #     if any(part.startswith('.') or part in excluded_dirs for part in file_path.parts):
    #         print(f'[-] Skipping: 📁 {file_path} {file_path.parts}')
    #         continue

    #     matches = fn(file_path)
    #     if matches:
    #         results_by_file[file_path] = matches

    # Output results
    for file_path, matches in results_by_file.items():
        print(f"\n🔍 File:: {file_path}")
        for lineno, line in matches:
            print(f"  Line {lineno}: {line}")

    # Summary
    _total_matches = sum(len(matches) for matches in results_by_file.values())
    _total_files = len(results_by_file)
    _total_dirs = len({f.parent for f in results_by_file})

    return _total_matches, _total_files, _total_dirs


if __name__ == "__main__":
    args = parse_args()

    target_dir = args.target_dir
    additional_excludes = set(args.exclude)
    EXCLUDED_DIRS = EXCLUDED_DIRS.union(additional_excludes)

    self_file_name = Path(__file__).stem

    print(f"{'-' * 88}\n🧩 Script  : {self_file_name}\n📁 Scanning: {Path(target_dir).absolute()}")
    print(f"🚫 Excluded: {EXCLUDED_DIRS}")

    print(f"{'-' * 88}\n🛠️ Finding filesystem write operations...\n{'-' * 88}")
    total_matches, total_files, total_dirs = scan_directory(target_dir, fn=find_write_ops_in_file)
    print(
        f"\n🧩 {total_matches} write ops found in "
        f"📜 {total_files} modules across 📁 {total_dirs} directories.\n"
    )

    print(f"{'-' * 88}\n📝 Finding possible filesystem operations...\n{'-' * 88}")
    total_matches, total_files, total_dirs = scan_directory(
        target_dir, fn=find_possible_fs_ops_in_file
    )
    print(
        f"\n🧩 {total_matches} possible fs ops found in "
        f"📜 {total_files} modules across 📁 {total_dirs} directories.\n"
    )
