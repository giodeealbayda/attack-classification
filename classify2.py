#!/usr/bin/python
import MySQLdb

#get from db
#connect to db
db = MySQLdb.connect(host="localhost",
			user = "root",
			passwd = "root",
			db = "mydb")

#create cursor object
cursor = db.cursor()


# GET ATTACKS WITHIN THE LAST SEVEN DAYS
#cursor.execute("select * from attack where attack_date between date_sub(now(), INTERVAL 1 week) and now()")
#week_attack = cursor.fetchall()

# get attacks within timeframe (to be monitored)
cursor.execute("SELECT a.attackid, a.source_ip, a.source_port, a.attackerID, a.destination_ip, a.destination_port, a.victimid, a.attack_name, a.protocol, a.level, a.attack_date, ap.to_monitor " 
"FROM attack a, attack_persistence ap, victim v " +
"WHERE a.attackID=ap.attackID AND a.victimID=v.victimID and ap.to_monitor=1 ORDER BY attackid")
week_attack = cursor.fetchall()

persistence_basis = 7.0 # 7 days

# per attack per attacker
cursor.execute("select a.attack_name, count(a.attack_name), a.attackerID from attack a, attack_persistence ap where ap.to_monitor = 1 and a.attackID = ap.attackID group by a.attack_name, a.attackerID");
to_evaluate = cursor.fetchall()

# get list of hp users na victim
cursor.execute("select hp.victimID from high_priority_users hp, victim v WHERE v.victimID = hp.victimID")
hp_users = cursor.fetchall()

i=0;
for row in week_attack:
	print row[0]

for row in to_evaluate:
	print row[0], ": ", row[1]


for row in to_evaluate:
	attack_rate = float(row[1])/persistence_basis

	i=0	
	for row1 in week_attack:
	
		if row[2]==row1[3]: # for the particular attacker only
			attackid = row1[0]
			protocol = row1[8]
			response = "none"


			if int(row1[1]) == 1: #high priority user
				response = "ACL Block (high priority)";
		
			# low priority users
			else: 
				if attack_rate > 1: # high
					response = "ACL Block!";

				elif attack_rate < 0.5: # low
					response = "ACL Block 2 days";
	
					if protocol == "TCP":
						response += " TCP Reset";

				else: # medium
	
					if protocol == "TCP":
						response += " TCP Reset";
	
#			print i, ": ", response
			i+=1
