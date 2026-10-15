@echo off
cd /d "%~dp0\.."
python -m src.main --vfs data\deep.csv --prompt "kamilla$" --script examples\stage4.txt
