#! /usr/bin/env python3

#This scripts fetches the data from the Oslo Bysykkel server, and then plots the relative variation in bikes mobility. It does so for the months specified in the "months" list. The variation is computed between 7-days rolling averages.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import public_bikes_functions
import mobility_report_functions
import visualizations

plt.style.use('seaborn')

#Folder where to save output figures
FIGURES_FOLDER = 'figures/'

#Range of months that we are analyzing
months = np.arange(5,13)

def extract_totals(df):
    '''Resamples data by day and computes total rides and total rides duration.'''
    return df.resample('D',on='started_at')['duration'].agg([np.size,np.sum])

#Set columns and dataframes names
def name_columns(df,year):
    '''Sets the correct names for the columns containing total rides and total rides duration. Also sets the dataframe name to "Rides YYYY".'''
    df.columns = ['Total rides','Total duration']
    df.name = 'Rides {:}'.format(year)

    return df

#As the index we use the day of the year (number of day in the year) instead of the date, so that they are comparable
def index_with_doy(df):
    '''Creates columns containing day and number of day in the year, then sets this last as index.'''
    df = df.assign(day = lambda x: x.index.date,
              doy = lambda x: x.index.dayofyear
       ).pipe(lambda x: x.set_index('doy'))
    return df


#Load datasets of public bikes data
df_19 = public_bikes_functions.load_months(2019,months)
df_20 = public_bikes_functions.load_months(2020,months)

#Extract total rides and total duration in structured dataframe
daily_2019 = df_19.pipe(extract_totals).pipe(name_columns,year=2019).pipe(index_with_doy)
daily_2020 = df_20.pipe(extract_totals).pipe(name_columns,year=2020).pipe(index_with_doy)


#We compute the 7-day rolling average of number of rides in both years
rolling_2019 = daily_2019.rolling(window=7,min_periods=3).mean()
rolling_2020 = daily_2020.rolling(window=7,min_periods=3).mean()

#Form big dataframe with union of the rolling data
rolling = pd.concat([rolling_2019,rolling_2020],axis=1)

#Compute the relative variation of the rolling averages. This is a series
variation_rolling = ((rolling_2020/rolling_2019) - 1)*100

#Plot the rolling average of total rides for 2019 and 2020 alongside
visualizations.plot_rolling_average(rolling['Total rides'])

#Plot the rolling average of total rides duration for 2019 and 2020 alongside
visualizations.plot_rolling_average(rolling['Total duration'])

#Plot the relative variation
plt.figure()
variation_rolling.plot()
plt.title("7-day Rolling relative variation in the number and duration of rides from 2019 to 2020")
plt.xlabel("Day of the year")
plt.ylabel("Percentage variation")
plt.savefig(FIGURES_FOLDER + 'rolling_variation.pdf')

#Load Google's dataset, for comparison
df_google = mobility_report_functions.load_google(2020)
df_google = df_google.loc[df_google['sub_region_1'] == 'Oslo',:].reset_index(drop=True)

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
