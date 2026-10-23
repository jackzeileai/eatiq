#!/bin/sh
# Builds /join, /join/v2 and /join/100 from _src.html (see _build.py).
cd "$(dirname "$0")" && python3 _build.py
