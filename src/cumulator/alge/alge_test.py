import sys
sys.path.append('../')
sys.path.append('../../msc-liamarcia/alge/db/tables')

import requests
import time
import cumulator as c


USER = 'tristan'
PASSWORD = 'latalu5665'
BASE_URL = 'http://127.0.0.1:8000/'
LOGIN_URL = BASE_URL + 'login/'
RUN_MODEL_URL = BASE_URL + 'running'


RUN_DATA = dict(file=['data'],
                # regression
                #label=['dem_child_house'],
                # classificaiton - only binary?
                label=['symp_fev24h'],
                #oversampling=['on'],
                models=['Linear Regression (Regression)'],
                #features=['lab_hb_d0'],
                #featureselection=['boruta'], #['lasso'],
                external=[''],
                # regression
                #metric=['mean_squared_error'],
                # classification
                metric=['accuracy'])

MODELS_REGRESSION=['GaussianNB (Regression)', 'Linear Regression (Regression)', 'Ridge (Regression)',
        'Random Forest (Regression)']
MODELS_CLASSIFICATION=['BernoulliNB (Classification)']#, 'Logistic Regression (Classification)',
                   #    'Neural Networks (Classification)', 'Random Forest (Classification)']

if __name__ == '__main__':
    cumulator = c.Cumulator()
    client = requests.session()
    client.get(LOGIN_URL)

    login_data = dict(username=USER, password=PASSWORD, csrfmiddlewaretoken=client.cookies.get('csrftoken'))
    response = client.post(LOGIN_URL, data=login_data)

    RUN_DATA['csrfmiddlewaretoken'] = client.cookies.get('csrftoken')

    for model in MODELS_CLASSIFICATION:
        RUN_DATA['models'] = model
        cumulator.on()
        response = client.post(RUN_MODEL_URL, data=RUN_DATA)
        cumulator.off()
        print(model)
        print(cumulator.time_list[-1])
'''
    new_model_url = response.url
    print(new_model_url)

    response = client.get(new_model_url, data=dict(csrfmiddlewaretoken=client.cookies.get('csrftoken')))
    print(response.content)
'''
