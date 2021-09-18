import pandas as pd
import requests
import numpy as np
import time

import mysql.connector
import sqlalchemy

from datetime import datetime

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from preparingcsvfiles import start_csvfiles_process

"""
    
    This module imports daily information from bikes by connecting to API.
    Then, this access to preparingcsvfile module to create csv files for
    easy access for real-time app.

"""

def start_dailybike_process():
        
    def check_bike_inarea(polygon_, la_, lo_):
        return polygon_.contains(Point(lo_, la_))
    
    # ------------------------------------------
    # SQL INFORMATION
    # ------------------------------------------
        
    config = {
      'user': '', # Change
      'password': '', # Change
      'host': '', # Change
      'database': '', # Change
    }
    
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(config['user'], config['password'], 
                                                          config['host'], config['database']))
    
    # ------------------------------------------
    # CALL TO API
    # ------------------------------------------
    
    lst = list()
    
    url = 'https://data.smartdublin.ie/mobybikes-api/last_reading/'
    
    while True:
        try:
            json_data = requests.get(url).json()
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
    
    maxdate = pd.to_datetime(df_.HarvestTime.max())
    maxdate_db = None
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    myquery = 'SELECT lastDateVisit FROM lastdatevisit;'
    cursor.execute(myquery)
    
    for lastDateVisit in cursor:
       maxdate_db = pd.to_datetime(lastDateVisit[0])
    
    cursor.close()
    cnx.close()
    
    if maxdate_db != maxdate:
        
        print("New data found!")
        
        # Cleaning
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
        
        # ----------------------------------------------
        # GPS
        # ----------------------------------------------
        gps = df_[['LastGPSTime', 'BikeID', 'Latitude', 'Longitude']].copy().drop_duplicates()
        
        # Correct format to variables    
        gps.LastGPSTime = pd.to_datetime(gps.LastGPSTime)
        
        # Verify that there is no duplicated values in last call to API
        myq_maxgps = "SELECT MAX(LastGPSTime) AS LastGPSTime, BikeID FROM gpsbikes GROUP BY BikeID;"
        gpsMAX_db = pd.read_sql_query(myq_maxgps, engine)
        comparison_df = gps.merge(gpsMAX_db,indicator=True,how='left', on=['LastGPSTime','BikeID'])
        
        # This is the one we gonna insert
        new_gps = comparison_df[comparison_df._merge=="left_only"][gps.columns]
        
        # Check if bikes are in dublin area
        myquery_dublinmap = "SELECT Longitude, Latitude FROM dublinmap;"
        coordinates = pd.read_sql_query(myquery_dublinmap, engine)
        coordinates = np.array(coordinates)
            
        #polygon = Polygon(coordinates) # create polygon
        new_gps.loc[:,'InDublinArea'] = 0 #new_gps.apply(lambda b: check_bike_inarea(polygon, b['Latitude'], b['Longitude']), axis=1)
        
        # Check if bikes are in moby area
        myquery_mobymap = "SELECT Longitude, Latitude FROM mobyarea;"
        coordinates = pd.read_sql_query(myquery_mobymap, engine)
        coordinates = np.array(coordinates)
        
        polygon = Polygon(coordinates) # create polygon
        new_gps.loc[:,'InMobyArea'] = new_gps.apply(lambda b: check_bike_inarea(polygon, b['Latitude'], b['Longitude']), axis=1)
        
        # Bikes located
        condition = (new_gps.Latitude == 0) | (new_gps.Longitude == 0)
        new_gps.loc[:,'Located'] = np.where(~condition, True, False)
        new_gps.BikeID = new_gps.BikeID.astype('int64')
        new_gps.sort_values(by='LastGPSTime', inplace=True)
        
        # Create a second dataframe to check and upgrade last valid gps table
        valid_gps = new_gps[new_gps.Located == True]
        
        myq_lastValidgps = "SELECT LastGPSTime, BikeID FROM gpsbikes_lastvalid;"
        lastValidgps_db = pd.read_sql_query(myq_lastValidgps, engine)
        comparison_df = valid_gps.merge(lastValidgps_db,indicator=True,how='left', on=['LastGPSTime', 'BikeID'])
        
        new_valid_gps = comparison_df[comparison_df._merge == 'left_only'][['LastGPSTime', 'BikeID', 'Latitude', 'Longitude']]
        new_valid_gps.BikeID = new_valid_gps.BikeID.astype('int64')
        new_valid_gps.sort_values(by='LastGPSTime', inplace=True)
        
        # Figure out if bike is missed by checking other coordinates.
        # If not, take the last coordinate, plot it and mark it red as missed.
        
        # Found bikes
        # Not found bikes
        # Plot recent points              
        
        # ----------------------------------------------
        # RENTING
        # ----------------------------------------------
        renting = df_[['LastRentalStart', 'BikeID']].copy().drop_duplicates()
        renting.LastRentalStart = pd.to_datetime(renting.LastRentalStart)
        
        # Verify that there is no duplicated values in last call to API
        myq_maxrenting = "SELECT MAX(LastRentalStart) AS LastRentalStart, BikeID AS MAXBikeID FROM rentedbikes GROUP BY BikeID;"
        rentingMAX = pd.read_sql_query(myq_maxrenting, engine)
        comparison_df = renting.merge(rentingMAX,indicator=True,how='outer').copy()
        
        # This is the one we gonna insert
        new_renting = comparison_df[comparison_df.MAXBikeID.isna()][renting.columns]
        new_renting.sort_values(by='LastRentalStart', inplace=True)
        
        # Get the total number of bikes rented today
        # Get the total number of bikes rented per hour.
        # Get the number of bikes rented per type of bike
                
        # ----------------------------------------------
        # BIKES
        # ----------------------------------------------
        bikes = df_[['HarvestTime', 'BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']]
        
        # Apply correct format
        bikes.HarvestTime = pd.to_datetime(bikes.HarvestTime)
        
        bikes = bikes.loc[bikes.reset_index().groupby(['BikeID'])['HarvestTime'].idxmax()]
        bikes = bikes[['BikeID', 'BikeIdentifier', 'BikeTypeName', 'EBikeProfileID', 'IsEBike', 'IsMotor', 'IsSmartLock', 'SpikeID']]
                
        # Verify that there is no duplicated values in last call to API
        myq_maxbikes = "SELECT * FROM bikes;"
        bikesMAX = pd.read_sql_query(myq_maxbikes, engine)
        comparison_df = bikes.merge(bikesMAX,indicator=True,how='outer')
        
        # This is the one we gonna insert
        new_bikes = comparison_df[comparison_df._merge == 'left_only'][bikes.columns]
        
        # INSERT INTO MYSQL ------------------------------------------------------------------------------------------------
        
        harvesting.to_sql(con=engine, schema="tanniest_mybikes", name='harvestedbikes', if_exists='append', index=False)
        
        if len(new_gps) > 0:
            new_gps.to_sql(con=engine, schema="tanniest_mybikes", name='gpsbikes', if_exists='append', index=False)
            print(len(new_gps), " gps records added.")
            #print(new_gps.head(20))
            
        else:
            print("No new gps information")
            
            
        # -------------------------------------------
        # CUMULATIVE NUM RENTED
        # -------------------------------------------
        
        
        def call_sp(storedp, args):
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            
            cursor.callproc(storedp, args)
            
            info_db = None
            desc = None
            
            for result in cursor.stored_results():
                desc = result.description
                info_db = result.fetchall()
            
            cursor.close()
            cnx.commit()
            cnx.close()
            
            cols = list()
            if desc is not None:
                for i in desc:
                    cols.append(i[0])
            
                return pd.DataFrame(info_db, columns=cols)
            else:
                return 1
            
                       
        # Rents
        
        if len(new_renting) > 0:
            new_renting.to_sql(con=engine, schema="tanniest_mybikes", name='rentedbikes', if_exists='append', index=False)
            print(len(new_renting), " rented bike records added.")
            #print(new_renting.head(20))
            
        else:            
            print("No new renting information")
            
        # Insert cumulative rents
        
        now = datetime.now()
        curr = now.date().strftime('%d/%m/%Y')
        currtime = now.time().strftime('%H:%M:%S')
        
        call_sp('insert_cumrents', (str(curr),str(currtime),))
                
        if len(new_valid_gps) > 0:
            
            # Remove bikes which will be upgraded
            to_delvalid = list(new_valid_gps['BikeID'].astype(str))
            to_delvalid = ",".join(to_delvalid)
            
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
                        
            delete_bikes = ("DELETE FROM gpsbikes_lastvalid WHERE BikeID IN (" + to_delvalid + ");")
            cursor.execute(delete_bikes)
            
            cnx.commit()          
            cursor.close()
            cnx.close()
            
            new_valid_gps.to_sql(con=engine, schema="tanniest_mybikes", name='gpsbikes_lastvalid', if_exists='append', index=False)
            print(len(new_valid_gps), " last valid gps records modifed.")
            #print(new_valid_gps.head(20))
            
        else:
            print("No new bike information")
                    
        if len(new_bikes) > 0:
            
            # Remove bikes which will be upgraded
            to_delbikes = list(new_bikes['BikeID'].astype(str))
            to_delbikes = ",".join(to_delbikes)
            
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
                        
            delete_bikes = ("DELETE FROM bikes WHERE BikeID IN (" + to_delbikes + ");")
            cursor.execute(delete_bikes)
            
            cnx.commit()          
            cursor.close()
            cnx.close()
            
            new_bikes['active'] = 1
            
            new_bikes.to_sql(con=engine, schema="tanniest_mybikes", name='bikes', if_exists='append', index=False)
            print(len(new_bikes), " bike records modifed.")
            
        else:
            print("No new bike information")
        
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
                
        truncate_lastDateVisit = ("DELETE FROM lastdatevisit; ")
        cursor.execute(truncate_lastDateVisit)
                
        insert_lastDateVisit = ("INSERT INTO lastdatevisit (lastdatevisit, description) "
                                "VALUES (%s, %s); ")
        
        data_lastvisit = (harvesting.HarvestTime.max().strftime("%Y-%m-%d %H:%M:%S"), " ")
        cursor.execute(insert_lastDateVisit, data_lastvisit)
        
        cnx.commit()
        
        cursor.close()
        cnx.close()
                
        print("Starting process for csv files...")
        start_csvfiles_process()
    
    else:
        print("No time to upgrade data.")
         
if __name__ == 'main':
    start_dailybike_process()
