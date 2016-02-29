CREATE DATABASE  IF NOT EXISTS `siera_final` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `siera_final`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: 127.0.0.1    Database: siera_final
-- ------------------------------------------------------
-- Server version	5.6.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attack`
--

DROP TABLE IF EXISTS `attack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attack` (
  `attack_id` int(11) NOT NULL AUTO_INCREMENT,
  `attack_name` varchar(100) NOT NULL,
  `security_id` int(11) NOT NULL,
  `protocol_type` varchar(5) NOT NULL,
  PRIMARY KEY (`attack_id`),
  KEY `security_id_idx` (`security_id`),
  CONSTRAINT `security_id` FOREIGN KEY (`security_id`) REFERENCES `security_level` (`security_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attack`
--

LOCK TABLES `attack` WRITE;
/*!40000 ALTER TABLE `attack` DISABLE KEYS */;
INSERT INTO `attack` VALUES (1,'Malware - Checks for open accounts',2,'tcp'),(2,'Malware - Open a TCP connection to port 0',2,'tcp'),(3,'Port Scanners - Performs portscan',6,'udp'),(4,'Windows - Check for the vulnerable certificates',3,'tcp');
/*!40000 ALTER TABLE `attack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attack_log`
--

DROP TABLE IF EXISTS `attack_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attack_log` (
  `attack_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `source_ip` varchar(45) NOT NULL,
  `source_port` int(11) NOT NULL,
  `destination_ip` varchar(45) NOT NULL,
  `destination_port` int(11) NOT NULL,
  `attack_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`attack_log_id`),
  KEY `attack_id_idx` (`attack_id`),
  KEY `role_id_idx` (`role_id`),
  CONSTRAINT `attack_id` FOREIGN KEY (`attack_id`) REFERENCES `attack` (`attack_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `source_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attack_log`
--

