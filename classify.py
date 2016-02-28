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
		persistence_id=persistence_id[0]

		# attack_rate_id
		cursor.execute("select attack_rate_id from attack_rate where value_from <=" + str(attack_rate) + " and value_to >" + str(attack_rate) )
		attack_rate_id = cursor.fetchone()
		attack_rate_id = attack_rate_id[0]
		# print attack_rate_id


		# get protocol_type
		cursor.execute("select protocol_type from attack where attack_id=" + str(attack_id) )
		protocol_type = cursor.fetchone()
		protocol_type = protocol_type[0]


		response = 0
		metric_id=0
		if attack_rate_id==1: # low
			if protocol_type=="tcp": # low tcp

				if role_id==1: # low tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=1")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "ACL"
					response=1

				else: # regular_user non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=1")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "TCP RESET + 2 DAYS ACL"
					response=2

			else: # non-tcp

				if role_id==1: # high_priority non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=1")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "ACL"
					response=1

				else: # regular_user non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=1")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "2 DAYS ACL"
					response=3

		elif attack_rate_id==2: #medium
			if protocol_type=="tcp": # medium tcp

				if role_id==1: #high_priority medium tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=2")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user medium tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate=2")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=4
#					print "TCP RESET + 5 DAYS ACL"

			else: # non-tcp

				if role_id==1: #high_priority medium non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate=2")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user medium non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate=2")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=5
#					print "5 DAYS ACL"

		else: # high (attack_rate_id = 3)

			if protocol_type=="tcp": # high tcp
				if role_id==1: #high_priority high tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate=3")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user high tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate=3")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

			else: # high non-tcp
				if role_id==1: #high_priority non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate=3")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate=3")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

		# check there is existing response id
		cursor.execute("select response_id from response where persistence_id="+str(persistence_id))
		response_id=cursor.fetchall()
		
		if len(response_id)==0:
			#print "NEW"
			cursor.execute("insert into response (timestamp, persistence_id, interval_id, attack_rate_id, metric_id, status) values (CURRENT_TIMESTAMP, " + str(persistence_id) + ", " + str(interval_id) + ", " + str(attack_rate_id) + " , " + str(metric_id) + ", 'ongoing' )")
			db.commit()
			
			# get current response id
			cursor.execute("select response_id from response where persistence_id="+str(persistence_id))
			response_id=cursor.fetchall()
		
			if response==1: # Permanent ACL
				for x in response_id:
					x = response_id[0] # temp for response id
#					print x[0]
					cursor.execute("insert into permanent_block (response_id, is_block, last_modified) values (" + str(x[0]) + ", 1, CURRENT_TIMESTAMP)")
					db.commit()

			elif response==2: # TCP Reset + 2 Days ACL
				for x in response_id:
					x = response_id[0]
					
					# create TCP Reset
					cursor.execute("insert into tcp_reset (response_id) values (" + str(x[0]) + ")")
					db.commit()

					# create 2 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", 1, NOW(), DATE_ADD(NOW(), INTERVAL + 2 DAY) )")
					db.commit()

			elif response==3: # 2 days ACL

					# create 2 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", 1, NOW(), DATE_ADD(NOW(), INTERVAL + 2 DAY) )")
					db.commit()

			elif response==4: # TCP Reset + 5 Days ACL
				for x in response_id:
					x = response_id[0]
					
					# create TCP Reset
					cursor.execute("insert into tcp_reset (response_id) values (" + str(x[0]) + ")")
					db.commit

					# create 5 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", 2, NOW(), DATE_ADD(NOW(), INTERVAL + 5 DAY) )")
					db.commit()

			elif response==5: # 5 days ACL

					# create 5 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", 2, NOW(), DATE_ADD(NOW(), INTERVAL + 5 DAY) )")
					db.commit()


		else:
			for a in response_id:
				print a[0]
