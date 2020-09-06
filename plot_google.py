#! /usr/bin/env python3

#This script loads Google data on mobility in Oslo, and then plots the variation as computed by Google. We are interested in the "transportation" column of the Google dataset.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('seaborn')

def plot_google():
    df = pd.read_csv("GOG-Global_Mobility_Report.csv",parse_dates=[7])
    df["doy"] = df["date"].dt.dayofyear
    #df_month = df[df["date"].dt.month.isin([5,6,7])].copy()
    sns.lineplot(data=df[df["date"].dt.month.isin([5,6,7,8])],x="doy",y="transit_stations_percent_change_from_baseline")
    plt.title("Google's relative variation in transit stations mobility")
    plt.ylabel("Transit stations percent variation from baseline")
    plt.xticks(rotation=45)
    plt.savefig("google_variation.pdf")

if __name__=='__main__':
    plot_google()
