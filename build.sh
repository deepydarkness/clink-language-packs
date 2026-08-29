#!/usr/bin/env bash

set -e

LANGUAGE="$1"

if [ -z "$LANGUAGE" ]; then
    echo "Usage: ./build.sh <language-code>"
    exit 1
fi

python build-language.py "$LANGUAGE"
