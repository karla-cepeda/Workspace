# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Statistics

Created on Fri Dic 11 07:48:22 2020

READ ME FIRST:
    Hi Siohbon,
    Please find below answers for CA 3.
    
    NOTES:
        Please, change dir if you want to run code.
        I added as much comments as possible, please read carefully.
    
"""

import pandas as pd
import numpy as np
import math
import os

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

import statsmodels.api as sm
from statsmodels.formula.api import ols
from matplotlib.cbook import boxplot_stats  
from scipy.stats import pearsonr, spearmanr, stats
from statsmodels.formula.api import ols
from statsmodels.graphics.factorplots import interaction_plot


os.chdir(r'E:\Karla\IRELAND v2\DKIT\1st Semester\Statistic\CA\Assessement 3')
cars = pd.read_csv('mtcars.csv')

# -------------------------------------------------------------------------------------------------

"""
a)	Briefly describe the dataset, dimensions and what type of variables there are.
    
"""

cars.info()
cars.head()

cars.rename(columns={'Unnamed: 0':'car'}, inplace=True) # Rename first column
cars['hp'] = cars['hp'].astype('float64')


"""
    ## Description:
     Dataset of 32 cars from 1975. This dataset is compound by performance and features.
     There dataset if compund by 12 columns and 32 rows.
     Columns are:
        - mpg:  Miles per gallon, how far a car is able to travel for every gallon. units: mpg
        - cyl:  Number of cylinders, chamber where the explotion occurs (number of pistons). unit: item. 
        - disp: Engine displacement, volumn of all cylinders. units: cubic inches 
        - hp:   Gross horsepower, amount of power an engine develops, units: horsepower
        - drat: Rear axle ratio
        - wt:   Weight (denominator of 1000).units: lbs
        - qsec: 1/4 mile time,
        - vs:   Engine (0 = V-shaped, 1 = straight)
        - am:   Transmission (0 = automatic, 1 = manual)
        - gear:	Number of forward gears, transmit power to car. 
        - carb:	Number of carburetors, place where air and fuel is mxixed for internal combustion.
    Rows and columns have non-null values, i.e. we have no missing values.
    
    ## Dimension and types of variables:
     There are 32 observations and 12 variables:
        - car   =>  categorical nominal
        - mpg   =>  continuous numerical
        - cyl   =>  discret numerical
        - disp =>   continous numerical
        - hp  =>    continuous numerical
        - drat =>   continous numerical
        - wt   =>   contonous numerical
        - qsec =>   continous numerical
        - vs => categorical nominal
        - am: => categorical nomincal
        - gear => discrete numerical
        - carb => discrete numerical   
    

"""

#----------------------------------------------------------------------------------------------------------

"""
b)	Investigate if any of the continuous numerical variables have a linear relationship by 
    producing scatterplots, interpret these plots.

"""

def myscatterplots(df):
    
    """
    Definition:
        This method provides three plots. Once scatter plot and two histograms and
        just takes continous variables. These need to be type "float" to be concider as
        continous varaible for this method.
        
    Parameters:
        df: dataset with at least two continous varaibles
        
    Return:
        plots and summary
    
    """
    
    numc = df.dtypes[df.dtypes == 'float64'].index
    size = len(numc)
    
    if size <= 1:
        print('There is no continous varibles in dataset.')
        return
    
    
    for i in np.arange(0,size):
        for j in np.arange(i, size):
            if i == j:
                continue
            
            fig, ax = plt.subplots(1,3,figsize=(10,3))
            sns.scatterplot(x=numc[i], y=numc[j], data=df, ax=ax[0])
            ax[0].set_xlabel = numc[i]
            ax[0].set_ylabel = numc[j]
                        
            sns.distplot(df[numc[i]], color='blue', label=numc[i], ax=ax[1])
            ax[1].set_xlabel = numc[i]
            
            sns.distplot(df[numc[j]], color='red', label=numc[j], ax=ax[2])
            ax[2].set_ylabel = numc[j]
            
            plt.tight_layout(pad=2)
            plt.suptitle(numc[i].upper() + ' and ' + numc[j].upper())
            plt.show()
            
            print('Statistic Summary: ', numc[i], ' and ', numc[j])
            print('Pearson R: ', pearsonr(df[numc[i]], df[numc[j]]))
            print('Spearman S: ', spearmanr(df[numc[i]], df[numc[j]]))
            print('Mean', numc[i]+': ', df[numc[i]].mean())
            print('Median', numc[i]+': ', df[numc[i]].median())
            print('Mean', numc[j]+': ', df[numc[j]].mean())
            print('Median', numc[j]+': ', df[numc[j]].median())
           
            input("press any key to continue.... ")
    
    
myscatterplots(cars)


"""

