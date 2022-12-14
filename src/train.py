import sys
import os
import pickle
import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
import logging 

#adding logging code
logging.basicConfig(level=logging.WARN)
logger=logging.getLogger(__name__)
version='v4'
params = yaml.safe_load(open('params.yaml'))['train']

if len(sys.argv) != 3:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython train.py features model\n')
    sys.exit(1)

input = sys.argv[1]
output = sys.argv[2]
seed = params['seed']
n_estimators = params['n_estimators']

mlflow.set_experiment('demo')

with open(os.path.join(input, 'train.pkl'), 'rb') as fd:
    matrix = pickle.load(fd)

labels = np.squeeze(matrix[:, 1].toarray())
x = matrix[:, 2:]

sys.stderr.write('Input matrix size {}\n'.format(matrix.shape))
sys.stderr.write('X matrix size {}\n'.format(x.shape))
sys.stderr.write('Y matrix size {}\n'.format(labels.shape))

#log data params
mlflow.log_param('data_url','data/data.xml')
mlflow.log_param('data_version',version)
mlflow.log_param('input_rows',matrix.shape[0])
mlflow.log_param('input_cols',matrix.shape[1])


clf = RandomForestClassifier(
    n_estimators=n_estimators,
    n_jobs=2,
    random_state=seed
)

clf.fit(x, labels)
# mlflow.sklearn.log_model(clf, "my_model")

with open(output, 'wb') as fd:
    pickle.dump(clf, fd)
