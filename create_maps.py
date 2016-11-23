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

ARGS = PARSER.parse_args()

ARGS.output = os.path.splitext(ARGS.output)[0]

MEANS = pd.read_csv(ARGS.means, sep=ARGS.delimiter, usecols=[ARGS.index], header=None)
STDS = pd.read_csv(ARGS.stds, sep=ARGS.delimiter, usecols=[ARGS.index], header=None)
STDS = STDS.fillna(0)
STDS = STDS.rename(columns = {0:1})

MEANS = MEANS.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))).values
STDS = STDS.apply(lambda x: 1 - (0.5 * (x - np.min(x))) / (np.max(x) - np.min(x))).values

#DATA = pd.concat([DATA, STDS], axis=1)

with open(ARGS.output + '.map', 'a+') as f:
    for i, row in enumerate(MEANS):
        c = Color(hue=row[0], saturation=STDS[i][0], luminance=0.5)
        f.write(str(round(c.red, 2)) + ',' + str(round(c.green, 2)) + ',' + str(round(c.blue, 2)) + '\n')