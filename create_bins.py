""" Create n-dimensinal bins from a set of given vectors """
import os
import sys
import argparse
import pandas as pd
import numpy as np

PARSER = argparse.ArgumentParser(
    description='Incremental PCA for dimension reduction of large data sets.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (csv) file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (csv) file')

PARSER.add_argument('dimensions', metavar='DIMENSION', type=int, nargs='*', default=[0, 1, 2],
                    help='the fields specifying the dimensions used to bin the data, ' +
                    'the default value is 0 1 2')

PARSER.add_argument('bins', metavar='BINS', type=int, nargs='*', default=[1000, 1000, 1000],
                    help='the fields specifying the number of bins used to bin the data, ' +
                    'the default value is 1000 1000 1000')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-c', '--chunksize', type=int, default=50000,
                    help='the number of lines to be read from the INPUT file ' +
                    'at a time and stored in memory, the default value is 50000')

ARGS = PARSER.parse_args()

if not ARGS.output.endswith('.bins'):
    ARGS.output = os.path.splitext(ARGS.output)[0] + '.bins'

READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize, header=None)

max_values = [-99999999] * len(ARGS.dimensions)
min_values = [99999999] * len(ARGS.dimensions)

for chunk in READER:
    max_vals = chunk.max(axis=0)
    min_vals = chunk.min(axis=0)
    j = 0
    for i in ARGS.dimensions:
        if max_vals[i] > max_values[j]:
            max_values[j] = max_vals[i]
        if min_vals[i] < min_values[j]:
            min_values[j] = min_vals[i]
        j += 1

# Seek(0) on reader with chunks?
READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize, header=None)

with open(ARGS.output, 'a+') as f:
    for chunk in READER:
        indices = pd.DataFrame()
        for i in range(len(ARGS.dimensions)):
            bins = np.linspace(min_values[i], max_values[i], ARGS.bins[i])
            indices[i] = np.digitize(chunk[ARGS.dimensions[i]], bins)
        indices.to_csv(f, header=False, index=False)
