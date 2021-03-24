import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, inspect, or_

from flask import Flask, jsonify

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/covid_vaccine_travel")
# engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
inspector = inspect(engine)
session = Session(engine)

# for table_name in inspector.get_table_names():
# 	print("Table: %s" % table_name)
# 	for column in inspector.get_columns(table_name):
# 		print("Column: %s" % column['name'])

MTS = Base.classes.mts
OWID = Base.classes.owid

Important_Cols = [
'date',
'location',
'total_vaccinations',
'people_vaccinated',
'total_vaccinations_per_hundred',
'people_vaccinated_per_hundred',
# 'daily_vaccinations_raw',
# 'daily_vaccinations',
# 'daily_vaccinations_per_million',
'people_fully_vaccinated',
'people_fully_vaccinated_per_hundred',
]

Important_attributes = [getattr(OWID, attr) for attr in Important_Cols]
NotNull_filters = (
	OWID.total_vaccinations != None,
	OWID.people_vaccinated != None,
	OWID.total_vaccinations_per_hundred != None,
	OWID.people_vaccinated_per_hundred != None,
	OWID.people_fully_vaccinated != None,
	OWID.people_fully_vaccinated_per_hundred != None
	)

def row2dict(row):
    return {
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/api/v1.0/covid_data")
def covid_data():
	results = session.query(*[getattr(OWID, attr) for attr in Important_Cols]).limit(10).all()
	rows = [ row2dict(result) for result in results]
	return jsonify(rows) 

@app.route("/api/v1.0/covid_data/<location>")
def covid_data_location(location="United States"):
	results = session \
		.query(*Important_attributes) \
		.with_entities(*Important_attributes) \
		.filter(OWID.location == location) \
		.filter(*NotNull_filters) \
		.all() 
	return jsonify(results) 

@app.route("/api/v1.0/covid_data_ab/<locationa>/<locationb>")
def covid_data_ab_location(locationa="United States", locationb="Israel"):
	results = session \
		.query(*Important_attributes) \
		.with_entities(*Important_attributes) \
		.filter(or_(OWID.location == locationa, OWID.location == locationb)) \
		.filter(*NotNull_filters) \
		.order_by(OWID.date.asc()) \
		.all() 
	return jsonify(results) 


if __name__ == '__main__':
	app.run(debug = True)

