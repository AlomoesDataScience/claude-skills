#!/bin/sh
# Assemble a standalone generator from the engine pieces plus a units file, then render.
#   build.sh UNITS_FILE OUT_SCRIPT OUTDIR [unit ...]
# UNITS_FILE defines build functions and UNITS (see examples/madscience_units.py).
# OUT_SCRIPT is the standalone result (keep a copy next to the sprites so they can be redrawn).
set -e
DIR=$(cd "$(dirname "$0")" && pwd)
UNITS_FILE=$1; OUT_SCRIPT=$2; OUTDIR=$3; shift 3
cat "$DIR/palette.py" "$DIR/sdf_core.py" "$DIR/rig.py" "$UNITS_FILE" "$DIR/render.py" > "$OUT_SCRIPT"
python3 -I "$OUT_SCRIPT" "$OUTDIR" "$@"
