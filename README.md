<p align="center">
  <img src="https://raw.githubusercontent.com/anti-ltd/clink-language-packs/main/icon-1024.png" width="96" alt="Clink app icon">
</p>

<h1 align="center">Clink Philippine Language Packs</h1>

<p align="center">Opinionated community language packs for Filipino users of Clink.</p>

This repository provides additional language packs for [Clink](https://github.com/anti-ltd/clink), with a focus on languages commonly spoken in the Philippines.

The goal is to make useful Filipino-language dictionaries available for Clink, including both **standard vocabulary** and **common everyday usage** that people actually type.

## Supported Languages

| Language    | Code  | Status      |
| ----------- | ----- | ----------- |
| Cebuano     | `ceb` | ✅ Available |
| Filipino     | `fil` | ✅ Available |

More Philippine languages and regional varieties may be added over time.

## Structure

Each dictionary in this repo is built from multiple word lists, separated by type:

```text
source/
└── fil/
    ├── standard.txt
    ├── colloquial.txt
    ├── slang.txt
    ├── shortcuts.txt
    └── proper-nouns.txt
```

Each file contains **one word per line**. The build process combines the lists, removes duplicates, sorts the words, and generates the Clink `.clex` dictionary.

This makes it easy to add or modify vocabulary without manually editing the compiled `.clex` file.

### Vocabulary categories

* **Standard** — commonly accepted vocabulary
* **Colloquial** — informal words and expressions commonly used in everyday speech
* **Slang** — highly informal or non-standard expressions
* **Shortcuts** — common shortened forms and typing conventions used in chats and messages

The dictionary may therefore contain words that are not found in formal dictionaries but are commonly used when typing.

## Building a Language Pack

Language packs can be built from multiple word-list files.

For example:

```bash
python build-language.py ceb
```

This combines the files in `source/ceb/`, removes duplicate words, sorts them, and generates:

```text
Lexicons/ceb.clex
```

The generated `.clex` file should not be edited manually.

After building, validate the pack:

```bash
python tools/validate-pack.py ceb
```

## Adding a New Language

To add another Philippine language, create a directory under `source/` using its language code:

```text
source/
└── ilo/
    ├── standard.txt
    ├── colloquial.txt
    ├── slang.txt
    ├── shortcuts.txt
    └── proper-nouns.txt
```

Then build it with:

```bash
python build-language.py ilo
```

The resulting dictionary will be:

```text
Lexicons/ilo.clex
```

## Contributing Vocabulary

When adding words, prioritize vocabulary that people actually use when typing.

Formal dictionary words are useful, but everyday typing may also include:

* informal spellings
* shortened words
* chat expressions
* commonly omitted letters
* regional expressions
* repeated-number forms such as `buot2`
* common shortcuts such as `dli`, `nman`, `lng`, and `sya`

These should generally be kept in the appropriate **colloquial, slang, or shortcuts** word list rather than mixed into the standard vocabulary.

## Next-Word Prediction

The current language packs primarily provide dictionary data.

The `.clex` dictionary contains words that Clink can recognize and suggest, but **the word lists themselves do not provide next-word prediction data**.

Next-word prediction can be added separately in the future using a sentence corpus.

## License

See the repository's license and individual source files for information about the licensing of the language data.
