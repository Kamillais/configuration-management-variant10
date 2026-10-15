#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m src.main --script examples/stage5.txt
