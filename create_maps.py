""" Create RGB color maps from bins """
import os
import sys
import collections
import linecache
import argparse
import pandas as pd
import numpy as np

from io import StringIO

PARSER = argparse.ArgumentParser(
    description='Create RGB color maps from bins.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (bins) file')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-i', '--index', type=int, required=True,
                    help='the index for the column to be exported as an RGB color map')

PARSER.add_argument('-c', '--chunksize', type=int, default=50000,
                    help='the number of lines to be read from the INPUT file ' +
                    'at a time and stored in memory, the default value is 50000')

ARGS = PARSER.parse_args()

READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize, header=None)

for chunk in READER:
    print(chunk[0].describe())
