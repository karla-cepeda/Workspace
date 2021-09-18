# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Fri Nov 13 07:48:22 2020

READ ME FIRST:
    Hi Siohbon,
    Please find below answers for Question 1, CA 2.
    
    NOTES:
        Please, change dir if you want to run code.
        I added as much comments as possible, please read carefully.
    
"""

import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.cbook import boxplot_stats  
from scipy.stats import wilcoxon, ranksums, ttest_ind

os.chdir('E:/Karla/IRELAND v2/DKIT/1st Semester/Statistic/CA/Assessement 2')

"""
# -------------------------------------------------------------------------------------------
 
Section A: Linear Regression: Cats’ Heart Weight
 	
 Load in the data “Cat_Hwt.csv” from the dataset available in moodle. 
  Data was collected on male and female adult cats used for experiments:
   Sex: "F" for female and "M" for male.
   Bwt: body weight in kg.
   Hwt: heart weight in g.
   Height: Height in cm
   Age: Age in years. 

# --------------------------------------------------------------------------------------------

"""

cats = pd.read_csv('Dataset/Cat_Hwt.csv') # Reading csv file


"""
# ---------------------------------------------------------------------------------------------
# (a) Describe the dataset, dimensions and what type of variables there are.
#
"""
cats.info()

# Describe dataset:
#   The dataset is a sample of adult cats for experiments.
#   Looking at the dataset, it is made up of 5 columns and 144 rows.
#   The function .info() says the data in the first column is an object type 
#    (probably string, since Sex is commonly given by 'F' and 'M', but we need to check).

# Let's just make sure that we have been given just 'F' and 'M' in Sex variable.
cats.Sex.unique() 
# array(['F', 'M'], dtype=object), Yes!

#   This data is regarding adult cats, and the variables taken to be analyzed were:
#    - sex: string, one character. ('F','M') where 'F' stands for 'female' and 'M' for male.
#    - body weight: decimal in kg.
#    - heart weight: decimal in g.
#    - age: decimal, decimal in years including fraction of year.
#   Also, it is stated that all rows and columns have non-null values, i.e. we have no missing values.

# Dimensions and type of variables:
#   We have five variables (i.e. cat's characteristics):
#       - Sex                          => Categorical Nominal, (Dtype object) 
#       - Bwt (i.e. body weight in kg) => Numerical Continuous (Dtype float64)
#       - Hwt (i.e. heart weight in g) => Numerical Continuous (Dtype float64)
#       - Height                       => Numerical Continuous (Dtype float64)
#       - Age                          => Numerical Continuous (Dtype float64)
#   Additionaly, we have 144 observations (i.e. 144 adult cats).
#   In total, we have 5*144 = 720 data.


"""
# -------------------------------------------------------------------------------------------------------------
# (b) Is there any missing data or outliers? If so, how do you recommend proceeding?
#
"""

# The funtion above .info() indicates that all the 144 observations in each variable are non-null, 
#  in other words, there are no missing values. Let's use another function just to verify:
cats.isna().sum()

# Now, let's check for outliers by getting information from the boxplot in the continuous variables:
boxplot_stats(cats.Bwt)[0]['fliers'] # No outliers
boxplot_stats(cats.Hwt)[0]['fliers'] # Two outliers, 17.2 and 20.5
boxplot_stats(cats.Height)[0]['fliers'] # No outliers
boxplot_stats(cats.Age)[0]['fliers'] #No outliers

# Lets check these outliers more careful from Hwt
hwt_outliers_v = [stat for stat in boxplot_stats(cats.Hwt)[0]['fliers']]
cats[cats['Hwt'].isin(hwt_outliers_v)]


# Not sure if we should drop observations with outliers.
# It might be that those cats are overweight, but we are not sure if hwt is related to bwt.
# Let's create a new column to see the ratio of heart weight and body weight, it might give a clue if this data was taken wrongly.
cats["Bwt_g"] = cats.Bwt * 1000        # create new column to store bw in g
cats["HBwt_r"] = cats.Hwt / cats.Bwt_g # create new column ratio hwt:bwt_g
cats

# Now let's check again outliers from the ratio, since now we are considering the body weight
boxplot_stats(cats.hbwt_r)[0]['fliers'] # No outliers

# And let's chekc out the boxplot just to see the five-number summary:
sns.boxplot(x="hbwt_r", data=cats)
plt.xlabel("Heart Weight:Body Weight (g)")

# The boxplot looks nice and symmetric. Now that we are taking in consideretion the body 
#  weight, I am happy and I can conclude that we should leave the observations with outliers in 
#  the hwt variable.

del hwt_outliers_v


"""
# ---------------------------------------------------------------------------------------------------------
# (c)	Create univariate plots and interpret the plots.
#
"""

#   First of all, let's define the type of graph for each variables:
#       - Sex    => Barplot, Table or Pie chart.
#       - Bwt    => Histogram or Boxplot.
#       - Hwt    => Histogram or Boxplot.
#       - Height => Histogram or Boxplot.
#       - Age    => Histogram or Boxplot.

# For Sex:
sns.countplot(cats.Sex) 
plt.title("Sex of adult cats")
plt.ylabel("Cats")
# The graph shows that there are more males than females in the sample of adult cats.

# For Bwt:
# Histagram
sns.distplot(cats["Bwt"]) 
plt.title("Body weight of adult cats")
plt.xlabel("Body weight (kg)")
# Boxplot
sns.boxplot(cats["Bwt"]) 
plt.title("Body weight of adult cats")
plt.xlabel("Body weight (kg)")
# There is a slight concentration of data in Q3 compared to Q2.
# 50% of data is balanced to the right.
# Therefore, positive skewness is shown in the histogram. Skewed-right distribution.
# No outliers

# For Hwt
# Histagram
sns.distplot(cats["Hwt"]) 
plt.title("Heart weight of adult cats")
plt.xlabel("Heart weight (g)")
# Boxplot
sns.boxplot(cats["Hwt"])
plt.title("Heart weight of adult cats")
plt.xlabel("Heart weight (g)")
# There is a strong concentration of data in Q2 compared to Q3.
# 50% of data is slightly balanced to the right.
# Therefore, positive right skewness is shown.
# There are two outliers. 

# For Height
# Histagram
sns.distplot(cats["Height"])
plt.title("Height of adult cats")
plt.xlabel("Height (cm)")
# Boxplot
sns.boxplot(cats["Height"])
plt.title("Height of adult cats")
plt.xlabel("Height (cm)")
# Q2 and Q3 data is symmetric. Symmetric box.
# Whiskers have same length.
# Therefore, plot shown a bell shape. No skewed data.
# No outliers.

# For Age
# Histagram
sns.distplot(cats["Age"])
plt.title("Age of adult cats")
plt.xlabel("Age (years)")
# Boxplot
sns.boxplot(cats["Age"])
plt.title("Age of adult cats")
plt.xlabel("Age (years)")
# Q2 has slighly more data concentrated comparing to Q3.
# Whiskers have slighly same length.
# Data is ok. Therefore, plot shown a symmetric shape.
# No outliers.


"""
# --------------------------------------------------------------------------------------------------------
# (d)	Based on the plots, examine appropriate summary statistics and interpret 
#
""""

# For Sex:   
cats['Sex'].value_counts()
# There are 47 female cats and 97 male cats, which summing up give 144 observations.

# For Bwt:    
sns.boxplot(x="Bwt", data=cats)
plt.title("Body weight of adult cats")
plt.xlabel("Body eight (kg)")
cats.Bwt.describe()
# The lowest body weight among the sample of adult cats is 2.0 kg
# The highest body weight among the sample of adult cats is 3.9 kg
# The average body weight in the sample is 2.72 kg,
# The median body weight is 2.70 kg 
# NOTE: it is interesting that mean and median has almost same value despite skewness.

# For Hwt:
sns.boxplot(x="Hwt", data=cats)
plt.title("Heart weight of adult cats")
plt.xlabel("Heart eight (g)")
cats.Hwt.describe()
# The lowest heart weight in the sample is 6.3 g
# The highest heart weight in the sample is 20.5 g
# The average heart weight among adult cats in sample is 10.6 g,
# The median heart weight in the sample is 10.1 g 

# For Height:
sns.distplot(cats["Height"]) 
plt.title("Height of adult cats")
plt.xlabel("Height (cm)")
cats.Height.describe()
# The largest cat is 33.9 cm
# The shortest cat is 14.3 cm
# The average height in the sample is 24.3 cm,
# The median height of adult cats is 24.3 cm

# For Age:
sns.distplot(cats["Age"]) 
plt.title("Age of adult cats")
plt.xlabel("Age (years)")
cats.Age.describe()
# The oldest cat is 19.5 years
# The youngest cat is 5.3 years
# The average age in the sample is 12.2 years
# The median age of adult cats is 12.1 years


"""
# -------------------------------------------------------------------------------------------------------
# (e) Create bivariate plots to explore the relationship between all 
#      pairs of variables. Interpret each plot
#
"""

# Let's create all pairs of variables:
# sex, Bwt    => boxplot
# sex, Hwt    => boxplot
# sex, Height => boxplot
# sex, Age    => boxplot
# No more combinations since Bwt, Hwt, Height and Age are numerical continuous variables.

# Next, for all numerical continuous variables, taking that x=independent, y=dependent for scatterbox:
# x=Bwt,    y=Hwt    => scatterbox
# x=Height, y=Bwt    => scatterbox
# x=Height, y=Hwt    => scatterbox
# x=Age,    y=Bwt    => scatterbox
# x=Age,    y=Hwt    => scatterbox
# x=Age,    y=Height => scatterbox

# With Sex:
sns.boxplot(x='Sex', y='Bwt', data=cats)
plt.title("Body Weight of adult cats")
plt.ylabel("Body Weight (kg)")
# There is a difference between medians.
# The median is noticeble higher for male cats.
# IQR from female cats do not overlaps.
# Spreadness is not the same in both groups.
# For group F: skewed shape.
# For group M: symmetric shape.
# Both groups have one outlier each.

sns.boxplot(x='Sex', y='Hwt', data=cats)
plt.title("Heart Weight of adult cats")
plt.ylabel("Heart Weight (g)")
# There is a difference between medians.
# The median is smaller among female cats.
# IQR from female cats overlaps just half.
# Spreadness is not the same in both groups.
# For group F: symmetric shape.
# For group M: symmetric shape.
# Both groups have one outlier each.

sns.boxplot(x='Sex', y='Height', data=cats)
plt.title("Height of adult cats")
plt.ylabel("Height (cm)")
# There is a diference between medians, and IQR almost overlaps.
# The median is slightly higher in male cats.
# IQR from male cats almost overlaps.
# Spread is the same for both groups.
# For group F: roughly symmetric shape.
# For group M: roughly symmetric shape.
# No outliers.

sns.boxplot(x='Sex', y='Age', data=cats)
plt.title("Age of adult cats")
plt.ylabel("Age (years)")
# There is a slight difference between medians, but male cats' IQR overlaps
# The median is slighly higher among male cats.
# IQR from male cats overlaps the IQR from female cats group.
# Spread is the same for both groups.
# For group F: roughly symmetric shape.
# For group M: symmetric shape.
# No outliers.

# For numerical continuous variables:
sns.regplot(x='Bwt', y='Hwt', data=cats, fit_reg=False) 
plt.title("Body weight VS Heart weight of adult cats")
plt.xlabel("Body weight (kg)")
plt.ylabel("Heart weight (g)")
# There is a positive relationship between body weight and heart weight

sns.regplot(x='Height', y='Bwt', data=cats, fit_reg=False) 
plt.title("Height VS Body weight of adult cats")
plt.xlabel("Height (cm)")
plt.ylabel("Body weight (kg)")
# There is a no relationship between height and body weight among adult cats
# There is a random scatter

sns.regplot(x='Height', y='Hwt', data=cats, fit_reg=False) 
plt.title("Height VS Heart weight of adult cats")
plt.xlabel("Height (cm)")
plt.ylabel("Heart weight (g)")
# There is a weak positive lineal relationship between height and heart weight

sns.regplot(x='Age', y='Bwt', data=cats, fit_reg=False) 
plt.title("Age VS Body weight of adult cats")
plt.xlabel("Age (years)")
plt.ylabel("Body weight (kg)")
# There is no relationship between age and body weight among adult cats
# There is a random scatter

sns.regplot(x='Age', y='Hwt', data=cats, fit_reg=False) 
plt.title("Age VS Heart weight of adult cats")
plt.xlabel("Age (years)")
plt.ylabel("Heart weight (g)")
# There is a weak positive lineal relationship between age and body weight.

sns.regplot(x='Age', y='Height', data=cats, fit_reg=False) 
plt.title("Age VS Height of adult cats")
plt.xlabel("Age (years)")
plt.ylabel("Height (cm)")
# There is no relationship between age and height among cats.
# There is a random scatter

"""
# -----------------------------------------------------------------------------------------------------------
# (f) Using the bivariate plots that appear to have a difference between 
#     two groups only, determine if there is a statistical difference 
#     between the groups using hypothesis testing. Make sure in your answer 
#     to explain the hypotheses, any assumptions needed and if they are met, 
#     results and interpretation of all the results. Conclude your findings. 
# 
"""

# For all the following tests, significant level value will be taken as 5%.

# Body weight among Sex
# Previously, in the boxplot there was shown a remarkable difference between medians.
# Assumptions for two-samples t-test:
# - Continuous data. Yes.
# - Samples must be independent and random. Yes.
# - Not be skewed (i.e. it has normally distirbuted / bell shaped). No, sample from females is strong skewed to the right.
# - Standard deviation must be the same (i.e. spread should be roughly the same). No.
# T-test cannot be performed since one violation in assumptions enlisted above. Therefore, a non-parametric 
#  test would be a better option. Boxplots show that 50% of the data is slightly balanced to the right. 
#  In this case, a Wilcoxon-Mann-Whitney test is enough to perform a an hypothesis test.
# Hypothesis:
# H0: median_female_bw  = median_male_bw (i.e. no relationship)
# H1: median_female_bw != median_male_bw (i.e. relationship)
m_cats_b=cats[cats["Sex"] == 'M']['Bwt']
f_cats_b=cats[cats["Sex"] == 'F']['Bwt']

sns.boxplot(m_cats_b, color="skyblue")
plt.title("Body weight of male adult cats")
plt.xlabel("Body weight (kg)")

sns.boxplot(f_cats_b,color="red")
plt.title("Body weight of female adult cats")
plt.xlabel("Body weight (kg)")

sns.distplot(m_cats_b, color="skyblue" ,label="Male adult cats")
sns.distplot(f_cats_b, color="red", label="Female adult cats")
plt.title("Body weight of male and female adult cats")
plt.xlabel("Body weight (kg)")
plt.legend()
ranksums(m_cats_b,f_cats_b)
# P-Value=1.64e-10 < 0.05. Therefore, we reject null hypothesis, there is a difference between
#  meadians. In other words, there is a relationship between sex and body weight. 
#  There is not enough evidence to suggest that body weight is not affected by sex. 


# For Sex - Heart weight:
# Previously, in the boxplot there was shown a slight difference between medians.
# Assumptions for two-samples t-test:
# - Continuous data. Yes.
# - Samples must be independent and random. Yes.
# - Not be skewed (i.e. it has normally distirbuted / bell shaped). Yes, roughly symmetric shape.
# - Standard deviation must be the same (i.e. spread should be roughly the same). No.
# T-test cannot be performed since one violation in assumptions enlisted above. 
#  Therefore, a non-parametric test would be the best option.
# Hypothesis:
# H0: median_female_hw  = median_male_hw (i.e. no relationship)
# H1: median_female_hw != median_male_hw (i.e. relationship)
m_cats_h=cats[cats["Sex"] == 'M']['Hwt']
f_cats_h=cats[cats["Sex"] == 'F']['Hwt']

sns.boxplot(m_cats_h, color="skyblue")
plt.title("Heart weight of male adult cats")
plt.xlabel("Heart weight (g)")

sns.boxplot(f_cats_h,color="red")
plt.title("Heart weight of female adult cats")
plt.xlabel("Heart weight (g)")

sns.distplot(m_cats_h, color="skyblue" ,label="Male adult cats")
sns.distplot(f_cats_h, color="red", label="Female adult cats")
plt.title("Heart weight of male and female adult cats")
plt.xlabel("Heart weight (g)")
plt.legend()
ranksums(m_cats_h, f_cats_h)
# P-Value=4.86X10^-7 < 0.05. Therefore, we reject null hypothesis, there is a difference between
#  meadians. In other words, there is a relationship between sex and heart weight. 
#  There is not enough evidence to suggest that heart weight is not affected by sex. 


# For Height - Sex:
# Previously, in the boxplot there was shown a slight difference between medians.
# Assumptions for two-samples ttest:
# - Samples must be independent and random. Yes.
# - Not be skewed (i.e. it has normally distirbuted / bell shaped). Yes.
# - Standard deviation must be the same (i.e. spread should be roughly the same). Yes.
# Hypothesis:
# H0: mean_female_Height  = mean_male_Height (i.e. no relationship)
# H1: mean_female_Height != mean_male_Height (i.e. relationship)
m_cats_he=cats[cats["Sex"] == 'M']['Height']
f_cats_he=cats[cats["Sex"] == 'F']['Height']

sns.boxplot(m_cats_h, color="skyblue")
plt.title("Height of male adult cats")
plt.xlabel("Height (cm)")

sns.boxplot(f_cats_h,color="red")
plt.title("Height of female adult cats")
plt.xlabel("Height (cm")

sns.distplot(m_cats_he, color="skyblue" ,label="Male adult cats")
sns.distplot(f_cats_he, color="red", label="Female audlt cats")
plt.title("Height of male and female adult cats")
plt.xlabel("Height (cm)")
plt.legend()

ttest_ind(m_cats_he, f_cats_he, equal_var=True)
# P-Value=0.16 > 0.05. Therefore, we failed to reject null hypothesis. There is not enough evidence
#  to suggest that height is affected by sex. In other words, there is no relationship between sex and height.


# For Age among Sex:
# Previously, in the boxplot there was shown a slight difference between medians.
# Assumptions for two-samples ttest:
# - Samples must be independent and random. Yes.
# - Not be skewed (i.e. it has normally distirbuted / bell shaped). Yes, roughly symmetric.
# - Standard deviation must be the same (i.e. spread should be roughly the same). Yes.
# Hypothesis:
# H0: mean_female_Age  = mean_male_Age (i.e. no relationship)
# H1: mean_female_Age != mean_male_Age (i.e. relationship)
m_cats_a=cats[cats["Sex"] == 'M']['Age']
f_cats_a=cats[cats["Sex"] == 'F']['Age']

sns.boxplot(m_cats_a,color="skyblue")
plt.title("Age of male adult cats")
plt.xlabel("Age (years)")

sns.boxplot(f_cats_a,color="red")
plt.title("Age of female adult cats")
plt.xlabel("Age (years)")

sns.distplot(m_cats_a, color="skyblue" ,label="Male adult cats")
sns.distplot(f_cats_a, color="red", label="Female adult cats")
plt.title("Age of male and female adult cats")
plt.xlabel("Age (years)")
plt.legend()

ttest_ind(m_cats_a, f_cats_a, equal_var=True)
# P-Value=0.83 > 0.05. Therefore, we failed to reject null hypothesis. There is not enough evidence
#  to suggest that age is affected by sex. In other words, there is no relationship between sex and age.

