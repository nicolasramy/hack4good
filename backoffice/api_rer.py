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

# commute4good
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
req = "SELECT name, ST_ASTEXT(way), ref, operator, ST_Distance(ST_PointFromText('POINT(2.371886 48.879860)',4326),ST_transform(way,4326),true) AS dist " 
req += "FROM planet_osm_point WHERE railway = 'station' ORDER BY dist ASC limit 5;"
cur.execute(req)
record_list  = cur.fetchall()
dict_stations = {}
for row in range(len(record_list)):
	for column in range(len(description)):
		dict_stations[cur.description[column].name] = record_list[row]

print dict_stations
# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()