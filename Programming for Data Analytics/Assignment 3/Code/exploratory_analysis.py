# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Sat Nov 28 08:10:44 2020
    
"""
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import numpy as np
import os
import calendar
from os import path

import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats  
import matplotlib.dates as mdates

import seaborn as sns

os.chdir(r'E:/Karla/IRELAND v2/DKIT/1st Semester/Programming with Python/Continuous Assessments/Assessement 2')
w = pd.read_csv('weather_2019.csv')

w.info()

w['date'] = pd.to_datetime(w['date'], format = '%d-%m-%Y')

w.set_index(['date'], inplace=True)
w.sort_index(inplace=True)

w[w['city']=='Mexico City'].shape
w[w['city']=='Dublin'].shape

# Droping icon and wind_gust since all observations have no values.
w.drop(columns=['wind_gust','icon'],inplace=True)

# Lets save in another dataframe the not found data.
w_missing = w[w['description']=='Not found']
w_missing['month'] = list(map(lambda d: int(d.month), w_missing.index))
w_missing['day'] = list(map(lambda d: int(d.day), w_missing.index))
w_missing['year'] = list(map(lambda d: int(d.day), w_missing.index))

# And remove from original dataset
w = w.drop(w_missing.index)

# No more missing values.
# Now, let's give proper format to variables
w['day'] = w['day'].apply(lambda x:int(x))
w['month'] = w['month'].apply(lambda x:int(x))
w['year'] = w['year'].apply(lambda x:int(x))
w['hour'] = w['hour'].apply(lambda x:int(x))
w['min'] = w['min'].apply(lambda x:int(x))

# new column
w['month_name'] = list(map(lambda x: calendar.month_abbr[int(x)],w.month))

# Missing values
w[w['description'].isnull()] 

# Looking at this data, randomly selecting some of them in the website
#  it looks like the description is regarding clear sky (e.i. no clouds).
w['description'].fillna('Clear', inplace=True)

w_mx = w[w['city']=='Mexico City']
w_dub = w[w['city']=='Dublin']

w_mx.shape
w_dub.shape

# Done, let's look at statistic data
# Originally, from the website:
#  10 variables.
#    from which:
#     mexico, 6393 observations
#     dublin, 12005 observations

#   I create 9 variables to describe better the data:
#    country => Ireland or Mexico
#    city => Dublin or Mexico City
#    station => Dublin aiport or Internacional Benito J (airport)
#    day, month and year => from date
#    hour, min => from time

# Describe variables:
#  Country, City, Station, time, description are categorical nominal variables
#  day, month, hour, min are numerical discrete variables
#  temperature, rel_temperature, wind, rel_humidity, dew_point, pressure are continuous variables
#  wind_dir has mixed data to descibe no wind no direction as "calm".

# Exploring missing data
w_dub_missing = w_missing[w_missing['city']=='Dublin']
w_mx_missing = w_missing[w_missing['city']=='Mexico City']

# 106 dates are missing in Mexico
# 108 dates in Ireland are missing
# Lets plot

def missing_vals(df_, df_miss, r, c, n):
    
    city_ = df_miss['city'].unique()[0]
    
    w_mx_not_missing_monthly = df_.groupby(by=['month','day']).mean().groupby('month').count()[['temperature']]
        
    w_mx_missing_monthly = df_miss.groupby('month').count()[['description']]
    w_mx_missing_monthly.rename(columns={'description':'temperature_m'}, inplace=True)
    
    w_temporal = pd.concat([w_mx_missing_monthly,w_mx_not_missing_monthly], join='inner', axis=1)
    
    x=w_mx_not_missing_monthly.index
    y=w_temporal.index
    z=x.difference(y).to_list()
    
    w_temporal_2 = pd.concat([w_temporal, w_mx_not_missing_monthly.loc[z]], ignore_index=False, sort=False)
    w_temporal_2['month_name'] = list(map(lambda x: calendar.month_abbr[int(x)], w_temporal_2.index))
    w_temporal_2.fillna(0, inplace=True)
    w_temporal_2['percentage_m'] = w_temporal_2['temperature_m']/(w_temporal_2['temperature']+w_temporal_2['temperature_m'])
    w_temporal['percentage_m'] = w_temporal['temperature_m']/(w_temporal['temperature']+w_temporal['temperature_m'])
        
    fig, ax = plt.subplots()
    plt.bar(w_temporal_2.index, w_temporal_2.temperature_m, label='Missing days', color='orange')
    plt.bar(w_temporal_2.index, w_temporal_2.temperature, bottom = w_temporal_2.temperature_m, label='Days', color='green')
    plt.xticks(w_temporal_2.index, w_temporal_2.month_name, rotation=90)
    ax.set_xlabel('Month')
    ax.set_ylabel('Observations')
    
    for i in w_temporal.sort_values(by=['percentage_m'], ascending=False).iterrows():
        ax.annotate(str(round(i[-1][-1]*100))+'%', xy=[i[0], 0.5], xytext=[i[0]-0.15, 0.8], rotation=90, color='white')
    
    plt.title('Missing observations per month in ' +city_ + ' in 2019')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.show()
    
    print(w_temporal_2)
    
missing_vals(w_mx, w_mx_missing, 2, 2, 1)
missing_vals(w_dub, w_dub_missing, 2, 2, 2)


fig, ax = plt.subplots()
ax.hist(w_mx["temperature"], histtype='step', label='Mexico City')
ax.hist(w_dub["temperature"], histtype='step', label='Dublin')
ax.set_xlabel("Temperature (C°)")
ax.set_ylabel("# of observations")
plt.title("Temperature of Mexico City and Dublin in 2019")
plt.legend()
plt.show()

# Distribution of observations after removing missing values
plt.subplot(2,2,1)
sns.distplot(w_mx_temp_daily['temperature'], label='Mexico City', color='orange')
plt.xlabel('Temperature (C°) in Mexico City')
plt.subplot(2,2,2)
sns.distplot(w_dub_temp_daily['temperature'], label='Dublin', color='green')
plt.xlabel('Temperature (C°) in Dublin')
plt.suptitle('Distirbution of Daily Temperature in Mexico City and Dublin. 2019')
plt.show()

#-----------------------------------------

def box_plot_desc(w_, column_n, units):
    sns.boxplot(y=w_[column_n], x=w_['city'])
    plt.xlabel('City')
    plt.ylabel(column_n.capitalize().replace('_',' ') + " in " + units)
    plt.title(column_n.capitalize().replace('_',' ') +" in "+str(w_['year'].unique()[0]))
    plt.show()
    print(w_[column_n].describe())

for i in w.describe().loc[:,'temperature':].columns:
    units = input("units of " + i)
    box_plot_desc(w,i, units)

w_mx.loc[:,'temperature':].describe().to_csv('summary_statistics_mx.csv')
w_dub.loc[:,'temperature':].describe().to_csv('summary_statistics_dub.csv')

# Temperature

# ----------------------------

w_mx_temp_monthly = w_mx[['month', 'temperature']].groupby('month').agg(['mean','min','max'])
w_mx_temp_monthly['month_name'] = list(map(lambda x: calendar.month_abbr[int(x)], w_mx_temp_monthly.index))
w_dub_temp_monthly = w_dub[['month', 'temperature']].groupby('month').agg(['mean','min','max'])
w_dub_temp_monthly['month_name'] = list(map(lambda x: calendar.month_abbr[int(x)], w_dub_temp_monthly.index))

fig, ax = plt.subplots(1,2,figsize=(10,3))
ax[0].plot(w_mx_temp_monthly.index, w_mx_temp_monthly['temperature']['min'], color='blue', label='Min temp', linestyle='--')
ax[0].plot(w_mx_temp_monthly.index, w_mx_temp_monthly['temperature']['mean'], color='green', label='Mean temp', marker='o')
ax[0].plot(w_mx_temp_monthly.index, w_mx_temp_monthly['temperature']['max'], color='red', label='Max temp', linestyle='--')
ax[0].set_xticks(w_mx_temp_monthly.index)
ax[0].set_xticklabels(w_mx_temp_monthly.month_name, rotation=90)
ax[0].set_ylabel('Temperature in C°')
ax[0].set_xlabel('Mexico')

ax[1].plot(w_dub_temp_monthly.index, w_dub_temp_monthly['temperature']['min'],  color='blue',  label='Min temp',  linestyle='--')
ax[1].plot(w_dub_temp_monthly.index, w_dub_temp_monthly['temperature']['mean'], color='green', label='Mean temp', marker='o')
ax[1].plot(w_dub_temp_monthly.index, w_dub_temp_monthly['temperature']['max'],  color='red',   label='Max temp',  linestyle='--')
ax[1].set_xticks(w_dub_temp_monthly.index)
ax[1].set_xticklabels(w_dub_temp_monthly.month_name, rotation=90)
ax[1].set_xlabel('Dublin')

ax[0].set(ylim=(-6, 33))
ax[1].set(ylim=(-6, 33))

fig.suptitle("Temperature of Mexico City and Dublin in 2019", fontsize=14)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
ax[0].grid(color='lightgray')
ax[1].grid(color='lightgray')
plt.show()


# ---------------------------------------------------------------


x = w_mx_temp_monthly.index
y1 = w_mx_temp_monthly['temperature']['min']
y2 = w_mx_temp_monthly['temperature']['mean']
y3 = w_mx_temp_monthly['temperature']['max']

x_dub = w_dub_temp_monthly.index
y1_dub = w_dub_temp_monthly['temperature']['min']
y2_dub = w_dub_temp_monthly['temperature']['mean']
y3_dub = w_dub_temp_monthly['temperature']['max']

fig, ax = plt.subplots()
ax.plot(x, y2, color='red', marker='o')
ax.plot(x_dub, y2_dub, color='green', marker='o')
ax.plot(x, y1, color='red', linestyle='--')
ax.plot(x, y3, color='red', linestyle='-.')
ax.fill_between(x, y1, y3, where= y1 <= y3, facecolor='red', alpha=0.1, interpolate=True)

ax.plot(x_dub, y1_dub, color='green', linestyle='--')
ax.plot(x_dub, y3_dub, color='green', linestyle='-.')
ax.fill_between(x_dub, y1_dub, y3_dub, where= y1_dub <= y3_dub, facecolor='green', alpha=0.1, interpolate=True)

ax.set_xticks(w_mx_temp_monthly.index)
ax.set_xticklabels(w_mx_temp_monthly.month_name, rotation=90)
ax.set_ylabel('Temperature in C°')
ax.set_xlabel('Month')

fig.suptitle("Mexico City and Dublin temperature in 2019", fontsize=14)
plt.legend(['Mexico City', 'Dublin'], bbox_to_anchor=(1.01, 1), loc='upper left')
plt.show()


# -----------------------------------------------------------------------
# Scatter plots fro daily weather measures.

sns.pairplot(w_dub_temp_daily)
plt.show()

w_mx_temp_daily = w_mx[['temperature','relative_temperature','rel_humidity','wind','pressure','dew_point']].groupby('date').mean()
w_mx_temp_daily['month_name'] = list(map(lambda x: calendar.month_abbr[int(x.month)], w_mx_temp_daily.index))
w_mx_temp_daily['city']='Mexico City'
w_dub_temp_daily = w_dub[['temperature','relative_temperature','rel_humidity','wind','pressure','dew_point']].groupby('date').mean()
w_dub_temp_daily['month_name'] = list(map(lambda x: calendar.month_abbr[int(x.month)], w_dub_temp_daily.index))
w_dub_temp_daily['city']='Dublin'
w_temp_daily = pd.concat([w_mx_temp_daily,w_dub_temp_daily])


plt. subplot(2,2,1)
tcat=plt.scatter(x=w_mx_temp_daily.temperature, y=w_mx_temp_daily.relative_temperature, alpha=0.5, c=w_mx_temp_daily.relative_temperature, cmap='rainbow')
plt.xlabel('Temperature C° in Mexico City')
plt.ylabel('Relative Temperature C°')
plt.colorbar(tcat)
plt.tight_layout(pad=2)
plt.grid(True)

plt.subplot(2,2,2)
tcat=plt.scatter(x=w_dub_temp_daily.temperature, y=w_dub_temp_daily.relative_temperature, alpha=0.5, c=w_dub_temp_daily.relative_temperature, cmap='rainbow')
plt.xlabel('Temperature C° in Dublin')
plt.ylabel('Relative Temperature C°')
plt.colorbar(tcat)
plt.suptitle('Daily Temperature and Relative Temperature in Mexico City and Dublin. 2019')
plt.tight_layout(pad=2)
plt.grid(True)
plt.show()

#---------------------------------------------------------------

plt. subplot(2,2,1)
tcat = plt.scatter(x=w_mx_temp_daily.pressure, y=w_mx_temp_daily.temperature, alpha=0.4, c=w_mx_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.xlabel('Pressure mb in Mexico City')
plt.ylabel('Temperature C°')
plt.tight_layout(pad=2)
plt.grid(True)

plt.subplot(2,2,2)
tcat = plt.scatter(x=w_dub_temp_daily.pressure, y=w_dub_temp_daily.temperature, alpha=0.4, c=w_dub_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.xlabel('Pressure mb in Dublin')
plt.ylabel('Temperature C°')
plt.suptitle('Daily Temperature and Pressure in Mexico City and Dublin. 2019')
plt.tight_layout(pad=2)
plt.grid(True)
plt.show()

# -------------------------------------------------------

plt.subplot(2,2,1)
tcat = plt.scatter(x=w_mx_temp_daily.wind, y=w_mx_temp_daily.temperature, alpha=0.4, c=w_mx_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.xlabel('Wind speed km/hr in Mexico City')
plt.ylabel('Temperature C°')
plt.tight_layout(pad=2)
plt.grid(True)

plt.subplot(2,2,2)
tcat = plt.scatter(x=w_dub_temp_daily.wind, y=w_dub_temp_daily.temperature, alpha=0.4, c=w_dub_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.xlabel('Wind speed km/hr in Dublin')
plt.ylabel('Temperature C°')
plt.suptitle('Daily Temperature and Wind Speed in Mexico City and Dublin. 2019')
plt.tight_layout(pad=2)
plt.grid(True)
plt.show()


# -----------------------------------------------------


plt.subplot(2,2,1)
tcat = plt.scatter(x=w_mx_temp_daily.temperature, y=w_mx_temp_daily.rel_humidity, alpha=0.4, c=w_mx_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.ylabel('Relative Humidity %')
plt.xlabel('Temperature C° in Mexico City')
plt.tight_layout(pad=2)
plt.grid(True)

plt.subplot(2,2,2)
tcat = plt.scatter(x=w_dub_temp_daily.temperature, y=w_dub_temp_daily.rel_humidity, alpha=0.4, c=w_dub_temp_daily.relative_temperature, cmap='rainbow')
plt.colorbar(tcat)
plt.ylabel('Relative Humidity %')
plt.xlabel('Temperature C° in Dublin')
plt.suptitle('Daily Temperature and Rel. Humidity in Mexico City and Dublin. 2019')
plt.tight_layout(pad=2)
plt.grid(True)
plt.show()

