# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Sat Dic 20 08:10:44 2020

READ ME:
    Hi Jack,
    Please find below code for CA 3.
    
    Each time I read a sheet, I checked the data
    from this sheet, remove not needed rows and saved it as a csv in the "raw" folder as a master
    of each sheet.
    
    In the end, I created a "super" master with all sheets combined and,
    selected the variables that I believed were significant to create the final dataset.
    
    I want to point out that I excluded PCA score variables since I could not understand the measure 
    (I read the paper about the experiment, but could not find a clue).
    
"""

import pandas as pd
import numpy as np
import os
import re
from os import path

os.chdir(r'E:\Karla\IRELAND v2\DKIT\1st Semester\Programming for Data Analytics\Continuous Assessments\Assessement 3\dataset')
mycolumnname = lambda s: s.replace(' ', '_').lower().strip()

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
"""
In this section, I will explore all the sheets in the WINGS.xlsx excel,
using a loop to explore main information.

This will give me a brief understanding of the information.

"""

wings_ = pd.read_excel('WING.xlsx', sheet_name=None)
wings_.keys()

for s in wings_.keys():
    print(s, "sheet in excel WINGS")
    print(wings_[s].info())
    print(wings_[s].columns)
    print(wings_[s].head(10))
    print("----------------------------------------------------------------- end ", s)
    input("")
        
"""
All sheets are interesting, and they have interesting variables and data to work on.
In this case, I will start by importing data from axes sheets:
    - 'Axis 1 measures'
    - 'Axis 2 measures'
    - 'Wild wings, axis 1'
    - 'Wild wings, axis 2'
    
The level would be the wings, not the butterflies, since the literature says that
mimicry is regarding shape of wings. So, I will focus my dataset with the shape and not
the butterfly.

