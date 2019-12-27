import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, Integer, String, Float, Text, inspect

from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def months():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    #precipatation = session.query(Measurement.prcp).order_by(Measurement.date.desc()).all().date
    date_end = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    last_12 = dt.datetime.strptime(date_end, '%Y-%m-%d') - dt.timedelta(days=365)

    last_12_data = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= last_12).\
                    group_by(Measurement.date).all()
    my_dict={}
    for tup in last_12_data:
        my_dict[tup[0]]=tup[1]

    session.close()

    return jsonify(my_dict)

@app.route("/api/v1.0/stations")
def station_func():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    no_stations = session.query(Station.name).count()

    station_list = session.query(Measurement.station).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()


    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_list))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def m_tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    date_end = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    last_12 = dt.datetime.strptime(date_end, '%Y-%m-%d') - dt.timedelta(days=365)

    last_12_data = session.query(Measurement.date, func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= last_12).\
                    group_by(Measurement.date).all()
    temp_dict={}
    for tup in last_12_data:
        temp_dict[tup[0]]=tup[1]


    session.close()

    return jsonify(temp_dict)



@app.route("/api/v1.0/<start>)
def date_start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
def calc_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date)all()

    session.close()

    return jsonify(calc_temps(<start_date>))

if __name__ == '__main__':
    app.run(debug=True)