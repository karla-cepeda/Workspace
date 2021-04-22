import pandas as pd
import numpy as np

df = pd.read_csv("../initial_data/crime.csv")


df_2 = pd.melt(df, id_vars=['Statistic', 'Garda Station', 'Type of Offence', 'UNIT'], 
                   value_vars=['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'],
                   value_name='counts',
                   var_name = "year"                   
                   )

df_2['Garda Station 2'] = df_2['Garda Station'].str.replace(' ', ',', 1).str.split(',')
df_2['id_station'] = df_2['Garda Station 2'].apply(lambda s: s[0])
df_2['station_division'] = df_2['Garda Station 2'].apply(lambda s:s[2])
df_2['station'] = df_2['Garda Station 2'].apply(lambda s:s[1])

df_2.drop(columns=['Garda Station 2', 'Garda Station'], inplace=True)

df_2.to_csv('crime_2.csv', index=False)


df = pd.read_csv("../initial_data/population.csv")


df_2 = pd.melt(df, id_vars=['Statistic', 'County', 'Sex', 'UNIT'], 
                   value_vars=['1841', '1851', '1861', '1871',
       '1881', '1891', '1901', '1911', '1926', '1936', '1946', '1951', '1956',
       '1961', '1966', '1971', '1979', '1981', '1986', '1991', '1996', '2002',
       '2006', '2011', '2016'],
                   value_name='counts',
                   var_name = "year"                   
                   )

df_2.to_csv('population_2.csv', index=False)
