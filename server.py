
# coding: utf-8

# In[1]:


#ML/AI 
from datetime import datetime
from fbprophet import Prophet
from matplotlib import pyplot

def contri(p):
    return p

#This function is the one that removes all the invalid data points that helps us refine the train and test data that 
# helps us improve the accuracy of the prophet time series prediction model. This function makes sure that the model
# only trains on data points that are in the timestamps where the dinning commons is open. 
def check_if_closed(row):
    time = row.ds.time()
    if (time < row.closing_hours and time > row.opening_hours):
        try: 
            return row.y
        except AttributeError:
            return row.yhat
    else:
        return None
# This is the main function that builds and runs the model. The location name will be passed in based on the user input
# and the function will fetch the data based on the location tittle from the overall dataset up untill the most recent 
# data and train the model based on that to predict the future busy-ness levels. 
def build_model(location_title):
    print('Training', location_title)
    df     = pd.read_sql_query(f"select * from business where location_title=$${location_title}$$;", con=engine)
    df     = df.rename({'timestamp':'ds', 'business_level': 'y'}, axis = 1)
    
    # setting business level to None if its closed
    df['y']  = df.apply(check_if_closed, axis = 1)
    
    if df['y'].count() < 3:
        return None
    # fit model
    m = Prophet() # We use the FB Prophet API to make a model that has some defaults set based on the documentation. 
    m.add_country_holidays(country_name='US')# We have our model trained on the standard United States Holidays in 
                                             # order to increase the accuracy of the model.  
    m.fit(df)# The fit function fits the data we have fed it into a format that the model can learn on. 
    
    horizon  = 24
    future   = m.make_future_dataframe(periods=horizon, freq = 'H')# This makes a dataframe of future timestamps and 
                                                                   # makes the model spit out predictions based on how 
                                                                   # far in the future we want it. 
    forecast = m.predict(future) #This is the nbuilt predict functionality that we used to make the predictions

    forecast['yhat'] = forecast.yhat.clip(lower=0)
    forecast['yhat_lower'] = forecast.yhat_lower.clip(lower=0)
    #fig1 = m.plot(forecast)
    return forecast # This finally returns the forecasted results. 


# In[2]:


#Data 

# load data from postgres database into pandas dataframe
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://jacob:password@206.189.69.98:5432/umass_dining') # using a query to get the user input.
models = {} #Making a dictionary so we can train same model onmultiple locations
location_titles = pd.read_sql_query("select distinct(location_title) from business", con=engine);
for location_title in location_titles['location_title']:
    models[location_title] = build_model(location_title) # We have a dictionary of models so we have the forecasted data of all dinning commons. 


# In[ ]:


#Server
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__) #Sets up the flask server where the Web Application and the Mobile Application will be hosted locally for now. 
CORS(app)

# @app.route('/predict_graph',methods=['GET'])
# def predict_graph():
#     fig = m.plot(forecast)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

@app.route('/predict', methods=['GET'])
#this fucntion helps us interact with the front end and send back the predicted values to the user. 
def predict():
    location_title = request.args.get('location_title')
    forecast = models[location_title]
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(24)
    return data.to_json(orient='records', date_format='iso')

app.run(debug=False, host='0.0.0.0', port=5000)



