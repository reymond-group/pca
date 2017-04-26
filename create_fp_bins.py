""" Create n-dimensinal bins from a set of given vectors """
import os
import sys
import collections
import linecache
import argparse
import pandas as pd
import numpy as np

from io import StringIO

PARSER = argparse.ArgumentParser(
    description='Create n-dimensinal bins from a set of given vectors.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (csv) file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (csv) file')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-c', '--chunksize', type=int, default=50000,
                    help='the number of lines to be read from the INPUT file ' +
                    'at a time and stored in memory, the default value is 50000')

ARGS = PARSER.parse_args()

READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize, header=None)

# Seek(0) on reader with chunks?
READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize, header=None)

thed = {}

index = 0
for chunk in READER:
    for line in chunk.as_matrix():
        thed.setdefault(np.array_str(line), []).append(index)
        index += 1

with open(ARGS.output, 'w+') as f:
    for key, value in thed.items():
        f.write(','.join(map(str, value)) + '\n')

