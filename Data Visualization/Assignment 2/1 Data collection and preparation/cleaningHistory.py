
import pandas as pd
import numpy as np
import requests
import time
import sqlalchemy
from datetime import date, timedelta


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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

    filename = r'Datasets\bikes_history.csv'
    
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
                df_.to_csv(filename, index=False, header=True)
                first_time = False
                        
            else:
                df_.to_csv(filename, mode='a', header=False, index=False, na_rep='nan')
        else:
            print("no information found", date_lambda(index_date))
           
        lst = list()    
        index_date = index_date + pd.DateOffset(months=1)
        
        print("")
        
    print("Process has ended")
    
    del lst, df_, first_time, index_date, end_date, start_date
    
    df_ = pd.read_csv(filename)
    
    df_.HarvestTime = pd.to_datetime(df_.HarvestTime)
    df_.LastGPSTime = pd.to_datetime(df_.LastGPSTime)
    df_.LastRentalStart = pd.to_datetime(df_.LastRentalStart)
    df_.BikeIdentifier = df_.BikeIdentifier.astype('int64')
    
    # ----------------------------------------------
    # HARVESTING
    # ----------------------------------------------
    harvesting = df_[['HarvestTime', 'BikeID', 'Battery', 'EBikeStateID']]
            
    # When values are NA, it means battery has ran out
    harvesting.Battery = harvesting.Battery.fillna(0)
    
    # Battery most be from 0 to 100, but have seen lower values, lets clip
    harvesting.Battery = np.clip(harvesting.Battery, 0, 100)
    
    # Correct format to variables
    harvesting.HarvestTime = pd.to_datetime(harvesting.HarvestTime)
    harvesting.Battery = harvesting.Battery.astype('int64')
    harvesting.EBikeStateID = harvesting.EBikeStateID.astype('int64')
    
    harvesting.to_sql(con=engine, schema="tanniest_mybikes", name='harvestedbikes', if_exists='append', index=False)
    
    del harvesting
    
    
    # ----------------------------------------------
    # RENTING
    # ----------------------------------------------
    renting = df_[['LastRentalStart', 'BikeID']].copy().drop_duplicates()
    renting.LastRentalStart = pd.to_datetime(renting.LastRentalStart)
    renting.sort_values(by='LastRentalStart', inplace=True)
    renting.to_sql(con=engine, schema="tanniest_mybikes", name='rentedbikes', if_exists='append', index=False)
    
    # ------------------------------------------
    # BIKES LAST INFORMATION
    # ------------------------------------------
    # Last data recorded
    #bikes = df_[df_.HarvestTime < '2020-10'][['HarvestTime', 'BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']].copy()
    bikes = df_[['HarvestTime', 'BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']].copy()
    
    # Last data recorded
    bikes = bikes.loc[bikes.reset_index().groupby(['BikeID'])['HarvestTime'].idxmax()]
    bikes = bikes.sort_values(by='BikeID')
    bikes = bikes.reset_index(drop=True)
    bikes = bikes[['BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']]
    bikes['active'] = 1
    
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
    
    def check_bike_inarea(polygon_, la_, lo_):
        return polygon_.contains(Point(lo_, la_))
    
    # Last data recorded
    gps = df_[['LastGPSTime', 'BikeID', 'Latitude', 'Longitude']].drop_duplicates()  
    gps.LastGPSTime = pd.to_datetime(gps.LastGPSTime)
    
    # Check if bikes are in dublin area
    myquery_dublinmap = "SELECT Longitude, Latitude FROM dublinmap;"
    coordinates = pd.read_sql_query(myquery_dublinmap, engine)
    coordinates = np.array(coordinates)
    
    polygon = Polygon(coordinates) # create polygon
    gps.loc[:,'InDublinArea'] = gps.apply(lambda b: check_bike_inarea(polygon, b['Latitude'], b['Longitude']), axis=1)
    
    # Check if bikes are in moby area
    myquery_mobymap = "SELECT Longitude, Latitude FROM mobyarea;"
    coordinates = pd.read_sql_query(myquery_mobymap, engine)
    coordinates = np.array(coordinates)
    
    polygon = Polygon(coordinates) # create polygon
    gps.loc[:,'InMobyArea'] = gps.apply(lambda b: check_bike_inarea(polygon, b['Latitude'], b['Longitude']), axis=1)
        
    condition = (gps.Latitude == 0) | (gps.Longitude == 0)
    gps.loc[:,'Located'] = np.where(~condition, True, False)
    gps.BikeID = gps.BikeID.astype('int64')
    gps.sort_values(by='LastGPSTime', inplace=True)
    
    gps.to_sql(con=engine, schema="tanniest_mybikes", name='gpsbikes', if_exists='replace', index=False)
    
    condition = (gps.Latitude == 0) | (gps.Longitude == 0)
    new_gps = gps[~condition].copy().reset_index(drop=True)
    new_gps = new_gps.loc[new_gps.reset_index().groupby(['BikeID'])['LastGPSTime'].idxmax()]
    new_gps = new_gps.reset_index(drop=True)
    new_gps = new_gps.sort_values(by='BikeID')
    
    new_gps.to_sql(con=engine, schema="tanniest_mybikes", name='gpsbikes_lastvalid', if_exists='replace', index=False)
    
    del gps
    
if __name__ == 'main':
    start_cleaningHistory_process()
