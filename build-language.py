#!/usr/bin/env python3

import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "source"
SHARED = SOURCE / "ph" / "proper-nouns.txt"
BUILD_PACK = ROOT / "build-pack.py"
VALIDATE_PACK = ROOT / "tools" / "validate-pack.py"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python build-language.py <language-code>")

    code = sys.argv[1]
    language_dir = SOURCE / code

    if not language_dir.is_dir():
        raise SystemExit(f"source directory not found: {language_dir}")

    txt_files = sorted(language_dir.glob("*.txt"))

    if not txt_files:
        raise SystemExit(f"no .txt source files found in {language_dir}")

    if not SHARED.is_file():
        raise SystemExit(f"shared proper-nouns file not found: {SHARED}")

    words = set()

    # Read language-specific word lists.
    for path in txt_files:
        with path.open(encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(word)

    # Read shared Philippine proper nouns.
    with SHARED.open(encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                words.add(word)

    # Sort the final combined dictionary.
    combined = sorted(words, key=str.casefold)

    # Temporary combined source file.
    temp_source = SOURCE / f".{code}.combined.txt"

    try:
        temp_source.write_text(
            "\n".join(combined) + "\n",
            encoding="utf-8"
        )

        print(f"Language: {code}")
        print(f"Language sources: {len(txt_files)}")
        print(f"Shared source: {SHARED}")
        print(f"Unique words: {len(combined)}")
        print()

        # Build CLEX.
        subprocess.run(
            [sys.executable, str(BUILD_PACK), code, str(temp_source)],
            cwd=ROOT,
            check=True
        )

        # Validate CLEX.
        subprocess.run(
            [sys.executable, str(VALIDATE_PACK), code],
            cwd=ROOT,
            check=True
        )

    finally:
        if temp_source.exists():
            temp_source.unlink()


if __name__ == "__main__":
    main()
