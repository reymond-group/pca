""" Create RGB color maps from bins """
import os
import sys
import collections
import linecache
import argparse
import colorsys
import pandas as pd
import numpy as np


from sklearn import preprocessing
from io import StringIO
from colour import Color


PARSER = argparse.ArgumentParser(
    description='Create RGB color maps from bins.')

PARSER.add_argument('means', metavar='MEANS', type=str,
                    help='the means file')

PARSER.add_argument('stds', metavar='STDS', type=str,
                    help='the stds file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (map) file')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-i', '--index', type=int, required=True,
                    help='the index for the column to be exported as an RGB color map')

PARSER.add_argument('-q', '--quantile', type=float, default=0.25,
                    help='use QUANTILE instead of \'0.25\' to determine the min and max')

ARGS = PARSER.parse_args()

ARGS.output = os.path.splitext(ARGS.output)[0]

MEANS = pd.read_csv(ARGS.means, sep=ARGS.delimiter, usecols=[ARGS.index - 1], header=None)
STDS = pd.read_csv(ARGS.stds, sep=ARGS.delimiter, usecols=[ARGS.index - 1], header=None)
STDS = STDS.fillna(0)
STDS = STDS.rename(columns = {0:1})

Q1 = MEANS.quantile(ARGS.quantile).values[0]
Q3 = MEANS.quantile(1.0 - ARGS.quantile).values[0]
IQR = Q3 - Q1
MIN = Q1 - 1.5 * IQR
MAX = Q3 + 1.5 * IQR

MEANS[MEANS < MIN] = MIN
MEANS[MEANS > MAX] = MAX

Q1_S = STDS.quantile(ARGS.quantile).values[0]
Q3_S = STDS.quantile(1.0 - ARGS.quantile).values[0]
IQR_S = Q3_S - Q1_S
MIN_S = Q1_S - 1.5 * IQR_S
MAX_S = Q3_S + 1.5 * IQR_S

STDS[STDS < MIN_S] = MIN_S
STDS[STDS > MAX_S] = MAX_S

MEANS = MEANS.apply(lambda x: (0.85 * (x - np.min(x)) / (np.max(x) - np.min(x))) + 0.66).values
STDS = STDS.apply(lambda x: 1 - (0.5 * (x - np.min(x))) / (np.max(x) - np.min(x))).values

#DATA = pd.concat([DATA, STDS], axis=1)

with open(ARGS.output + '.map', 'a+') as f:
    for i, row in enumerate(MEANS):
        if row[0] > 1.0: row[0] = row[0] - 1.0
        row[0] = (1 - row[0]) + 0.33
        if row[0] > 1.0: row[0] = row[0] - 1.0
        c = Color(hue=row[0], saturation=STDS[i][0], luminance=0.5)
        f.write(str(round(c.red, 2)) + ',' + str(round(c.green, 2)) + ',' + str(round(c.blue, 2)) + '\n')
