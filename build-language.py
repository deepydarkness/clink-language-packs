#!/usr/bin/env python3

import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "source"
SHARED = SOURCE / "ph" / "proper-nouns.txt"
BUILD_PACK = ROOT / "build-pack.py"
BUILD_NEXT_WORD = ROOT / "tools" / "build-next-word.py"
VALIDATE_PACK = ROOT / "tools" / "validate-pack.py"


def read_words(path):
    words = set()

    with path.open(encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
                words.add(word)

    return words


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python build-language.py <language-code>")

    code = sys.argv[1]
    language_dir = SOURCE / code

    if not language_dir.is_dir():
        raise SystemExit(f"source directory not found: {language_dir}")

    txt_files = sorted(
        path for path in language_dir.glob("*.txt")
        if path.name != "sentences.txt"
    )

    if not txt_files:
        raise SystemExit(f"no dictionary .txt source files found in {language_dir}")

    if not SHARED.is_file():
        raise SystemExit(f"shared proper-nouns file not found: {SHARED}")

    words = set()

    # Read language-specific dictionary word lists.
    for path in txt_files:
        words.update(read_words(path))

    # Read shared Philippine proper nouns.
    words.update(read_words(SHARED))

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
        print(f"Shared proper nouns: {SHARED}")
        print(f"Unique words: {len(combined):,}")
        print()

        # Build CLEX.
        print("Building dictionary...")
        subprocess.run(
            [
                sys.executable,
                str(BUILD_PACK),
                code,
                str(temp_source)
            ],
            cwd=ROOT,
            check=True
        )

        # Build next-word model if sentences.txt exists.
        sentences = language_dir / "sentences.txt"

        if sentences.is_file():
            print()
            print("Building next-word model...")
            print("Sentence source:", sentences)

            subprocess.run(
                [
                    sys.executable,
                    str(BUILD_NEXT_WORD),
                    code,
                    str(temp_source),
                    str(sentences)
                ],
                cwd=ROOT,
                check=True
            )
        else:
            print()
            print("No sentences.txt found; skipping next-word model.")

        # Copy emoji metadata if present.
        emoji_source = language_dir / "emoji.json"
        emoji_destination = ROOT / "Lexicons" / f"{code}.emoji.json"

        if emoji_source.is_file():
            print()
            print("Copying emoji metadata...")

            emoji_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(emoji_source, emoji_destination)

            print(f"Copied {emoji_destination}")
        else:
            # Remove an old generated emoji file if the source was deleted.
            if emoji_destination.exists():
                emoji_destination.unlink()
                print()
                print(f"Removed {emoji_destination}")

        # Validate everything.
        print()
        print("Validating pack...")

        subprocess.run(
            [
                sys.executable,
                str(VALIDATE_PACK),
                code
            ],
            cwd=ROOT,
            check=True
        )

        print()
        print(f"✓ {code} build complete.")

    finally:
        if temp_source.exists():
            temp_source.unlink()


if __name__ == "__main__":
    main()
