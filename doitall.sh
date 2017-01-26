#!/usr/bin/env bash
SCRIPT_DIR="${BASH_SOURCE%/*}/"
INPUT_FILE=$1
DATABASE_NAME=$2
FINGERPRINT_NAME=$3
BINS=$4
OUTPUT_DIR=$(readlink -f "$INPUT_FILE")
OUTPUT_DIR="${OUTPUT_DIR%/*}/"

IDS_FILE="$OUTPUT_DIR$DATABASE_NAME.ids"
SMILES_FILE="$OUTPUT_DIR$DATABASE_NAME.smiles"
FP_FILE="$OUTPUT_DIR$DATABASE_NAME.$FINGERPRINT_NAME.fp"
PROP_FILE="$OUTPUT_DIR$DATABASE_NAME.$FINGERPRINT_NAME.prop"
MODEL_FILE="$OUTPUT_DIR$DATABASE_NAME.$FINGERPRINT_NAME.3.pkl"
COORD_FILE="$DATABASE_NAME.$FINGERPRINT_NAME.xyz"
BIN_FILES="$DATABASE_NAME.$FINGERPRINT_NAME.$BINS"

IDS_INDEX_FILE="$IDS_FILE.index"
SMILES_INDEX_FILE="$SMILES_FILE.index"
COORDS_INDEX_FILE="$COORD_FILE.index"
FPS_INDEX_FILE="$FP_FILE.index"

echo "Writing output files to $OUTPUT_DIR."

# IDs and smiles files are written only once per database
if [ ! -f $IDS_FILE ]; then
    echo "Writing $IDS_FILE ..."
    cut -f1 -d' ' "$INPUT_FILE" > "$IDS_FILE"
fi

if [ ! -f $SMILES_FILE ]; then
    echo "Writing $SMILES_FILE ..."
    cut -f2 -d' ' "$INPUT_FILE" > "$SMILES_FILE"
fi

# Write fingerprints and properties per fingerprint
if [ ! -f $FP_FILE ]; then
    echo "Writing $FP_FILE ..."
    cut -f3 -d' ' "$INPUT_FILE" > "$FP_FILE"
fi

if [ ! -f $PROP_FILE ]; then
    echo "Writing $PROP_FILE ..."
    cut -f4 -d' ' "$INPUT_FILE" > "$PROP_FILE"
fi

# Incremental PCA
if [ ! -f $COORD_FILE ]; then
    echo "Running incremental pca on $FP_FILE ..."
    python3 "$SCRIPT_DIR/incremental_pca.py" "$FP_FILE" "$COORD_FILE" -d ";" -m "$MODEL_FILE"
fi

# Binning
if [ ! -f "$BIN_FILES.xyz" ]; then
    echo "Binning ..."
    python3 "$SCRIPT_DIR/create_bins.py" "$COORD_FILE" "$BIN_FILES" -p "$PROP_FILE" -pd ";" -b $BINS
fi

N_PROP="$(awk -F';' '{print NF; exit}' $PROP_FILE)"

# Creating Maps
for (( c=1; c<=$N_PROP; c++ ))
do
    MAP_FILE="$OUTPUT_DIR$DATABASE_NAME.$FINGERPRINT_NAME.$BINS.$c.map"

    if [ ! -f $MAP_FILE ]; then
        echo "Writing map file $c ..."
        python3 "$SCRIPT_DIR/create_map.py" "$BIN_FILES.means" "$BIN_FILES.stds" "$MAP_FILE" -i $c
    fi
done

# Indexing Files
if [ ! -f "$IDS_INDEX_FILE" ]; then
    echo "Indexing $IDS_FILE ..."
    python3 "$SCRIPT_DIR/index_file.py" "$IDS_FILE"
fi

if [ ! -f "$SMILES_INDEX_FILE" ]; then
    echo "Indexing $SMILES_FILE ..."
    python3 "$SCRIPT_DIR/index_file.py" "$SMILES_FILE"
fi

if [ ! -f "$COORDS_INDEX_FILE" ]; then
    echo "Indexing $COORD_FILE ..."
    python3 "$SCRIPT_DIR/index_file.py" "$COORD_FILE"
fi

if [ ! -f "$FPS_INDEX_FILE" ]; then
    echo "Indexing $FP_FILE ..."
    python3 "$SCRIPT_DIR/index_file.py" "$FP_FILE"
fi

