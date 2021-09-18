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
import os
import numpy as np

import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor

from statsmodels.stats.anova import anova_lm

import seaborn as sns

os.chdir(r'E:\Karla\IRELAND v2\DKIT\1st Semester\Statistic\CA\Assessement 3\Docs')
cars = pd.read_csv('mtcars.csv')

cars.rename(columns={'Unnamed: 0':'car'}, inplace=True)

#----------------------------------------------------------------------------------------------------------

"""
a)	Fit a suitable multiple linear regression model, based on your answers 
    from question 1, explain your choice. Comment on whether the assumptions
    are satisfied, interpretation of the results and the fit of the model.

"""

# I am going to start by adding all the variables that have a relationship with
# mpg and all categorical / numerical variables.

X =cars[['hp','drat', 'wt', 'qsec', 'cyl', 'vs', 'am', 'gear', 'carb' ]]
X = sm.add_constant(X)

# first, I will check VIF to avoid multicollinearity
pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])],index=X.columns).sort_values(ascending=False)

# VIF ok, let's continue.
X =cars[['hp','drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb' ]]
X = sm.add_constant(X)
y = cars['mpg']
model_mlr = sm.OLS(y, X).fit()

model_fitted_vals = model_mlr.fittedvalues
model_residuals = model_mlr.resid
model_norm_residuals = model_mlr.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_fitted_vals,y=model_residuals,ci=False,lowess=True,line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
ax.set_xlim(10,30)
plt.show()
# it doesnt look terrible.

stats.probplot(model_norm_residuals, plot=sns.mpl.pyplot)
plt.show()
# Not terrible.

# Residual Standard Error.
model_mlr.summary()
np.sqrt(model_mlr.scale)



#----------------------------------------------------------------------------------------------------------

"""
b)	Are there any variables you would like to remove/add from/to the model and why? 
    Re-run the multiple linear regression model.  (You can do this more than once, 
    in a background stepwise elimination if you think appropriate, to find 
    the most suitable model). Compare the fit of this model to the model in part a.  
    Perform an F-test to compare the two models, stating your hypothesis and the 
    conclusion of this test.

"""

#X =cars[['hp','drat', 'wt', 'qsec', 'cyl', 'vs', 'am', 'gear', 'carb' ]]
#X =cars[['hp','drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb' ]]
#X =cars[['hp','drat', 'wt', 'qsec', 'am', 'gear', 'carb' ]]
#X =cars[['hp','drat', 'wt', 'qsec', 'am', 'carb' ]]
#X =cars[['drat', 'wt', 'qsec', 'am', 'carb' ]]
#X =cars[['wt', 'qsec', 'am', 'carb' ]]
X =cars[['wt', 'qsec', 'am']]
X = sm.add_constant(X)
y = cars['mpg']
r_model_mlr = sm.OLS(y, X).fit()

model_fitted_vals = r_model_mlr.fittedvalues
model_residuals = r_model_mlr.resid
model_norm_residuals = r_model_mlr.get_influence().resid_studentized_internal

fig, ax = plt.subplots()
sns.regplot(x=model_fitted_vals,y=model_residuals,ci=False,lowess=True,line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
ax.set_xlim(10,30)
plt.show()
# it doesnt look terrible.

stats.probplot(model_norm_residuals, plot=sns.mpl.pyplot)
plt.show()
# Not terrible.

# Residual Standard Error
print(r_model_mlr.summary())
np.sqrt(r_model_mlr.scale)

# ---------------------------------------------------------------

# Partial Regression Plot
from statsmodels.graphics.regressionplots import plot_partregress_grid
def get_partial_regression_plot(fitted_model, figure_size=(12, 8), save_to_file=False,file_name="regression_plot"):
    reg_plot = plot_partregress_grid(fitted_model, fig=plt.figure(figsize=figure_size))
    if save_to_file:
        reg_plot.savefig(file_name + ".png")
    return reg_plot

reg_plot = get_partial_regression_plot(model_mlr, save_to_file=True)
plt.show()


# --------------------------------------------------------

## cook's distance lines

def graph(formula, x_range, label=None):
    """
    Helper function for plotting cook's distance lines on plot
    """
    x = x_range
    y = formula(x)
    plt.plot(x, y, label=label, lw=1, ls='--', color='red')
    
model_norm_residuals = r_model_mlr.get_influence().resid_studentized_internal
model_leverage = r_model_mlr.get_influence().hat_matrix_diag
model_cooks = r_model_mlr.get_influence().cooks_distance[0]

plot_cooks = plt.figure();
plt.scatter(model_leverage, model_norm_residuals, alpha=0.5);
sns.regplot(model_leverage, model_norm_residuals, scatter=False,ci=False, lowess=True, line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
plot_cooks.axes[0].set_xlim(0, max(model_leverage)+0.01)
plot_cooks.axes[0].set_ylim(-3.5, 3.5)
plot_cooks.axes[0].set_title('Residuals vs Leverage')
plot_cooks.axes[0].set_xlabel('Leverage')
plot_cooks.axes[0].set_ylabel('Standardized Residuals');

# annotations top 3 cooks distance points
leverage_top_3 = np.flip(np.argsort(model_cooks), 0)[:3]
for i in leverage_top_3:
    plot_cooks.axes[0].annotate(i,xy=(model_leverage[i],model_norm_residuals[i]));
#create cooks distance lines
p = len(r_model_mlr.params) # number of model parameters
graph(lambda x: np.sqrt((0.5 * p * (1 - x)) / x),np.linspace(0.001, max(model_leverage), 50),'Cook\'s distance') # 0.5 line
graph(lambda x: np.sqrt((1 * p * (1 - x)) / x),np.linspace(0.001, max(model_leverage), 50)) # 1 line
plot_cooks.legend(loc='upper right');


# there is no points above cook's distance, its ok.



# --------------------------------

# F-test


anovaResults = anova_lm(r_model_mlr, model_mlr)
print(anovaResults)
# h0:
