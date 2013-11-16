from flask import Flask, render_template, send_from_directory
import pytz
from pytz import timezone
from datetime import datetime as time
from random import choice
import os.path
import re

app = Flask(__name__)

@app.route('/images/<image>')
def load_image(image=None):
    if(os.path.isfile('images/' + image)):
        return send_from_directory('images', image)

def get_place(hour):
    places = [time_zone.split("/")[1].replace("_"," ")
        for time_zone in pytz.all_timezones
        if(time.now(timezone(time_zone)).hour == hour
        and len(time_zone.split("/")) == 2
        and len(re.findall("[0-9]",time_zone)) == 0)]
    return choice(places)

@app.route('/<hour>')
def hour_page(hour="4"):
    assert hour.isdigit()
    ihour = int(hour)
    if(ihour > 11):
        period = 'afternoon'
        hour = (12 if ihour == 12 else ihour - 12)
    else:
        period = 'morning'
        hour = (12 if ihour == 0 else ihour)
    return render_template('hour.html',
            hour=hour, period=period, 
            loc=get_place(ihour))

@app.route('/')
def menu_page():
    return 'Menu'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
