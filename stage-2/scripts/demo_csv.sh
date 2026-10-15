#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m src.main --vfs data/deep.csv --prompt "kamilla$" --script examples/stage4.txt
