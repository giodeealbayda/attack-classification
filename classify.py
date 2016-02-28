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
	i=0

	attack_log_id=row[0]
	timestamp=row[1]
	source_ip=row[2]
	source_port=row[3]
	destination_ip=row[4]
	destination_port=row[5]
	attack_id=row[6]
	role_id=row[7]


	# calculate attack persistence
	cursor.execute("select count(attack_id) from attack_log where source_ip='" +str(source_ip)+ "' and attack_id=" + str(attack_id) + " and attack_log_id<"+str(attack_log_id) )
	persistence_list=cursor.fetchall()

	# insert into attack_persistence
	for row in persistence_list:
		value = row[0]+1
		a = "insert into attack_persistence (attack_log_id, persistence_count) values (" + str(attack_log_id) + ", " + str(value) + ")"
		cursor.execute(a)
		#print a 
		db.commit()



