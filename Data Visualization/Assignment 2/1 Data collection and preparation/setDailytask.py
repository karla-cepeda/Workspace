import schedule
import time
from datetime import datetime

from cleaningHistory import start_cleaningHistory_process
from getCoordinates import start_getCoordinates_process
from getDailyBikes import start_dailybike_process

"""
    
    This file runs all files to set the database for the real-time app, 
    for more information about the structure of the whole app, please
    read the report.

"""

def job():
    # This tasks it is executed every minute to look for new data.
    print(datetime.today())
    print("Starting bikes process...")
    start_dailybike_process()
    print("Bikes process completed.")
    print(datetime.today())
    print("")
    return

print("Importing initial data...")
print("Importing coordinates from moby...")
start_getCoordinates_process()
print("Importing historical data...")
start_cleaningHistory_process()
print("Inicial importation has been completed.")
print("")
print("Daily task to be scheduled...")

schedule.every(60).seconds.do(job)

while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
