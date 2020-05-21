TABLE="data.csv"

# choose a variable with a low zero rate
# regression
TARGET_VARIABLE='dem_age_int'
# classificaiton
TARGET_VARIABLE='dxfinal_anemia_sev'

# regression with lasso
'file': ['data'],
'label': ['dem_age_int'],
'models': ['GaussianNB (Regression)', 'Linear Regression (Regression)', 'Ridge (Regression)',
 'Random Forest (Regression)'],
'features': ['dem_child_house'],
'featureselection': ['lasso'],
'external': [''],
'metric': ['mean_squared_error']}>

# classificaiton, boruta, oversampling
'file': ['data'],
'label': ['dxfinal_anemia_sev'],
'oversampling': ['on'],
'models': ['BernoulliNB (Classification)', 'Logistic Regression (Classification)', 'Neural Networks (Classification)', 'Random Forest (Classification)'],
'features': ['dem_age_int'],
'featureselection': ['boruta'],
'external': [''],
'metric': ['accuracy']

# train a simple model on each data set
# list of the different models
# function to run the model based on a query dict
def get_query_dict(mydata=TABLE,
                   mylabel=TARGET_VARIABLE,
                   mymodels=MODELS,
                   mymetric=['mean_squared_error'],
                   oversamppling=0,
                   featureselection=0
                   ):
    # gets features without the specified label
    predictor_variables = list(pd.read_csv(TABLE).columns.drop(labels=mylabel))


    RUN_DATA= dict(file=mydata.split('.')[0],
                    label=mylabel)

    # adds oversampling
    if oversamppling==1:
        RUN_DATA.update({'oversampling': ['on']})

    RUN_DATA.update({'models': mymodels,
                     'features': predictor_variables})

    # adds a feature selection
    if featureselection=='boruta':
        RUN_DATA.update({'featureselection': ['boruta']})
    elif featureselection=='lasso':
        RUN_DATA.update({'featureselection': ['lasso']})

    RUN_DATA.update({'external': ['']
                     'metric': mymetric})

    return RUN_DATA

