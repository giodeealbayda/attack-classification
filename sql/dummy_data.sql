-- create attacker
INSERT INTO `mydb`.`attacker` (`ip_address`) VALUES (inet_aton('172.16.5.4'));
INSERT INTO `mydb`.`attacker` (`ip_address`) VALUES (inet_aton('56.32.45.6'));
INSERT INTO `mydb`.`attacker` (`ip_address`) VALUES (inet_aton('45.12.32.21'));
INSERT INTO `mydb`.`attacker` (`ip_address`) VALUES (inet_aton('27.23.12.3'));
INSERT INTO `mydb`.`attacker` (`ip_address`) VALUES (inet_aton('38.56.32.2'));

-- create victim
INSERT INTO victim (ip_address, name) VALUES
(inet_aton('10.37.59.93'),'bob'),
(inet_aton('192.168.6.138'),'mary'), -- 2
(inet_aton('192.168.1.21'),'bill'),
(inet_aton('192.168.1.2'),'sarah'), -- 4
(inet_aton('192.168.1.22'),'tony'),
(inet_aton('192.168.5.3'), 'john'), -- 6
(inet_aton('192.168.27.39'), 'alice'),
(inet_aton('192.168.59.64'), 'anna'), -- 8
(inet_aton('192.168.4.45'), 'taylor'),
(inet_aton('192.168.1.13'), 'tyler'), -- 10
(inet_aton('192.168.5.32'), 'sasha'),
(inet_aton('192.168.7.35'), 'johnny'),
(inet_aton('192.168.15.32'), 'elsa'),
(inet_aton('192.168.24.32'), 'rob'),
(inet_aton('192.168.101.32'), 'carl')

-- create attack
INSERT INTO attack (source_ip, source_port, attackerID, destination_ip, destination_port, victimID, attack_name, protocol, level, attack_date) VALUES 
(inet_aton('192.168.1.26'), 3121, 5, inet_aton(192.168.2.136), 3121, 5, 'tcp attack 1', 'tcp', 3, '2016-02-23 15:41:29'),
(inet_aton('192.168.5.137'), 2685, 14, inet_aton('192.168.6.138'), 2685, 2, 'udp attack 2', 'udp', 3, '2016-02-23 15:46:29'),
(inet_aton('192.169.52.36'), 8542, 12, inet_aton('192.170.53.37'), 8542, 15, 'tcp attack 3', 'tcp', 5, '2016-02-23 15:47:29'),
(inet_aton('192.167.54.65'), 9600, 20, inet_aton('192.168.55.66'), 9600, 13, 'udp attack 4', 'udp', 1, '2016-02-23 15:56:29'),
(inet_aton('172.168.2.13'), 1234, 1, inet_aton('172.169.3.14'), 1234, 5, 'tcp attack 5', 'tcp', 6, '2016-02-23 16:32:29'),
(inet_aton('10.100.26.35'), 22, 7, inet_aton('10.101.27.36'), 22, 8, 'tcp attack 132', 'tcp', 1, '2016-02-23 16:41:29'),
(inet_aton('10.102.63.95'), 23, 14, inet_aton('10.103.64.96'), 23, 9, 'udp attack 3', 'udp', 2, '2016-02-23 16:41:36'),
(inet_aton('192.95.63.25'), 13, 16, inet_aton('192.96.64.26'), 13, 14, 'udp attack 4', 'udp', 4, '2016-02-23 16:41:45'),
(inet_aton('192.68.54.3'), 1563, 5, inet_aton('192.69.55.4'), 1563, 2, 'tcp attack 12', 'tcp', 6, '2016-02-23 18:13:29'),
(inet_aton('172.68.4.5'), 36, 8, inet_aton('172.69.5.6'), 36, 3, 'udp attack 6', 'udp', 7, '2016-02-23 18:26:29'),
(inet_aton('172.17.17.17'), 58, 3, inet_aton('192.18.18.59'), 58, 4, 'tcp attack 33', 'tcp', 2, '2016-02-23 18:41:29'),
(inet_aton('192.163.20.58'), 75, 14, inet_aton('192.164.21.59'), 7, 5, 'udp attack 2', 'udp', 4, '2016-02-23 20:41:29'),
(inet_aton('10.36.58.92'), 7560, 5, inet_aton('10.37.59.93'), 7560, 1, 'tcp attack 12', 'tcp', 5, '2016-02-23 20:52:29'),
(inet_aton('10.30.25.36'), 63, 8, inet_aton('10.31.26.37'), 63, 6, 'tcp attack 32', 'tcp', 3, '2016-02-23 20:53:29'),
(inet_aton('10.113.13.58'), 56, 11, inet_aton('10.114.14.59'), 56, 7, 'tcp attack 52', 'tcp', 8, '2016-02-23 21:15:29'),
(inet_aton('192.168.1.36'), 135, 9, inet_aton('192.169.2.37'), 135, 9, 'tcp attack 52', 'tcp', 8, '2016-02-23 22:30:29'),
(inet_aton('192.168.1.36'), 135, 9, inet_aton('192.169.2.37'), 135, 12, 'tcp attack 52', 'tcp', 8, '2016-02-23 22:45:29'),
(inet_aton('192.168.1.36'), 135, 9, inet_aton('192.169.2.37'), 135, 6, 'tcp attack 52', 'tcp', 8, '2016-02-23 23:00:29'),
(inet_aton('192.168.1.36'), 135, 9, inet_aton('192.169.2.37'), 135, 3, 'tcp attack 52', 'tcp', 8, '2016-02-23 23:45:29')

-- create response
--INSERT INTO response (response_time, attackID) VALUES
--('2016-02-23 15:43:29', 1), --tcp 1
--('2016-02-23 15:47:29', 2), --udp 2
--('2016-02-23 15:48:29', 3), --tcp 3
--('2016-02-23 15:57:29', 4), --udp 4
--('2016-02-23 16:33:29', 5), --tcp 5
--('2016-02-23 16:42:29', 6), --tcp 6
--('2016-02-23 16:42:36', 7), --udp 7
--('2016-02-23 16:42:45', 8), --udp 8
--('2016-02-23 18:14:29', 9), --tcp 9
--('2016-02-23 18:27:29', 10) --udp 10

-- create TCP_Reset
--INSERT INTO TCP_Reset (responseID) VALUES
--(1), (3), (5), (6), (9)

-- create Timebased_Block

-- create Permanent_Block

-- create high_priority_users
INSERT INTO high_priority_users (victimID) VALUES
(2), (4), (6), (8), (10)


-- create attack_persistence



-- create time_interval_persistence



