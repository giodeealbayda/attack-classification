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
		# double check if may entry na
		cursor.execute("select * from attack_persistence where attack_log_id=" + str(attack_log_id) )
		check_entry = cursor.fetchall()
		
		if len(check_entry)==0:
			a = "insert into attack_persistence (attack_log_id, persistence_count) values (" + str(attack_log_id) + ", " + str(value) + ")"
			cursor.execute(a)
			#print a 
			db.commit()

		# compute for attack_rate
		cursor.execute("select * from time_persistence_interval order by interval_id desc limit 1")
		interval_record = cursor.fetchone()
		interval_id = interval_record[0]
		timestamp = interval_record[1]
		interval = interval_record[2]

		attack_rate = float(value)/float(interval)
		
		# persistence_id
		cursor.execute("select persistence_id from attack_persistence where attack_log_id=" + str(attack_log_id) )
		persistence_id = cursor.fetchone()

		# attack_rate_id
		cursor.execute("select attack_rate_id from attack_rate where value_from <=" + str(attack_rate) + " and value_to >" + str(attack_rate) )
		attack_rate_id = cursor.fetchone()
		attack_rate_id = attack_rate_id[0]
		# print attack_rate_id


		# get protocol_type
		cursor.execute("select protocol_type from attack where attack_id=" + str(attack_id) )
		protocol_type = cursor.fetchone()
		protocol_type = protocol_type[0]
	#	print attack_id, ": ", protocol_type

		# create response
#		cursor.execute("insert into response (persistence_id, interval_id, attack_rate_id, metric_id, status) values (" + str(persistence_id[0] +", " + str(interval_id) + ", " + str(attack_rate_id) , <metric_id>, 'ongoing' )
		response = "none"

		if attack_rate_id==1: # low
			if protocol_type=="tcp": # low tcp
				response = "TCP Reset + 2 days acl block"

			else:
				response = "2 days acl block"

		elif attack_rate_id==2: #medium
			if protocol_type=="tcp": # medium tcp
				response = "TCP Reset + 5 days acl block"
			else:
				response = "5 days acl block"

		else: # high (attack_rate_id = 3)
			response = " forever acl block"


		print response

