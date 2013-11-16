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
    

@app.route('/')
def hello_world():
    location = "It's four  o'clock in the morning in ";
    four_places = [time_zone.split("/")[1].replace("_"," ")
        for time_zone in pytz.all_timezones
        if(time.now(timezone(time_zone)).hour == 4
        and len(time_zone.split("/")) == 2
        and len(re.findall("[0-9]",time_zone)) == 0)]
    print four_places
    return render_template('four.html', loc=choice(four_places))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
