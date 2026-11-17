#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
ARCHIVE_DIR="csv_power_law_zenodo_${TIMESTAMP}"
ARCHIVE_FILE="${ARCHIVE_DIR}.tar.gz"

echo "Staging Zenodo deposition package in ${ARCHIVE_DIR}..."
mkdir -p "${ARCHIVE_DIR}/scripts" "${ARCHIVE_DIR}/figures" "${ARCHIVE_DIR}/telemetry"

# Copy Python simulation scripts
cp -f *.py "${ARCHIVE_DIR}/scripts/" 2>/dev/null || true

# Copy generated figures
cp -f *.png "${ARCHIVE_DIR}/figures/" 2>/dev/null || true

# Copy JSON telemetry and SQLite database
cp -f *.json "${ARCHIVE_DIR}/telemetry/" 2>/dev/null || true
cp -f *.db "${ARCHIVE_DIR}/telemetry/" 2>/dev/null || true

# Generate structured Zenodo metadata descriptor
cat << 'META' > "${ARCHIVE_DIR}/zenodo.json"
{
  "metadata": {
    "title": "Chromatic Spacetime Viscosity (CSV) Framework: Non-Newtonian Power-Law Xel Lattice Simulation & Telemetry",
    "upload_type": "dataset",
    "description": "Numerical simulation scripts, effective viscosity heatmaps, multi-index peak velocity decay curves, and SQLite/JSON telemetry records modeling non-Newtonian Ostwald-de Waele power-law rheology on a 2D sub-Planckian xel lattice.",
    "creators": [
      {
        "name": "Gillispie, Jesse Arron",
        "affiliation": "Independent Researcher"
      }
    ],
    "keywords": [
      "Chromatic Spacetime Viscosity",
      "Power-Law Fluid Dynamics",
      "Non-Newtonian Rheology",
      "Sub-Planckian Lattice",
      "Xel Lattice",
      "Computational Physics"
    ],
    "license": "cc-by-4.0"
  }
}
META

# Generate archive README
cat << 'DOC' > "${ARCHIVE_DIR}/README.md"
# CSV Framework: Power-Law Xel Lattice Simulation Package

## Directory Structure
- `scripts/`: Python modules implementing analytical pipe flow (`power_law_pipe.py`), 2D xel lattice non-Newtonian stress updates (`power_law_lattice.py`, `power_law_lattice_telemetry.py`), multi-index comparisons (`compare_power_law_indices.py`), and JSON exporters (`export_telemetry_payload.py`).
- `figures/`: High-resolution (300 DPI) velocity profiles, effective viscosity ($\eta_{\text{eff}}$) heatmaps, and multi-index damping plots.
- `telemetry/`: Raw SQLite database (`csv_telemetry.db`) and serialized JSON telemetry payloads (`power_law_telemetry_payload.json`).
- `zenodo.json`: Zenodo deposition metadata record.
DOC

# Generate SHA-256 manifest for data integrity verification
(
  cd "${ARCHIVE_DIR}"
  find . -type f ! -name "SHA256SUMS.txt" -exec sha256sum {} + | sort -k 2 > SHA256SUMS.txt
)

# Create compressed archive and remove staging directory
tar -czf "${ARCHIVE_FILE}" "${ARCHIVE_DIR}"
rm -rf "${ARCHIVE_DIR}"

echo "=========================================="
echo "Zenodo archive created: ${ARCHIVE_FILE}"
echo "Archive SHA-256: $(sha256sum "${ARCHIVE_FILE}" | awk '{print $1}')"
echo "=========================================="
