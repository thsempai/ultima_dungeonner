-- MySQL dump 10.13  Distrib 5.1.63, for debian-linux-gnu (x86_64)
--
-- Host: 1gamdb.gsmproductions.com    Database: 1gam201302
-- ------------------------------------------------------
-- Server version	5.1.56-log

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
-- Table structure for table `dungeon`
--

DROP TABLE IF EXISTS `dungeon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dungeon` (
  `dun_id` int(11) NOT NULL AUTO_INCREMENT,
  `dun_date` date DEFAULT NULL,
  PRIMARY KEY (`dun_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dungeon`
--

LOCK TABLES `dungeon` WRITE;
/*!40000 ALTER TABLE `dungeon` DISABLE KEYS */;
/*!40000 ALTER TABLE `dungeon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enemy`
--

DROP TABLE IF EXISTS `enemy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enemy` (
  `ene_id` int(11) NOT NULL,
  `ene_name` varchar(45) NOT NULL,
  `ene_til_xid` int(11) NOT NULL,
  `ene_til_x` int(11) NOT NULL,
  `ene_til_y` int(11) NOT NULL,
  PRIMARY KEY (`ene_id`),
  UNIQUE KEY `ene_name_UNIQUE` (`ene_name`),
  KEY `fk_tileset_fk2` (`ene_til_xid`),
  CONSTRAINT `fk_tileset_fk2` FOREIGN KEY (`ene_til_xid`) REFERENCES `tileset` (`til_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enemy`
--

LOCK TABLES `enemy` WRITE;
/*!40000 ALTER TABLE `enemy` DISABLE KEYS */;
INSERT INTO `enemy` VALUES (0,'imp',7,0,0);
/*!40000 ALTER TABLE `enemy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object`
--

DROP TABLE IF EXISTS `object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object` (
  `obj_id` int(11) NOT NULL AUTO_INCREMENT,
  `obj_name` varchar(45) NOT NULL,
  `obj_til_xid` int(11) NOT NULL,
  `obj_til_x` int(11) NOT NULL,
  `obj_til_y` int(11) NOT NULL,
  PRIMARY KEY (`obj_id`),
  KEY `fk_tileset_fk` (`obj_til_xid`),
  CONSTRAINT `fk_tileset_fk` FOREIGN KEY (`obj_til_xid`) REFERENCES `tileset` (`til_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object`
--

LOCK TABLES `object` WRITE;
/*!40000 ALTER TABLE `object` DISABLE KEYS */;
INSERT INTO `object` VALUES (4,'poison trap',6,0,1);
/*!40000 ALTER TABLE `object` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room` (
  `roo_id` int(11) NOT NULL AUTO_INCREMENT,
  `roo_name` varchar(100) NOT NULL,
  `roo_use_xid` int(11) NOT NULL,
  `roo_til_xid` int(11) NOT NULL,
  PRIMARY KEY (`roo_id`),
  UNIQUE KEY `ndx_roo_name` (`roo_name`),
  KEY `fk_user_fk1` (`roo_use_xid`),
  KEY `fk_tileset_fk1` (`roo_til_xid`),
  CONSTRAINT `fk_tileset_fk1` FOREIGN KEY (`roo_til_xid`) REFERENCES `tileset` (`til_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_fk1` FOREIGN KEY (`roo_use_xid`) REFERENCES `user` (`use_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (3,'first_room',6,5);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_dungeon`
--

DROP TABLE IF EXISTS `room_dungeon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room_dungeon` (
  `rod_roo_xid` int(11) NOT NULL AUTO_INCREMENT,
  `rod_dun_xid` int(11) NOT NULL,
  PRIMARY KEY (`rod_roo_xid`,`rod_dun_xid`),
  KEY `fk_dungeon_fk1` (`rod_dun_xid`),
  KEY `fk_room_fk1` (`rod_roo_xid`),
  CONSTRAINT `fk_dungeon_fk1` FOREIGN KEY (`rod_dun_xid`) REFERENCES `dungeon` (`dun_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_room_fk1` FOREIGN KEY (`rod_roo_xid`) REFERENCES `room` (`roo_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_dungeon`
--

LOCK TABLES `room_dungeon` WRITE;
/*!40000 ALTER TABLE `room_dungeon` DISABLE KEYS */;
/*!40000 ALTER TABLE `room_dungeon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_enemy`
--

DROP TABLE IF EXISTS `room_enemy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room_enemy` (
  `ren_roo_xid` int(11) NOT NULL,
  `ren_x` int(11) NOT NULL,
  `ren_y` int(11) NOT NULL,
  `ren_ene_xid` int(11) NOT NULL,
  `ren_ene_lvl` int(11) NOT NULL,
  PRIMARY KEY (`ren_roo_xid`,`ren_x`,`ren_y`),
  KEY `fk_room_fk2` (`ren_roo_xid`),
  KEY `fk_enemy_fk1` (`ren_ene_xid`),
  CONSTRAINT `fk_enemy_fk1` FOREIGN KEY (`ren_ene_xid`) REFERENCES `enemy` (`ene_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_room_fk2` FOREIGN KEY (`ren_roo_xid`) REFERENCES `room` (`roo_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_enemy`
--

LOCK TABLES `room_enemy` WRITE;
/*!40000 ALTER TABLE `room_enemy` DISABLE KEYS */;
INSERT INTO `room_enemy` VALUES (3,3,3,0,1),(3,5,2,0,1),(3,10,10,0,1);
/*!40000 ALTER TABLE `room_enemy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_object`
--

DROP TABLE IF EXISTS `room_object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room_object` (
  `rob_roo_xid` int(11) NOT NULL,
  `rob_x` int(11) NOT NULL,
  `rob_y` int(11) NOT NULL,
  `rob_obj_xid` int(11) NOT NULL,
  PRIMARY KEY (`rob_roo_xid`,`rob_x`,`rob_y`),
  KEY `fk_object_fk1` (`rob_obj_xid`),
  KEY `fk_room_fk` (`rob_roo_xid`),
  CONSTRAINT `fk_object_fk1` FOREIGN KEY (`rob_obj_xid`) REFERENCES `object` (`obj_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_room_fk` FOREIGN KEY (`rob_roo_xid`) REFERENCES `room` (`roo_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_object`
--

LOCK TABLES `room_object` WRITE;
/*!40000 ALTER TABLE `room_object` DISABLE KEYS */;
INSERT INTO `room_object` VALUES (3,1,1,4),(3,5,10,4),(3,10,12,4);
/*!40000 ALTER TABLE `room_object` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tileset`
--

DROP TABLE IF EXISTS `tileset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tileset` (
  `til_id` int(11) NOT NULL AUTO_INCREMENT,
  `til_name` varchar(45) NOT NULL,
  `til_path` varchar(100) NOT NULL,
  `til_type` varchar(100) NOT NULL,
  PRIMARY KEY (`til_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tileset`
--

LOCK TABLES `tileset` WRITE;
/*!40000 ALTER TABLE `tileset` DISABLE KEYS */;
INSERT INTO `tileset` VALUES (5,'room','img/tileset/dungeon.png','room'),(6,'trap','img/tileset/object.png','item'),(7,'imp','img/tileset/imp.png','enemy');
/*!40000 ALTER TABLE `tileset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `use_id` int(11) NOT NULL AUTO_INCREMENT,
  `use_nickname` varchar(45) NOT NULL,
  `use_password` varchar(45) NOT NULL,
  PRIMARY KEY (`use_id`),
  UNIQUE KEY `ndx_use_name` (`use_nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (6,'sempai','');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-15 21:29:05
