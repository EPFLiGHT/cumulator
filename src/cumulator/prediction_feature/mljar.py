#definition of add_dataset that creates the meta-dataset
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

rootdir = os.path.dirname(__file__)
results_dir = rootdir + '/results/'
dataset_dir = rootdir + '/datasets_list_final/'
datasets_to_add_dir = rootdir + '/datasets_list_toadd/'

algorithm_list = ['Linear', 'Random Forest', 'Decision Tree', 'Neural Network']


def encode_y(y):
    le = LabelEncoder()
    le.fit(y)
    y_enc = le.transform(y)
    return y_enc

def compute_max_corr(df):
    y = encode_y(df[df.columns[-1]])
    y = pd.Series(y)
    corr = df[df.columns[:-1]].corrwith(y)
    return np.max(np.absolute(corr))

def compute_max_corr_between_X_and_y(X, y):
    y = encode_y(y)
    y = pd.Series(y)
    X = X.apply(pd.to_numeric, errors='ignore')
    return np.max(np.absolute(X.apply(lambda x: x.corr(y) if is_numeric_dtype(x) else 0)))

def add_dataset(dataset, dataset_dataframe):
    path = rootdir + "/ml_dataset.csv"
    try:
        df = pd.read_csv(path)
    except:
        df = pd.DataFrame()
        df['did'] = 0

    dataset_id = dataset.dataset_id
    if dataset_id in df['did'].values:
        print("Dataset %d already present in the dataset!" % dataset_id)
    else:
        # PERFORM AUTOML
        X, y, _, _ = dataset.get_data(
            target=dataset.default_target_attribute)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
        automl = AutoML(algorithms=algorithm_list, eval_metric='f1', results_path=results_dir + str(dataset_id),
                        explain_level=1, top_models_to_improve=4, random_state=2, optuna_verbose=False)
        automl.fit(X_train, y_train)
        predictions = automl.predict(X_test)

        # ADD DATASET
        # Retrieve results from automl
        results_col_list = ['metric_value', 'train_time', 'model_type']
        results_col_new_names = ['F1', 'time', 'algo']
        df_automl_results = pd.read_csv(results_dir + str(dataset_id) + '/leaderboard.csv')[results_col_list]
        df_automl_results.columns = results_col_new_names


        # Add information about dataset
        interesting_columns = dataset_dataframe.columns[6:]
        for column in interesting_columns:
            df_automl_results[column] = dataset_dataframe.loc[dataset_id, column]

        df_automl_results['TDP'] = 250
        df_automl_results['country'] = 'Switzerland'
        df_automl_results['max_corr'] = compute_max_corr_between_X_and_y(X, y)
        df_automl_results['did'] = dataset_id

        # Set algo as the last column
        i = list(df_automl_results.columns)
        pos = i.index('algo')
        new_i = i[0:pos] + i[pos + 1:] + [i[pos]]
        df_automl_results = df_automl_results[new_i]


        # Append new dataset
        df = pd.concat([df, df_automl_results])
        df = df.reset_index(drop=True)
        df.to_csv(path, index=False)
        print("Dataset %d successfully added!" % dataset_id)
