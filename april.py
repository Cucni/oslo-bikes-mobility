#! /usr/bin/env python3

#This script contains the function used in the April.ipynb notebook

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import zscore #Z-score function to detect outliers

#Function that takes in a pandas series and returns outliers with a z-score larger than 3
def get_zscore_outliers(series):
    '''Returns values of a pandas series with z-score larger than 3'''
    z = np.abs(zscore(series))
    outliers = series[z>3]
    return outliers

#Function that takes a dataframe with the rides in a subperiod of a year, and return a dataframe with the data aggreagated by day. Resulting columns are the total number of rides, the total rides duration and the year. Note: it is specific for the study of the Oslo public bikes data, so the columns "started_at" and "duration" are always present
def aggregate_by_day(dataframe):
    '''Returns a pandas dataframe with the data on total rides and total duration aggregated by day'''
    groups = dataframe.groupby(dataframe['started_at'].dt.date)
    days_df = groups['duration'].aggregate([np.size,np.sum])
    days_df.columns = ['Total rides','Total duration']
    days_df.index = days_df.index.astype('datetime64[ns]').day
    days_df.index.name = 'Day'
    days_df['Year'] = dataframe.loc[0,'started_at'].year
    return days_df

#Function that takes two dataframes with rides (in two different years), and returns a unique dataframes with all the data, aggregated by year and by weekday. Resulting columns are the total number of rides and the total rides duration. Note: it is specific for the study of the Oslo public bikes data, so the columns "started_at" and "duration" are always present
def joint_aggregate_by_weekday(dataframe1,dataframe2):
    df = pd.concat([dataframe1,dataframe2])
    mask_weekday = np.where(df['started_at'].dt.weekday<5,"Weekday","Weekend")
    groups = df.groupby([df['started_at'].dt.year,mask_weekday])

    df_weekday = groups['duration'].aggregate([np.size,np.sum])
    df_weekday.columns = ['Total rides','Total duration']
    df_weekday.index.names = ['Year',None]
    return df_weekday


#Function that takes two dataframes with rides (in two different years), and returns a unique dataframes with all the data, aggregated by year, week and weekday. Resulting columns are the total number of rides and the total rides duration. Note: it is specific for the study of the Oslo public bikes data, so the columns "started_at" and "duration" are always present
def joint_aggregate_by_week(dataframe1,dataframe2):
    df = pd.concat([dataframe1,dataframe2])
    mask_weekday = np.where(df['started_at'].dt.weekday<5,"Weekday","Weekend")
    groups = df.groupby([df['started_at'].dt.year,df['started_at'].dt.week,mask_weekday])

    df_week = groups['duration'].aggregate([np.size,np.sum])
    df_week.columns = ['Total rides','Total duration']
    df_week.index.names = ['Year','Week',None]
    return df_week


#Function that takes a dataframe containing data on rides and plots the relative variation between 2020 and 2019. It plots the relative variation of the following quantities: Total rides, Total duration and Average ride duration (computed from the other two). It uses a bar plot.
def plot_rel_variations(dataframe):
    _variation = (dataframe.loc[2020,'Total rides'] / dataframe.loc[2019,'Total rides']) - 1
    _variation = _variation.to_frame(name='Total rides')
    _variation['Total duration'] = (dataframe.loc[2020,'Total duration'] / dataframe.loc[2019,'Total duration']) - 1
    _variation['Average duration'] = ((dataframe.loc[2020,'Total duration'] / dataframe.loc[2020,'Total rides']) / (dataframe.loc[2019,'Total duration'] / dataframe.loc[2019,'Total rides'])) - 1

    _variation.plot(kind='bar')
    plt.legend(bbox_to_anchor=(1,1))
    plt.xticks(rotation=0)
    plt.title('Relative variation by weekday')

    display(_variation)
 

#Function that takes a dataframe containing data on rides and plots the relative variation between 2020 and 2019, by week. It plots separately the relative variation of Total rides and Total duration, with two bar plots. The data is further separated (with the "hue" parameter) by weekday.
def plot_weekly_var(dataframe):
    _week_var = ((dataframe.loc[2020] / dataframe.loc[2019]) - 1).reset_index()
    plt.subplot(121)
    sns.barplot(x='Week',y='Total rides',hue='level_1',data=_week_var)
    plt.ylabel('')
    plt.legend('')
    plt.title('Rides variation by week')
    plt.subplot(122)
    sns.barplot(x='Week',y='Total duration',hue='level_1',data=_week_var)
    plt.ylabel('')
    plt.legend(bbox_to_anchor=(1,1))
    plt.title('Duration variation by week')
