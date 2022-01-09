import pandas as pd
import matplotlib.pyplot as plt

#Folder where to save output figures
FIGURES_FOLDER = 'figures/'

#Function that plots the rolling averages of a given dataframe containing 2019 and 2020 data. The window defaults to 7 time units.
def plot_rolling_average(series,window=7,min_periods=3):
    series.rolling(window=window,min_periods=min_periods).mean().plot(color=['tab:blue','tab:orange'])
    plt.title(f"{window}-day {series.columns[0].capitalize()} rolling average in 2019 and 2020")
    plt.xlabel("Day of the year")
    plt.ylabel(series.columns[0].capitalize())
    plt.legend(['2019','2020'])
    plt.show()
    plt.savefig(FIGURES_FOLDER + 'rolling_{:}.pdf'.format(series.columns[0].lower().replace(' ','_')))
    print(FIGURES_FOLDER + 'rolling_{:}.pdf'.format(series.columns[0].lower().replace(' ','_')))
