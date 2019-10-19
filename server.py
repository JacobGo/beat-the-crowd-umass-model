#!/usr/bin/env python
# coding: utf-8


# load data from postgres database into pandas dataframe
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('postgresql://jacob:password@206.189.69.98:5432/umass_dining')
df     = pd.read_sql_query("select * from business where location_title='Worcester Dining Commons';", con=engine)
df     = df.rename({'timestamp':'ds', 'business_level': 'y'}, axis = 1);

# setting business level to None if its closed
from datetime import datetime

def check_if_closed(row):
    time = row.ds.time()
    if (time < row.closing_hours and time > row.opening_hours):
        try: 
            return row.y
        except AttributeError:
            return row.yhat
    else:
        return None
    
df['y']  = df.apply(check_if_closed, axis = 1)



from fbprophet import Prophet
m = Prophet()
m.fit(df)


# from fbprophet.diagnostics import cross_validation
# from fbprophet.plot import plot_cross_validation_metric
# df_cv = cross_validation(m, period='10 hour', horizon = '6 hours')




# fig = plot_cross_validation_metric(df_cv, metric = 'mae')
# df_cv.head(200)

horizon = 36
future = m.make_future_dataframe(periods=horizon, freq = 'H')
forecast = m.predict(future)

forecast['yhat'] = forecast.yhat.clip(lower=0)
forecast['yhat_lower'] = forecast.yhat_lower.clip(lower=0)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(36)




from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)
CORS(app)

@app.route('/predict_graph',methods=['GET'])
def predict_graph():
    fig = m.plot(forecast)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/predict', methods=['GET'])
def predict():
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(36)
    return data.to_json(orient='records', date_format='iso')

app.run(debug=False, host='206.189.69.98', port=80)



