import sys
import os
import argparse
import pandas as pd
import numpy as np
import flask

from sklearn.decomposition import IncrementalPCA
from sklearn.externals import joblib

# Initialize the Flask application
app = flask.Flask(__name__)

app.config.update(
    PROPAGATE_EXCEPTIONS='DEBUG'
)

if len(sys.argv) < 2:
    print('Please provide a directory containing the models.')
    print('Usage: ' + sys.argv[0] + ' /directory/to/models/')
    sys.exit()

port = 8081
if len(sys.argv) > 2:
    port = int(sys.argv[2])

model_dir = sys.argv[1]

if not model_dir.endswith('/'):
    model_dir += '/'

# For GET, show a simple message
@app.route('/')
def form():
    return flask.render_template('index.html')

# The POST request doing the incremental pca
@app.route('/', methods=['POST'])
def ipca():
    json = flask.request.get_json(silent=True)

    if (json is None) or ('database' not in json) or ('fingerprint' not in json) or ('dimensions' not in json):
        return flask.jsonify({'success': False, 'error': 'Malformed request.'})

    database = json['database']
    fingerprint = json['fingerprint']
    dimensions = json['dimensions']
    data = json['data']

    file = database + '.' + fingerprint + '.' + str(dimensions) + '.pkl'
    path = model_dir + database + '/' + fingerprint + '/' + str(dimensions) + '/'
    
    if not os.path.isfile(path + file):
        return flask.jsonify({'success': False, 'error': 'Transformation not available.'})

    pca = joblib.load(path + file)

    transformed_data = None

    try:
        transformed_data = pca.transform(data).tolist()
    except:
        return flask.jsonify({'success': False, 'error': 'Could not transform data. Do the fingerprints match the selected model?'})

    return flask.jsonify({
        'success': True,
        'database': database,
        'fingerprint': fingerprint,
        'dimensions': dimensions,
        'data': transformed_data
    })
    
# Run the app
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = port
    )