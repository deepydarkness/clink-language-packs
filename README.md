<p align="center">
  <img src="https://github.com/anti-ltd/clink-index" width="96" alt="Clink app icon">
</p>

<h1 align="center">Clink Philippine Language Packs</h1>

<p align="center">Opinionated community language packs for Filipino users of Clink.</p>

This repository provides additional language packs for [Clink](https://github.com/anti-ltd/clink), with a focus on languages commonly spoken in the Philippines.

The goal is to provide useful language data that reflects how people actually type, including **standard vocabulary, everyday language, slang, common typing shortcuts, and next-word prediction**.

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
│   └── proper-nouns.txt
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

Dictionary files contain **one word per line**. `sentences.txt` is different: it contains **one complete sentence per line** and is used to build the next-word prediction model.

When a language is built, its dictionary word lists are combined with the shared Philippine `proper-nouns.txt` list. The build process then **removes duplicates, sorts the words, and generates the Clink `.clex` dictionary**.

If `sentences.txt` is present, it is also used to generate the language's `.cngm` next-word prediction model.

For example:

```text
source/ceb/
├── standard.txt
├── colloquial.txt
├── slang.txt
├── shortcuts.txt
└── sentences.txt

source/ph/proper-nouns.txt
        ↓
  combine word lists
        ↓
  deduplicate + sort
        ↓
   ┌────┴────┐
   ↓         ↓
ceb.clex   ceb.cngm
```

This keeps the source data easy to edit while avoiding duplication between Philippine language packs.

### Vocabulary categories

* **Standard** — commonly accepted vocabulary
* **Colloquial** — informal words and expressions commonly used in everyday speech
* **Slang** — highly informal or non-standard expressions
* **Shortcuts** — shortened forms and typing conventions commonly used in chats and messages
* **Proper nouns** — names of places, people, organizations, brands, institutions, and other named entities commonly used in the Philippines

The dictionary may therefore contain words that are not found in formal dictionaries but are commonly used when typing.

## Shared Philippine Proper Nouns

`source/ph/proper-nouns.txt` contains proper nouns that are useful across multiple Philippine language packs.

Examples include:

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

These words do not need to be duplicated in every language's source files. When a language pack is built, the shared proper-noun list is automatically included in its `.clex` dictionary.

Keep this list focused on **widely recognizable Philippine proper nouns** rather than ordinary vocabulary.

## Building a Language Pack

Language packs are built using `build-language.py`.

For example:

```bash
python build-language.py ceb
```

The script automatically:

1. Reads the dictionary word lists in `source/ceb/`
2. Adds the shared `source/ph/proper-nouns.txt`
3. Removes duplicate words
4. Sorts the combined word list
5. Generates `Lexicons/ceb.clex`
6. Builds `Lexicons/ceb.cngm` if `source/ceb/sentences.txt` exists
7. Validates the resulting pack

The generated `.clex` and `.cngm` files should **not** be edited manually.

You can also validate the pack separately:

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

The `sentences.txt` file is optional. If provided, it should contain one complete sentence per line and will be used for next-word prediction.

Then build it with:

```bash
python build-language.py ilo
```

The resulting files will be:

```text
Lexicons/
├── ilo.clex
└── ilo.cngm
```

The shared Philippine proper-noun list will automatically be included in the dictionary.

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

When possible, prefer words that are actually used by speakers rather than mechanically generated or translated vocabulary.

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

To add one, create:

```text
source/ceb/sentences.txt
```

and put one complete sentence on each line:

```text
Moadto ko sa Cebu ugma.
Ganahan ko mokaon ug Jollibee.
Asa ka padulong?
Unsa imong gibuhat?
Murag ulan karon.
```

Then simply run:

```bash
python build-language.py ceb
```

The build script automatically uses the combined dictionary and `sentences.txt` to generate:

```text
Lexicons/ceb.cngm
```

The next-word model only uses words that are present in the language's dictionary, keeping the model consistent with the `.clex` file.

Use sentence data that you are legally allowed to redistribute or process. Larger and more varied collections of natural sentences generally produce better predictions.

## License

See the repository's license and individual source files for information about the licensing of the language data.
