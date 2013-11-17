# -*- coding: utf-8 -*-
import sys
import datetime
import json
import urllib2

# Flask
from flask import Flask, request, jsonify, make_response, abort

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Computes distance
from numpy import arccos, arcsin, cos, sin, sqrt, pi

## commute4good
import config
from model import commute4good
import psycopg2

# Connect to an existing database
conn = psycopg2.connect(host="localhost", port=5432, database="gisdatabase", user="postgres", password="plop")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
req = "SELECT name, ST_X(way) as lon, ST_Y(way) as lat, ref, operator, ST_Distance(ST_PointFromText('POINT(%s %s)',4326),ST_transform(way,4326),true) AS dist " 
req += "FROM planet_osm_point WHERE railway = 'station' ORDER BY dist ASC limit 5;"
cur.execute(req, (2.371886, 48.879860))
record_list = cur.fetchall()
data = {}
neighbours_stations = []
for row in range(len(record_list)):
	item = {} # une station particulière
	for column in range(len(cur.description)):
		item[cur.description[column].name] = record_list[row][column]
	neighbours_stations.append(item)

data['nearest_stations'] = neighbours_stations

print jsonify(data)
# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()