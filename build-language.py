#!/usr/bin/env python3

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python build-language.py <language-code>")

    code = sys.argv[1]
    source_dir = ROOT / "source" / code
    combined = ROOT / "source" / f"{code}.txt"

    if not source_dir.is_dir():
        raise SystemExit(f"Source directory not found: {source_dir}")

    files = sorted(source_dir.glob("*.txt"))

    if not files:
        raise SystemExit(f"No .txt files found in {source_dir}")

    # Combine, deduplicate, and sort
    words = set()

    for file in files:
        with file.open(encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(word)

    combined.write_text(
        "\n".join(sorted(words)) + "\n",
        encoding="utf-8"
    )

    print(f"Combined {len(files)} source files → {len(words)} unique words")

    try:
        subprocess.run(
            [sys.executable, "build-pack.py", code, str(combined)],
            cwd=ROOT,
            check=True,
        )

        subprocess.run(
            [sys.executable, "tools/validate-pack.py", code],
            cwd=ROOT,
            check=True,
        )

    finally:
        combined.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
