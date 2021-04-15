# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:20:58 2021

@author: karla cepeda
"""

import pandas as pd
import requests
import time
import sqlalchemy
from datetime import date, timedelta

import os

os.chdir(r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Data Visualization\CA\CA2')

# pd.set_option('display.max_columns', None)


def start_cleaningHistory_process():

    # ------------------------------------------
    # SQL INFORMATION
    # ------------------------------------------
    
    """
    config = {
      'user': 'root',
      'password': 'k4Rl4#05',
      'host': 'localhost',
      'database': 'bikes',
    }
    """
    
    config = {
      'user': 'tanniest_mybikes',
      'password': 'WNZvC=M^u.pQ',
      'host': 'mx74.hostgator.mx',
      'database': 'tanniest_mybikes',
    }
    
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(config['user'], config['password'], 
                                                          config['host'], config['database']))

    # ------------------------------------------
    # RETRIVE ALL HISTORY
    # ------------------------------------------
    start_date = date(2020,1,1)
    end_date = date.today() + timedelta(days=1)
    index_date = start_date
    
    date_format = "%Y-%m-%d"
    date_lambda = lambda d: str(d.strftime(date_format))
    
    url = r'https://data.smartdublin.ie/mobybikes-api/historical/?start={}&end={}'
    url_new = ''
    
    file_name = 'bikes_history.csv'
    
    lst = list()
    first_time = True
    
    print("Process has started....")
    while index_date <= end_date:
        url_new = url.format(date_lambda(index_date), date_lambda(index_date + pd.DateOffset(months=1)))
        print(url_new)
        
        while True:
            try:
                json_data = requests.get(url_new).json()
                break
            except Exception:
                print("Error while connecting to API")
                time.sleep(10)
                print("Lets try again...")
                continue
        
        for d in json_data:
            lst.append(
                    {'HarvestTime':d['HarvestTime'],
                     'BikeID':d['BikeID'],
                     'Battery':d['Battery'],
                     'BikeIdentifier': d['BikeIdentifier'],
                     'BikeTypeName':d['BikeTypeName'],
                     'EBikeProfileID': d['EBikeProfileID'],
                     'EBikeStateID': d['EBikeStateID'],
                     'IsEBike':d['IsEBike'],
                     'IsMotor':d['IsMotor'],
                     'IsSmartLock':d['IsSmartLock'],
                     'LastGPSTime':d['LastGPSTime'],
                     'LastRentalStart':d['LastRentalStart'],
                     'Latitude':d['Latitude'],
                     'Longitude':d['Longitude'],
                     'SpikeID':d['SpikeID'],
                        
                     }
                )
            
        df_ = pd.DataFrame(lst)
        
        if len(df_) > 0:
            print("information found", date_lambda(index_date))
            if first_time:
                df_.to_csv(file_name, index=False, header=True)
                first_time = False
                        
            else:
                df_.to_csv(file_name, mode='a', header=False, index=False, na_rep='nan')
        else:
            print("no information found", date_lambda(index_date))
           
        lst = list()    
        index_date = index_date + pd.DateOffset(months=1)
        
        print("")
        
    print("Process has ended")
    
    del lst, df_, first_time, index_date, end_date, start_date
    
    df_ = pd.read_csv(r'Datasets\bikes_history.csv')
    
    df_.HarvestTime = pd.to_datetime(df_.HarvestTime)
    df_.LastGPSTime = pd.to_datetime(df_.LastGPSTime)
    df_.LastRentalStart = pd.to_datetime(df_.LastRentalStart)
    df_.BikeIdentifier = df_.BikeIdentifier.astype('int64')
    
    # ------------------------------------------
    # BIKES LAST INFORMATION
    # ------------------------------------------
    # Last data recorded
    bikes = df_[df_.HarvestTime < '2020-10'][['HarvestTime', 'BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']].copy()
    
    # Last data recorded
    bikes = bikes.loc[bikes.reset_index().groupby(['BikeID'])['HarvestTime'].idxmax()]
    bikes = bikes.sort_values(by='BikeID')
    bikes = bikes.reset_index(drop=True)
    bikes = bikes[['BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']]
    
    bikes.to_sql(con=engine, schema="tanniest_mybikes", name='bikes', if_exists='replace', index=False)
    
    del bikes
    
    # ------------------------------------------
    # GPA LAST VALID INFORMATION
    # ------------------------------------------
    
    def truncate(f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])
    
    # Last data recorded
    gps = df_[['LastGPSTime', 'BikeID', 'Latitude', 'Longitude']]
    condition = (gps.Latitude == 0) | (gps.Longitude == 0)
    gps = gps[~condition].reset_index(drop=True)
    gps = gps.loc[gps.reset_index().groupby(['BikeID'])['LastGPSTime'].idxmax()]
    gps = gps.reset_index(drop=True)
    gps = gps.sort_values(by='BikeID')
    gps.Latitude = gps.Latitude.apply(lambda x: truncate(x,4))
    gps.Longitude = gps.Longitude.apply(lambda x: truncate(x,4))
    
    gps.to_sql(con=engine, schema="tanniest_mybikes", name='gpsbikes_lastvalid', if_exists='replace', index=False)
    
    del gps
    

if __name__ == 'main':
    start_cleaningHistory_process()