INTERPRETATIONS:

mpg and disp
mpg has is symmetric.
disp varaible is slightly skewed to the right.
There is non-linear relationship between mpg and disp. It seems to exponential relationship since
the shape looks like a curve.

mpg and hp
mpg has is symmetric.
hp is slightly skewed to the right.
There is a non-linear relationship between mpg and disp. It seems to be an exponential relationship since the shape looks like a curve.

mpg and drat
mpg has is symmetric.
drat is symmetric.
There is a positive linear relationship between mpg and drat (pearsonr: 0.6811)

mpg and drat
mpg has is symmetric.
drat is symmetric.
There is a negative linear relationship between mpg and wt (pearsonr: -0.8676)

mpg and qsec
mpg has is symmetric.
qsec is symmetric.
There is a weak positive linear relationship between mpg and qsec (pearsonr: 0.4186)

disp and hp
disp is slightly skewed to the right.
hp is skewed to the right.
There is a positive linear relationship between disp and hp (spearman: 0.8510)

disp and drat
disp is slightly skewed to the right.
drat is symmetric
There is no relationship between disp and drat, it seems to have two clusters.

disp and wt
disp is slightly skewed to the right.
wt is symmetric
There is a strong positive relationship between disp and wt (spearman: 0.8977)

disp and qsec
disp is slightly skewed to the right.
qsec is symmetric
There is a weak negative relationship between disp and qsec (spearman: -0.4597)

hp and drat
hp is skewed to the right.
drat is symmetric
There is not clear a relationship between hp and drat. It seems to be a quadratic relationship, but stills not clear for me.

hp and wt
hp is skewed to the right.
wt is symmetric
There is a positive linear relationship between hp and wt. (spearman: 0.7746)

hp and qsec
hp is skewed to the right.
qsec is symmetric
There is a negative linear relationship between hp and wt. (spearman: -0.6666)

drat and wt
drat is symmetric.
wt is symmetric.
There is a negative linear relationship between drat and wt. (pearson r: -0.7124)

drat and qsec
drat is symmetric.
qsec is symmetric.
There is no relationship between drat and qsec. 

wt and qsec
wt is symmetric.
qsec is symmetric.
There is no relationship between drat and qsec. 

"""

# -------------------------------------------------------------------------------------------------

"""
c)	What is the response variable and why? What is the research question of interest in this dataset?
    
    RESPONSE VARAIBLE:
    According to the scatterplots, first I would pick the varaibles that have more linear relationships. 
    I have three candidates: miles per gallon and weight. Both varaibles have three strong relationships and
    one week relationship. However, weight has more outliers, and it would be a concern for future analysis,
    so, I would take mpg as my response variable.
    
    RESERACH QUESTION:
    In this case, we want to investigate what are the other factors that impact the value of mpg.
    
"""

sns.boxplot(cars['mpg'])
sns.boxplot(cars['wt'])

"""
d)	Investigate if any of the categorical /discrete variables seem to have a 
    relationship with the response variable (selected in part b)  using boxplots. 
    Interpret these plots. 

