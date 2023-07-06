import json
import pandas as pd

# convert the dataset downloaded from https://ourworldindata.org/electricity-mix to a compact dataset that can be used from Cumulator
# generate the new dataset in the current folder
def dataset_converter(df):
    # Keep only the last year, in order to have the latest estimation for each country
    df = df.drop_duplicates(subset = 'Entity', keep = 'last', ignore_index = True)

    # Load the country-code list
    with open('countr_2_dig.json') as conv_file:
        country_list = json.load(conv_file)

    # Replace the name of each country with its code :
    for country_block in country_list:
        df = df.replace(country_block.get('Name'), country_block.get('Code'))

    # Sanity checks
    df.dropna(inplace = True)
    df = df[df['Carbon intensity of electricity (gCO2/kWh)'] > 0]

    # Keep only the interesting columns :
    df = df[['Country', 'co2_per_unit_energy']]

    # Save the adjusted dataset to .csv
    df.to_csv('country_dataset_adjusted.csv')