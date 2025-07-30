#!/bin/bash

# Find all subdirectories of pyharp.devices and join them with ':'
PYHARP_DEVICES_PATHS=$(find -L ./pyharp.devices -mindepth 1 -maxdepth 1 -type d | paste -sd ":" -)

# Prepend to PYTHONPATH (preserve existing PYTHONPATH)
export PYTHONPATH="$PYHARP_DEVICES_PATHS:$PYTHONPATH"

# Optionally print for debugging
echo "PYTHONPATH set to: $PYTHONPATH"

# Launch mkdocs build or serve
mkdocs serve