"""

# --------------------------------------------------------------------------------
# BROOD BUTTERFLY'S WING
# --- axis 1 per brood butterfly's wing ------------------------------------------
# Preparing data from 'Axis 1 measure' sheet
# Removing not needed rows.
# Renaming columns to a standard format.
# And I will save this as a backup file.
bbw_axe1_raw = pd.read_excel('WING.xlsx', sheet_name='Axis 1 measures')
bbw_axe1_raw.drop(index=bbw_axe1_raw[-11:].index, inplace=True)
bbw_axe1_raw.columns = list(map(mycolumnname, bbw_axe1_raw.columns))
bbw_axe1_raw.to_csv("raw/myWINGS_axis_1_measures_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove sex, genotype and area.
bbw_axe1 = bbw_axe1_raw.copy()
bbw_axe1.drop(columns=['sex', 'genotype', 'area'], inplace=True)

bbw_axe1.set_index('name', inplace=True)

# --- axis 2 per brood butterfly's wing -----------------------------------------
# Preparing data from 'Axis 2 measure' sheet
# Removing not needed rows.
# Renaming columns to a standard format.
# And I will save this as a backup file.
bbw_axe2_raw = pd.read_excel('WING.xlsx', sheet_name='Axis 2 measures')
bbw_axe2_raw.drop(index=bbw_axe2_raw[-4:].index, inplace=True)
bbw_axe2_raw.columns = list(map(mycolumnname, bbw_axe2_raw.columns))
bbw_axe2_raw.to_csv("raw/myWINGS_axis_2_measures_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove area.
# There are two columns regarding name: name and name.1 (renamed by python)
# I will use name.1 which has the shortened id of the butterfly.
bbw_axe2 = bbw_axe2_raw.copy()
bbw_axe2.drop(columns=['name', 'area'], inplace=True)
bbw_axe2.rename(columns={'name.1':'name'}, inplace=True)

bbw_axe2.set_index('name', inplace=True)

# Now, I will verify columns to see if in these two datasets
# the columns are the same
intersaction_ = bbw_axe1.columns.intersection(bbw_axe2.columns)
intersaction_

# No, there are one column which is in both datasets.
# I will explore the values to check if data is the same.
conditional_ = bbw_axe1['max_axe_1_length'] == bbw_axe2['max_axe_1_length']
bbw_axe2[~conditional_] # same data
bbw_axe2.drop(columns='max_axe_1_length', inplace=True)

# The data in cells are the same in both columns.
# Since it says it is from axe 1 I have to remove from 'Axis 2 measures'.
# Now, I will join these datasets to make one.
bbw_axies = pd.merge(bbw_axe1, bbw_axe2, on='name')
bbw_axies.info()

# --------------------------------------------------------------------------------
# WILD BUTTERFLY'S WING
# --- axis 1 per wild butterfly's wing -------------------------------------------
# Preparing data from 'Axis 1 measure' sheet
# Removing not needed rows.
# Renaming columns to a standard format.
# And I will save this as a backup file.
wbw_axe1_raw = pd.read_excel('WING.xlsx', sheet_name='Wild wings, axis 1')
wbw_axe1_raw.drop(index=wbw_axe1_raw[-3:].index, inplace=True)
wbw_axe1_raw.columns = list(map(mycolumnname, wbw_axe1_raw.columns))
wbw_axe1_raw.to_csv("raw/myWINGS_wild_wings_axis_1_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove name, 'unnamed: 1' (sex), tribe, genuns, species, sub-species, area, and perimeter
wbw_axe1 = wbw_axe1_raw.copy()
wbw_axe1.drop(columns=['name', 'unnamed: 1', 'tribe', 'genus', 'species', 'sub-species', 'area', 'perimeter'], inplace=True) # Not needed

wbw_axe1.set_index('name', inplace=True)

# --- axis 2 per wild's wing ------------------------------------------------------
# Preparing data from 'Axis 2 measure' sheet
# Removing not needed rows.
# Renaming columns to a standard format.
# And I will save this as a backup file.
wbw_axe2_raw = pd.read_excel('WING.xlsx', sheet_name='Wild wings, axis 2')
wbw_axe2_raw.drop(index=wbw_axe2_raw[-3:].index, inplace=True)
wbw_axe2_raw.columns = list(map(mycolumnname, wbw_axe2_raw.columns))
wbw_axe2_raw.to_csv("raw/myWINGS_wild_wings_axis_2_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove name, doresal/ventral, anterior/posterior, left/right, sex, sub/family, genus, species, subspecies and area
wbw_axe2 = wbw_axe2_raw.copy()
wbw_axe2.drop(columns=['name', 'doresal/ventral', 'anterior/posterior', 'left/right', 'sex', 'sub/family', 'genus', 'species', 'subspecies', 'area'], inplace=True) # Not needed

wbw_axe2.set_index('name', inplace=True)

# Verify same columns
# Now I will again verify columns with same name
intersaction_ = wbw_axe1.columns.intersection(wbw_axe2.columns)
intersaction_ # No different columns

# And now, I will combine both datasets in one.
wbw_axies = pd.merge(wbw_axe1, wbw_axe2, on='name', how='left')
wbw_axies.info()

# In the wild butterfly process I detected that the full id of a butterfly
# is made up of wwdd.dddd, I realized the brood butterfly dataset I created
# previously do not have full format name. I inspected the columns from 'Axis 2 measures'
# and found the complete name. Let's work on this.
df_ = bbw_axe2_raw[['name.1', 'name']].copy()
df_.columns = ['name', 'complate_name']
df_.set_index('name', inplace=True)

# New dataset with complete name and shortened name .
# I will join these two datasets on name.
bbw_axies = pd.merge(bbw_axies, df_, on='name')

# Now, I have two columns with name data, I have
# to remove the shortened and leave the complete one.
bbw_axies.reset_index(inplace=True)
bbw_axies.drop(columns='name', inplace=True)
bbw_axies.rename(columns={'complate_name':'name'}, inplace=True)
bbw_axies.set_index('name', inplace=True)

# Before concating the axe 1 and 2 datasets, I will
# create a new column to distinguish which wing is from wild or brood experimental
wbw_axies['seg'] = 'w'
bbw_axies['seg'] = 'b'

# Now, it is time to concat those two datasets.
wings_v1 = pd.concat([bbw_axies, wbw_axies])

# this is the first version of my final dataset.
# Now, it is time to join area and perimeter.

# WILD AND BROOD BUTTERFLIES - AREA AND PERIMETER ----------------------------------
# --- area and perimeter for wild and brood butterflies ----------------------------
# I will start with area, which it is the most straight forward
bbw_area = bbw_axe2_raw[['name','area']].copy()
bbw_area.set_index('name', inplace=True)

# Now, I will get the perimeter from the sheet 'Wing perimeter'
# which is the one from the brood butterflies.
# I will first prepare the raw file and save it as a backup.
bbw_perimeter_raw = pd.read_excel('WING.xlsx', sheet_name='Wing perimeter')
bbw_perimeter_raw.drop(index=bbw_perimeter_raw[-5:].index, inplace=True)
bbw_perimeter_raw.columns = list(map(mycolumnname, bbw_perimeter_raw.columns))
bbw_perimeter_raw.columns = ['name', 'complate_name', 'perimeter']
bbw_perimeter_raw.to_csv("raw/myWINGS_wing_perimeter_raw.csv", na_rep='NA', index=False)

# Now, I will take just the necesary columns and rename them.
bbw_perimeter = bbw_perimeter_raw[['complate_name', 'perimeter']].copy()
bbw_perimeter.rename(columns={'complate_name':'name', 'perimeter':'peri'}, inplace=True)
bbw_perimeter.set_index('name', inplace=True)

# And then, the two datasets will be merged on 'name' and since I have
# more area data than permeter, I will apply left join.
bbw_area_per = pd.merge(bbw_area, bbw_perimeter, on='name', how='left')
wbw_area_per = wbw_axe1_raw[['name', 'area', 'peri']]
wbw_area_per.rename(columns={'perimeter':'peri'}, inplace=True)
wbw_area_per.set_index('name', inplace=True)

# Finally, I will concat areas and perimeters from wild and brood butterflies.
wings_area_per = pd.concat([wbw_area_per, bbw_area_per])

# ----------------------------------------------------------------------------------
# Next, a new version is created from the v1 and new 
# dataset of area and perimeters
wings_v2 = pd.merge(wings_v1, wings_area_per, on='name', how='right')

# BROOD BUTTERFILES -----------------------------------------------------------------
# Let's work now with butterflies. --------------------------------------------------
# The data I will take just for butterflies is sex and genotype.
# Preparing data from 'Outline analysis -brood' sheet
# Removing not needed rows.
# Renaming columns to a standard format.
# And I will save this as a backup file.
bb_raw = pd.read_excel('WING.xlsx', sheet_name='Outline analysis -brood')
bb_raw.drop(index=bb_raw[-10:].index, inplace=True)
bb_raw.columns = list(map(mycolumnname, bb_raw.columns))

lst_columns = list(bb_raw.columns[:8])
lst2_columns = list(bb_raw.iloc[0,8:].apply(lambda n: 'av_' + str(n) + '_pca_score'))

for s in lst2_columns:
    lst_columns.append(s)

bb_raw.drop(index=0, inplace=True)
bb_raw.columns = lst_columns
bb_raw.to_csv("raw/myWINGS_outline_analysis_brood_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove sex, genotype and area.
bb = bb_raw[['ind_name', 'sex', 'genotype_1', 'genotype_2']].copy()
bb.rename(columns={'ind Name':'id_butterfly'}, inplace=True)

# Adding new columns 
bb['tribe'] = 'Heliconiinae'
bb['genus'] = 'Heliconius'

bb.sex.unique()
bb['genotype_1'].unique()
bb['genotype_2'].unique()

bb.set_index('id_butterfly', inplace=True)

# WILD BUTTERFILES -----------------------------------------------------------------
# In this case, I will compare three difference sheets to get all 
# the data to reduce missing values.
# First, I will do 'Wild wings, axis 1'
# variables to be compared are: name, sex, tribe, genus, genotype_1, and genotype_2
wb = wbw_axe1_raw[['name', 'Unnamed: 1', 'Tribe', 'Genus', 'Species', 'sub-species']].copy()
wb.columns = list(map(mycolumnname, wb.columns))
wb.rename(columns={'unnamed:_1':'sex', 'species':'genotype_1', 'sub-species':'genotype_2'}, inplace=True)

wb['id_butterfly'] = list(map(lambda s: re.split(r'-\w_',s)[0], wb['name']))
wb.drop(columns='name', inplace=True)
wb.drop_duplicates(inplace=True)
wb.set_index('id_butterfly', inplace=True)

# And I will compare against 'Outline analysis -wild'
# Also, save it as a backup.
wb_outa_raw = pd.read_excel('WING.xlsx', sheet_name='Outline analysis -wild')
wb_outa_raw.drop(index=wb_outa_raw[-8:].index, inplace=True)
wb_outa_raw.columns = list(map(mycolumnname, wb_outa_raw.columns))

lst_columns = list(wb_outa_raw.columns[:8])
lst2_columns = list(wb_outa_raw.iloc[0,8:].apply(lambda n: 'av_' + str(n) + '_pca_score'))

for s in lst2_columns:
    lst_columns.append(s)

wb_outa_raw.drop(index=0, inplace=True)
wb_outa_raw.columns = lst_columns
wb_outa_raw.to_csv("raw/myWINGS_outline_analysis_wild_raw.csv", na_rep='NA', index=False)

# Copy raw dataset to remove not needed columns.
# Since I am working with wings and I will mainly focus on axies first
# I will remove not needed columns regarding PCA score.
wb2 = wb_outa_raw[wb_outa_raw.columns[2:6]].copy()
wb2.rename(columns={'ind_name':'id_butterfly'}, inplace=True)
wb2.drop_duplicates(inplace=True)
wb2.set_index('id_butterfly', inplace=True)

# Mergin data to check different values.
df_ = pd.merge(wb, wb2, on='id_butterfly')

aux1 = df_[df_['sex_x'] != df_['sex_y']][['sex_x', 'sex_y']]
aux2 = df_[df_['genotype_1_x'] != df_['genotype_1_y']]
aux3 = df_[df_['genotype_2_x'] != df_['genotype_2_y']]

aux1[['sex_x','sex_y']] # There is just one different data
aux2[['genotype_1_x', 'genotype_1_y']] # No data difference
aux3[['genotype_2_x', 'genotype_2_y']] # there are 45 different data

# I will overread on first dataset since it is the main one.
wb.loc[aux1.index, 'sex'] = aux1['sex_y'] 
wb.loc[aux3.index, 'genotype_2'] = aux3['genotype_2_y']

# I will do the same, but this time with 'Wild wing, axe 1' and 'Wild wing, axe 2'
wb2 = wbw_axe2_raw[['name', 'Sex', 'sub/Family', 'Genus', 'Species', 'Subspecies']].copy()
wb2.columns = list(map(mycolumnname, wb2.columns))
wb2.rename(columns={'sex':'sex', 'sub/family':'tribe', 'species':'genotype_1', 'subspecies':'genotype_2'}, inplace=True)

wb2['id_butterfly'] = list(map(lambda s: re.split(r'-\w_',s)[0], wb2['name']))
wb2.drop(columns='name', inplace=True)
wb2.drop_duplicates(inplace=True)
wb2.set_index('id_butterfly', inplace=True)

df_ = pd.merge(wb, wb2, on='id_butterfly')

aux1 = df_[df_['sex_x'] != df_['sex_y']]
aux2 = df_[df_['tribe_x'] != df_['tribe_y']]
aux3 = df_[df_['genus_x'] != df_['genus_y']]
aux4 = df_[df_['genotype_1_x'] != df_['genotype_1_y']]
aux5 = df_[df_['genotype_2_x'] != df_['genotype_2_y']]

aux1[['sex_x','sex_y']]
aux2[['tribe_x', 'tribe_y']]
aux3[['genus_x', 'genus_y']]
aux4[['genotype_1_x', 'genotype_1_y']]
aux5[['genotype_2_x', 'genotype_2_y']] 

# Differences are not significant in first dataset, however it is
# interesting that there is an inconsistency in MJ99.0064.
# I will check it later.
# Now, I will check values.
wb['sex'].unique()
wb['tribe'].unique()
wb['genus'].unique() # There is an inconsistency with two same values but spaces in right and left side.
wb['genotype_1'].unique()
wb['genotype_2'].unique() 

wb[wb['tribe'].isna()] # The butterfly does not have a tribe and couldnt find it in other sheets.

wb['genus'] = wb['genus'].str.strip() # Remove left/right spaces

# Now, I will concat these datasets to get one.
butterflies = pd.concat([wb, bb])

# New version of dataset ------------------------------------------------------------
# I just have column name which is the id of each wing.
# To merge the dataset butterflies, I need to extract the id of the butterfly
# from the column name.
wings_v2.reset_index(inplace=True)
wings_v2['id_butterfly'] = list(map(lambda s: re.split(r'-\w_',s)[0], wings_v2['name']))
wings_v2.set_index('id_butterfly', inplace=True)

# And after this, I will merge the butterfiles in the last wings version
wings_v3 = pd.merge(wings_v2, butterflies, on='id_butterfly', how='left')
wings_v3.reset_index(inplace=True)

wings_v3[wings_v3.duplicated()] # no duplicated values

# More variables from wing's name
wings_v3['wing'] = wings_v3['name'].str.split('_').apply(lambda s: s[1])
wings_v3['dg_wing'] = wings_v3['name'].str.split('_').apply(lambda s: s[-1])
wings_v3['s_wing'] = wings_v3['name'].str.split('_').apply(lambda s: s[0][-1])

# -----------------------------------------------------
# Quick examination to find out missing values
wings_v3[wings_v3['sex'].isna()][['seg', 'sex']]
wings_v3[wings_v3['tribe'].isna()][['seg', 'tribe']]
wings_v3[wings_v3['genus'].isna()][['seg', 'genus']]
wings_v3[wings_v3['genotype_1'].isna()][['seg', 'genotype_1']]
wings_v3[wings_v3['genotype_2'].isna()][['seg', 'genotype_2']]

# there is no data in butterfly 1017,
# it is not in outline analysis sheet because wings were damaged.
# Let's add information from 'Experimental brood'
brood_raw = pd.read_excel('WING.xlsx', sheet_name='Experimental brood')
brood_raw.drop(index=brood_raw[-6:].index, inplace=True)
brood_raw.columns = list(map(mycolumnname, brood_raw.columns))
brood_raw.to_csv("raw/myWINGS_experimental_brood_raw.csv", na_rep='NA', index=False)

brood_ = brood_raw.copy()
brood_[brood_['name'] == 1017]

# I will update by hand butterfly 1017
wings_v3.set_index('id_butterfly', inplace=True)
wings_v3.loc['MJ02.1017','sex'] = 'f'
wings_v3.loc['MJ02.1017','tribe'] = 'Heliconiinae'
wings_v3.loc['MJ02.1017','genus'] = 'Heliconius'
wings_v3.loc['MJ02.1017','genotype_1'] = 'aurora'
wings_v3.loc['MJ02.1017','genotype_2'] = 'silvana'
wings_v3.reset_index(inplace=True)

wings_v3.info()
# Now data looks very good.

# FINAL VERSIONS -------------------------------------------------------------
# Copy last version into new one
# and assign short names.

wings_v4 = wings_v3.copy()
wings_v4.rename(columns={
    'name':'id_wing',
    'ellipse_axe_1_length':'e_len_axe1',
    'max_axe_1_length':'max_len_axe1',
    'deviation_max_axe_1_from_center':'devmax_cent_axe1',
    'axe_1_moment_2':'m2_axe1', 
    'axe_1_moment_3':'m3_axe1',
    'axe_1_moment_4':'m4_axe1', 
    'std_axe_1_moment_2':'stdm2_axe1', 
    'std_axe_1_moment_3':'stdm3_axe1',
    'std_axe_1_moment_4':'stdm4_axe1',
    'ellipse_axe_2_length':'e_len_axe2',
    'max_axe_2_length':'max_len_axe2',
    'deviation_max_axe_2_from_center':'devmax_cent_axe2',
    'axe_2_moment_2':'m2_axe2', 
    'axe_2_moment_3':'m3_axe2',
    'axe_2_moment_4':'m4_axe2', 
    'std_axe_2_moment_2':'stdm2_axe2', 
    'std_axe_2_moment_3':'stdm3_axe2',
    'std_axe_2_moment_4':'stdm4_axe2',
    'genotype_1':'geno1',
    'genotype_2':'geno2'
    }, inplace=True)

wings_v4['id_wing'] = wings_v4['id_wing'].astype('str')
wings_v4['id_butterfly'] = wings_v4['id_butterfly'].astype('str')
wings_v4['sex'] = wings_v4['sex'].astype('category')
wings_v4['tribe'] = wings_v4['tribe'].astype('category')
wings_v4['genus'] = wings_v4['genus'].astype('category')
wings_v4['geno1'] = wings_v4['geno1'].astype('category')
wings_v4['geno2'] = wings_v4['geno2'].astype('category')
wings_v4['seg'] = wings_v4['seg'].astype('category')
wings_v4['wing'] = wings_v4['wing'].astype('category')
wings_v4['dg_wing'] = wings_v4['dg_wing'].astype('category')
wings_v4['s_wing'] = wings_v4['s_wing'].astype('category')

wings_v4.info()

# save MASTER version ---------------------------------------------------------
wings_v4.to_csv('myWINGS_master.csv', index=False)

# FINAL VERSION OF DATASET ------------------------------------------------------------
# -------------------------------------------------------------------------------------
# Lastly:
# Looking at the structure of the data, lets check the following:
#   Common problems with messy datasets:
#    - Column headers are values, not variable names.
#       In this dataset, it seems this is not a problem. In my point of view,
#        axe 1 and  axe 2 are measures, not variables.
#        In this case, I will leave columns regargin axe 1 and axe 2.
#   - Multiple variables are stored in one column.
#       Id_wing has multiple values stored (e.g. side of wing, left or right wing), 
#        but this is the way a wing is identified. This dataset is about wings of butterflies
#        not butterflies. Therefore, to identify each wing I will keep id_wing in the way it 
#        is in the original dataset.

# Last version, reorganized columns.
# I remove id_butterfly since this is a dataset regarding wings, not butterflies.
# Also, I will remove PAC scores from final dataset.

wings = wings_v4[['id_wing', 's_wing', 'wing', 'dg_wing', 'area', 'peri', 'e_len_axe1', 'max_len_axe1',
                     'devmax_cent_axe1', 'm2_axe1', 'm3_axe1', 'm4_axe1', 'stdm2_axe1',
                     'stdm3_axe1', 'stdm4_axe1', 'e_len_axe2', 'max_len_axe2',
                     'devmax_cent_axe2', 'm2_axe2', 'm3_axe2', 'm4_axe2', 'stdm2_axe2',
                     'stdm3_axe2', 'stdm4_axe2', 'sex', 'tribe',
                     'genus', 'geno1', 'geno2', 'seg']]

# My final dataset.
wings.to_csv("myWINGS.csv", na_rep='NA', index=False)

# -----------------------------------------------------------------------------------------
"""

