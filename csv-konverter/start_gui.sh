#!/bin/bash
# Startet die GUI für den CSV-Konverter
cd "$(dirname "$0")/src"
source ../.venv/bin/activate
python3 gui.py
