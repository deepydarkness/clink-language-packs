#!/usr/bin/env python3

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "source"
SHARED = SOURCE / "ph" / "proper-nouns.txt"
BUILD_PACK = ROOT / "build-pack.py"
BUILD_NEXT_WORD = ROOT / "tools" / "build-next-word.py"
VALIDATE_PACK = ROOT / "tools" / "validate-pack.py"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python build-language.py <language-code>")

    code = sys.argv[1]
    language_dir = SOURCE / code
    sentence_file = language_dir / "sentences.txt"

    if not language_dir.is_dir():
        raise SystemExit(f"source directory not found: {language_dir}")

    if not SHARED.is_file():
        raise SystemExit(f"shared proper-nouns file not found: {SHARED}")

    # Only use dictionary word lists.
    # sentences.txt is reserved for next-word prediction.
    txt_files = sorted(
        path for path in language_dir.glob("*.txt")
        if path.name != "sentences.txt"
    )

    if not txt_files:
        raise SystemExit(f"no dictionary .txt files found in {language_dir}")

    words = set()

    # Read language-specific word lists.
    for path in txt_files:
        with path.open(encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith("#"):
                    words.add(word)

    # Read shared Philippine proper nouns.
    with SHARED.open(encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
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
        print(f"Dictionary sources: {len(txt_files)}")
        print(f"Shared source: {SHARED}")
        print(f"Unique words: {len(combined)}")
        print()

        # Build CLEX.
        print("Building CLEX...")
        subprocess.run(
            [sys.executable, str(BUILD_PACK), code, str(temp_source)],
            cwd=ROOT,
            check=True
        )

        # Build next-word model if sentences.txt exists.
        if sentence_file.is_file():
            print()
            print(f"Building next-word model from: {sentence_file}")

            subprocess.run(
                [
                    sys.executable,
                    str(BUILD_NEXT_WORD),
                    code,
                    str(temp_source),
                    str(sentence_file),
                ],
                cwd=ROOT,
                check=True
            )
        else:
            print()
            print(f"No sentences.txt found; skipping next-word model.")

        # Validate everything.
        print()
        print("Validating pack...")
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
