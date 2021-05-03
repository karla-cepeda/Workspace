import os
import schedule
import time
from datetime import datetime

from cleaningHistory import start_cleaningHistory_process
from getCoordinates import start_getCoordinates_process
from getDailyBikes import start_dailybike_process


def job():
    print(datetime.today())
    print("starting bikes process...")
    start_dailybike_process()
    #start_csvfiles_process()
    print("bikes process completed...")
    print(datetime.today())
    print("")
    return

print("Starting...")
print("Inicial import coordinates...")
#start_getCoordinates_process()
print("Inicial import history...")
#start_cleaningHistory_process()
print("Import completed...")
print("")
print("Daily task to be scheduled...")

schedule.every(60).seconds.do(job)

while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
