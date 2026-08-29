<p align="center">
  <img src="images/Clink-PH.jpg" width="96" alt="Clink Philippine Language Packs">
</p>

<h1 align="center">Clink Philippine Language Packs</h1>

<p align="center">Opinionated community language packs for Filipino users of Clink.</p>

This repository provides additional language packs for [Clink](https://github.com/anti-ltd/clink-index), with a focus on languages commonly spoken in the Philippines.

The goal is to provide useful language data that reflects how people actually type, including **standard vocabulary, everyday language, slang, common typing shortcuts, proper nouns, and next-word prediction**.

## Supported Languages

| Language | Code  | Status      |
| -------- | ----- | ----------- |
| Cebuano  | `ceb` | ✅ Available |
| Filipino | `fil` | ✅ Available |

More Philippine languages and regional varieties will be added over time.

## Structure

Each language is built from multiple word lists separated by vocabulary type:

```text
source/
├── ph/
│   ├── proper-nouns.txt
│   └── sentences.txt
│
├── ceb/
│   ├── standard.txt
│   ├── colloquial.txt
│   ├── slang.txt
│   ├── shortcuts.txt
│   └── sentences.txt
│
└── fil/
    ├── standard.txt
    ├── colloquial.txt
    ├── slang.txt
    ├── shortcuts.txt
    └── sentences.txt
```

Dictionary files contain **one word per line**.

`sentences.txt` is different: it contains **one complete sentence per line** and is used to build the next-word prediction model.

### Dictionary sources

Each language has its own vocabulary lists:

* **`standard.txt`** — commonly accepted vocabulary
* **`colloquial.txt`** — informal words and expressions commonly used in everyday speech
* **`slang.txt`** — highly informal or non-standard expressions
* **`shortcuts.txt`** — shortened forms and typing conventions commonly used in chats and messages

The dictionary may therefore contain words that are not found in formal dictionaries but are commonly used when typing.

For example, Cebuano shortcuts such as:

```text
dli
nman
lng
sya
```

can be included even though they are not standard dictionary spellings.

## Shared Philippine Data

The `source/ph/` directory contains data that can be shared across multiple Philippine language packs.

### Proper nouns

`source/ph/proper-nouns.txt` contains widely recognizable Philippine proper nouns such as:

```text
Cebu
Manila
Davao
Mindanao
Visayas
Luzon
Jollibee
McDo
Ayala
Globe
PLDT
```

These words do not need to be duplicated in every language's source files.

When a language is built, the shared proper-noun list is automatically combined with that language's dictionary.

The list is intended for **widely recognizable places, people, organizations, brands, institutions, and other named entities in the Philippines**.

### Shared sentences

`source/ph/sentences.txt` contains Philippine-wide sentences that can be useful for next-word prediction across multiple language packs.

Language-specific sentence data can still be added under the individual language directory:

```text
source/
├── ph/
│   └── sentences.txt
│
├── ceb/
│   └── sentences.txt
│
└── fil/
    └── sentences.txt
```

This allows common Philippine terms and contexts to be shared without requiring the same data to be duplicated in every language.

## How Building Works

The repository uses `build.sh` as the main build command.

For example:

```bash
./build.sh ceb
```

The build script automatically:

1. Reads all dictionary `.txt` files in `source/ceb/`
2. Adds the shared `source/ph/proper-nouns.txt`
3. Combines the word lists
4. Removes duplicate words
5. Sorts the dictionary
6. Generates `Lexicons/ceb.clex`
7. Collects the available sentence sources
8. Builds `Lexicons/ceb.cngm`
9. Validates the completed language pack

The source files remain human-readable and easy to edit. The generated `.clex` and `.cngm` files should **not** be edited manually.

The build process can be thought of as:

```text
source/ceb/*.txt
        +
source/ph/proper-nouns.txt
        ↓
  combine word lists
        ↓
  deduplicate + sort
        ↓
   ┌────┴────┐
   ↓         ↓
ceb.clex   sentence data
              ↓
           ceb.cngm
```

## Building a Language

The recommended command is:

```bash
./build.sh ceb
```

You should see output similar to:

```text
Language: ceb
Dictionary sources: 4
Shared proper nouns: source/ph/proper-nouns.txt
Unique words: 18136

Building dictionary...
Built Lexicons/ceb.clex with 18,036 words.

Building next-word model...
Sentence sources: 2
Unique sentences: 360

Built Lexicons/ceb.cngm with 365 next-word pairs.
Validating pack...
ceb: looks ready for release.

✓ ceb build complete.
```

To validate a language separately:

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
    └── sentences.txt
```

All dictionary files should contain one word per line.

The `sentences.txt` file is optional. If provided, it should contain one complete sentence per line and will be used for next-word prediction.

Then run:

```bash
./build.sh ilo
```

The resulting files will be:

```text
Lexicons/
├── ilo.clex
└── ilo.cngm
```

The shared Philippine proper-noun list is automatically included in the dictionary.

## Contributing Vocabulary

When adding words, prioritize vocabulary that people actually use when typing.

Useful additions can include:

* formal dictionary words
* informal spellings
* shortened words
* chat expressions
* commonly omitted letters
* regional expressions
* slang
* repeated-number forms such as `buot2`
* common shortcuts such as `dli`, `nman`, `lng`, and `sya`

Keep words in the most appropriate category rather than mixing everything into `standard.txt`.

For example:

```text
standard.txt
    → standard vocabulary

colloquial.txt
    → everyday informal usage

slang.txt
    → slang and highly informal expressions

shortcuts.txt
    → common texting and typing shortcuts
```

The purpose of these packs is not to enforce formal spelling. They are intended to reflect **how people actually type**.

When possible, prefer vocabulary that is genuinely used by speakers rather than mechanically generated or translated vocabulary.

## Proper Nouns

Proper nouns that are broadly useful across the Philippines should generally be placed in:

```text
source/ph/proper-nouns.txt
```

Examples include Philippine cities, provinces, regions, major organizations, brands, institutions, and other widely recognized names.

For example:

```text
Bacoor
Cebu
Davao
Jollibee
McDo
Manila
```

This also allows proper nouns to participate in next-word prediction.

For example, sentence data can contain:

```text
Moadto ko sa Bacoor City.
Ganahan ko mokaon sa Jollibee.
```

Because `Bacoor`, `City`, and `Jollibee` are part of the combined dictionary, the next-word model can learn relationships such as:

```text
Bacoor → City
```

Keep the shared proper-noun list focused on names that are useful across multiple Philippine languages rather than ordinary vocabulary.

## Next-Word Prediction

A dictionary knows individual words. A next-word model learns relationships between words based on real sentences.

For example, a model may learn that after:

```text
Ganahan ko
```

the next word is more likely to be:

```text
mokaon
```

than an unrelated word.

Next-word prediction requires a **sentence corpus**, not a list of individual words.

### Sentence sources

Sentences can come from two locations:

```text
source/ph/sentences.txt
```

for shared Philippine sentences, and:

```text
source/ceb/sentences.txt
source/fil/sentences.txt
```

for language-specific sentences.

Each line should contain one complete sentence:

```text
Moadto ko sa Cebu ugma.
Ganahan ko mokaon ug Jollibee.
Asa ka padulong?
Unsa imong gibuhat?
Murag ulan karon.
```

When you run:

```bash
./build.sh ceb
```

the build process automatically collects the applicable sentence data and generates:

```text
Lexicons/ceb.cngm
```

The next-word model only uses words that are present in the language's combined dictionary. This keeps the `.cngm` model consistent with the `.clex` dictionary.

Larger and more varied collections of natural sentences generally produce better predictions.

Use sentence data that you are legally allowed to redistribute or process.

## Adding a New Language

A new language can be added by creating its source directory:

```text
source/
└── <code>/
    ├── standard.txt
    ├── colloquial.txt
    ├── slang.txt
    ├── shortcuts.txt
    └── sentences.txt
```

For example:

```text
source/
└── ilo/
    ├── standard.txt
    ├── colloquial.txt
    ├── slang.txt
    ├── shortcuts.txt
    └── sentences.txt
```

Then simply run:

```bash
./build.sh ilo
```

The build script handles dictionary generation, next-word prediction, deduplication, sorting, and validation.

## Publishing

After making changes, use:

```bash
./update.sh
```

This automatically:

1. Commits the changes
2. Pushes them to GitHub
3. Creates a version tag
4. Publishes the language-pack release

GitHub Actions then builds the release manifest and publishes the generated language-pack assets.

## License

See the repository's license and individual source files for information about the licensing of the language data.
