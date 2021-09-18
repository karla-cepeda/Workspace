# -*- coding: utf-8 -*-
"""
@author: Karla Cepeda
@studentID: D00242569
@module: Programming for Data Analytics

Created on Sat Nov 28 08:10:44 2020

READ ME FIRST:
    Hi Jack,
    Please find below code for scraping data from freemeteo.
    I made an authomatic web scraping process.
    Also, I created a log file to make sure everything is going good.
    
    I gathered information from capitals of Mexico and Ireland to compare temperature and other data regarded.
    
    CHALLANGES FACED:
        - Create an authomatic process to collect data from 2019.
        - The internet service had been gone out for several times (just for seconds), and could not request information, I had to add a while until process can connect to website.
        - Information I could not gather since this is from javascript code.
        - Curing data:
            - Wind information was a pain in the neck, the information has wind direction and wind speed in same column.
        - Cleaning.
    
"""
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import numpy as np
import os
from os import path

os.chdir(r'E:/Karla/IRELAND v2/DKIT/1st Semester/Programming with Python/Continuous Assessments/Assessement 2')

td = timedelta(days=1)
last_date, first_date = date(2020,1,1)-td, date(2019,1,1)

date_lambda, datetime_lambda = lambda d: d.strftime('%d-%m-%Y'), lambda d: d.strftime('%d-%m-%Y %H:%M:%S')

url = r'https://ie.freemeteo.com/weather/{}/history/daily-history/?gid={}&date={}-{}-{}&station={}&country={}&language=english'
url_new = ''

# Locations I will gather information from.
stations = pd.DataFrame({'id':['21677','1767'], 
                         'country':['mexico','ireland'], 
                         'capital':['mexico-city','baile-atha-cliath'], 
                         'gid':['9036028','2964574']})

file_name, file_name_new ='weather_{}.csv', ''

year_in_process = 0
header_lst = []
index = 0

exit_while = False

#-------------------------------------------------------------------------------------------------------------
# Methods....

def split_unconsistent_wind_info(i):
    units = "Km/h"
    wind_speed = "{} " + units
    
    if i.strip().lower() == 'calm':
        return ('Calm',wind_speed.format("0"))
    
    i_c=i.replace(' ','').replace(units,'').strip()[::-1]
    
    index = 0
    for h in i_c:
        try:
            if h == '.':
                continue
            int(h)
        except:
            break
        index+=1
    
    wind_speed = wind_speed.format(str(i_c[0:index][::-1]))
    
    if len(wind_speed) == 0:
        return(i, np.nan)
    else:
        return(i.replace(wind_speed,''), wind_speed)

def log_error(error_type):
    mode = 'w'
    file_name = 'log.txt'
    
    if path.exists(file_name):
        mode = 'a'
        
    txt_file = open(file_name, mode)
    txt_file.write('{}. In {} station. Date: {}. Message error: {}\n'.format(datetime_lambda(datetime.today()),station,date_lambda(weather_date),error_type))
    txt_file.close()

def lst_typo_conv(typo, lst, name):
    try:
        lst = list(map(typo,lst))
    except:
        log_error("Convertion error in type " + str(typo) + " in " + name)
    finally:
        return lst
    
def replace_character(s,char):
    s = s.replace(char,'')
    s = s.strip()
    return s

# -------------------------------------------------------------------------------------------
# Scraping process...

