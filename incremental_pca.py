""" Incremental PCA for dimension reduction of large data sets.  """

import argparse
import pandas as pd

from sklearn.decomposition import IncrementalPCA

PARSER = argparse.ArgumentParser(
    description='Incremental PCA for dimension reduction of large data sets.')

PARSER.add_argument('input', metavar='I', type=str,
                    help='The input (csv) file.')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

ARGS = PARSER.parse_args()

print ARGS
