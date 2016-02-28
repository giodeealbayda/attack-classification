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

cursor.execute("SELECT a.attackID, a.source_ip, a.source_port, a.attackerID, a.destination_ip, a.destination_port, a.victimID, a.attack_name, a.protocol, a.level, a.attack_date, ap.to_monitor "
" FROM attack a, attack_persistence ap, victim v, high_priority_users hp"
" WHERE a.attackID=ap.attackID and a.victimID=v.victimID and ap.to_monitor=1 AND hp.victimID=a.victimID")
hp_attack=cursor.fetchall()

cursor.execute("select a.attackID, a.source_ip, a.source_port, a.attackerID, a.destination_ip, a.destination_port, a.victimID, a.attack_name, a.protocol, a.level, a.attack_date "
"	from attack a LEFT JOIN ( "
"	select v.victimID from victim v left join high_priority_users hp on hp.victimID=v.victimID where hp.victimID is null "
"	) b on b.victimID=a.victimID "
" where b.victimID is not null "
)
not_hp_attack=cursor.fetchall()

# get list of hp users na victim
cursor.execute("select hp.victimID from high_priority_users hp, victim v WHERE v.victimID = hp.victimID")
hp_users = cursor.fetchall()

# per attack per attacker
cursor.execute("select a.attack_name, count(a.attack_name), a.attackerID from attack a, attack_persistence ap where ap.to_monitor = 1 and a.attackID = ap.attackID group by a.attack_name, a.attackerID");
to_evaluate = cursor.fetchall()

# set hp attack to block (ACL BLOCK)
for entry in hp_attack:
	response = "ACL Block"
	# write response as acl
	print "Attack ID: ", entry[0], response

print "---"

persistence_basis = 7.0 # 7 days

for entry in to_evaluate: #  
	attack_rate = float(entry[1])/persistence_basis

	for row1 in not_hp_attack:
		
		if entry[2]==row1[3]: # for the particular attacker only
			attackid = row1[0]
			protocol = row1[8]
			response = ""

			if attack_rate > 1: # high
				response = "(high rate) ACL Block!";

			elif attack_rate < 0.5: # low
				response = "(low rate) ACL Block 2 days";
	
				if protocol == "tcp":
					response += " TCP Reset";

			else: # medium

				if protocol == "tcp":
					response += "(medium) TCP Reset ";
	
			print row1[0], ": ", response
