# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 10:02:34 2021

@author: acjimenez
"""
import schedule
import time
from datetime import date, datetime, timedelta
from 1_cleaningHistory import start_cleaningHistory_process
from 2_getCoordinates import start_getCoordinates_process
from 3_getDailyBikes import start_dailybike_process


def job():
    print(datetime.today())
    print("starting bikes")
    start_dailybike_process()
    return

print("Starting...")
start_cleaningHistory_process()
start_getCoordinates_process()

schedule.every(5).minutes.do(job)

while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
