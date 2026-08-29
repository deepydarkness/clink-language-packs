<p align="center">
  <img src="images/Clink-PH.jpg" width="96" alt="Clink Philippine Language Packs">
</p>

<h1 align="center">Clink Philippine Language Packs</h1>

<p align="center">Opinionated community language packs for Filipino users of Clink.</p>

This repository provides additional language packs for [Clink](https://github.com/anti-ltd/clink-index), focusing on languages commonly spoken in the Philippines.

The goal is to provide language data that reflects how people actually type, including **standard vocabulary, everyday language, slang, typing shortcuts, proper nouns, emoji aliases, and next-word prediction**.

## Supported Languages

| Language | Code | Status |
|---|---|---|
| Cebuano | `ceb` | ✅ Available |
| Filipino | `fil` | ✅ Available |

More Philippine languages and regional varieties will be added over time.

## What makes these packs different?

These packs are intended for **real-world typing**, rather than only formal dictionary use.

They may include:

- Standard vocabulary
- Colloquial and everyday words
- Slang and informal expressions
- Common chat shortcuts and spellings
- Philippine places, brands, organizations, and other proper nouns
- Local emoji aliases
- Next-word prediction based on real sentences

For example, Cebuano may include common typed forms such as `dli`, `nman`, `lng`, `sya`, and `buot2` alongside standard vocabulary.

## Sources

Language data is organized into editable text files containing one word or sentence per line.

Shared Philippine proper nouns are maintained separately so they can be reused across multiple language packs.

The compiled `.clex` dictionaries and `.cngm` next-word models are generated automatically from these source files.

## Building

A language pack can be built with:

```bash
./build.sh ceb