METADATA of FINAL DATASET myWINGS

Dataset: WINGS.xlsx
Description
The original data was extracted from brood and wild butterfiles. It has information on
butterfly's characteristics and wings' features.

Format
A data frame with 3052 wings and 30 variables

Columns:
    'id_wing' => wing identifier, made up of butterfly ID and side of wing
    's_wing' => side of wing (d=doresal, v=ventral)
    'wing' => Ant=Anterior or Post=Posterior
    'dg_wing', => d=right, g=left
    'area', => area of wing, units: pixel2
    'peri', => perimeter of wing, units: pixel
    'e_len_axe1', => ellipse axe 1 length, units: pixel
    'max_len_axe1', => max axe 1 length, units: pixel
    'devmax_cent_axe1', => deviation max axe 1 from center
    'm2_axe1', => axe 1 Moment 2
    'm3_axe1', => axe 1 Moment 3
    'm4_axe1', => axe 1 Moment 4
    'stdm2_axe1', => std axe 1 Moment 2
    'stdm3_axe1', => std axe 1 Moment 3
    'stdm4_axe1', => std axe 1 Moment 4
    'e_len_axe2', => ellipse axe 2 length, units: pixel
    'max_len_axe2', => max axe 2 length, units: pixel
    'devmax_cent_axe2', => deviation max axe 2 from center
    'm2_axe2', => axe 2 Moment 2
    'm3_axe2', => axe 2 Moment 3
    'm4_axe2', => axe 2 Moment 4
    'stdm2_axe2', => std axe 2 Moment 2
    'stdm3_axe2', => std axe 2 Moment 3
    'stdm4_axe2', => std axe 2 Moment 4
    'sex', => sex of butterfly (f=female, m=male)
    'tribe', => tribe of butterfly
    'genus', => genus of butterfly
    'geno1', => genotype 1 of butterfly
    'geno2', => genotype 2 of butterfly
    'seg' => b=brood butterfly or w=wild butterfly
    
"""