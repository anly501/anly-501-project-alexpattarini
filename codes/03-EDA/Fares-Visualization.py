# Import relevant libraries
import numpy as np
import pandas as pd
import os
import re
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as md
import random

# Set working directory to current file location
wdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(wdir)

# Import cleaned fares data
fares = pd.read_csv("../../data/01-modified-data/MTA-Fare-Card-Cleaned-Gathered.csv",index_col=0)
#print(fares.head())

### TIME SERIES FOR FOUR FARE TYPES ###
fare_type_list = ["full_fare","X_30_day_unlimited","X_7_day_unlimited","senior_citizen_disabled"]
fname = ["Full Fare","30 Day Unlimited","7 Day Unlimited","Senior Citizen-Disabled"]
# Set seed for reproducible colors of plots
random.seed(1771)
# Loop by dataframe filters of interest and formatted names of metrocard types
for index,ftype in enumerate(fare_type_list):
    # Subset overall df by fare type
    new_fares = fares.loc[fares['fare_type']==ftype]
    # Sum fare counts by date range
    new_fares_g = new_fares.groupby(['to_date','fare_type']).sum()
    # Reformat to have appropriate columns
    new_fares_g.reset_index(inplace=True)
    #print(full_fares_g.head())
    # Retypecast to_date to date type
    new_fares_g['to_date'] = pd.to_datetime(new_fares_g['to_date'],format='%Y-%m-%d')
    #print(new_fares_g.head())
    #print(new_fares_g.sort_values('fare_count'))

    fig, ax = plt.subplots(figsize=(12,8))
    # Set color for dataframe (random)
    color_n = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    # Create plot for specific data frame
    fares_dates = new_fares_g['to_date']
    sns.lineplot(x='to_date',y='fare_count',data=new_fares_g,color=color_n)
    ax.set_xticklabels(labels=fares_dates,rotation=45)
    ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    plt.title("Time Series of "+fname[index]+" MetroCard Counts by Week 2017-2021")
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel("Count of Fares")
    plt.xlabel("Date")
    # Uncomment below to display plots
    #plt.show()
    # Save plot as png
    filepath = "../../501-project-website/images/TIMESERIES-"+fname[index]+"-MetroCard.png"
    plt.savefig(filepath)


### TESTING PLOTS ###
'''
# Create plot
fig,ax = plt.subplots(nrows=2,ncol=2)
sns.lineplot(x='to_date',y='fare_count',data=full_fares_g)
fares_dates = full_fares_g['to_date']
ax.set_xticklabels(labels=fares_dates,rotation=45)
ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
plt.title("Time Series of Full Fare Counts by Week 2017-2021")
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel("Count of Fares")
plt.xlabel("Date")
plt.show()
'''
'''
fig, ax = plt.subplots(2,2)
fares_dates = new_fare_list[0]['to_date']
sns.lineplot(x='to_date',y='fare_count',data=new_fare_list[0],ax=ax[0,0])
sns.lineplot(x='to_date',y='fare_count',data=new_fare_list[1],ax=ax[0,1])
sns.lineplot(x='to_date',y='fare_count',data=new_fare_list[2],ax=ax[1,0])
sns.lineplot(x='to_date',y='fare_count',data=new_fare_list[3],ax=ax[1,1])
# Reformat dates on plot
fares_dates = new_fare_list[0]['to_date']
ax[0,0].set_xticklabels(labels=fares_dates,rotation=45)
ax[0,0].xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
ax[0,1].set_xticklabels(labels=fares_dates,rotation=45)
ax[0,1].xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
ax[1,0].set_xticklabels(labels=fares_dates,rotation=45)
ax[1,0].xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
ax[1,1].set_xticklabels(labels=fares_dates,rotation=45)
ax[1,1].xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
# Reformat ticks and labels
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel("Count of Fares")
plt.xlabel("Date")
plt.show()
'''