"""
y_='mpg'

def boxplot_summary(df,x_,y_):    
    sns.boxplot(x=x_, y=y_, data=df)
    plt.title('1974 Motor Trend US magazine. ' + x_.upper()  + " and " + y_.upper())
    
    """
    legend_elements = [Patch(facecolor='blue', label='Automatic'),
                       Patch(facecolor='orange', label='Manual')]

    
    plt.legend(handles=legend_elements)
    """
    
    plt.show()
    outcome = cars.groupby(x_)[y_].describe()[['mean','50%','std']]
    print("====== results ======")
    print(outcome)

# ---------------------------- Number of cylinders
boxplot_summary(cars,'cyl', y_)
# there is a relationship.

# --------------------- Number of Gear
boxplot_summary(cars,'gear', y_)
# standard has a higher mean. There is a relationship.
# there is a relationship

# ---------------------------- engine
boxplot_summary(cars,'vs', y_)
# standard has a higher mean. There is a relationship.
# there is a relationship

# ------------------------------- number carburators
boxplot_summary(cars,'carb', y_)
# there is a relationship.

# ---------------------- Transmition type
boxplot_summary(cars,'am', y_)
# there is a relationship
# standard has a higher mean. There is a relationship.

"""

e)	Using part d), choose one categorical/discrete variable with at 
    least 3 categories to test to see if there is any difference 
    between the means of the response variable (selected in part c) 
    using an one-way ANOVA test. Explain your choice and hypothesis, 
    check the assumptions and interpret the results if appropriate. 
    Conclude your findings.


"""

# ------------------------------------------------------------------ gear

model_oneway = ols('mpg ~ gear', data=cars).fit()

model_oneway_fitted_vals = model_oneway.fittedvalues
model_oneway_residuals = model_oneway.resid
model_oneway_norm_residuals = model_oneway.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_oneway_fitted_vals, 
            y=model_oneway_residuals,
            ci=False, lowess=True,
            line_kws={'color':'red', 'lw':1 ,'alpha':0.5})
ax.set_xlim(15,25)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()
# spread is not that terrible, we can continue.

stats.probplot(model_oneway_norm_residuals,plot=sns.mpl.pyplot)
# not a strong devation from normality. 
# normality is ok, we can continoue.

model_oneway.summary()
sm.stats.anova_lm(model_oneway, typ=1)

"""
H0: the mean from groups are all the same
H1: one mean from one group is different. At least one is different.

since p-value=0.000459 < 0.05 we reject the null hyp and there is no evidence all means from groups are
equal to zero. i.e., there is a relationship between mpg and gear.

"""

#--------------------------------------------------------------------- cyl

model_oneway = ols('mpg ~ cyl', data=cars).fit()

model_oneway_fitted_vals = model_oneway.fittedvalues
model_oneway_residuals = model_oneway.resid
model_oneway_norm_residuals = model_oneway.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_oneway_fitted_vals, 
            y=model_oneway_residuals,
            ci=False, lowess=True,
            line_kws={'color':'red', 'lw':1 ,'alpha':0.5})
ax.set_xlim(14,27)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()

stats.probplot(model_oneway_norm_residuals,plot=sns.mpl.pyplot)
# not a strong devation from normality. 
# normality is ok, we can continoue.

model_oneway.summary()
sm.stats.anova_lm(model_oneway, typ=1)

"""
H0: the mean from groups are all the same
H1: one mean from one group is different. At least one is different.

since p-value=0.005401 < 0.05 we reject the null hyp and there is no evidence all means from groups are
equal to zero. i.e., there is a relationship between mpg and cyl.

"""

# --------------------------------------------------------------------------- carb

model_oneway = ols('mpg ~ carb', data=cars).fit()

model_oneway_fitted_vals = model_oneway.fittedvalues
model_oneway_residuals = model_oneway.resid
model_oneway_norm_residuals = model_oneway.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_oneway_fitted_vals, 
            y=model_oneway_residuals,
            ci=False, lowess=True,
            line_kws={'color':'red', 'lw':1 ,'alpha':0.5})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
ax.set_xlim(14,27)
plt.show()
# spread is not ok. One of the groups does not have enough observations.
# This assumption is violated.

stats.probplot(model_oneway_norm_residuals,plot=sns.mpl.pyplot)
# not a strong devation from normality. 
# normality is ok, but spread was violated. Cant continue with test.




# ------------------------------------------------------------------------------------------------

"""

