import mysql.connector
import pandas as pd
from datetime import datetime

import ftplib

"""
    
    This module saves all important information into files
    for an easy connection when comes to real-time upgrades on APP.
    I found it much effective by saving files in a location than connecting to 
    database every 5 minutes.

"""

def start_csvfiles_process():
    
    # FTP to save in repository,
    # this is a personal repository, please be aware this is my real information,
    # and would be expire on 15-may-2021
    FTP_HOST = "" # Change
    FTP_USER = "" # Change
    FTP_PASS = "" # Change
        
    # Database login credentials,
    # this is a personal repository, please be aware this is my real information,
    # and would be expire on 15-may-2021
    config = {
		  'user': '', # Change
		  'password': '', # Change
		  'host': '', # Change
		  'database': '', # Change
       }
    
    def call_sp(storedp, args):
        
        # Method to connect to database and collect data from stored procedure
        
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
    
    
    # Create ftp object to save file in repository
    ftp = ftplib.FTP(FTP_HOST,FTP_USER, FTP_PASS)
        
    # current day
    now = datetime.now()
    curr = now.date().strftime('%d/%m/%Y')
    
    """
    # SAVE THIS TO LET KNOW REAL-TIME DATA PROCESS HAS STARTED
    f = open("datasets/running.txt", "w")
    f.write("1")
    f.close()
    
    with open("datasets/running.txt", "rb") as file:
        ftp.storbinary('STOR running.txt', file)    
    """
    
    ftp.enconding="utf-8"
    
    """
    # This is run just once, not needed to be in daily task
    mobyarea = pd.read_sql_query('SELECT Longitude, Latitude FROM mobyarea;', engine)
    mobyarea.to_csv('../3 Data visualization/datasets/mobyarea.csv')    
    
    with open('../3 Data visualization/datasets/mobyarea.csv', 'rb') as file:
        ftp.storbinary('STOR mobyarea.csv', file)
        
    del mobyarea
    """
    
    lastgps = call_sp('BikesLastGPS', (curr,))
    lastgps.to_csv('datasets/lastgps.csv')    
    
    rented_cum = call_sp('BikesRented_cum', (curr,))
    rented_cum.to_csv('datasets/rented_cum.csv')  
    
    BikesRented = call_sp('BikesRented', (curr,))
    BikesRented.to_csv('datasets/BikesRented.csv')  
    
    get_batteryStatus = call_sp('get_batteryStatus', (curr,))
    get_batteryStatus.to_csv('datasets/get_batteryStatus.csv') 
    
    get_bikestatus = call_sp('get_bikestatus', (curr,))
    get_bikestatus.to_csv('datasets/get_bikestatus.csv') 
    
    summary = call_sp('summary', (curr,))
    summary.to_csv('datasets/summary.csv')   
    
    get_location = call_sp('get_location', (curr,))
    get_location.to_csv('datasets/get_location.csv') 
    
    get_inarea = call_sp('get_inarea', (curr,))
    get_inarea.to_csv('datasets/get_inarea.csv')  
    
    get_batterystatusbikes_all = call_sp('get_batterystatusbikes_all', (curr,))
    get_batterystatusbikes_all.to_csv('datasets/get_batterystatusbikes_all.csv') 
    
    
    with open('datasets/lastgps.csv', 'rb') as file:
        ftp.storbinary('STOR lastgps.csv', file)    
    del lastgps    
      
    with open('datasets/rented_cum.csv', 'rb') as file:
        ftp.storbinary('STOR rented_cum.csv', file)      
    del rented_cum
      
    with open('datasets/BikesRented.csv', 'rb') as file:
        ftp.storbinary('STOR BikesRented.csv', file)      
    del BikesRented
       
    with open('datasets/get_batteryStatus.csv', 'rb') as file:
        ftp.storbinary('STOR get_batteryStatus.csv', file)
                
    del get_batteryStatus
       
    with open('datasets/get_bikestatus.csv', 'rb') as file:
        ftp.storbinary('STOR get_bikestatus.csv', file)                
    del get_bikestatus
        
    with open('datasets/summary.csv', 'rb') as file:
        ftp.storbinary('STOR summary.csv', file)                
    del summary
           
    with open('datasets/get_location.csv', 'rb') as file:
        ftp.storbinary('STOR get_location.csv', file)                
    del get_location
      
    with open('datasets/get_inarea.csv', 'rb') as file:
        ftp.storbinary('STOR get_inarea.csv', file)                
    del get_inarea
           
    with open('datasets/get_batterystatusbikes_all.csv', 'rb') as file:
        ftp.storbinary('STOR get_batterystatusbikes_all.csv', file)                
    del get_batterystatusbikes_all
    
    """
    get_batterystatusbikes_all = call_sp('get_cat_statusbikes', ())
    get_batterystatusbikes_all.to_csv('datasets/get_cat_statusbikes.csv') 
    with open('datasets/get_cat_statusbikes.csv', 'rb') as file:
        ftp.storbinary('STOR get_cat_statusbikes.csv', file)                
    del get_cat_statusbikes
    """
if __name__ == 'main':
    
    start_csvfiles_process()
    
