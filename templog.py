from app import app, db
from app.models import Sensors, TemperatureData, Dailymaxmindata, User
#from app.sqljobs import populatedailydata

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Sensors': Sensors, 'TemperatureData': TemperatureData, 'Dailymaxmindata': Dailymaxmindata, 'User': User} #'populatedailydata': populatedailydata}

