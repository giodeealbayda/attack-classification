#!/usr/bin/python
import MySQLdb

# connect to db
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="siera_final")

# create cursor
cursor = db.cursor()

# calculate persistence
