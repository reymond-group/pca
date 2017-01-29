#!/usr/bin/env bash
SCRIPT_DIR="${BASH_SOURCE%/*}/"
INPUT_FILE=$1

awk -F "," 'BEGIN {max_x = -99999; max_y = -99999; max_z = -99999; min_x = 99999; min_y = 99999; min_z = 99999} {if ($1>max_x) max_x=$1; if ($1<min_x) min_x=$1; if ($2>max_y) max_y=$2; if ($2<min_y) min_y=$2; if ($3>max_z) max_z=$3; if ($3<min_z) min_z=$3} END {printf("%f,%f\n", min_x, max_x); printf("%f,%f\n", min_y, max_y); printf("%f,%f", min_z, max_z);}' "$INPUT_FILE" 
