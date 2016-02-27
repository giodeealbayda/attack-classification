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


	# per attack per attacker
	cursor.execute("select distinct(attack_id), count(source_ip), source_ip from attack_log al where attack_id="+str(attack_id)+" group by attack_id")
	persistence_list=cursor.fetchall()

	if role_id==1:
		# permanent block
		print "HIGH PRIORITY"
	else:
		#update persistence_count per attack per attacker
	
		for row1 in persistence_list:
			attack_id1=row1[0]
			count=row1[1]
			source_ip1=row[2]
		
			print i, ": ", attack_id1, ": ", source_ip1

			# calculate persistence
			cursor.execute("select ap.persistence_id, ap.attack_log_id, ap.timestamp, ap.persistence_count "
			"from attack_persistence ap, attack_log al "
			"where al.attack_id="+str(attack_id1)+" "
			"and al.source_ip = '"+str(source_ip1)+"' "
			"order by ap.persistence_id desc")
			persistence_list = cursor.fetchall()

		
			if len(persistence_list)==0: # first entry
				cursor.execute("insert into attack_persistence (attack_log_id, persistence_count) values (" + str(attack_log_id) + ", 1)")
				db.commit()

			else:
				cursor.execute("insert into attack_persistence (attack_log_id, persistence_count) values (" + str(attack_log_id) + "," + str(i) + " )" )
				db.commit()
		
	#		cursor.execute("select ap.persistence_id, ap.attack_log_id, ap.timestamp, ap.persistence_count "
	#		"from attack_persistence ap "
	#		"left join attack_log al "
	#		"on al.attack_id="+str(attack_id1) + " " +
	#		"where ap.attack_log_id is null")
	#		persistence_attack_logs=cursor.fetchall()
			print "----"
	#		for row2 in persistence_attack_logs:

	#			persistence_size = len(persistence_attack_logs) + 1
	#			print persistence_size
	#			insert_persistence = "insert into attack_persistence (attack_log_id, persistence_count) values (" +str(attack_log_id) + ", " + str(persistence_size) + ")"
	#			print insert_persistence
	#			cursor.execute(insert_persistence)
	#			db.commit()	
	
# set response
