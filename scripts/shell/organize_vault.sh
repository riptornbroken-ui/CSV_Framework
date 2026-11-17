#!/usr/bin/env bash
set -euo pipefail
TARGET_DIR="${1:-$(pwd)}"
cd "$TARGET_DIR"
mkdir -p documents/markdown documents/pdfs documents/spreadsheets scripts/python scripts/shell telemetry/db archives/zips
for f in *.md *.txt; do [ -f "$f" ] && mv "$f" documents/markdown/; done
for f in *.pdf; do [ -f "$f" ] && mv "$f" documents/pdfs/; done
for f in *.csv *.xlsx *.xls; do [ -f "$f" ] && mv "$f" documents/spreadsheets/; done
for f in *.py; do [ -f "$f" ] && mv "$f" scripts/python/; done
for f in *.sh; do [ -f "$f" ] && mv "$f" scripts/shell/; done
for f in *.db *.log *.sqlite; do [ -f "$f" ] && mv "$f" telemetry/db/; done
for f in *.zip *.tar.gz *.tgz; do [ -f "$f" ] && mv "$f" archives/zips/; done
echo "[+] Vault structure organized."
