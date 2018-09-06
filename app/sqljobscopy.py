from sqlalchemy.sql import text
from sqlalchemy import create_engine
from app import db
from app.models import TemperatureData
import schedule
import time

sql = text(
    "INSERT INTO dailymaxmindata (location, date_of_reading, mintemp, maxtemp) " 
    "SELECT DISTINCT location, timestamp as date_of_reading, MIN(temperature) as mintemp, MAX(temperature) as maxtemp " 
    "FROM sensors INNER JOIN temperature_data on temperature_data.sensor_serial_number = sensors.serial_number "
    "GROUP BY (date(timestamp)), location")

#works in sqlite - test again, why not here?
engine = create_engine('sqlite:///app.db')

def populatedailydata():
    db.engine.execute(sql.execution_options(autocommit=True))
    print("dailymaxmindata populated")
    return schedule.CancelJob

def purgetemperaturedata():
    readings = TemperatureData.query.all()
    for r in readings:
        db.session.delete(r)
        db.session.commit()                       
    print("TemperatureData purged")
    return schedule.CancelJob



schedule.every().day.at('23:59').do(populatedailydata)
schedule.every().day.at('00:00').do(purgetemperaturedata)                           

#while True:
#    schedule.run_pending()
#    time.sleep(1)
