#! /usr/bin/env python3

#This scripts fetches the data from the Oslo Bysykkel server, and then plots the relative variation in bikes mobility. It does so for the months specified in the "months" list. The variation is computed between 5-days rolling averages.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')

datasets19 = {}
datasets20 = {}
months = ['05','06','07']

for month in months:
    datasets19[month] = pd.read_csv('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2019/'+month+'.csv',parse_dates=[0,1])
    datasets20[month] = pd.read_csv('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2020/'+month+'.csv',parse_dates=[0,1])

df_19 = pd.concat(datasets19)
df_20 = pd.concat(datasets20)

daily_2019 = df_19.groupby(df_19['started_at'].dt.date).count()['started_at']
daily_2020 = df_20.groupby(df_20['started_at'].dt.date).count()['started_at']

daily_2019.name = 'Rides'
daily_2020.name = 'Rides'
daily_2019.index.name = 'Day'
daily_2020.index.name = 'Day'

rolling_2019 = daily_2019.rolling(window=5,min_periods=3).mean()
rolling_2020 = daily_2020.rolling(window=5,min_periods=3).mean()
rolling_2019.index = rolling_2019.index.astype("datetime64[ns]").dayofyear
rolling_2020.index = rolling_2020.index.astype("datetime64[ns]").dayofyear


variation = (rolling_2020/rolling_2019) - 1

fig = plt.figure()
variation.plot()
fig.savefig('variation.png')
