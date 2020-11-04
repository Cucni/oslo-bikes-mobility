# Analysis of Oslo city bikes mobility data #

The aim of this project is to deduce insights about public mobility in Oslo, through the analysis of the data on public shared bikes of the city. It currently contains two studies.

## April 2020 mobility data and Covid-19 lockdown ##

The goal of the first study is to deduce insights about the intensity of the lockdown at Oslo in April.

The motivation for this study is to try to use data to find possible trends or interesting insights about biking mobility, and possibly overall mobility; and then use these findings to draw deductions on the lockdown.

The naive observation at the time was that people apparently started to get out more in mid-April, to be less concerned about crowded places and in general more relaxed about the Covid-19 contagion risk. I then created this project in order to check if these observations were backed by mobility data. In general, the harder the lockdown, the fewer the people travelling. Therefore I should be able to assess how strong the restrictions are, and how closely people are following them, by looking at mobility data.


There are two interconnected questions I am trying to answer with this analysis:
 - I expect a decrease in (biking) mobility in 2020, compared to previous years. Is there any trend in this expected decrease? For example, did people pick up the bike more as the days passed by?
 - If such a trend exists, is it a day-by-day trend? A week-by-week trend?
 - Is the expected decrease different on weekdays and in weekends?
 - Do other mobility-related factors, such as the type of travel, play any role in this?
 - Do other non-mobility-related factors, such as public holidays or the weather, play any role in this?


The methodology for the study is to compare the 2020 data with the 2019 data. I use 2019 data on public bikes as the baseline (no data on April 2018 is available). After setting up the environment I clean the data by identifying and removing outliers in both years. I then proceed to analyze the data, aggregating it in different ways, to deduce trends and insights.


I have decided to analyse mobility data on the use of the city public bikes. This decision comes from the following facts:
 - bike rides are less essential for commuting than car travels or other public transport, so I believe they are more likely linked to travels for personal leisure (e.g. weekend cycling). This kind of travel is generally more impacted by a lockdown.
 - Bike sharing is a public transport service even though the bike is a 1-person means of transport; hence the Oslo city bikes could be a proxy for measuring the use of public trasport.
 - The data is open and freely licensed for personal and study use.

### Code ###

The file [April.ipynb](April.ipynb) contains the analysis in a jupyter notebook file that you can visualise directly in the browser, with all the deductions, charts and explanations. The file [april.py](april.py) contains the code used to work on the data: clean the dataframe, grouping data, aggregating it, computing and plotting.

For ease of use and transparency, the CSV files ['04-2019.csv']('04-2019.csv') and ['04-2020.csv']('04-2020.csv') with the data on April 2019 and 2020 are included in the repository.

## Estimate of variation in mobility and use as proxy for overall mobility (work in progress) ##

The second study aims to estimate the variation in the public bike mobility, and to compare it agains the variation in the overall mobility as estimated by Google. This could give some indication of how good of a proxy public bike mobility is, with respect to overall mobility. This study is in a development stage. It is hosted on the branch ``2020-summer-analysis``.

### Code ###

The file [main.py](main.py) is the main script. It loads public bikes data and processes it to compute the relative variation in the period from May to August. It also loads Google's data and compares the two. The script ['public_bikes_functions.py']('public_bikes_functions.py') contains the function to load and preprocess public bikes data. The script ['plot_google.py']('plot_google.py') contains the functions to load, preprocess and plot Google's data. If run standalone, it plots the relative variation in transit stations mobility, as computed by Google.

## Technologies ##

Python 3.7.3, Numpy 1.16.2, Pandas 0.23.3, SciPy 1.1.0, Matplotlib 3.0.2, Seaborn 0.9.0, Jupyter Notebook 4.4.0.

## Data source and licensing ##

The currently used data is updated at September 29, 2020. The data about April is complete.

The data on Oslo public bikes comes directly from the service:

https://oslobysykkel.no/en/open-data

It is available under the NLOD license (Norwegian Licence for Open Government Data), version 2.0.

https://data.norge.no/nlod/no/2.0

In particular it is free to use for personal study and research, upon correct attribution.

Data from Google comes from its published mobility reports, as found at

_"Google COVID-19 Community Mobility Reports"_
https://www.google.com/covid19/mobility/
