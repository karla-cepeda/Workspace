# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Sat Nov  7 08:10:44 2020

READ ME FIRST:
    Hi Jack,
    Please find below answers for Question 2, CA 1.
    
    NOTES:
        Please, change dir if you want to run code.
        I added as much comments as possible, please read carefully.
    
"""

import pandas as pd
import numpy as np
import os


# -----------------------------
#
# Having tidied the dataset, answer the following questions. The questions should be
#  answered using Python code to output the answer to the console, not by visual
#  inspection.
#
# -----------------------------
# From Question 1
# Lets use csv file we created in previous question.
# Important to remember what I have done previously:
#   - Replacing '--' for np.nan
#   - Removing Duplicated rows

# Please, change directory file according to location of CA1 folder in your computer. Thank you.
os.chdir('E:/Karla/IRELAND v2/DKIT/1st Semester/Programming with Python/Continuous Assessments/Assessement 1')

wd = pd.read_csv('Dataset/brazil_weather_tidy_version.csv')
wd.name = "WeatherFromBrazil"

# And, just for fun, lets apply format to the column date
wd.date = pd.to_datetime(wd.date, format = '%d/%m/%Y')

# For some help with name of columns, 
#  lets create a new variable with the first 7 rows from original dataset
#  of the csv file which contains the descripcion of the columns as a Series Object.  
wd_d = pd.read_csv("Dataset/brazil_weather.csv",nrows=7,usecols=[0],squeeze=True)

# -----------------------------


# -----------------------------------------
# Question 2.a
# What was the hourly maximum temperature (i.e. mxt) at station 
#  number 304 at 07:00 on 10/03/2010?
# ------------------------------------------
# Lets make things more easier. Index would help lots.
wd.set_index(["wsid","year","month","day","hr"],inplace=True)
wd.loc[304,2010,10,3,7][["mxt"]]
wd.reset_index(inplace=True)

# Now that I had seen the answer displayed in console, we can conclude that the hourly max temp is 0.0
#--------------------------------------------


# -----------------------------------------
# Question 2.b
# What was the highest minimum temperature in the dataset? At which station
#  number was this temperature measured?
# ------------------------------------------
wd2 = wd.groupby("wsid")[["mnt"]].max() 

# I can tell the max value of each station by printing wd2, but let's go further:
wd2[wd2["mnt"]==wd2.mnt.max()]

del wd2 # Let's free some space

# The highest minimum temperature in the dataset is 38.0
# This temperature mesured was at station number 178.
# ------------------------------------------


# -----------------------------------------
# Question 2.c
# Output the values of row index 145 in the first 
#  7 columns to the console.
# -----------------------------------------

#  NOTE: duplicated rows had been removed, row 145 might be different.
wd.iloc[145,:7]

# wsid                     178
# year                    2007
# month                     11
# day                       12
# hr                         1
# date     2007-11-12 00:00:00
# rn                       NaN
# Name: 145, dtype: object
# -----------------------------------------


# -----------------------------------------
# Question 2.d
# How many hourly total rainfall values in the dataset exceed 50mm?
# -----------------------------------------
wd[wd["rn"]>50]
wd.rn[wd["rn"]>50].count()

# There are 6 rows which exceed 50mm.
# -----------------------------------------


# -----------------------------------------
# Question 2.e
# Find the daily total rainfall at station number 304 on 07/01/2009
# -----------------------------------------
wd.set_index(["wsid","year","month","day"],inplace=True)
wd.loc[304,2009,7,1][["hr","rn"]]
wd.reset_index(inplace=True)

# For year 2009 month 07 day 01, data is missing. 
#  We can not say it is zero since data is NaN (i.e. Unknown)
# -----------------------------------------


# -----------------------------------------
# Question 2.f
# Sort the dataset by hourly maximum temperature in descending order.
# -----------------------------------------
wd.sort_values(by="mxt",ascending=False)

# -----------------------------------------


# -----------------------------------------
# Question 2.g
# Sort the dataset by hourly maximum temperature in descending order, then by
#   minimum temperature in ascending order.
# -----------------------------------------
# Just shown first 5 rows and last 5 rows.
wd.sort_values(by=["mxt","mnt"],ascending=[False, True])

# -----------------------------------------


# -----------------------------------------
# Question 2.h
# Find all rows in the dataset in which hourly rainfall exceeded 60mm or the hourly
#  maximum temperature was at least 39 °C.
# -----------------------------------------
wd[(wd["rn"]>60) | (wd["mxt"]>=39)]

# Just found 9 rows with conditions stated in Q 2.h
# -----------------------------------------


# -----------------------------------------
# Question 2.i
# Output all rows that do not have any missing values.
# -----------------------------------------
# Drop rows without replacement in order to not affect original dataset 
#  and see information. 
wd.dropna(axis='rows', how='any')

# We found 34916 rows that have all values != nan
# -----------------------------------------


# -----------------------------------------
# Question 2.j
# Find the mean of the non-missing hourly minimum temperatures at station number
#  178 in December 2007.
# -----------------------------------------
wd.set_index(["wsid","year","month"],inplace=True)
wd.loc[178,2007,12][["mnt"]].dropna(axis='rows').mean() # or
wd.loc[178,2007,12][["mnt"]].mean() # See NOTE below
wd.reset_index(inplace=True)

# NOTE:
# Function .dropna() is not needed since function .mean() skip NaN values.
#   Parameter skipna default True.
#   See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mean.html
# Mean of the hourly minimum temperatures at 178 station in December 2007 is 14.689637
# -----------------------------------------


# -----------------------------------------
# Question 2.k
# Output the values of hourly maximum temperature when the mean hourly humidity
#  is 100%.
# -----------------------------------------
wd.loc[wd["hmdy"]==100]["mxt"]

# We found 12306 mxt values with hourly humidity is 100%
# -----------------------------------------


# -----------------------------------------
# Question 2.l
# Which station number had the highest number of mean hourly humidity values
#  equal to 100%?
# -----------------------------------------
wd2 = wd.loc[wd["hmdy"]==100][["wsid","hmdy"]].groupby("wsid").count()

# I can tell the max value of each station by printing wd2, but let's go further:
wd2[wd2["hmdy"]==wd2.hmdy.max()]

del wd2 # Let's free some space

# The station 304 has the highest number of mean hourly humidity values equal to 100%.
# -----------------------------------------


del wd, wd_d # Let's free some space
