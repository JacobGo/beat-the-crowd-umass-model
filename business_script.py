#!/usr/bin/env python3


import requests



url = 'https://umassdining.com/uapp/get_infov2'

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

for dc in response.json():
  if dc['opening_hours'] == 'Closed':
    dc['opening_hours'] = '12:00 AM'
    dc['closing_hours'] = '12:00 AM'

  cursor.execute(f" INSERT INTO business VALUES ( $${dc['location_title']}$$, \
                                                  {dc['business_level']}, \
                                                  {dc['notbusy_level']}, \
                                                  {dc['moderate_level']}, \
                                                  $${dc['opening_hours']}$$, \
                                                  $${dc['closing_hours']}$$ \
                                                  )")
connection.commit()
cursor.close()
connection.close()