#!/usr/bin/env python3


import requests



url = 'https://api.darksky.net/forecast/476f7bc9a1b6f074eb62c9f023dcef9a/42.3868,-72.5301'

headers = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}
response = requests.get(url, headers=headers)



import psycopg2
import json
import datetime

connection = psycopg2.connect(user = "jacob",
                              password = "password",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "umass_dining")

cursor = connection.cursor()

weather = response.json()['currently']

'''
create table weather (precipIntensity FLOAT, 
                      precipProbability FLOAT,
                      temperature FLOAT, 
                      apparentTemperature FLOAT, 
                      humidity FLOAT, 
                      windSpeed FLOAT, 
                      summary TEXT, 
                      timestamp timestamp default (current_timestamp at time zone 'est'),
                      PRIMARY KEY (timestamp)
                      );
'''

cursor.execute(f" INSERT INTO weather VALUES ( {weather['precipIntensity']}, \
                                               {weather['precipProbability']}, \
                                               {weather['temperature']}, \
                                               {weather['apparentTemperature']}, \
                                               {weather['humidity']}, \
                                               {weather['windSpeed']}, \
                                               $${weather['summary']}$$ \
                                                );")
connection.commit()
cursor.close()
connection.close()