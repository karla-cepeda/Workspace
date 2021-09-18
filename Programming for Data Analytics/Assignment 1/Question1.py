# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Sat Nov  7 08:10:44 2020

READ ME FIRST:
    Hi Jack,
    Please find below answers for Question 1, CA 1.
    
    NOTES:
        Please, change dir if you want to run code.
        I added as much comments as possible, please read carefully.
    
"""

import pandas as pd
import numpy as np
import os


# -----------------------------------------
# Question 1.a
#  There is a file containing weather data for three Brazilian stations in the
#   brazil_weather csv file on Moodle. 
#   Read it in to Python as a Pandas DataFrame.
# ------------------------------------------
# Please, change directory file according to location of CA1 folder in your computer. Thank you.
os.chdir('E:/Karla/IRELAND v2/DKIT/1st Semester/Programming with Python/Continuous Assessments/Assessement 1')

wd = pd.read_csv('Dataset/brazil_weather.csv') # Reading csv file
wd.head() # Lets display the first 10 rows.
# ------------------------------------------


# -----------------------------------------
# Question 1.b
#  List all problems you can find with the dataset that could be improved before
#   analysing it.
# ------------------------------------------
# Lets see the shape and info
wd.info() 
wd.shape

# So far:
#   The dataset contains 245204 rows and 11 columns.
#   It seems name of columns are awkward, we need to inspect this more careful
#   All columns have missing values.
#   Data from columns do not have a type defined.

# Lets check rows of dataset
wd.head()

# Information is still akward. Lets look at the first 15 rows.
wd.head(15)

# Now I can see there is consistence information below index 9. We are making progress. 
#  Lets see the rows from index 9 to index 20
wd.iloc[9:21]

# There it is! it seems our dataset starts in index 9.
#  Lets have a glance at the indexes above index 9
wd.iloc[:9]

# Reading through this information, we can tell that index 8 is the header and 
#  information from index 0 to index 7 is the description of each column header.

# Lets make sure column 0 from index 0 to index 7 is the only column with data
wd.iloc[0:7,:].notnull().sum()

# Now, lets look quick at index 8, looking for missing values
wd.iloc[8].isnull().sum() 

# Next, lets see data after index 9. 
wd_copy = wd.iloc[9:].copy()

# Lets look at values.
wd_copy.iloc[:,0].unique() # Integer. OK
wd_copy.iloc[:,1].unique() # This is dates. OK
wd_copy.iloc[:,2].unique() # Seems like years, no award values. OK
wd_copy.iloc[:,3].unique() # More integers. OK
wd_copy.iloc[:,4].unique() # More integers. OK
wd_copy.iloc[:,5].unique() # Still integers. OK
wd_copy.iloc[:,6].unique() # Not all values are numbers, there is a '--' value. 
wd_copy.iloc[:,7].unique() # Not all values are numbers, there is a '--' value. 
wd_copy.iloc[:,8].unique() # Some nan values
wd_copy.iloc[:,9].unique() # Not all values are numbers, there is a '--' value. 
wd_copy.iloc[:,10].unique() # Some nan values

# Now, lets just check how many nulls do we have in our dataset
wd_copy.isnull().sum()

# We have way too many nulls in column unnamed 6 and 10, and some in column 7, 8 and 9.
# Now, lets look for some duplicated rows, why not?
wd_copy[wd_copy.duplicated()]

# Let's free some space
del wd
del wd_copy

# There are 11 duplicated rows. 
# Pretty cool. Lets draw some conclusions:
#   - Header of dataset starts at index 8
#   - Dataset information starts at index 9
#   - Since wd.info() display missing values but dataset isn't well loaded, we need to check missing values again after reloading dataset.
#   - There are some '--' values which we can conclude they are unknown values. Need to change to NaN value.
#   - There are 11 row duplicated elements.

# Extra Part!!, since I did a course in Datacamp regarding messy datasets:
# Looking at the structure of the data, lets check the following:
#   Common problems with messy datasets:
#    - Column headers are values, not variable names.
#       In this dataset, it seems this is not a problem
#   - Multiple variables are stored in one column.
#       All data looks good.
#   - Variables are stored in both rows and columns.
#       Not a problem for now.
#   - Multiple types of observational units are stored in the same table.
#       All data looks good.
#   - A single observational unit is stored in multiple tables
#       We just have one dataset. No problem.
#  Reference: https://www.jstatsoft.org/index.php/jss/article/view/v059i10/v59i10.pdf
# -----------------------------------------


# -----------------------------------------
# Question 1.c
# Use Python to make the dataset as tidy as possible for analysis 
#  ie. solve the problems you have identified. Make sure the dataset 
#  is being updated with the changes you make.
# ------------------------------------------

# Read again csv but indicate header is row line 9 in csv
#  and lets replace values '--' to np.nan
wd = pd.read_csv('Dataset/brazil_weather.csv', header=9, na_values=['--'])
wd.name = "WeatherFromBrazil"

# We detected 11 rows that are duplicated. Let's get rid out of them.
#   Since minutes and seconds are not specified in the dataset, we can not tell if this duplicated 
#     data comes from minutes or seconds, so we will treat it as duplicate values.
duplicated = wd[wd.duplicated()].index
wd.drop(axis=0,labels=duplicated,inplace=True)
del duplicated # Let's free some space

# Lets see the info again
wd.info()
wd.shape 
wd.head()

# Lets try to get rid of the missing values, but for question 2 I am going to use the dataset 
#  with NaN values since some questions asked to work with NaN values.

#  For the missing values, I am thinking of filling them with the .mean() value for each column, but
#   lets check if the overall mean from each column would be affected.
#  First lets check again which columns have null values.
wd.isnull().sum()

# Now that we now the columns with null values, lets have a look at stats data from these columns.
wd.loc[:,"rn":].describe()

# Ok, now, apply a mean to all this columns to see how this could affect the original mean.
# But lets make a copy
wd_copy = wd.copy()
wd_copy['rn'].fillna(wd_copy['rn'].mean(),inplace=True)
wd_copy['mxt'].fillna(wd_copy['mxt'].mean(), inplace=True)
wd_copy['mnt'].fillna(wd_copy['mnt'].mean(),inplace=True)
wd_copy['hmdy'].fillna(wd_copy['hmdy'].mean(),inplace=True)

# And lets compare both datasets
wd.loc[:,"rn":].describe()
wd_copy.loc[:,"rn":].describe()

del wd_copy # Let's free some space

# It does not seem like stats data were affected by taking the mean to fill nan values,
# If I have to fill na values with .mean(), code would be as follows:
# wd['rn'].fillna(wd['rn'].mean(),inplace=True)
# wd['mxt'].fillna(wd['mxt'].mean(), inplace=True)
# wd['mnt'].fillna(wd['mnt'].mean(),inplace=True)
# wd['hmdy'].fillna(wd['hmdy'].mean(),inplace=True)
# -----------------------------------------


# -----------------------------------------
# Question 1.d
# Remove the mean hourly wind speed column. 
#  It is not needed for analysis.
# ------------------------------------------
# Lets use .drop function to remove column
wd.drop(columns=['wdsp'],inplace=True) 
# ------------------------------------------


# -----------------------------------------
# Question 1.e
# Save the cleaned dataset as a new csv file called 
#  brazil_weather_edit.csv for later analysis.
# ------------------------------------------
# NOTE: I executed the code in order to get the dataset with missing values (i.e. NaN)
wd.to_csv("Dataset/brazil_weather_tidy_version.csv", na_rep='NA', index=False)

del wd # Let's free some space

#-------------------------------------------