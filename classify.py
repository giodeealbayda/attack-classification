#!/usr/bin/python
import MySQLdb
import datetime

# connect to db
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="siera_final")

# create cursor
cursor = db.cursor()

#get latest attack interval
cursor.execute("SELECT tl.interval_number from time_persistence_interval tl order by tl.timestamp desc limit 1")
numdays=cursor.fetchall()

for row1 in numdays:
	interval = row1[0]

# select ALL attacks within timerange
#cursor.execute("set @date = (select timestamp from attack_log where attack_log_id=" + str(attack_log_id) +"); select attack_log_id, @date from attack_log where timestamp between date_sub(@date, interval "+interval+" day) and @date");
#	"set @date = (select timestamp from attack_log 
#select al.attack_log_id, al.timestamp, al.source_ip, al.sour
cursor.execute("SELECT al.attack_log_id, al.timestamp, al. source_ip, al.source_port, al.destination_ip, al.destination_port, al.attack_id, al.role_id FROM attack_log al, time_persistence_interval tpi where al.timestamp < date_add(al.timestamp, interval tpi.interval_number day);")


#set @date = (select timestamp from attack_log where attack_log_id=8);
#select attack_log_id, @date from attack_log where timestamp between date_sub(@date, interval 7 #day) and  @date;
#cursor.execute("select * from attack_log order by attack_log_id");
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

	# get latest timestamp
#	cursor.execute("select timestamp from attack_log where attack_log_id="+str(attack_log_id) )
#	end_date_record = cursor.fetchall()

#	for i in end_date_record:
#		end_date=end_date_record[0]


#	DD = datetime.timedelta(days=interval)
#	start_date = end_date[0] - DD
	# calculate attack persistence
#	cursor.execute("select count(al.attack_id) from attack_log al, time_persistence_interval tpi where al.source_ip='" +str(source_ip)+ "' and al.attack_id=" + str(attack_id) + " and al.attack_log_id<"+str(attack_log_id) + " and al.timestamp between '"
#+str(start_date)+"' and '"+str(end_date[0])+"'")
#" and CURRENT_TIMESTAMP")
#'"+str(end_date[0])+"'" )
#select al.attack_log_id  from attack_log al, time_persistence_interval tpi where date_sub(tpi.timestamp, INTERVAL 7 day);
#	print end_date[0]
#	print DD
#	print start_date

	print source_ip
	cursor.execute("set @date = (select timestamp from attack_log where attack_log_id="+str(attack_log_id)+ "); ")
	cursor.execute("select count(al.attack_id) from attack_log al, time_persistence_interval tpi where al.timestamp between date_sub(@date, interval tpi.interval_number day) and @date " +
		"and al.source_ip='"+ str(source_ip) + "' and al.attack_log_id<"+str(attack_log_id) +" and al.attack_id=" +str(attack_id))
#select count(al.attack_id) from attack_log al where timestamp between date_sub(@date, interval 7 day) and  @date
#and al.source_ip='209.193.76.194' and al.attack_id=1;
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

				if role_id==1: # hp low tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=1 and protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "ACL"
					response=1

				else: # ru low-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=1 and  protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "TCP RESET + 2 DAYS ACL"
					response=2

			else: # non-tcp

				if role_id==1: # hp non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=1 and protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "ACL"
					response=1

				else: # ru non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=1 and protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
#					print "2 DAYS ACL"
					response=3

		elif attack_rate_id==2: #medium
			if protocol_type=="tcp": # tcp

				if role_id==1: #high_priority medium tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=2 and protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user medium tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=2 and  protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=4
#					print "TCP RESET + 5 DAYS ACL"

			else: # non-tcp

				if role_id==1: #high_priority medium non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=2 and  protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user medium non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=2 and  protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=5
#					print "5 DAYS ACL"

		else: # high (attack_rate_id = 3)

			if protocol_type=="tcp": # high tcp
				if role_id==1: #high_priority high tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=3 and  protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user high tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and attack_rate_id=3 and  protocol_type='tcp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

			else: # high non-tcp
				if role_id==1: #high_priority non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=1 and attack_rate_id=3 and  protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

				else: #regular_user non-tcp
					cursor.execute("select metric_id from metric_conjunction where role_id=2 and  attack_rate_id=3 and  protocol_type='udp'")
					metric_id=cursor.fetchone()
					metric_id=metric_id[0]
					response=1
#					print "ACL"

		# check there is existing response id
		cursor.execute("select response_id from response where persistence_id="+str(persistence_id))
		response_id=cursor.fetchall()
		
		if len(response_id)==0:
			#print "NEW"
			cursor.execute("insert into response (timestamp, persistence_id, interval_id, attack_rate_id, metric_id, status) values (CURRENT_TIMESTAMP, " + str(persistence_id) + ", " + str(interval_id) + ", " + str(attack_rate_id) + " , " + str(metric_id) + ", '0' )")
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
				#print a[0]
				print ' '
