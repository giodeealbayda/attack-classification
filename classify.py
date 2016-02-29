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

# get num_days low attack
cursor.execute("select * from time_based_range where level='Low'")
low_num_all = cursor.fetchall()

for row in low_num_all:
	time_based_range_id_low = row[0]
	level_low = row[1]
	num_days_low = row[2]

# get num_days medium
cursor.execute("select * from time_based_range where level='Medium'")
medium_num_all = cursor.fetchall()

for row in medium_num_all:
	time_based_range_id_medium = row[0]
	level_medium = row[1]
	num_days_medium = row[2]

# select ALL attacks within timerange
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

		cursor.execute("select metric_id from metric_conjunction where role_id="+str(role_id)+" and attack_rate_id="+str(attack_rate_id)+" and protocol_type='"+str(protocol_type)+"'")
		metric_id = cursor.fetchone()
		metric_id = metric_id[0]

		print metric_id




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
		

			if metric_id==1: # tcp reset + 2 days
				for x in response_id:
					x = response_id[0]
					
					# create TCP Reset
					cursor.execute("insert into tcp_reset (response_id) values (" + str(x[0]) + ")")
					db.commit()

					# create 2 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", " + str(time_based_range_id_low) + ", NOW(), DATE_ADD(NOW(), INTERVAL + " + str(num_days_low) + " DAY) )")
					db.commit()

	
			elif metric_id==2: # tcp reset + 5 days
				for x in response_id:
					x = response_id[0]
					
					# create TCP Reset
					cursor.execute("insert into tcp_reset (response_id) values (" + str(x[0]) + ")")
					db.commit()

					# create 5 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + "," + str(time_based_range_id_medium) + ", NOW(), DATE_ADD(NOW(), INTERVAL + " + str(num_days_low) + " DAY) )")

					db.commit()
	
			elif metric_id==7: # 2 days
					# create 2 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + ", " + str(time_based_range_id_low) + ", NOW(), DATE_ADD(NOW(), INTERVAL + " + str(num_days_low) + " DAY) )")
					db.commit()

			elif metric_id==8: # 5 days
					# create 5 Days ACL
					cursor.execute("insert into time_based (response_id, num_days, block_start, block_end) values (" + str(x[0]) + "," + str(time_based_range_id_medium) + ", NOW(), DATE_ADD(NOW(), INTERVAL + " + str(num_days_low) + " DAY) )")
					db.commit()

			else: # metric_id = 3, 4, 5, 6, 9, 10, 11, 12 (ACL Block)
				for x in response_id:
					x = response_id[0] # temp for response id
#					print x[0]
					cursor.execute("insert into permanent_block (response_id, is_block, last_modified) values (" + str(x[0]) + ", 1, CURRENT_TIMESTAMP)")
					db.commit()


		else:
			for a in response_id:
				#print a[0]
				print ' '
