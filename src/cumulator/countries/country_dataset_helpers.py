import json

import pandas as pd


# country dataset has 3 digits country codes, incompatibles with elaboration, need to be converted
def dig3_to_dig2_conversion(dataset):
    df_data = pd.read_csv(dataset)
    # open file containing mapping 2digits-3digits
    with open('countr_2_dig.json') as conv_file:
        country_list = json.load(conv_file)

    for country_block in country_list:
        df_data = df_data.replace(country_block.get('Name'), country_block.get('Code'))
    return df_data


def drop_columns_keeping_max_year(df_data):
    df_data = df_data[df_data['co2_per_unit_energy'].notnull()]
    idx = df_data.groupby(['country'])['year'].transform(max) == df_data['year']
    df_updated = df_data[idx]
    df_useful = df_updated[['country', 'co2_per_unit_energy']]
    df_useful.to_csv('country_dataset_adjusted.csv')


# convert the dataset downloaded from https://ourworldindata.org/electricity-mix to a compact dataset that can be used from Cumulator
# generate the new dataset in the current folder
def dataset_converter(dataset_fr):
    df_data = dig3_to_dig2_conversion(dataset_fr)
    drop_columns_keeping_max_year(df_data)
