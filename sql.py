# execute the SQL query for attack.
cursor.execute("select * from attack")
attack_record = cursor.fetchall()

for row in attack:
	attackID = row[0]
	source_ip = row[1]
	source_port = row[2]
	attackerID = row[3]
	destination_ip = row[4]
	destination_port = row[5]
	victimID = row[6]
	attack_name = row[7]
	protocol = row[8]
	level = row[9]
	attack_date = row[10]

#	print "\n\n--- Attack: ", attackID, ": ", source_ip, ":" source_port, ": ", attackerID, ": ",  destination_ip, ":", destination_port, ": ", victimID, ": ", attack_name, ": ", protocol, ": ", level, ": ", attack_date

#attack information
attack = {
	'source_ip': source_ip,
	'source_port': source_port,
	'attackerID': attackerID,
	'destination_ip': destination_ip,
	'destination_port': destination_port,
	'victimID': victimID,
	'protocol': protocol,
	'level': level,
	'attack_date': attack_date
}

# create attack
create_attack = ("INSERT INTO attack (source_ip, source_port, attackerID, destination_ip, destination_port, victimID, attack_name, protocol, level, attack_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s")
cursor.execute(create_attack, attack)
cursor.commit()

# edit attack
edit_attack = cursor.execute("""
UPDATE attack SET source_ip=%s, source_port=%s, attackerID=%s, destination_ip=%s, destination_port=%s, victimID=%s, attack_name=%s, protocol=%s, level=%s, attack_date=%s WHERE attackID==%s
""", (source_ip, source_port, attackerID, destination_ip, destination_port, victimID, protocol, level, attack_date) )

# delete attack
delete_attack = cursor.execute("DELETE FROM attack WHERE attackID==%s" % (attackID) )


# execute the SQL query for attacker.
cursor.execute("select * from attacker")
attacker_record = cursor.fetchall()

attacker {
	'ip_address': ip_address
}

# create attacker
create_attacker = ("INSERT INTO attacker (ip_address) values (%s)")
cursor.execute(create_attacker, attacker)
cursor.commit()

for row in attacker:
	attackerID = row[0]
	ip_address = row[1]

#	print "\n\n--- Attacker: ", attackerID, ": ", ip_address

# edit attacker
edit_attacker = cursor.execute("""
UPDATE attacker SET ip_address=%s WHERE attackerID==%s
""", (ip_address, attackerID) )

# delete attacker
delete_attacker = cursor.execute("DELETE FROM attacker WHERE attackerID==%s" % (attackerID) )

# execute the SQL query for attack_persistence.
cursor.execute("select * from attack_persistence")
attack_persistence_record = cursor.fetchall()

attack_persistence {
	'attackID': attackID,
	'to_monitor': to_monitor,
	'response': response
	
}

for row in attack_persistence:
	attackpersistenceID = row[0]
	attackID = row[1]
	to_monitor = row[2]
	response = row[3]

#	print "\n\n---Attack Persistence: ", attackpersistenceID, ": ", attackID, ": ", to_monitor, ": ", response

# create attack persistence
create_attack_persistence = ("INSERT INTO attack_persistence (attackID, to_monitor, response) VALUES (%s, %s, %s)")
cursor.execute(create_attack_persistence, attack_persistence)
cursor.commit()

# edit attack persistence
edit_attack_persistence = cursor.execute("""
UPDATE attack_persistence SET attackID=%s, to_monitor=%s, response=%s WHERE attackpersistenceID==%s
""", (attackID, to_monitor, response, attackpersistenceID) )
# delete attack persistence

# execute the SQL query for permanent_block
cursor.execute("select * from Permanent_Block")
permanent_block = cursor.fetchall()

for row in permanent_block:
	permanent_blockID = row[0]
	responseID = row[1]

#	print"\n\n--- Permanent Block: ", permanent_blockID, ": ", responseID

# execute the SQL query for TCP reset.
cursor.execute("select * from TCP_Reset")
tcp_reset = cursor.fetchall()

for row in tcp_reset:
	tcp_resetID = row[0]
	responseID = row[1]

#	print"\n\n--- TCP Reset: ", tcp_resetID, ": ", responseID

# execute the SQL query for Timebased Block
cursor.execute("select * from Timebased_Block")
timebased_block = cursor.fetchall()

for row in timebased_block:
	timebased_blockID = row[0]
	responseID = row[1]
	time_blocked = row[2]



# execute the SQL query for time_interval_persistence.
#cursor.execute("select * from time_interval_persistence")
#time_interval_persistence = cursor.fetchall()

#for row in time_interval_persistence:
#	time_interval_persistenceID = row[0]
#	time_persistence = row[1]
#	time_interval_date = row[2]

#	print "\n\n---Time Interval Persistence: ", time_interval_persistenceID, ": ", time_persistence, ": ", time_interval_date

# execute the SQL query for Victim.
cursor.execute("select * from victim")
victim = cursor.fetchall()

for row in victim:
	victimID = row[0]
	ip_address = row[1]
	name = row[2]
	role = row[3]

#	print"\n\n--- Victim: ", victimID, ": ", ip_address, ": ", name, ": ", role

