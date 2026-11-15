# Chromatic Spacetime Viscosity (CSV) Framework

## Overview
The Chromatic Spacetime Viscosity (CSV) Framework is a discrete, integer-based sub-Planckian lattice model of spacetime. It replaces continuous approximations and unphysical singularities with countable xel units and thermodynamic shear viscosity tensor dynamics.

## Repository Structure
- `csv_constants.py`: Fundamental physical constants and lattice parameters.
- `xel_lattice.py`: 3D spatial simulation engine modeling mass injection, gradient shear stress, and causal pinch-off.
- `verify_telemetry.py`: Telemetry verification utility for validating simulation runs against density ceilings.
- `zenodo_deposition_payload.json`: Metadata and radial boundary layer profiles prepared for Zenodo open-access archival.

## Execution
Run the core simulation:
py xel_lattice.py

Verify telemetry records:
py verify_telemetry.py
