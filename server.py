#!/usr/bin/env python
# coding: utf-8

# In[110]:


from datetime import datetime
from fbprophet import Prophet

def check_if_closed(row):
    time = row.ds.time()
    if (time < row.closing_hours and time > row.opening_hours):
        try: 
            return row.y
        except AttributeError:
            return row.yhat
    else:
        return None
    
def build_model(location_title):
    print('Training', location_title)
    df     = pd.read_sql_query(f"select * from business where location_title=$${location_title}$$;", con=engine)
    df     = df.rename({'timestamp':'ds', 'business_level': 'y'}, axis = 1)
    
    # setting business level to None if its closed
    df['y']  = df.apply(check_if_closed, axis = 1)
    
    if df['y'].count() < 3:
        return None
    # fit model
    m = Prophet()
    m.add_country_holidays(country_name='US')
    m.fit(df)
    
    horizon  = 24
    future   = m.make_future_dataframe(periods=horizon, freq = 'H')
    forecast = m.predict(future)

    forecast['yhat'] = forecast.yhat.clip(lower=0)
    forecast['yhat_lower'] = forecast.yhat_lower.clip(lower=0)
    
    return forecast



    
    


# In[111]:


# load data from postgres database into pandas dataframe
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://jacob:password@206.189.69.98:5432/umass_dining')
models = {}
location_titles = pd.read_sql_query("select distinct(location_title) from business", con=engine);
for location_title in location_titles['location_title']:
    models[location_title] = build_model(location_title)


# In[86]:


# from fbprophet.diagnostics import cross_validation
# from fbprophet.plot import plot_cross_validation_metric
# df_cv = cross_validation(m, period='10 hour', horizon = '6 hours')


# In[87]:


# fig = plot_cross_validation_metric(df_cv, metric = 'mae')
# df_cv.head(200)


# In[99]:


# import numpy as np
# import matplotlib.pyplot as plt


# fig = m.plot(forecast)
# fig = m.plot_components(forecast)


# np.mean(np.abs(df['y'] - forecast['yhat']))


# In[ ]:


from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)
CORS(app)

# @app.route('/predict_graph',methods=['GET'])
# def predict_graph():
#     fig = m.plot(forecast)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

@app.route('/predict', methods=['GET'])
def predict():
    location_title = request.args.get('location_title')
    forecast = models[location_title]
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(24)
    return data.to_json(orient='records', date_format='iso')

app.run(debug=False, host='0.0.0.0', port=5000)


# In[ ]:




