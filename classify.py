#!/usr/bin/python
import MySQLdb

# connect to db
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="siera_final")

# create cursor
cursor = db.cursor()

# select ALL attacks
cursor.execute("SELECT * FROM attack_log") # lacking: specify yung time
all_attack_log=cursor.fetchall()

for row in all_attack_log:
	attack_log_id=row[0]
	timestamp=row[1]
	source_ip=row[2]
	source_port=row[3]
	destination_ip=row[4]
	destination_port=row[5]
	attack_id=row[6]
	role_id=row[7]

	

# calculate persistence
cursor.execute("select ap.persistence_id, ap.attack_log_id, ap.timestamp, ap.persistence_count "
"from attack_persistence ap "
"left join attack_log al "
"on al.attack_log_id=ap.attack_log_id")
persistence_attack_logs=cursor.fetchall()

persistence_size = len(persistence_attack_logs)
# create new entry in attack_persistence
create_persistence = ("insert into attack_persistence (attack_log_id, timestamp, persistence_count) VALUES (%s, %s, %s")

# set response
