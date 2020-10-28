#! /usr/bin/env python3

#This scripts fetches the data from the Oslo Bysykkel server, and then plots the relative variation in bikes mobility. It does so for the months specified in the "months" list. The variation is computed between 5-days rolling averages.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from public_bikes_functions import load_years
from plot_google import load_google

plt.style.use('seaborn')

#Folder where to save output figures
FIGURES_FOLDER = 'figures/'

#Range of months that we are analyzing
months = ['05','06','07','08','09']

#We build the dataset of public bikes data for those years
df_19 = load_years('2019',months)
df_20 = load_years('2020',months)

#We now separate the data by day, and aggregate it by counting the total rides and summing the total duration. The resulting dataframes have two columns
daily_2019 = df_19.groupby(df_19['started_at'].dt.date)['duration'].aggregate([np.size,np.sum])
daily_2020 = df_20.groupby(df_20['started_at'].dt.date)['duration'].aggregate([np.size,np.sum])

#Set columns and dataframes names
daily_2019.columns = ['Total rides','Total duration']
daily_2020.columns = ['Total rides','Total duration']
daily_2019.name = 'Rides 2019'
daily_2020.name = 'Rides 2020'

#As the index we use the day of the year (number of day in the year) instead of the date, so that they are comparable
daily_2019.index = daily_2019.index.astype("datetime64[ns]").dayofyear
daily_2020.index = daily_2020.index.astype("datetime64[ns]").dayofyear

#We reindex against the union of the indexes. This is needed because in a certain year there may be missing data for a particular day, and we are filling those days with NaN data. The reason we are doing this is because when performing operations like computations and unions it is easier to have matching indices (and we can also easily refer to missing data by checking NaNs).
newindex = daily_2019.index.union(daily_2020.index)
daily_2019 = daily_2019.reindex(newindex)
daily_2020 = daily_2020.reindex(newindex)

daily_2019.index.name = 'DOY'
daily_2020.index.name = 'DOY'

#Form big dataframe with union of the data
daily = pd.concat([daily_2019,daily_2020],axis=1)

#We compute the relative variation, day-by-day, in both total rides and total duration
variation_daily = ((daily_2020 / daily_2019) - 1)*100

#For the moment we avoid this passage
#We drop the rows where the computed values are NaN. We use isnull() to detect NaN values, and any(axis=1) to get a series of boolean values with True only in rows where there was at least one True value (i.e. at least one NaN).
#variation_daily = variation_daily.drop(variation_daily[variation_daily.isnull().any(axis=1)].index)

#We compute the 5-day rolling average of number of rides in both years
rolling_2019 = daily_2019.rolling(window=5,min_periods=3).mean()
rolling_2020 = daily_2020.rolling(window=5,min_periods=3).mean()
rolling_2019.index = rolling_2019.index.astype("datetime64[ns]").dayofyear
rolling_2020.index = rolling_2020.index.astype("datetime64[ns]").dayofyear


#Compute the relative variation. This is a series
variation = ((rolling_2020/rolling_2019) - 1)*100
rolling = pd.concat([rolling_2019,rolling_2020],axis=1)

#Plot the rolling averages for 2019 and 2020 alongside
rolling.plot(color=['tab:blue','tab:orange'])
plt.title("5-day Rides rolling average in 2019 and 2020")
plt.xlabel("Day of the year")
plt.ylabel("Number of rides")
plt.savefig(FIGURES_FOLDER + 'total_rides.pdf')

#Plot the relative variation
plt.figure()
variation.plot()
plt.title("5-day Rolling relative variation in the number of rides from 2019 to 2020")
plt.xlabel("Day of the year")
plt.ylabel("Percentage variation")
plt.savefig(FIGURES_FOLDER + 'rides_variation.pdf')

#Load Google's dataset, for comparison
df_google = load_google()

#Variation is a Series. When we join a Dataframe with a Series, the Series data are joined in the table as a column, but the name of the column is the name of the series so it must have a name (nameless series throw errors). Also, since we want to join on the "day of the year" feature, which is the index in the Series, we name it as "doy", which is the name it has in the Google dataframe. In this joining on "doy" is straightforward.
variation.index.name = 'doy'
variation.name = 'Public bikes variation'
df_joined = df_google.join(variation,on="doy",how="left") #dataframe with joined data


#Plot Google's and public bikes' data alongside. What we are plotting is the relative variation from baseline, from 2019 to 2020, in mobility. Google's data pertains all the mobility in transit stations, while the bikes' data only refers to the use of public bikes. The comparison attempt to evaluate how well the data on public bikes describes broader data.
plt.figure()
sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='transit_stations_percent_change_from_baseline',color='tab:blue',label='Google')
sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='Public bikes variation',color='tab:orange',label='Public bikes')
plt.legend()
plt.title("Comparison of Google's variation and public bikes variation")
plt.xlabel("Day of the year")
plt.ylabel("Percent variation from baseline")
plt.savefig(FIGURES_FOLDER + 'comparison_variations.pdf')
