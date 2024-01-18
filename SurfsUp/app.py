# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, redirect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Placing reused code here so it can be used in multiple routes
most_recent_date = session.query(measurement.date).\
    order_by(measurement.date.desc()).first()[0]
    
year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') \
    - dt.timedelta(days = 366)

active_stations = session.query(measurement.station, func.count(measurement.station))\
        .group_by(measurement.station)\
        .order_by(func.count(measurement.station).desc())\
        .all()
    
most_active_station = active_stations[0][0]

# Beginning of the routes:
# Welcome page that lists all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"<h3><center>Welcome to the Hawaii Stations API!</center></h3>"
        f"<p><b>Available Routes:</b></p>"
        f"<b>/api/v1.0/precipitation</b> -- the date and amount of precipitation \
            each day for the last year of collection<br/>"
        f"<b>/api/v1.0/stations</b> -- the list of all the stations, by code and name<br/>"
        f"<b>/api/v1.0/tobs</b> -- the list of temperature readings for the \
            most active station ({most_active_station}) in the last year of data collection<br/>"
        f"<b>/api/v1.0/start</b> -- replace 'start' with a date (YYYY-MM-DD) \
            to see the minimum, maximum, and average temperature \
            after that start date.<br/>"
        f"<b>/api/v1.0/start/end</b> -- replace 'start' and 'end' with dates \
            (YYYY-MM-DD) to see the minimum, maximum, and average \
            temperature between those dates, inclusive<br/><br/>"
        f"<b>/api/v1.0/secret</b> -- if you dare"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_query = session\
        .query(measurement.date, measurement.prcp)\
        .filter(measurement.date >= year_ago)\
        .filter(measurement.date <= most_recent_date)\
        .all()
    
    precip_dict = {date: prcp for (date, prcp) in precip_query}
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_query = session\
        .query(station.station, station.name).all()
    
    station_list = list(np.ravel(station_query))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session\
        .query(measurement.date, measurement.tobs)\
        .filter(measurement.date >= year_ago)\
        .filter(measurement.date <= most_recent_date)\
        .filter(measurement.station == most_active_station)\
        .order_by(measurement.date)\
        .all()
    
    tobs_list = list(np.ravel(tobs_query))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start = None, end = None):
    # I wanted to make sure the values for start and end were valid and I found
    # that the datetime library had the fromisoformat method that could do so.
    # This verifies that both the start and end values entered are actually dates.
    try:
        if start:
            dt.date.fromisoformat(start)
        elif end:
            dt.date.fromisoformat(end)
    except:
        return jsonify({"error": f"Date(s) entered were not properly formatted (YYYY-MM-DD)"})

    # I wanted to make sure that the start date came before the end date,
    # that the end date came after the earliest date in the data, and that
    # the start date came before the latest date in the data. This ensures 
    # that happens. I could have used a try/except block, but each case required
    # a specific response.
    if end:
        if start > end:
            return jsonify({"error": f"Start date occurs after end date. Please try again."}), 404
        elif end < session.query(measurement.date).order_by(measurement.date).first()[0]:
            return jsonify({"error": f"End date occurs before first date with data. Please try again."}), 404
    elif start > most_recent_date:
        return jsonify({"error": f"Start date occurs after most recent date with data. Please try again."}), 404
    
    
    temps_query = session\
        .query(func.min(measurement.tobs),\
            func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start)
        
    if not end:
        temps_list = list(np.ravel(temps_query.all()))
        
        return jsonify(temps_list)
    else:
        temps_query = temps_query.filter(measurement.date <= end).all()
        
        temps_list = list(np.ravel(temps_query))

        return jsonify(temps_list)

@app.route('/api/v1.0/secret')
def reroute():
    return redirect('https://www.youtube.com/watch?v=o-YBDTqX_ZU')
    
if __name__ == '__main__':
    app.run(debug = True)