for station in stations.index:
    
    date_index = first_date    
    
    s_gid = stations.loc[station,'gid']
    s_id = stations.loc[station,'id']
    s_capital = stations.loc[station,'capital']
    s_country = stations.loc[station,'country']
    
    print(s_country,"in process...")
    
    while date_index <= last_date:
        
        new_url = url.format(s_capital,
                             str(s_gid),
                             str(date_index.year), 
                             str(date_index.month).zfill(2), 
                             str(date_index.day).zfill(2),
                             str(s_id),
                             s_country)
        
        while True:
            try:
                r = requests.get(new_url)
                html_doc = r.text
                
                soup = BS(html_doc)
                
                # All data is in table daily-history
                cal_table_bs = soup.find('table', class_='daily-history')
                # After that, I select just the body, since header will be procesed in the following steps.
                cal_body_bs = cal_table_bs.find('tbody').select('tr')
                break
            
            except:
                # Any problem regarding internet or reponse of website
                print('cannot get information....')
                outcome = 0  
                exit_while = False
                while outcome not in (1,2):
                    try:
                        outcome = int(input("How to proceed? 1->Try again, 2->Exit.... "))  
                        if outcome == 2:
                            exit_while = True
                            break
                    except:
                        outcome = 0
        
            if exit_while:
                break
                       
        if exit_while:
            break
        
        # Construct header
        # Previously, I checked if every day in 2019 had
        #  the same number and text of hearder. The test passed and I 
        #  proceed to just construct one header starting from the first date of the period
        #  to be extracted.
        if index == 0:
            cal_header_bs = cal_table_bs.select('th')
            cal_header_bs[-1].find('a').extract()
            
            for header in cal_header_bs:
                header_lst.append(header.text.lower())
                
            header_lst = list(map(lambda s: s.replace(' ', '_').replace('.', '').strip().lower(), header_lst))
        
        # Order of data: 
        #   Time, Temperature, Relative Temperature, Wind, Wind Gust, Rel. humidity, Dew Point, Pressure, Icon & Description.
        weather = pd.DataFrame()
            
        time_lst = []
        temp_lst, r_temp_lst = [], []
        wind_lst, g_wind_lst = [], []
        rel_hum_lst = []
        dew_point_lst = []
        press_lst = []
        icon_lst = []
        desc_lst = [] 
        
        # Extra variables
        time_split_lst = []
        time_hr_lst, time_min_lst = [], []
        wind_dir_lst = []
        
        # Date
        # Just to make sure we are processing correct date
        weather_date_str = soup.select('.weather-now .cal')[0].text
        weather_date_str = weather_date_str.replace('\r\n          \xa0\r\n          ','').strip()
        weather_date = pd.to_datetime(weather_date_str, format = '%A, %B %d, %Y')
        
        # Station name registed in website
        station = soup.select('.weather-now .station a.show-station-ui')[0].text
        station = station.replace('\r\n          ','').strip()
            
        # City name registed in website
        city_station = soup.select('.weather-now .station a.show-station-map')[0].text
        city_station = city_station.replace('\r\n          ','').strip()
        
        # This bit is just in case URL was wrongly formed, since website automaticaly redirect to current date when
        #  url is wrong.
        if weather_date != date_index:
            print("There is a problem with URL....")
            outcome = 0  
            exit_while = False
            while outcome not in (1,2):
                try:
                    outcome = int(input("How to proceed? 1->Continue, 2->Exit.... "))  
                    if outcome == 1:
                        break
                    elif outcome == 2:
                        exit_while = True
                        break
                except:
                    outcome = 0
             
        if exit_while:
            break
        
        # Since the data is located in a table, there was not proper css to 
        #  select data, the only thing that I could find it might work is by taking all the data
        #  and going through every column like a list.
        for t in cal_body_bs:
            row = t.select('td')
            time_lst.append(row[0].text)
            temp_lst.append(row[1].text)
            r_temp_lst.append(row[2].text)
            wind_lst.append(row[3].text)
            g_wind_lst.append(row[4].text)
            rel_hum_lst.append(row[5].text)
            dew_point_lst.append(row[6].text)
            press_lst.append(row[7].text)
            icon_lst.append(row[8].text)
            desc_lst.append(row[9].text)
        
        # Split hour and minute
        time_split_lst = list(map(lambda t: t.split(":"), time_lst))
        time_hr_lst = list(map(lambda t: t[0],time_split_lst))    
        time_hr_lst = lst_typo_conv(int, time_hr_lst, "time_hr_lst")
        
        time_min_lst = list(map(lambda t: t[1],time_split_lst)) 
        time_min_lst = lst_typo_conv(int, time_min_lst, "time_min_lst")
            
        # Clean temperature data. Remove C° label and clean any space 
        #  that could be.
        temp_lst = list(map(lambda t: replace_character(t,'°C'), temp_lst))    
        temp_lst = lst_typo_conv(int, temp_lst, "temp_lst")
        
        # Clean relative temperature data. Remove C° label and clean any space
        #  that could be.
        r_temp_lst = list(map(lambda t: replace_character(t,'°C'), r_temp_lst))    
        r_temp_lst = lst_typo_conv(int, r_temp_lst, "r_temp_lst")  
        
        # Direction and speed of wind is together in same cell.
        # Some other inforamtion is also in some cells, like "Calm" instead of speed = 0
        temp_wind_lst = list(map(lambda t: split_unconsistent_wind_info(t), wind_lst))
        
        # Remove degrees symbol of wind's direction
        wind_dir_lst = list(map(lambda t: t[0].replace('°','').strip(),temp_wind_lst))  
        wind_dir_lst = lst_typo_conv(int, wind_dir_lst, "wind_dir_lst")
        
        # Remove units of wind's speed
        wind_lst = list(map(lambda t: t[1].strip(), temp_wind_lst))
        wind_lst = list(map(lambda w: w.replace('Km/h','').strip(), wind_lst))    
        wind_lst = lst_typo_conv(int, wind_lst, "wind_lst")
        
        # Remove %
        rel_hum_lst = list(map(lambda h: replace_character(h,'%'), rel_hum_lst))   
        rel_hum_lst = lst_typo_conv(int, rel_hum_lst, "rel_hum_lst")
        
        # Remove C°
        dew_point_lst = list(map(lambda d: replace_character(d,'°C'), dew_point_lst))    
        dew_point_lst = lst_typo_conv(int, dew_point_lst, 'dew_point_lst')
        
        # Remove mb
        press_lst = list(map(lambda p: replace_character(p,'mb'), press_lst))    
        press_lst = lst_typo_conv(float, press_lst, 'press_lst')
        
        # Remove spaces
        desc_lst = list(map(lambda d: d.strip(), desc_lst))
        
        # I detected some dates do not have information, e.g. Dublin has just two dates in September with data,
        #   it might be a problem with the website, since in Met Éireann Weather website september has data in each day
        #   (I could have done the scraping process in Met Éireann website, but the problem is that it is made on php 
        #    and cannot use a URL since it is working with POST and GET requests, I suppose).
        if len(cal_body_bs)>0:
            weather = pd.DataFrame({"country":s_country,
                                    "city":city_station,
                                    "station":station,
                                    "date":date_lambda(weather_date),
                                    header_lst[0]:time_lst,
                                    "day":weather_date.day,
                                    "month":weather_date.month,
                                    "year":weather_date.year,
                                    "hour":time_hr_lst,
                                    "min":time_min_lst,
                                    header_lst[1]:temp_lst,
                                    header_lst[2]:r_temp_lst,
                                    header_lst[3]:wind_lst,
                                    "wind_dir":wind_dir_lst,
                                    header_lst[4]:g_wind_lst,
                                    header_lst[5]:rel_hum_lst,
                                    header_lst[6]:dew_point_lst,
                                    header_lst[7]:press_lst,
                                    header_lst[8]:icon_lst,
                                    header_lst[9]:desc_lst
                                    })
        else:
            # data of dates which do not exist, register empty row.
            weather = pd.Series([s_country,
                                 city_station,
                                 station,
                                 date_lambda(weather_date),
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 np.nan,
                                 "Not found"])
            
            weather = pd.DataFrame(weather).T            
            log_error("Not data found")
    
        # Files are created depending of year.
        if date_index.year != year_in_process:
            file_name_new = file_name.format(date_index.year)
            year_in_process = date_index.year
            weather.to_csv(file_name_new, index=False, header=True)
            print("First date of the year", date_index, "added.")
            
        else:
            weather.to_csv(file_name_new, mode='a', header=False, index=False, na_rep='N/A')
            print(date_index, "added.")              
        
        date_index += td  # next day
        index+=1 # counter
    
    if exit_while:
        break
            
print("Process ended.")
