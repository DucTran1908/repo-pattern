#!/usr/bin/env sh
# Runs a Python hook with the first working interpreter (python3, python, py).
# Fails open (exit 0, no output) when no Python 3.8+ is available.
# Usage: sh run-hook.sh <script.py>
dir=$(dirname "$0")
for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1 &&
     "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    exec "$py" "$dir/$1"
  fi
done
exit 0