LOCK TABLES `attack_log` WRITE;
/*!40000 ALTER TABLE `attack_log` DISABLE KEYS */;
INSERT INTO `attack_log` VALUES (1,'2016-01-26 16:45:58','209.193.76.194',443,'172.16.4.104',76,1,1),(2,'2016-02-03 13:03:29','209.193.76.194',443,'172.16.4.26',1243,1,2),(3,'2016-02-05 00:20:04','24.34.23.12',46766,'172.16.4.52',80,4,1),(4,'2016-02-05 01:12:23','209.193.76.194',443,'172.16.4.104',76,1,1),(5,'2016-02-05 01:13:18','209.193.76.194',443,'172.16.4.104',76,1,1),(6,'2016-02-06 15:12:05','24.34.23.12',46491,'172.16.4.26',1534,2,2),(7,'2016-02-06 15:15:37','209.193.76.194',443,'172.16.4.104',76,1,1),(8,'2016-02-06 18:12:43','74.124.24.34',1245,'172.16.4.67',17538,3,2);
/*!40000 ALTER TABLE `attack_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attack_persistence`
--

DROP TABLE IF EXISTS `attack_persistence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attack_persistence` (
  `persistence_id` int(11) NOT NULL AUTO_INCREMENT,
  `attack_log_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `persistence_count` int(11) NOT NULL,
  PRIMARY KEY (`persistence_id`),
  KEY `attack_log_id_idx` (`attack_log_id`),
  CONSTRAINT `attack_log_id` FOREIGN KEY (`attack_log_id`) REFERENCES `attack_log` (`attack_log_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attack_persistence`
--

LOCK TABLES `attack_persistence` WRITE;
/*!40000 ALTER TABLE `attack_persistence` DISABLE KEYS */;
/*!40000 ALTER TABLE `attack_persistence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attack_rate`
--

DROP TABLE IF EXISTS `attack_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attack_rate` (
  `attack_rate_id` int(11) NOT NULL AUTO_INCREMENT,
  `value_from` float NOT NULL,
  `value_to` float NOT NULL,
  `attack_level` varchar(45) NOT NULL,
  PRIMARY KEY (`attack_rate_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attack_rate`
--

LOCK TABLES `attack_rate` WRITE;
/*!40000 ALTER TABLE `attack_rate` DISABLE KEYS */;
INSERT INTO `attack_rate` VALUES (1,0,0.4999,'low'),(2,0.5,0.9999,'medium'),(3,1,100,'high');
/*!40000 ALTER TABLE `attack_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `high_priority_users`
--

DROP TABLE IF EXISTS `high_priority_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `high_priority_users` (
  `high_priority_id` int(11) NOT NULL AUTO_INCREMENT,
  `source_ip` varchar(45) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`high_priority_id`),
  KEY `role_id_idx` (`role_id`),
  CONSTRAINT `hp_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `high_priority_users`
--

LOCK TABLES `high_priority_users` WRITE;
/*!40000 ALTER TABLE `high_priority_users` DISABLE KEYS */;
INSERT INTO `high_priority_users` VALUES (1,'172.16.4.104',1),(2,'172.16.4.52',1);
/*!40000 ALTER TABLE `high_priority_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metric_conjunction`
--

DROP TABLE IF EXISTS `metric_conjunction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metric_conjunction` (
  `metric_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `attack_rate_id` int(11) NOT NULL,
  `protocol_type` varchar(5) NOT NULL,
  `tcp_reset` int(1) NOT NULL,
  `time_based` int(1) NOT NULL,
  `acl_block` int(1) NOT NULL,
  PRIMARY KEY (`metric_id`),
  KEY `metric_role_id_idx` (`role_id`),
  KEY `metric_attack_rate_id_idx` (`attack_rate_id`),
  CONSTRAINT `metric_attack_rate_id` FOREIGN KEY (`attack_rate_id`) REFERENCES `attack_rate` (`attack_rate_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `metric_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metric_conjunction`
--

LOCK TABLES `metric_conjunction` WRITE;
/*!40000 ALTER TABLE `metric_conjunction` DISABLE KEYS */;
INSERT INTO `metric_conjunction` VALUES (1,2,1,'tcp',1,1,0),(2,2,2,'tcp',1,1,0),(3,2,3,'tcp',0,0,1),(4,1,1,'tcp',0,0,1),(5,1,2,'tcp',0,0,1),(6,1,3,'tcp',0,0,1),(7,2,1,'udp',0,1,0),(8,2,2,'udp',0,1,0),(9,2,3,'udp',0,0,1),(10,1,1,'udp',0,0,1),(11,1,2,'udp',0,0,1),(12,1,3,'udp',0,0,1);
/*!40000 ALTER TABLE `metric_conjunction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permanent_block`
--

DROP TABLE IF EXISTS `permanent_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permanent_block` (
  `permanent_block_id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) NOT NULL,
  `is_block` int(11) NOT NULL,
  `last_modified` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`permanent_block_id`),
  KEY `permanent_response_id_idx` (`response_id`),
  CONSTRAINT `permanent_response_id` FOREIGN KEY (`response_id`) REFERENCES `response` (`response_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permanent_block`
--

LOCK TABLES `permanent_block` WRITE;
/*!40000 ALTER TABLE `permanent_block` DISABLE KEYS */;
/*!40000 ALTER TABLE `permanent_block` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `response` (
  `response_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `persistence_id` int(11) NOT NULL,
  `interval_id` int(11) NOT NULL,
  `attack_rate_id` int(11) NOT NULL,
  `metric_id` int(11) NOT NULL DEFAULT '-1',
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`response_id`),
  KEY `response_attack_persistence_id_idx` (`persistence_id`),
  KEY `response_time_interval_id_idx` (`interval_id`),
  KEY `response_attack_rate_id_idx` (`attack_rate_id`),
  KEY `response_metric_id_idx` (`metric_id`),
  CONSTRAINT `response_metric_id` FOREIGN KEY (`metric_id`) REFERENCES `metric_conjunction` (`metric_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `response_attack_persistence_id` FOREIGN KEY (`persistence_id`) REFERENCES `attack_persistence` (`persistence_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `response_attack_rate_id` FOREIGN KEY (`attack_rate_id`) REFERENCES `attack_rate` (`attack_rate_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `response_time_interval_id` FOREIGN KEY (`interval_id`) REFERENCES `time_persistence_interval` (`interval_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(45) NOT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'High Priority'),(2,'Low Priority');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `security_level`
--

DROP TABLE IF EXISTS `security_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `security_level` (
  `security_id` int(11) NOT NULL AUTO_INCREMENT,
  `security_name` varchar(45) NOT NULL,
  PRIMARY KEY (`security_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_level`
--

LOCK TABLES `security_level` WRITE;
/*!40000 ALTER TABLE `security_level` DISABLE KEYS */;
INSERT INTO `security_level` VALUES (1,'serious'),(2,'high'),(3,'medium'),(6,'low'),(7,'info');
/*!40000 ALTER TABLE `security_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tcp_reset`
--

DROP TABLE IF EXISTS `tcp_reset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tcp_reset` (
  `tcp_reset_id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) NOT NULL,
  PRIMARY KEY (`tcp_reset_id`),
  KEY `response_id_idx` (`response_id`),
  CONSTRAINT `tcp_response_id` FOREIGN KEY (`response_id`) REFERENCES `response` (`response_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tcp_reset`
--

LOCK TABLES `tcp_reset` WRITE;
/*!40000 ALTER TABLE `tcp_reset` DISABLE KEYS */;
/*!40000 ALTER TABLE `tcp_reset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_based`
--

DROP TABLE IF EXISTS `time_based`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_based` (
  `time_based_id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) NOT NULL,
  `num_days` int(11) NOT NULL,
  `block_start` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `block_end` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`time_based_id`),
  KEY `response_id_idx` (`response_id`),
  KEY `num_days_idx` (`num_days`),
  CONSTRAINT `num_days` FOREIGN KEY (`num_days`) REFERENCES `time_based_range` (`timebased_range_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `time_response_id` FOREIGN KEY (`response_id`) REFERENCES `response` (`response_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_based`
--

LOCK TABLES `time_based` WRITE;
/*!40000 ALTER TABLE `time_based` DISABLE KEYS */;
/*!40000 ALTER TABLE `time_based` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_based_range`
--

DROP TABLE IF EXISTS `time_based_range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_based_range` (
  `timebased_range_id` int(11) NOT NULL AUTO_INCREMENT,
  `level` varchar(45) NOT NULL,
  `num_days` int(11) NOT NULL,
  PRIMARY KEY (`timebased_range_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_based_range`
--

LOCK TABLES `time_based_range` WRITE;
/*!40000 ALTER TABLE `time_based_range` DISABLE KEYS */;
INSERT INTO `time_based_range` VALUES (1,'Low',2),(2,'Medium',5);
/*!40000 ALTER TABLE `time_based_range` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_persistence_interval`
--

DROP TABLE IF EXISTS `time_persistence_interval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_persistence_interval` (
  `interval_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `interval` int(11) NOT NULL,
  PRIMARY KEY (`interval_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_persistence_interval`
--

-- DEFAULT: 7 DAYS
-- INSERT INTO `siera_final`.`time_persistence_interval` (`interval_id`, `timestamp`, `interval`) VALUES ('1', CURRENT_TIMESTAMP, '7');
INSERT INTO `time_persistence_interval` VALUES (1,'2016-01-25 14:37:13',7);

LOCK TABLES `time_persistence_interval` WRITE;
/*!40000 ALTER TABLE `time_persistence_interval` DISABLE KEYS */;
INSERT INTO `time_persistence_interval` VALUES (1,'2016-01-25 14:37:13',7);
/*!40000 ALTER TABLE `time_persistence_interval` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-02-29  1:12:56
