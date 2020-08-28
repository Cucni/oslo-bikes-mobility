# Analysis of Oslo city bikes mobility data #

The aim of this project is to deduce insights about public mobility in Oslo, through the analysis of the data on public shared bikes of the city.

## April 2020 mobility data and Covid-19 lockdown ##

The first study aims to deduce insights about the intensity of the lockdown at Oslo in April.

I was inspired to create this project by naive observations: at the eye tests, people started to get out more in mid-April, to be less concerned about crowded places and in general more relaxed about the Covid-19 contagion risk. I then created this project in order to check mobility data backed my observations. In general, the harder the lockdown, the fewer the people travelling. Therefore we should be able to assess how strong the restrictions are, and how closely people are following them, by looking at mobility data.

I have decided to analyse mobility data on the use of the city public bikes. This decision comes from the following facts:
 - bike rides are less essential for commuting than car travels or other public transport, so I believe they are more likely linked to travels for personal leisure (e.g. weekend cycling)
 - bike sharing is a public transport service even though the bike is a 1-person means of transport; hence the Oslo city bikes could measure more reliably the use of public trasport
 - the data is open and freely licensed for personal and study use

There are two interconnected questions I am trying to answer with this analysis:
 - Were people going out more as the weeks passed, as result of a general relaxation about lockdown measures?
 - Were people going out more, as the result of less strict lockdown measures?

### Code ###

The file [April.ipynb](April.ipynb) contains the actual analysis, with all the code, the charts and the comments and deductions one can make (or try to make). It is a jupyter notebook file that you can visualise directly in the browser.

For ease of use and transparency, the CSV files ['04-2019.csv']('04-2019.csv') and ['04-2020.csv']('04-2020.csv') with the data on April 2019 and 2020 are included in the repository.

## Estimate of variation in mobility and use as proxy for overall mobility ##

The second study aims to estimate the variation in the public bike mobility, and to compare it agains the variation in the overall mobility as estimated by Google. This could give some indication of how good of a proxy public bike mobility is, with respect to overall mobility.

This study is still a work in progress heavily.

## Technologies ##

Python 3.5.2, Numpy 1.18.2, Pandas 0.24.2, Matplotlib 3.0.2, Seaborn 0.9.0

## Data source and licensing ##

The currently used data is updated at May 22, 2020. The data about April is complete.

The data comes directly from the service:

https://oslobysykkel.no/en/open-data

It is available under the NLOD license (Norwegian Licence for Open Government Data), version 2.0.

https://data.norge.no/nlod/no/2.0

In particular it is free to use for personal study and research, upon correct attribution.
