from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from flask import request
from flask import json
from flask import jsonify
from app.models import Sensors, TemperatureData, Dailymaxmindata, User
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
#    user = {'username': 'Robbie'}
    return render_template('index.html', title='Home')#, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/insertTemp', methods = ['GET','POST'])
def insertTemp():
    content = request.json
    temp = content['Temperature']
    timestamp = content['Timestamp']
##convert json string to datetime object
    dttimestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    sensorcode = content['Serialnumber']
    inserttempdata = TemperatureData(temperature=temp, timestamp=dttimestamp, sensor_serial_number=sensorcode)
    db.session.add(inserttempdata)
    db.session.commit()
    print (temp, timestamp,sensorcode)
    return jsonify(request.json)

@app.route('/displayTemp')
@login_required
def displayTemp():
    displaytc = Dailymaxmindata.query.all()
#    for d in displaytc:
#        print (d.id, d.date_of_reading, d.location, d.mintemp, d.maxtemp)
    return render_template('display.html', title='Temperature Logs', displaytc=displaytc)
