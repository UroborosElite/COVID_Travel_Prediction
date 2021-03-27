import datetime as dt
import json

import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from config import username, password

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, inspect, or_
import matplotlib.pyplot as plt

from flask import Flask, jsonify

engine = create_engine(f"postgres://{username}:{password}@ec2-52-7-115-250.compute-1.amazonaws.com:5432/doai2olijqiuk")
# engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

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
	locationList = json.loads(covid_locations().data)
	return render_template("index.html", locationList=locationList)

@app.route("/api/v1.0/covid_data")
def covid_data():
	results = session.query(*[getattr(OWID, attr) for attr in Important_Cols]).limit(10).all()
	rows = [ row2dict(result) for result in results]
	return jsonify(rows) 

@app.route("/api/v1.0/locations")
def covid_locations():
	results = session \
		.query(OWID.location) \
		.filter(*NotNull_filters) \
		.distinct() \
		.all() 
	results_arr = []
	for row in results:
		results_arr.append(row[0])
	return jsonify(results_arr)

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

@app.route("/api/v1.0/predict_fully_vaccinated/<location>")
def predict_fully_vaccinated(location="United States"):
	results = session \
		.query(OWID.date, OWID.people_fully_vaccinated_per_hundred) \
		.filter(OWID.location == location) \
		.filter(*NotNull_filters) \
		.all() 

	data_time = np.asarray([])
	data_count = np.asarray([])

	for r in results:
		data_time = np.append(data_time, r[0])
		data_count = np.append(data_count, r[1])
	
	df = pd.DataFrame({'time': data_time, 'count': data_count})
	df['conv_date'] = pd.to_datetime(df.time)
	df['conv_date'] = df['conv_date'].map(dt.datetime.toordinal)
	df.time = pd.to_datetime(df.time)

	# Linear regression
	w = np.exp(np.linspace(0,10,len(df.conv_date.values)))
	regr = LinearRegression()
	regr.fit(df.conv_date.values.reshape(-1, 1), df['count'].values.reshape(-1, 1),w)

	#Poly regression
	# poly_reg = np.polyfit(df.conv_date.values, df['count'].values, 2)
	# poly_line = np.poly1d(poly_reg)

	# Make predictions using the testing set
	pred_time = np.asarray([])
	start_date = dt.date(2021, 1, 1)
	end_date = dt.date(2021, 10, 1)
	delta = dt.timedelta(days=1)
	while start_date <= end_date:
		pred_time = np.append(pred_time, start_date)
		start_date += delta

	# y_pred = regr.predict(df.time.values.astype(float).reshape(-1, 1))
	df_pred = pd.DataFrame({'time': pred_time})
	df_pred['conv_date'] = pd.to_datetime(df_pred.time)
	df_pred['conv_date'] = df_pred['conv_date'].map(dt.datetime.toordinal)
	df_pred.time = pd.to_datetime(df_pred.time)

	# print(df_pred.to_string())
	y_pred = regr.predict(df_pred.conv_date.values.astype(float).reshape(-1, 1))
	# y_poly_pred = poly_line(df_pred.conv_date.values.astype(float).reshape(-1, 1))
	

	df_pred['pred'] = y_pred
	# df_pred['poly'] = y_poly_pred

	# ax = df.plot(x='time', y='count', color='black', style='.')
	# df_pred.plot(x='time', y='pred', color='orange', linewidth=3, ax=ax, alpha=0.5)
	# # df_pred.plot(x='time', y='poly', color='orange', linewidth=3, ax=ax, alpha=0.5)
	# ax.set_title('My Title')
	# ax.set_xlabel('Date')
	# ax.set_ylabel('Metric')
	# ax.set_ylim(0, 100)
	# plt.savefig('predict_fully_vaccinated.png')
	# df_values = df_pred.values()

	prediction_vs_real = []
	for index, row in df_pred.iterrows():
		prediction_vs_real.append([ row['time'].strftime("%Y-%m-%d"), row['pred']])
	return jsonify(prediction_vs_real)


if __name__ == '__main__':
	app.run(debug = True)

