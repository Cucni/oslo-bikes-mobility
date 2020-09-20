#! /usr/bin/env python3

#This scripts fetches the data from the Oslo Bysykkel server, and then plots the relative variation in bikes mobility. It does so for the months specified in the "months" list. The variation is computed between 5-days rolling averages.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from public_bikes_functions import load_years
from plot_google import load_google

plt.style.use('seaborn')

months = ['05','06','07','08']

df_19 = load_years('2019',months)
df_20 = load_years('2020',months)

daily_2019 = df_19.groupby(df_19['started_at'].dt.date).count()['started_at']
daily_2020 = df_20.groupby(df_20['started_at'].dt.date).count()['started_at']

daily_2019.name = 'Rides 2019'
daily_2020.name = 'Rides 2020'
daily_2019.index.name = 'Day'
daily_2020.index.name = 'Day'

rolling_2019 = daily_2019.rolling(window=5,min_periods=3).mean()
rolling_2020 = daily_2020.rolling(window=5,min_periods=3).mean()
rolling_2019.index = rolling_2019.index.astype("datetime64[ns]").dayofyear
rolling_2020.index = rolling_2020.index.astype("datetime64[ns]").dayofyear


variation = ((rolling_2020/rolling_2019) - 1)*100
rolling = pd.concat([rolling_2019,rolling_2020],axis=1)

rolling.plot(color=['tab:blue','tab:orange'])
plt.title("5-day Rides rolling average in 2019 and 2020")
plt.xlabel("Day of the year")
plt.ylabel("Number of rides")
plt.savefig('total_rides.pdf')

plt.figure()
variation.plot()
plt.title("5-day Rolling relative variation in the number of rides from 2019 to 2020")
plt.xlabel("Day of the year")
plt.ylabel("Percentage variation")
plt.savefig('variation.pdf')

df_google = load_google()

#Variation is a Series. When we join a Dataframe with a Series, the Series data are joined in the table as a column, but the name of the column is the name of the series so it must have a name (nameless series throw errors). Also, since we want to join on the "day of the year" feature, which is the index in the Series, we name it as "doy", which is the name it has in the Google dataframe. In this joining on "doy" is straightforward.
variation.index.name = 'doy'
variation.name = 'Public bikes variation'
df_joined = df_google.join(variation,on="doy",how="left")


sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='transit_stations_percent_change_from_baseline',color='tab:blue',label='Google')
sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='Public bikes variation',color='tab:orange',label='Public bikes')
plt.legend()
plt.title("Comparison of Google's variation and public bikes variation")
plt.ylabel("Percent variation from baseline")
plt.savefig("variation_comparison.pdf")
