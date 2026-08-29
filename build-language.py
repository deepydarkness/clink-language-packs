#!/usr/bin/env python3

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "source"

SHARED_PROPER_NOUNS = SOURCE / "ph" / "proper-nouns.txt"
SHARED_SENTENCES = SOURCE / "ph" / "sentences.txt"

BUILD_PACK = ROOT / "build-pack.py"
BUILD_NEXT_WORD = ROOT / "tools" / "build-next-word.py"
VALIDATE_PACK = ROOT / "tools" / "validate-pack.py"


def read_words(path):
    words = set()

    with path.open(encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                words.add(word)

    return words


def read_sentences(path):
    if not path.is_file():
        return []

    with path.open(encoding="utf-8") as f:
        return [
            line.rstrip()
            for line in f
            if line.strip()
        ]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python build-language.py <language-code>")

    code = sys.argv[1]
    language_dir = SOURCE / code

    if not language_dir.is_dir():
        raise SystemExit(f"source directory not found: {language_dir}")

    # ------------------------------------------------------------
    # Dictionary
    # ------------------------------------------------------------

    txt_files = sorted(
        path for path in language_dir.glob("*.txt")
        if path.name != "sentences.txt"
    )

    if not txt_files:
        raise SystemExit(f"no dictionary source files found in {language_dir}")

    if not SHARED_PROPER_NOUNS.is_file():
        raise SystemExit(
            f"shared proper-nouns file not found: {SHARED_PROPER_NOUNS}"
        )

    words = set()

    # Language-specific word lists.
    for path in txt_files:
        words.update(read_words(path))

    # Shared Philippine proper nouns.
    words.update(read_words(SHARED_PROPER_NOUNS))

    # Sort the final dictionary.
    combined = sorted(words, key=str.casefold)

    # Temporary combined dictionary source.
    temp_source = SOURCE / f".{code}.combined.txt"

    # ------------------------------------------------------------
    # Next-word corpus
    # ------------------------------------------------------------

    language_sentences = SOURCE / code / "sentences.txt"

    sentence_sources = []

    if language_sentences.is_file():
        sentence_sources.append(language_sentences)

    if SHARED_SENTENCES.is_file():
        sentence_sources.append(SHARED_SENTENCES)

    temp_sentences = SOURCE / f".{code}.combined.sentences.txt"

    try:
        # --------------------------------------------------------
        # Write combined dictionary
        # --------------------------------------------------------

        temp_source.write_text(
            "\n".join(combined) + "\n",
            encoding="utf-8"
        )

        print(f"Language: {code}")
        print(f"Dictionary sources: {len(txt_files)}")
        print(f"Shared proper nouns: {SHARED_PROPER_NOUNS}")
        print(f"Unique words: {len(combined)}")
        print()

        # --------------------------------------------------------
        # Build CLEX
        # --------------------------------------------------------

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

        print()

        # --------------------------------------------------------
        # Build CNGM if sentence data exists
        # --------------------------------------------------------

        if sentence_sources:
            sentences = []

            for path in sentence_sources:
                sentences.extend(read_sentences(path))

            # Remove duplicate sentences while preserving order.
            sentences = list(dict.fromkeys(sentences))

            temp_sentences.write_text(
                "\n".join(sentences) + "\n",
                encoding="utf-8"
            )

            print("Building next-word model...")
            print(f"Sentence sources: {len(sentence_sources)}")
            print(f"Unique sentences: {len(sentences)}")
            print()

            subprocess.run(
                [
                    sys.executable,
                    str(BUILD_NEXT_WORD),
                    code,
                    str(temp_source),
                    str(temp_sentences)
                ],
                cwd=ROOT,
                check=True
            )

        else:
            print("No sentence corpus found.")
            print("Skipping next-word model.")
            print()

        # --------------------------------------------------------
        # Validate
        # --------------------------------------------------------

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
        # Clean temporary files.
        if temp_source.exists():
            temp_source.unlink()

        if temp_sentences.exists():
            temp_sentences.unlink()


if __name__ == "__main__":
    main()
