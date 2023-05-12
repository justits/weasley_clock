import schedule
import time
import os

from global_const import MINUTE
from gps_tracker.icloud_gps_tracker import iCloudGPSTracker
from read_data import users

gps_tracker = iCloudGPSTracker(os.getenv('EMAIL', None), os.getenv('PASSWORD', None))


def update_user():
    family_locations = gps_tracker.select_query('family_locations')
    for user in users:
        user.change_place(family_locations.get(user.app_cloud_id, None))
        user.print()
    print('frequency: ', min([user.frequency for user in users]) / MINUTE, end='\n\n')


def job():
    update_user()
    # if min([user.frequency for user in users]) != frequency:
    #     return schedule.CancelJob


update_user()
while True:
    frequency = min([user.frequency for user in users])
    # schedule.every(frequency).seconds.do(job)
    schedule.every(120).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

