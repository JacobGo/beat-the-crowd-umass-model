# building model

# load data from postgres database into pandas dataframe
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('postgresql://jacob:password@206.189.69.98:5432/umass_dining')
df     = pd.read_sql_query("select * from business where location_title='Worcester Dining Commons';", con=engine)
df     = df.rename({'timestamp':'ds', 'business_level': 'y'}, axis = 1);

# setting business level to 0 if its closed
from datetime import datetime

def check_if_closed(row):
    time = row.ds.time()
    if (time < row.closing_hours and time > row.opening_hours):
        return row.y
    else:
        return 0
    
df['y']  = df.apply(check_if_closed, axis = 1)

from fbprophet import Prophet
m = Prophet()
m.fit(df)




# serving model
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

@app.route('/predict',methods=['POST'])
def predict():
  horizon = int(request.form['horizon'])

  future = m.make_future_dataframe(periods=horizon, freq = 'H')
  forecast = m.predict(future)
  data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(36)
  return data.to_json(orient='records', date_format='iso')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)