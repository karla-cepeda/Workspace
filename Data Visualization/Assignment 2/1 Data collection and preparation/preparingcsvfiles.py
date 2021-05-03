
import mysql.connector
import sqlalchemy

import pandas as pd
import numpy as np

from datetime import datetime, date, timedelta

import ftplib

def start_csvfiles_process():
    
    FTP_HOST ="ftp.tanniestudio.com"
    FTP_USER ="datavis@tanniestudio.com"
    FTP_PASS ="6=.at(dD/]@4Z3g~"
        
    config = {
         'user': 'tanniest_mybikes',
         'password': 'WNZvC=M^u.pQ',
         'host': 'mx74.hostgator.mx',
         'database': 'tanniest_mybikes',
       }
    
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                      format(config['user'], config['password'], 
                                             config['host'], config['database']))
    
    
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
        cnx.close()
        
        cols = list()
        for i in desc:
            cols.append(i[0])
        
        return pd.DataFrame(info_db, columns=cols)
    
    
    ftp = ftplib.FTP(FTP_HOST,FTP_USER, FTP_PASS)
    ftp.enconding="utf-8"
        
    now = datetime.now()
    curr = now.date().strftime('%d/%m/%Y')
    
    lastgps = call_sp('BikesLastGPS', (curr,))
    lastgps.to_csv('../3 Data visualization/datasets/lastgps.csv')
    
    with open('../3 Data visualization/datasets/lastgps.csv', 'rb') as file:
        ftp.storbinary('STOR lastgps.csv', file)
    
    del lastgps
    
    """
    mobyarea = pd.read_sql_query('SELECT Longitude, Latitude FROM mobyarea;', engine)
    mobyarea.to_csv('../3 Data visualization/datasets/mobyarea.csv')    
    
    with open('../3 Data visualization/datasets/mobyarea.csv', 'rb') as file:
        ftp.storbinary('STOR mobyarea.csv', file)
        
    del mobyarea
    """
    
    rented_cum = call_sp('BikesRented_cum', (curr,))
    rented_cum.to_csv('../3 Data visualization/datasets/rented_cum.csv')
    
    with open('../3 Data visualization/datasets/rented_cum.csv', 'rb') as file:
        ftp.storbinary('STOR rented_cum.csv', file)
      
    del rented_cum
    
    BikesRented = call_sp('BikesRented', (curr,))
    BikesRented.to_csv('../3 Data visualization/datasets/BikesRented.csv')
    
    with open('../3 Data visualization/datasets/BikesRented.csv', 'rb') as file:
        ftp.storbinary('STOR BikesRented.csv', file)
      
    del BikesRented
        
    lastinfo = call_sp('lastinfo', (curr,))
    lastinfo.to_csv('../3 Data visualization/datasets/lastinfo.csv')
    
    with open('../3 Data visualization/datasets/lastinfo.csv', 'rb') as file:
        ftp.storbinary('STOR lastinfo.csv', file)
              
    del lastinfo
        
    get_batteryStatus = call_sp('get_batteryStatus', (curr,))
    get_batteryStatus.to_csv('../3 Data visualization/datasets/get_batteryStatus.csv')
    
    with open('../3 Data visualization/datasets/get_batteryStatus.csv', 'rb') as file:
        ftp.storbinary('STOR get_batteryStatus.csv', file)
                
    del get_batteryStatus
    
    get_bikestatus = call_sp('get_bikestatus', (curr,))
    get_bikestatus.to_csv('../3 Data visualization/datasets/get_bikestatus.csv')
    
    with open('../3 Data visualization/datasets/get_bikestatus.csv', 'rb') as file:
        ftp.storbinary('STOR get_bikestatus.csv', file)
                
    del get_bikestatus
        
    summary = call_sp('summary', (curr,))
    summary.to_csv('../3 Data visualization/datasets/summary.csv')
    
    with open('../3 Data visualization/datasets/summary.csv', 'rb') as file:
        ftp.storbinary('STOR summary.csv', file)
                
    del summary
        
    get_location = call_sp('get_location', (curr,))
    get_location.to_csv('../3 Data visualization/datasets/get_location.csv')
    
    with open('../3 Data visualization/datasets/get_location.csv', 'rb') as file:
        ftp.storbinary('STOR get_location.csv', file)
                
    del get_location
    
    get_inarea = call_sp('get_inarea', (curr,))
    get_inarea.to_csv('../3 Data visualization/datasets/get_inarea.csv')
    
    with open('../3 Data visualization/datasets/get_inarea.csv', 'rb') as file:
        ftp.storbinary('STOR get_inarea.csv', file)
                
    del get_inarea
    
    
    get_totalbikesrented = call_sp('get_totalbikesrented', (curr,))
    get_totalbikesrented.to_csv('../3 Data visualization/datasets/get_totalbikesrented.csv')
    
    with open('../3 Data visualization/datasets/get_totalbikesrented.csv', 'rb') as file:
        ftp.storbinary('STOR get_totalbikesrented.csv', file)
                
    del get_totalbikesrented
    
    
    get_batterystatusbikes = call_sp('get_batterystatusbikes', (curr,))
    get_batterystatusbikes.to_csv('../3 Data visualization/datasets/get_batterystatusbikes.csv')
    
    with open('../3 Data visualization/datasets/get_batterystatusbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_batterystatusbikes.csv', file)
                
    del get_batterystatusbikes
    
    get_batterystatusbikes_all = call_sp('get_batterystatusbikes_all', (curr,))
    get_batterystatusbikes_all.to_csv('../3 Data visualization/datasets/get_batterystatusbikes_all.csv')
    
    with open('../3 Data visualization/datasets/get_batterystatusbikes_all.csv', 'rb') as file:
        ftp.storbinary('STOR get_batterystatusbikes_all.csv', file)
                
    del get_batterystatusbikes_all
    
    
    get_historical_statusbikes = call_sp('get_historical_statusbikes', ())
    get_historical_statusbikes.to_csv('../3 Data visualization/datasets/get_historical_statusbikes.csv')
    
    with open('../3 Data visualization/datasets/get_historical_statusbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_historical_statusbikes.csv', file)
                
    del get_historical_statusbikes
    
    get_historical_rentalbikes = call_sp('get_historical_rentalbikes', ())
    get_historical_rentalbikes.to_csv('../3 Data visualization/datasets/get_historical_rentalbikes.csv')
    
    with open('../3 Data visualization/datasets/get_historical_rentalbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_historical_rentalbikes.csv', file)
                
    del get_historical_rentalbikes
    
    get_historical_locationbikes = call_sp('get_historical_locationbikes', ())
    get_historical_locationbikes.to_csv('../3 Data visualization/datasets/get_historical_locationbikes.csv')
    
    with open('../3 Data visualization/datasets/get_historical_locationbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_historical_locationbikes.csv', file)
                
    del get_historical_locationbikes
    
    
    """
    get_cat_statusbikes = call_sp('get_cat_statusbikes', ())
    get_cat_statusbikes.to_csv('../3 Data visualization/datasets/get_cat_statusbikes.csv')
    
    with open('../3 Data visualization/datasets/get_cat_statusbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_cat_statusbikes.csv', file)
                
    del get_cat_statusbikes
    """
    
    
    """
    get_cat_statusbattery = call_sp('get_cat_statusbattery', ())
    get_cat_statusbattery.to_csv('../3 Data visualization/datasets/get_cat_statusbattery.csv')
    
    with open('../3 Data visualization/datasets/get_cat_statusbattery.csv', 'rb') as file:
        ftp.storbinary('STOR get_cat_statusbattery.csv', file)
                
    del get_cat_statusbattery
    """
    
    

if __name__ == 'main':
    
    print(datetime.today())
    print("starting cvs file process...")
    start_csvfiles_process()
    print(datetime.today())
    print("ending cvs file process...")
