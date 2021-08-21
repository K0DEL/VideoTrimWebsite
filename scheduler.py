from flask_apscheduler import APScheduler
from time import time
import os
from constants import DOWNLOAD_FOLDER, SCHEDULER_TIME, SESSION_FOLDER


scheduler = APScheduler()


@scheduler.task('interval', id='do_job_1', seconds=SCHEDULER_TIME,
                misfire_grace_time=2*SCHEDULER_TIME)
def delete_cache():
    if os.path.isdir(DOWNLOAD_FOLDER) and os.path.isdir(SESSION_FOLDER):
        now = time()
        print(f"Deletion Performed at {now}")
        for f in os.listdir(DOWNLOAD_FOLDER):
            f = os.path.join(DOWNLOAD_FOLDER, f)
            if os.stat(f).st_mtime < now - SCHEDULER_TIME:
                os.remove(f)

        for f in os.listdir(SESSION_FOLDER):
            f = os.path.join(SESSION_FOLDER, f)
            if os.stat(f).st_mtime < now - SCHEDULER_TIME:
                os.remove(f)
