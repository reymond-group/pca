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

PARSER.add_argument('dimensions', metavar='DIMENSION', type=int, nargs='*', default=[0, 1, 2],
                    help='the fields specifying the dimensions used to bin the data, ' +
                    'the default value is 0 1 2')

PARSER.add_argument('bins', metavar='BINS', type=int, nargs='*', default=[500, 500, 500],
                    help='the fields specifying the number of bins used to bin the data, ' +
                    'the default value is 1000 1000 1000')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-c', '--chunksize', type=int, default=50000,
                    help='the number of lines to be read from the INPUT file ' +
                    'at a time and stored in memory, the default value is 50000')

PARSER.add_argument('-p', '--properties', type=str, default='',
                    help='a csv file containing properties to be averaged inside each bin')

PARSER.add_argument('-pd', '--propertiesdelimiter', type=str, default=',',
                    help='the delimiter used for fields in the properties csv file')

PARSER.add_argument('-pf', '--propertiesfunc', choices=['mean', 'median'], default='mean',
                    help='the function used to caluclate the properties of each bin')

ARGS = PARSER.parse_args()

ARGS.output = os.path.splitext(ARGS.output)[0]

def load_properties(filename, lines):
    properties = ''
    for line in lines:
        properties += linecache.getline(filename, line + 1)
    return properties

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

with open(ARGS.output + '.tmp', 'a+') as f:
    for chunk in READER:
        indices = pd.DataFrame()
        for i in range(len(ARGS.dimensions)):
            bins = np.linspace(min_values[i], max_values[i], ARGS.bins[i])
            indices[i] = np.digitize(chunk[ARGS.dimensions[i]], bins)
        indices.to_csv(f, header=False, index=False)


# Now group the indices into bins
bins = collections.defaultdict(list)
READER = pd.read_csv(ARGS.output + '.tmp', sep=ARGS.delimiter, 
                     chunksize=ARGS.chunksize, header=None)

index = 0
for chunk in READER:
    for line in chunk.as_matrix():
        bins[(line[0], line[1], line[2])].append(index)
        index += 1

if not ARGS.properties:
    with open(ARGS.output + '.xyz', 'a+') as f:
        with open(ARGS.output + '.dat', 'a+') as g:
            for key, value in bins.items():
                if len(value) < 1:
                    continue
                f.write(str(key[0]) + ',' + str(key[1]) + ',' + str(key[2]) + '\n')
                values = ''
                for item in value:
                    values += str(item) + ','
                g.write(values[:-1] + '\n')
else:
    with open(ARGS.output + '.xyz', 'a+') as f:
        with open(ARGS.output + '.dat', 'a+') as g:
            with open(ARGS.output + '.means', 'a+') as h:
                with open(ARGS.output + '.stds', 'a+') as k:
                    for key, value in bins.items():
                        if len(value) < 1:
                            continue
                        f.write(str(key[0]) + ',' + str(key[1]) + ',' + str(key[2]) + '\n')
                        properties = load_properties(ARGS.properties, value)
                        props = pd.read_csv(StringIO(properties), sep=ARGS.propertiesdelimiter, header=None)
                        means = None
                        if ARGS.propertiesfunc == 'mean':
                            means = props.mean(axis=0)
                        elif ARGS.propertiesfunc == 'median':
                            means = props.medium(axis=0)

                        stds = props.std(axis=0)

                        values = ''
                        for p in means:
                            values += str(p) + ','
                        h.write(values[:-1] + '\n')

                        values = ''
                        for p in stds:
                            values += str(p) + ','
                        k.write(values[:-1] + '\n')

                        values = ''
                        for item in value:
                            values += str(item) + ','
                        g.write(values[:-1] + '\n')
