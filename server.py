from flask import Flask, request, render_template, send_from_directory
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

@app.route('/clock')
def hour_page(hour="4"):
    if(len(request.args.getlist('hour')) > 0):
        hour = request.args.getlist('hour')[0]
    ihour = int(hour)
    if(ihour > 11):
        period = 'afternoon' if ihour < 18 else 'evening'
        hour = (12 if ihour == 12 else ihour - 12)
    else:
        period = 'morning'
        hour = (12 if ihour == 0 else ihour)
    return render_template('hour.html',
            hour=hour, period=period, 
            loc=get_place(ihour))

@app.route('/')
def menu_page():
    blank_option = "\t\t<option value=\"{0}\">{1}</option>"
    option_list = "\n".join([
        blank_option.format(hour, 
        str(12 if hour % 12 == 0 else hour % 12) + " o'clock in the "
            + (("afternoon" if hour < 18 else "evening")
            if hour > 11 else "morning"))
        for hour in range(24)])
    return render_template('menu.html',
        options=option_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
