#! /usr/bin/env python3

#Collection of functions to work with the public bikes data

import pandas as pd
from os.path import exists

DATA_FOLDER_RAW = 'data/raw/'

#This function retrieves public bikes data for a single month. If necessary, it fetches data from the Oslo Bysykkel server and stores it locally.
def load_monthly_data(year,month):
    if not exists(DATA_FOLDER_RAW + '{:}-{:02d}.csv'.format(year,month)):
        df = pd.read_csv('https://data.urbansharing.com/oslobysykkel.no/trips/v1/{:}/{:02d}.csv'.format(year,month),parse_dates=[0,1])
        df.to_csv(DATA_FOLDER_RAW + '{:}-{:02d}.csv'.format(year,month),index=False)
    else:
        df = pd.read_csv(DATA_FOLDER_RAW + '{:}-{:02d}.csv'.format(year,month),parse_dates=[0,1])

    return df

#This function loads public bikes data for every month the "months" list, and for the specified year. It returns an aggregated dataset.
def load_months(year,months):
    datasets = {}

    for month in months:
        datasets[month] = load_monthly_data(year,month)

    df = pd.concat(datasets)
    return df
