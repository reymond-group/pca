""" Incremental PCA for dimension reduction of large data sets.  """
import os
import argparse
import pandas as pd
import numpy as np

from sklearn.decomposition import IncrementalPCA
from sklearn.externals import joblib
from scipy import stats

quantile = 0.25

df = pd.DataFrame(np.array([102, 105, 106, 122, 9999, 99999, 0, 1]))

print(stats.zscore(df))

print(df.quantile(quantile))
print(df.quantile(1.0 - quantile))

print(df.quantile(quantile)[0])
