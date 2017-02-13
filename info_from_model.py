""" Incremental PCA for dimension reduction of large data sets.  """
import os
import argparse
import pandas as pd
import numpy as np

from sklearn.decomposition import IncrementalPCA
from sklearn.externals import joblib

PARSER = argparse.ArgumentParser(
    description='Incremental PCA for dimension reduction of large data sets.')

PARSER.add_argument('model', metavar='MODEL', type=str,
                    help='the model file to extract the info from.')

PARSER.add_argument('-k', '--dimensions', type=int, default=3,
                    help='use DIMENSIONS instead of 3 as the number of dimensions' +
                    ' to reduce the data to')


ARGS = PARSER.parse_args()

PCA = IncrementalPCA(n_components=ARGS.dimensions)

total_read = 0
total_written = 0

PCA = joblib.load(ARGS.model)

np.savetxt(ARGS.model + '-means.csv', PCA.mean_, delimiter=',')
np.savetxt(ARGS.model + '-vars.csv', PCA.var_, delimiter=',')
np.savetxt(ARGS.model + '-explained_variances.csv', 
           PCA.explained_variance_, delimiter=',')
np.savetxt(ARGS.model + '-explained_variance_ratios.csv', 
           PCA.explained_variance_ratio_, delimiter=',')
