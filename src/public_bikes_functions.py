#! /usr/bin/env python3

#Collection of functions to work with the public bikes data

import pandas as pd

#This function fetches the data from the Oslo Bysykkel server, and then aggregates it in a dataset. It does so for the months specified in the "months" list, and for the year specified in the "year" variable
def load_years(year,months):
    datasets = {}

    for month in months:
        datasets[month] = pd.read_csv('https://data.urbansharing.com/oslobysykkel.no/trips/v1/'+year+'/'+month+'.csv',parse_dates=[0,1])

    df = pd.concat(datasets)
    return df
