from sqlalchemy.sql import text
from sqlalchemy import create_engine
from app import db
from app.models import TemperatureData
import schedule
import time
import datetime
import threading

#example from rach sharp how to use run_continuously
class ContinuousScheduler(schedule.Scheduler):
      def run_continuously(self, interval=1):
            """Continuously run, while executing pending jobs at each elapsed
            time interval.
            @return cease_continuous_run: threading.Event which can be set to
            cease continuous run.
            Please note that it is *intended behavior that run_continuously()
            does not run missed jobs*. For example, if you've registered a job
            that should run every minute and you set a continuous run interval
            of one hour then your job won't be run 60 times at each interval but
            only once.
            """
            cease_continuous_run = threading.Event()

            class ScheduleThread(threading.Thread):
                @classmethod
                def run(cls):
                    # I've extended this a bit by adding self.jobs is None
                    # now it will stop running if there are no jobs stored on this schedule
                    while not cease_continuous_run.is_set() and self.jobs:
                        # for debugging
                        # print("ccr_flag: {0}, no. of jobs: {1}".format(cease_continuous_run.is_set(), len(self.jobs)))
                        self.run_pending()
                        time.sleep(interval)

            continuous_thread = ScheduleThread()
            continuous_thread.start()
            return cease_continuous_run
        
sql_schedule = ContinuousScheduler()

# raw sql query translated from access
sql = text(
    "INSERT INTO dailymaxmindata (location, date_of_reading, mintemp, maxtemp) " 
    "SELECT DISTINCT location, timestamp as date_of_reading, MIN(temperature) as mintemp, MAX(temperature) as maxtemp " 
    "FROM sensors INNER JOIN temperature_data on temperature_data.sensor_serial_number = sensors.serial_number "
    "GROUP BY (date(timestamp)), location")

#connect to sqlite
engine = create_engine('sqlite:///app.db')

def populatedailydata():
    db.engine.execute(sql.execution_options(autocommit=True))
    print("dailymaxmindata populated")
    
def purgetemperaturedata():
    readings = TemperatureData.query.all()
    for r in readings:
        db.session.delete(r)
        db.session.commit()                       
    print("TemperatureData purged")
    
sql_schedule.every().day.at('23:59').do(populatedailydata)
sql_schedule.every().day.at('00:00').do(purgetemperaturedata)
halt_schedule_flag = sql_schedule.run_continuously()

#while True:
#    schedule.run_pending()
#    time.sleep(1)