f)	Create a boxplot to see if there is any difference between the means 
    of the response variable (selected in part c) across the two 
    variables “vs” and “am”. Also, create a plot to see if there is an 
    interaction effect for these two variables with the response variable. 
    Interpret these plots. Test to see if any of these factors and/or interactions 
    have a significant relationship with the response variable (selected in part c) 
    using an two-way ANOVA test. 

"""

cars_am_vs = cars[['mpg','am','vs']]

cars_am_vs['vs_n'] = cars_am_vs['vs'].apply(lambda x: 'V-Shaped' if (x == 0) else 'Straight')
cars_am_vs['am_n'] = cars_am_vs['am'].apply(lambda x: 'Automatic' if (x == 0) else 'Manual')


fig, ax = plt.subplots()
sns.boxplot(x='am_n', y='mpg', hue='vs_n', data=cars_am_vs)
plt.title('Miles per galon across am and vs')
plt.legend()
plt.xlabel('am')
plt.show()
cars_am_vs.groupby(by=['am','vs'])['mpg'].describe()[['mean','50%','std']]
# there is difference amoung 
# variance almost same 
# roughly symmetri. im happy with that.

interaction_plot(cars_am_vs['am_n'], cars_am_vs['vs_n'], cars_am_vs['mpg'], colors=['orange','blue'], markers=['D','^'])
plt.xlabel('am')
plt.show()
# there is roughly a interaction, since lines do not look like parallel. in the end side, it is more broaden than
# in the start line.
# lets included in the full model


# -------------------------- 2 WAY ANOVA WITH MPG, AM AND VS and AM:VS intreaction

model2way= ols('mpg ~ C(vs) * C(am)', data=cars).fit()

model_fitted_vals = model2way.fittedvalues #fitted values
#model residuals
model_residuals = model2way.resid
#standardised residuals
model_norm_residuals = model2way.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_fitted_vals,
            y=model_residuals,
            ci=False,
            lowess=True,
            line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
ax.set_xlim(14,29)
plt.show()
# it doesnt look terrible.

stats.probplot(model_norm_residuals, plot=sns.mpl.pyplot)
plt.show()
# looks not terrible.


# balance sample, type 1 from anova function
model2way.summary()
sm.stats.anova_lm(model2way, typ=1)

"""

# two hypothesis
# 1 h0: mpg means are equal in among transaction type level
# 2 h0: mpg means are equal among type of engine
# h1: not all mpg means are equal

# interaction test
# h0: there is no interaction between am and vs
# h1: there is interaction between am and vs

p-value = 0.000003 < 0.05, which means we reject null hypothesis.
 There is no evidence to suggest that mpg means throught transaction type levels are cero.
 Therefore, there is a relaionship between mpg and transmision type. SIGNIFICANT
 
p-value = 0.000007 < 0.05, which means we reject null hypothesis.
 There is no evidence to suggest that mpg means throught engine type level are cero.
 Therefore, there is a relationship between mpg and engine type. SIGNIFICANT
 
p-value = 0.2588 < 0.05 which means we fail to reject the null hypothesis.
 There is not enough evidence to suggest that there is  significant interaction between am and vs.
 Therefore, there is not interaction between am and vs. NOT SIGNIFICANT



"""


# without interaction

model2way= ols('wt ~ C(vs) + C(am)', data=cars).fit()
#fitted values
model_fitted_vals = model2way.fittedvalues
#model residuals
model_residuals = model2way.resid
#standardised residuals
model_norm_residuals = model2way.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_fitted_vals,y=model_residuals,ci=False,lowess=True,line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
#ax.set_xlim(10,30)
plt.show()
# it doesnt look terrible.

stats.probplot(model_norm_residuals, plot=sns.mpl.pyplot)
plt.show()
# looks good.


# balance sample, type 1 from
cars.head(40)

model2way.summary()
sm.stats.anova_lm(model2way, typ=1)




