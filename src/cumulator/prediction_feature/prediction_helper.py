import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

models_directory = f'{parentdir}/prediction_feature/models/'


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


def compute_features(df, target):
    label=target
    features=list(df.columns)
    features.remove(target)
    computed_features=[]

    MajorityClassSize=df.groupby(by=label).size().max()
    computed_features.append(MajorityClassSize)


    series_max_nominal=df[features].select_dtypes(exclude=[np.number]).nunique()
    if series_max_nominal.empty:
        MaxNominalAttDistinctValues=0
    else:
        MaxNominalAttDistinctValues=series_max_nominal.values().max()
    computed_features.append(MaxNominalAttDistinctValues)

    MinorityClassSize=df.groupby(by=label).size().min()
    computed_features.append(MinorityClassSize)

    NumberOfClasses=df[label].unique().shape[0]
    computed_features.append(NumberOfClasses)

    NumberOfFeatures=df.shape[1]-1
    computed_features.append(NumberOfFeatures)

    NumberOfInstances=df.shape[0]
    computed_features.append(NumberOfInstances)

    NumberOfInstancesWithMissingValues=df.isnull().any(axis=1).sum()
    computed_features.append(NumberOfInstancesWithMissingValues)

    NumberOfMissingValues=df.isnull().all(axis=1).sum()
    computed_features.append(NumberOfMissingValues)

    NumberOfNumericFeatures=df[features].select_dtypes([np.number]).shape[1]
    computed_features.append(NumberOfNumericFeatures)

    NumberOfSymbolicFeatures=df[features].select_dtypes(exclude=[np.number]).shape[1]
    computed_features.append(NumberOfSymbolicFeatures)

    max_corr=compute_max_corr(df)
    computed_features.append(max_corr)

    computed_features=np.array(computed_features)
    computed_features=computed_features.reshape(1,-1)
    computed_features=np.log(1+computed_features)

    return np.array(computed_features)


def get_predictions(x):
    """

    Parameters
    ----------
    x vector representing the dataset on which to predict consumption and f1 for the different classification algorithms

    Returns
    -------

    """
    algorithms = ['Linear', 'Decision_Tree', 'Random_Forest', 'Neural_Network']

    consumptions_list = []
    scores_list = []
    for algorithm in algorithms:
        support_consumption = pickle.load(open(models_directory+'support_consumption_' + algorithm + '.pkl', 'rb'))
        support_F1 = pickle.load(open(models_directory+'support_F1_' + algorithm + '.pkl', 'rb'))
        consumption_model = pickle.load(open(models_directory+'consumption_model_' + algorithm + '.sav', 'rb'))
        score_model = pickle.load(open(models_directory+'F1_model_' + algorithm + '.sav', 'rb'))
        x_consumption=x[:,support_consumption]
        x_F1=x[:,support_F1]
        consumption_prediction = consumption_model.predict(x_consumption)
        score_prediction = score_model.predict(x_F1)
        consumptions_list.append(consumption_prediction)
        scores_list.append(score_prediction)

    consumption_rmse_list = pickle.load(open(models_directory+'consumption_rmse.pkl', 'rb'))
    score_rmse_list = pickle.load(open(models_directory+'F1_rmse.pkl', 'rb'))

    return consumptions_list, scores_list, consumption_rmse_list, score_rmse_list
