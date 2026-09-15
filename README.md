# mml_automation1


Python-based automation tools for lens and filter fabrication in the McMahon Metamaterials Lab
using Aerotech Automation1 API.

The package is developed as part of the migration of the lab’s fabrication systems from Aerotech A3200 software to Automation1 Python API. 

`mml_automation1` is an independent Python package for Metamaterials Lab automation workflows built on top of Aerotech’s Automation1 Python API. It does not include or redistribute Aerotech Automation1 software, libraries, firmware, documentation, or license keys. Users must obtain and install the official Automation1-MDK / Automation1 Python API from Aerotech separately and must comply with Aerotech’s licensing terms.

## Overview

`mml_automation1` provides the machine-control and metrology workflows used to
prepare metamaterial-coated optics for fabrication on the lab's Automation1
systems.

The package is currently used in lens and filter production. It supports the
workflow from metrology measurements through machine initialization and
preparation for cutting, significantly reducing the amount of manual operator
intervention required by the previous AeroBasic-based process.

The package was developed during the migration of the lab's fabrication systems
from Aerotech A3200 to Automation1. Its initial deployment focused on Saw1, but
the code is structured around reusable motion-control, metrology, I/O, and
machine-preparation utilities.

The goal is not to remove operator oversight. Instead, the package automates
repeatable setup and measurement sequences so that operators can move from
optic metrology to a validated, cut-ready machine state more efficiently and
consistently.

## Why This Package Exists

The lab's earlier fabrication workflows were implemented primarily in
AeroBasic. Those workflows required more manual intervention between metrology,
machine preparation, and the start of cutting.

`mml_automation1` moves these operations into a Python-based Automation1
workflow. The package automates repeated setup steps, makes machine-state
transitions more explicit, and reduces the number of manual actions required
before fabrication begins.

This provides several practical advantages:

- More consistent setup between production runs.
- Fewer manual transitions between metrology and cutting preparation.
- Easier inspection of axis positions, I/O states, and probe measurements.
- Reusable functions for lens and filter production.
- A clearer path for maintaining and extending the fabrication workflow.

## Operator Verification Before Cutting

The automated workflow prepares the machine for fabrication but does not
replace operator verification.

Before starting cuts, confirm:

1. The correct optic and fabrication program are loaded.
2. The measured metrology profile is appropriate for the optic.
3. The active Z axis matches the intended spindle.
4. The spindle and flood-coolant output mappings are correct.
5. The starting coordinates, clearance heights, and cut depth are correct.
6. The machine is in the expected cut-ready state.
7. The emergency-stop path is accessible.

The operator remains responsible for authorizing the start of the cutting run.
