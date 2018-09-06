from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Sensors(db.Model):
    serial_number = db.Column(db.String(15), primary_key=True)
    location = db.Column(db.String(120), index=True, unique=True)
#    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')

    def __repr__(self):
        return '<Sensors {}>'.format(self.serial_number)

class TemperatureData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sensor_serial_number = db.Column(db.String(15), db.ForeignKey('sensors.serial_number'))

    def __repr__(self):
        return '<TemperatureData {}>'.format(self.temperature)

class Dailymaxmindata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_reading = db.Column(db.DateTime)
    location = db.Column(db.String(120))
    mintemp = db.Column(db.Float)
    maxtemp = db.Column(db.Float)

    def __repr__(self):
        return '<Dailymaxmindata {}>'.format(self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
