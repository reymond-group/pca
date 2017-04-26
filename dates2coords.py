""" Create coordinates from dates based on a bin, info and map file (SureChEMBL). """
import os
import sys
import collections
import linecache
import argparse
import pandas as pd
import numpy as np
import datetime

from io import StringIO

PARSER = argparse.ArgumentParser(
    description='Create n-dimensinal bins from a set of given vectors.')

PARSER.add_argument('dat', metavar='DAT', type=str,
                    help='the bin (.dat) file identifying compounds per bin')

PARSER.add_argument('info', metavar='INFO', type=str,
                    help='the compound info (.info) file')

PARSER.add_argument('map', metavar='map', type=str,
                    help='a file mapping SureChEMBL ids to dates')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (csv) file')

ARGS = PARSER.parse_args()
CHUNKSIZE = 50000

dates = {}

def load_ids(filename, lines):
    ids = []
    for line in lines:
        ids.append(linecache.getline(filename, int(line) + 1).split(' ')[0])

    return ids

def get_dates(ids):
    dts = []
    for i in ids:
        i = i.split('_')[0]
        if i in dates:
            dts.append(dates[i])

    return dts

with open(ARGS.map, 'r') as f:
    for line in f:
        values = line.split(' ')
        dates[values[0]] = values[1]


dates_ordered = []

with open(ARGS.dat, 'r') as f:
    for line in f:
        ids = load_ids(ARGS.info, line.split(','))
        dts = get_dates(ids)
        # Get the oldest date
        dts.sort()
        dt = 0
        if len(dts) > 0:
            oldest = dts[0]
            dtstr = oldest.replace('-', '')
            dt = int(dtstr)
        dates_ordered.append(dt);

min_val = min([x for x in dates_ordered if x > 0])
max_val = max(dates_ordered)

dates_ordered = map(lambda x: (250 - 10) * ((x - min_val) / (max_val - min_val)) + 10 if x > 0 else 0, dates_ordered)

with open(ARGS.output, 'a+') as f:
    for val in dates_ordered:
        f.write(str(round(val)) + '\n')




