#!/usr/bin/env python3


import requests
import psycopg2
import json
import datetime

connection = psycopg2.connect(user = "jacob",
                              password = "password",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "umass_dining")

cursor = connection.cursor()


cursor.execute('SELECT DISTINCT timestamp FROM business;')

times = cursor.fetchall()

for time in times:
  print(time)
  time = time[0]
  url = f'https://api.darksky.net/forecast/476f7bc9a1b6f074eb62c9f023dcef9a/42.3868,-72.5301,{time.strftime("%s")}'
  response = requests.get(url)

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

  cursor.execute(f" INSERT INTO weather VALUES ({weather['precipIntensity']}, \
                                                {weather['precipProbability']}, \
                                                {weather['temperature']}, \
                                                {weather['apparentTemperature']}, \
                                                {weather['humidity']}, \
                                                {weather['windSpeed']}, \
                                                $${weather['summary']}$$, \
                                                $${time}$$ \
                                                  );")
connection.commit()
cursor.close()
connection.close()