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
newindex.name = 'doy'
daily_2019 = daily_2019.reindex(newindex)
daily_2020 = daily_2020.reindex(newindex)

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

#Form big dataframe with union of the rolling data
rolling = pd.concat([rolling_2019,rolling_2020],axis=1)

#Compute the relative variation of the rolling averages. This is a series
variation_rolling = ((rolling_2020/rolling_2019) - 1)*100

#Plot the rolling average of total rides for 2019 and 2020 alongside
rolling['Total rides'].plot(color=['tab:blue','tab:orange'])
plt.title("5-day Total Rides rolling average in 2019 and 2020")
plt.xlabel("Day of the year")
plt.ylabel("Number of rides")
plt.legend(['2019','2020'])
plt.savefig(FIGURES_FOLDER + 'rolling_total_average.pdf')

#Plot the relative variation
plt.figure()
variation_rolling.plot()
plt.title("5-day Rolling relative variation in the number and duration of rides from 2019 to 2020")
plt.xlabel("Day of the year")
plt.ylabel("Percentage variation")
plt.savefig(FIGURES_FOLDER + 'rolling_variation.pdf')

#Load Google's dataset, for comparison
df_google = load_google()

#We join the Dataframe with Google's data with the one with rolling variation data. We want to join on the "day of the year" feature, which is the index in the rolling Dataframe, named "doy" in the Google dataframe. Since it is the same name of the rolling dataframe index, joining on "doy" is straightforward.
#If variation were a Series, then it would have been joined in the table as a column, but the name of the column would have been the name of the series so it would have needed a name (nameless series throw errors).
variation_rolling.columns = ['Total rides variation','Total duration variation']
df_joined = df_google.join(variation_rolling,on="doy",how="left") #dataframe with joined data


#Plot Google's and public bikes' data alongside. What we are plotting is the relative variation from baseline, from 2019 to 2020, in mobility. Google's data pertains all the mobility in transit stations, while the bikes' data only refers to the use of public bikes. The comparison attempt to evaluate how well the data on public bikes describes broader data.
plt.figure()
sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='transit_stations_percent_change_from_baseline',color='tab:blue',label='Google')
sns_plot = sns.lineplot(data=df_joined[df_joined['date'].dt.month.isin(months)],x='doy',y='Total rides variation',color='tab:orange',label='Public bikes')
plt.legend()
plt.title("Comparison of Google's variation and public bikes variation")
plt.xlabel("Day of the year")
plt.ylabel("Percent variation from baseline")
plt.savefig(FIGURES_FOLDER + 'comparison_variations.pdf')
