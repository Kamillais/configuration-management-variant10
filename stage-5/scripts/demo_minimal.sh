#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m src.main --vfs data/minimal.csv --script examples/stage3.txt
